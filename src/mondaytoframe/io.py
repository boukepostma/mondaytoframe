import pandas as pd
from mondaytoframe.model import (
    ColumnType,
    SchemaBoard,
    SchemaResponse,
    ItemsByBoardResponse,
)
from mondaytoframe.parsers_for_frame import PARSERS_FOR_DF

from monday import MondayClient


from typing import Any

from mondaytoframe.parsers_for_monday import PARSERS_FOR_MONDAY


def fetch_schema_board(monday: MondayClient, board_id: str) -> SchemaBoard:
    query_result = monday.boards.fetch_boards_by_id(board_id)
    validated = SchemaResponse(**query_result)
    return validated.data.boards[0]


def create_or_get_tag(monday: MondayClient, tag_name: str):
    query_result = monday.custom.execute_custom_query(
        f"""mutation {{ create_or_get_tag (tag_name: "{tag_name}") {{ id }} }}"""
    )
    return int(query_result["data"]["create_or_get_tag"]["id"])


def load(monday: MondayClient, board_id: str, **kwargs: dict[str, Any]):
    column_specifications = fetch_schema_board(monday, board_id).columns

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
    board_schema = fetch_schema_board(monday, board_id)
    column_specifications = board_schema.columns
    tag_specifications = board_schema.tags

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
        tag: create_or_get_tag(monday, tag)
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
