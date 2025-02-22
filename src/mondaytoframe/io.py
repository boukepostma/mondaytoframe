import pandas as pd
from mondaytoframe.model_manual import (
    ColumnsByBoardColumn,
    ColumnsByBoardResponse,
    ItemsByBoardResponse,
)
from mondaytoframe.parsers_for_frame import PARSERS_FOR_DF

from monday import MondayClient


from typing import Any

from mondaytoframe.parsers_for_monday import PARSERS_FOR_MONDAY


def fetch_column_specifications(
    monday: MondayClient, board_id: str
) -> list[ColumnsByBoardColumn]:
    query_result = monday.boards.fetch_columns_by_board_id(board_id)
    validated = ColumnsByBoardResponse(**query_result)
    col_specs = validated.data.boards[0].columns

    titles = [col.title for col in col_specs]
    if len(titles) != len(set(titles)):
        raise ValueError("Duplicate column titles found in Monday board.")

    return col_specs


def load(monday: MondayClient, board_id: str, **kwargs: dict[str, Any]):
    column_specifications = fetch_column_specifications(monday, board_id)

    items = []
    while True:
        query_result = monday.boards.fetch_items_by_board_id(board_id)
        validated = ItemsByBoardResponse(**query_result)
        board = validated.data.boards[0]
        items += board.items_page.items
        if board.items_page.cursor is None:
            break

    items_parsed = []
    for item in items:
        column_values_dict = {
            (column_value.id): PARSERS_FOR_DF[column_value.type](column_value)
            for column_value in item.column_values
            if column_value.type in PARSERS_FOR_DF
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


def save(monday: MondayClient, board_id: str, df: pd.DataFrame, **kwargs: Any):
    if df.empty:
        return
    column_specifications = fetch_column_specifications(monday, board_id)

    parser_mapping = {
        spec.title: PARSERS_FOR_MONDAY[spec.type]
        for spec in column_specifications
        if spec.title in df.columns and spec.title != "Name"
    } | {"Name": PARSERS_FOR_MONDAY["Name"]}
    name_mapping = {spec.title: spec.id for spec in column_specifications}
    df = df.apply(
        lambda s: s if s.name == "Group" else s.apply(parser_mapping[s.name])
    ).rename(columns=name_mapping)

    for item_id, row in df.iterrows():
        monday.items.change_multiple_column_values(
            board_id=board_id,
            item_id=item_id,
            column_values=row.drop("Group").to_dict(),
            **kwargs,
        )
