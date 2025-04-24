import os
from typing import Any
from monday import MondayClient
import pytest
import pandas as pd
from mondaytoframe import read, update, create_board, create_items, delete_board
from mondaytoframe.io import TokenType
from mondaytoframe.model import BoardKind
from monday.resources.types import ColumnType
import requests  # type: ignore[import-untyped]
from graphql import build_schema, parse, validate
from pydantic import validate_call

from tests.conftest import MULTIPLE_PERSON_PLACEHOLDER


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


def test_read_board_as_frame(
    mocker,
    response_fetch_boards_by_id: dict[str, Any],
    response_fetch_items_by_board_id: dict[str, Any],
    dataframe_representation: pd.DataFrame,
):
    mock_monday_client = mocker.patch("mondaytoframe.io.MondayClient")
    mock_monday_client().boards.fetch_boards_by_id.return_value = (
        response_fetch_boards_by_id
    )
    mock_monday_client().custom.execute_custom_query.return_value = (
        response_fetch_items_by_board_id
    )

    result = read("board_123", "fake_token", unknown_type="drop")

    _check_queries_were_valid(mock_monday_client)
    pd.testing.assert_frame_equal(
        result,
        dataframe_representation.drop(columns=NON_SUPPORTED_COLUMNS),
        check_column_type=False,
        check_like=True,
    )


def test_update_calls_monday_api(
    mocker,
    dataframe_representation,
    response_fetch_boards_by_id,
):
    mock_monday_client = mocker.patch("mondaytoframe.io.MondayClient")
    mock_monday_client().boards.fetch_boards_by_id.return_value = (
        response_fetch_boards_by_id
    )

    update("board_123", dataframe_representation, "fake_token", unknown_type="drop")

    # Ensure the Monday API was called for each item
    assert mock_monday_client().items.change_multiple_column_values.call_count == len(
        dataframe_representation
    )

    # Ensure the Monday API was called for each item
    assert mock_monday_client().items.change_multiple_column_values.call_count == len(
        dataframe_representation
    )

    _check_queries_were_valid(mock_monday_client)

    # Ensure the Monday API was called for each item
    assert mock_monday_client().items.change_multiple_column_values.call_count == len(
        dataframe_representation
    )


def _check_queries_were_valid(mock_monday_client):
    """Validates whether the queries done to mock client are valid for Monday's graphql schema"""
    for call_args in mock_monday_client().client.execute.call_args_list:
        query = call_args[0][0]
        parsed_query = parse(query)
        assert not validate(schema, parsed_query), f"Error in query {query}"


def test_update_empty_dataframe(mocker, dataframe_representation):
    mock_monday_client = mocker.patch("monday.MondayClient")
    empty_df = dataframe_representation.iloc[0:0, :]
    update("board_123", empty_df, "fake_token")
    mock_monday_client().items.change_multiple_column_values.assert_not_called()


@pytest.fixture(scope="module")
def monday_token() -> str | None:
    token = os.getenv("MONDAY_TOKEN")
    if token is None:
        pytest.skip("MONDAY_TOKEN environment variable is not set")
    return token


@pytest.fixture(scope="module")
def monday_client(monday_token) -> MondayClient:
    return MondayClient(monday_token)


@pytest.fixture
def board_for_test(monday_token, response_fetch_boards_by_id):
    board_name = "Test Board"

    column_types = {
        col["title"]: col["type"]
        for col in response_fetch_boards_by_id["data"]["boards"][0]["columns"]
        if col["title"] != "Name" and col["type"].upper() in ColumnType.__members__
    }

    try:
        board_id = create_board(
            column_types, monday_token, board_name, BoardKind.public
        )

        create_items(
            board_id,
            pd.DataFrame(
                {
                    "Name": ["Task 2"],
                    "Group": ["topics"],
                }
            ),
            monday_token,
        )
        yield board_id
    finally:
        delete_board(board_id, monday_token)


def test_integration_with_monday_api(
    monday_token, monday_client, board_for_test, dataframe_representation
):
    board_id = board_for_test

    # Load (empty) board
    df = read(board_id, monday_token)

    # Some of the monday-defined ID's must come from the API, such as item and user id's
    users = monday_client.users.fetch_users()
    user_id = users["data"]["users"][0]["id"]
    adjusted_df = (
        dataframe_representation.set_index(df.index)
        .replace(MULTIPLE_PERSON_PLACEHOLDER, user_id)
        .assign(Group="Group Title")
    )

    # Update the adjusted dataframe to the board and verify everything is still the same
    update(
        board_id,
        adjusted_df,
        monday_token,
        unknown_type="drop",
        create_labels_if_missing=True,
    )
    first_result = read(board_id, monday_token, unknown_type="drop", limit=1)
    pd.testing.assert_frame_equal(
        adjusted_df.drop(columns=NON_SUPPORTED_COLUMNS),
        first_result,
        check_column_type=False,
        check_like=True,
    )

    # Switch the content of the rows (not the index) and do a round trip again to test emptying
    switched_rows_df = first_result.iloc[::-1].set_index(first_result.index)
    update(
        board_id,
        switched_rows_df,
        monday_token,
        unknown_type="raise",
        create_labels_if_missing=True,
    )
    second_result = read(board_id, monday_token)
    pd.testing.assert_frame_equal(
        switched_rows_df, second_result, check_column_type=False, check_like=True
    )


def test_tokentype_annotation(mocker):
    os_patched = mocker.patch("mondaytoframe.io.os")
    os_patched.getenv.return_value = None

    @validate_call
    def function_with_token_type_argument(token: TokenType): ...

    with pytest.raises(ValueError, match="Input should be a valid string"):
        function_with_token_type_argument()
