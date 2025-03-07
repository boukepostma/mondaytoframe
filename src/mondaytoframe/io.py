import os
import pandas as pd
from mondaytoframe.model import (
    ColumnType,
    SchemaBoard,
    SchemaResponse,
    ItemsByBoardResponse,
)
from mondaytoframe.parsers_for_frame import PARSERS_FOR_DF

from monday import MondayClient


from typing import Any, Literal

from mondaytoframe.parsers_for_monday import PARSERS_FOR_MONDAY
import logging
from pydantic import Field, validate_call
from typing_extensions import Annotated

logger = logging.getLogger(__name__)

TOKEN_NAME = "MONDAYTOFRAME_TOKEN"

TokenType = Annotated[str, Field(default=os.getenv(TOKEN_NAME), validate_default=True)]


def _fetch_schema_board(monday: MondayClient, board_id: str) -> SchemaBoard:
    query_result = monday.boards.fetch_boards_by_id(board_id)
    validated = SchemaResponse(**query_result)
    return validated.data.boards[0]


def _create_or_get_tag(monday: MondayClient, tag_name: str):
    query_result = monday.custom.execute_custom_query(
        f"""mutation {{ create_or_get_tag (tag_name: "{tag_name}") {{ id }} }}"""
    )
    return int(query_result["data"]["create_or_get_tag"]["id"])


@validate_call()
def load(
    board_id: str,
    monday_token: TokenType,
    unknown_type: Literal["text", "drop", "raise"] = "text",
    **kwargs: dict[str, Any],
):
    """
    Load data from a Monday.com board into a pandas DataFrame.

    Arguments:
        board_id (str): The ID of the Monday.com board to load data from.
        monday_token (TokenType): The authentication token for Monday.com API.
        unknown_type (Literal["text", "drop", "raise"]): Specifies how to handle unknown column types.
            - "text": Use a default text parser for unknown column types (default).
            - "drop": Ignore unknown column types.
            - "raise": Raise a ValueError if unknown column types are found.
        **kwargs (dict[str, Any]): Additional arguments to pass to the Monday.com API.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the board data.

    Raises:
        ValueError: If unknown column types are found and `unknown_type` is set to "raise".

    Notes:
        The function uses predefined parsers for known column types. If a column type is not recognized and `unknown_type`
        is set to "text", a default text parser will be used. If `unknown_type` is set to "drop", the unknown columns will
        be ignored.

    Usage:

    ```python
    from mondaytoframe import load

    df = load(board_id="123456", monday_token="your_token")
    print(df.head())
    ```
    """
    monday = MondayClient(monday_token)
    column_specifications = _fetch_schema_board(monday, board_id).columns

    cols_without_parsers = {
        spec.id: spec.type
        for spec in column_specifications
        if spec.type not in PARSERS_FOR_DF and spec.id != "name"
    }
    col_parser_mapping = {
        spec.id: PARSERS_FOR_DF[spec.type]
        for spec in column_specifications
        if spec.type in PARSERS_FOR_DF
    }
    if cols_without_parsers:
        match unknown_type:
            case "raise":
                raise ValueError(
                    f"Unknown column types found in the board: {cols_without_parsers}."
                    "Set unknown_type='text' to try to get them using a default parser or "
                    "set unknown_type='drop' to ignore them."
                )
            case "drop":
                msg = (
                    f"Unknown column types found in the board: {cols_without_parsers}. Not loading them."
                    "Set unknown_type='text' to try to get them using a default text parser."
                )
                logger.warning(msg)
            case "text":
                col_parser_mapping.update(
                    {
                        col: PARSERS_FOR_DF[ColumnType.text]
                        for col in cols_without_parsers
                    }
                )

    items = []
    while True:
        query_result = monday.boards.fetch_items_by_board_id(board_id, **kwargs)
        validated = ItemsByBoardResponse(**query_result)
        board = validated.data.boards[0]
        items += board.items_page.items
        if board.items_page.cursor is None:
            break

    items_parsed = []
    for item in items:
        column_values_dict = {
            (column_value.id): col_parser_mapping[column_value.id](column_value)
            for column_value in item.column_values
            if column_value.id not in cols_without_parsers
        }

        record = {
            "id": item.id,
            "Name": item.name,
            "Group": item.group.title,
            **column_values_dict,
        }
        items_parsed.append(record)

    name_mapping = {
        spec.id: spec.title for spec in column_specifications if spec.title != "Name"
    }
    return pd.DataFrame.from_records(items_parsed, index="id").rename(
        columns=name_mapping
    )


@validate_call(config=dict(arbitrary_types_allowed=True))
def save(
    board_id: str,
    df: pd.DataFrame,
    monday_token: TokenType,
    unknown_type: Literal["drop", "raise"] = "raise",
    **kwargs: Any,
):
    """
    Save a pandas DataFrame to a Monday.com board.

    Arguments:
        board_id (str): The ID of the Monday.com board.
        df (pd.DataFrame): The DataFrame to save to the board.
        monday_token (TokenType): The authentication token for Monday.com.
        unknown_type (Literal["drop", "raise"]): Specifies how to handle columns in the DataFrame that do not have a corresponding parser in the board schema.
            - "drop": Ignore columns that do not have a corresponding parser (default).
            - "raise": Raise a ValueError if columns do not have a corresponding parser.
        **kwargs (Any): Additional keyword arguments to pass to the Monday.com API.

    Raises:
        ValueError: If unknown_type is "raise" and there are columns in the DataFrame that do not have a corresponding parser in the board schema.

    Usage:

    ```python
    from mondaytoframe import save
    import pandas as pd

    df = pd.DataFrame({
        "Name": ["Task 1", "Task 2"],
        "Status": ["Done", "In Progress"],
        "Tags": [["tag1"], ["tag2", "tag3"]],
    })
    save(board_id="123456", df=df, monday_token="your_token")
    ```
    """

    if df.empty:
        return
    monday = MondayClient(monday_token)
    board_schema = _fetch_schema_board(monday, board_id)
    column_specifications = board_schema.columns
    tag_specifications = board_schema.tags

    # Check if all columns in the dataframe are in the board schema
    cols_without_parsers = []
    col_parser_mapping = {
        "Name": PARSERS_FOR_MONDAY[ColumnType.text],
        "Group": PARSERS_FOR_MONDAY[ColumnType.text],
    }
    for column in df.columns.drop(["Name", "Group"]):
        col_spec = [spec for spec in column_specifications if spec.title == column]
        if not col_spec or col_spec[0].type not in PARSERS_FOR_MONDAY:
            cols_without_parsers.append(column)
        else:
            col_parser_mapping[column] = PARSERS_FOR_MONDAY[col_spec[0].type]

    if cols_without_parsers:
        match unknown_type:
            case "raise":
                raise ValueError(
                    f"Unknown column types found in the board: {cols_without_parsers}."
                    "Set unknown_type='drop' to ignore this error and save all other columns."
                )
            case "drop":
                msg = f"Unknown column types found in the board: {cols_without_parsers}. Not saving them."
                logger.warning(msg)

    # Convert tags names to ids. Create new ids for tags that do not exist yet
    tag_mapping = {tag.name: tag.id for tag in tag_specifications}
    cols_with_tags = [
        spec.title for spec in column_specifications if spec.type == ColumnType.tags
    ]
    tags_in_board = set(
        df[cols_with_tags]
        .apply(lambda s: s.explode().dropna().unique(), axis=1)
        .explode()
        .dropna()
    )
    missing_tag_mapping = {
        tag: _create_or_get_tag(monday, tag)
        for tag in tags_in_board - tag_mapping.keys()
    }
    all_tag_mapping = tag_mapping | missing_tag_mapping

    df = df.assign(
        **{
            col: df[col].map(
                lambda ls: [all_tag_mapping[tag] for tag in ls] if ls else None
            )
            for col in cols_with_tags
        }
    )

    name_mapping = {spec.title: spec.id for spec in column_specifications}
    df = (
        df[list(col_parser_mapping)]
        .apply(lambda s: s.apply(col_parser_mapping[s.name]))
        .rename(columns=name_mapping)
    )

    for item_id, row in df.iterrows():
        monday.items.change_multiple_column_values(
            board_id=board_id,
            item_id=item_id,
            column_values=row.drop("Group").to_dict(),
            **kwargs,
        )
