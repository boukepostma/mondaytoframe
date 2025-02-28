import os
from typing import Any
from monday import MondayClient
import pytest
import pandas as pd
from mondaytoframe.io import load, save
from mondaytoframe.model import BoardKind
from monday.resources.types import ColumnType
import requests  # type: ignore[import-untyped]
from graphql import build_schema, parse, validate


NON_SUPPORTED_COLUMNS = ["Connected Board", "Mirror", "Formula", "Files"]


@pytest.fixture
def mock_monday_client(mocker):
    return mocker.MagicMock()


@pytest.fixture
def schema():
    schema_url = "https://api.monday.com/v2/get_schema?format=sdl"
    response = requests.get(schema_url)

    if response.status_code != 200:
        pytest.skip("Unable to fetch schema")
    response.raise_for_status()

    return build_schema(response.text)


def test_load_board_as_frame(
    mock_monday_client,
    response_fetch_boards_by_id: dict[str, Any],
    response_fetch_items_by_board_id: dict[str, Any],
    dataframe_representation: pd.DataFrame,
):
    mock_monday_client.boards.fetch_boards_by_id.return_value = (
        response_fetch_boards_by_id
    )
    mock_monday_client.boards.fetch_items_by_board_id.return_value = (
        response_fetch_items_by_board_id
    )

    result = load(mock_monday_client, "board_123", unknown_type="drop")

    _check_queries_were_valid(mock_monday_client)
    pd.testing.assert_frame_equal(
        result,
        dataframe_representation.drop(columns=NON_SUPPORTED_COLUMNS),
        check_column_type=False,
        check_like=True,
    )


def test_save_calls_monday_api(
    mock_monday_client,
    dataframe_representation,
    response_fetch_boards_by_id,
):
    # Mock fetch_schema_board
    mock_monday_client.boards.fetch_boards_by_id.return_value = (
        response_fetch_boards_by_id
    )

    save(mock_monday_client, "board_123", dataframe_representation, unknown_type="drop")

    _check_queries_were_valid(mock_monday_client)

    # Ensure the Monday API was called for each item
    assert mock_monday_client.items.change_multiple_column_values.call_count == len(
        dataframe_representation
    )


def _check_queries_were_valid(mock_monday_client):
    """Validates whether the queries done to mock client are valid for Monday's graphql schema"""
    for call_args in mock_monday_client.client.execute.call_args_list:
        query = call_args[0][0]
        parsed_query = parse(query)
        assert not validate(schema, parsed_query), f"Error in query {query}"


def test_save_empty_dataframe(mock_monday_client, dataframe_representation):
    empty_df = dataframe_representation.iloc[0:0, :]
    save(mock_monday_client, "board_123", empty_df)
    mock_monday_client.items.change_multiple_column_values.assert_not_called()


@pytest.fixture(scope="module")
def monday_client():
    token = os.getenv("MONDAY_TOKEN")
    if not token:
        pytest.skip("MONDAY_TOKEN environment variable is not set")
    return MondayClient(token)


@pytest.fixture
def board_for_test(monday_client, response_fetch_boards_by_id):
    board_name = "Test Board"
    board = monday_client.boards.create_board(
        board_name=board_name, board_kind=BoardKind.public
    )

    try:
        board_id = board["data"]["create_board"]["id"]

        columns = [
            {"title": col["title"], "type": col["type"]}
            for col in response_fetch_boards_by_id["data"]["boards"][0]["columns"]
            if col["title"] != "Name" and col["type"].upper() in ColumnType.__members__
        ]

        for column in columns:
            monday_client.columns.create_column(
                board_id=board_id,
                column_title=column["title"],
                column_type=getattr(ColumnType, column["type"].upper()),
            )

        # Create the second item on the board. The first one is made automatically when the board is created
        monday_client.items.create_item(
            board_id=board_id,
            item_name="Task 2",
            group_id="topics",
        )

        yield board_id
    finally:
        monday_client.custom.execute_custom_query(
            f"mutation {{ delete_board (board_id: {board_id}) {{ id }} }}"
        )


def test_integration_with_monday_api(
    monday_client, board_for_test, dataframe_representation
):
    board_id = board_for_test

    # Load (empty) board
    df = load(monday_client, board_id)

    # Some of the monday-defined ID's must come from the API, such as item and user id's
    users = monday_client.users.fetch_users()
    user_id = users["data"]["users"][0]["id"]
    adjusted_df = (
        dataframe_representation.set_index(df.index)
        .replace("1,2", user_id)
        .assign(Group="Group Title")
    )

    # Save the adjusted dataframe to the board and verify everything is still the same
    save(
        monday_client,
        board_id,
        adjusted_df,
        unknown_type="drop",
        create_labels_if_missing=True,
    )
    first_result = load(monday_client, board_id, unknown_type="drop")
    pd.testing.assert_frame_equal(
        adjusted_df.drop(columns=NON_SUPPORTED_COLUMNS),
        first_result,
        check_column_type=False,
        check_like=True,
    )

    # Switch the content of the rows (not the index) and do a round trip again to test emptying
    switched_rows_df = first_result.iloc[::-1].set_index(first_result.index)
    save(
        monday_client,
        board_id,
        switched_rows_df,
        unknown_type="raise",
        create_labels_if_missing=True,
    )
    second_result = load(monday_client, board_id)
    pd.testing.assert_frame_equal(
        switched_rows_df, second_result, check_column_type=False, check_like=True
    )
