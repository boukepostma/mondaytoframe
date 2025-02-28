import os
from typing import Any
from monday import MondayClient
import pytest
import pandas as pd
from mondaytoframe.io import load, save
from mondaytoframe.model import BoardKind
from monday.resources.types import ColumnType


@pytest.fixture
def mock_monday_client(mocker):
    return mocker.MagicMock()


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

    result = load(mock_monday_client, "board_123")

    pd.testing.assert_frame_equal(
        result, dataframe_representation, check_column_type=False
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

    save(mock_monday_client, "board_123", dataframe_representation)

    # Ensure the Monday API was called for each item
    assert mock_monday_client.items.change_multiple_column_values.call_count == len(
        dataframe_representation
    )


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
    save(monday_client, board_id, adjusted_df, create_labels_if_missing=True)
    result_df = load(monday_client, board_id)[adjusted_df.columns]
    pd.testing.assert_frame_equal(adjusted_df, result_df, check_column_type=False)
