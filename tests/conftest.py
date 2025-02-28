from pytest import fixture
import pandas as pd

from typing import Any


@fixture
def response_fetch_boards_by_id() -> dict[str, Any]:
    return {
        "data": {
            "boards": [
                {
                    "id": "13",
                    "name": "Test Board",
                    "permissions": "everyone",
                    "tags": [],
                    "groups": [{"id": "topics", "title": "Group Title"}],
                    "columns": [
                        {
                            "title": "Name",
                            "id": "name",
                            "type": "name",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Person",
                            "id": "person",
                            "type": "people",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Status",
                            "id": "status",
                            "type": "status",
                            "settings_str": '{"done_colors":[1],"labels":{"0":"Working on it","1":"Done","2":"Stuck"},"labels_positions_v2":{"0":0,"1":2,"2":1,"5":3},"labels_colors":{"0":{"color":"#fdab3d","border":"#e99729","var_name":"orange"},"1":{"color":"#00c875","border":"#00b461","var_name":"green-shadow"},"2":{"color":"#df2f4a","border":"#ce3048","var_name":"red-shadow"}}}',
                        },
                        {
                            "title": "Dropdown",
                            "id": "dropdown_mkmyr6sf",
                            "type": "dropdown",
                            "settings_str": '{"limit_select":false,"hide_footer":false,"labels":[{"id":1,"name":"a"},{"id":2,"name":"b"}],"deactivated_labels":[]}',
                        },
                        {
                            "title": "Label",
                            "id": "label_mkmytka4",
                            "type": "status",
                            "settings_str": '{"done_colors":[1],"labels":{"3":"Label 2","105":"Label 1","156":"Label 3"},"labels_positions_v2":{"3":1,"5":3,"105":0,"156":2},"labels_colors":{"3":{"color":"#007eb5","border":"#3db0df","var_name":"blue-links"},"105":{"color":"#9aadbd","border":"#9aadbd","var_name":"winter"},"156":{"color":"#9d99b9","border":"#9d99b9","var_name":"purple_gray"}}}',
                        },
                        {
                            "title": "Date",
                            "id": "date4",
                            "type": "date",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Text",
                            "id": "text_mkmyax8a",
                            "type": "text",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Long text",
                            "id": "long_text_mkmy4rab",
                            "type": "long_text",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Numbers",
                            "id": "numbers_mkmyz9a4",
                            "type": "numbers",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Files",
                            "id": "files_mkmysy47",
                            "type": "file",
                            "settings_str": '{"hide_footer":false}',
                        },
                        {
                            "title": "Formula",
                            "id": "formula_mkmy4vct",
                            "type": "formula",
                            "settings_str": '{"formula":"{text_mkmyax8a}"}',
                        },
                        {
                            "title": "Priority",
                            "id": "priority_mkmyqwh7",
                            "type": "status",
                            "settings_str": '{"done_colors":[1],"labels":{"7":"Low","10":"Critical ⚠️️","109":"Medium","110":"High"},"labels_positions_v2":{"5":4,"7":3,"10":0,"109":2,"110":1},"labels_colors":{"7":{"color":"#579bfc","border":"#4387e8","var_name":"bright-blue"},"10":{"color":"#333333","border":"#000","var_name":"soft-black"},"109":{"color":"#5559df","border":"#5559df","var_name":"indigo"},"110":{"color":"#401694","border":"#401694","var_name":"dark_indigo"}}}',
                        },
                        {
                            "title": "Board with all types for testing",
                            "id": "connect_boards_mkmyc6sf",
                            "type": "board_relation",
                            "settings_str": '{"allowCreateReflectionColumn":false,"boardIds":[8426052206]}',
                        },
                        {
                            "title": "Mirror",
                            "id": "mirror_mkmynj95",
                            "type": "mirror",
                            "settings_str": '{"relation_column":{"connect_boards_mkmyc6sf":true},"displayed_column":{},"displayed_linked_columns":{"8426052206":["status"]}}',
                        },
                        {
                            "title": "Tags",
                            "id": "tags_mkmy81rw",
                            "type": "tags",
                            "settings_str": '{"hide_footer":false}',
                        },
                        {
                            "title": "Check",
                            "id": "check_mkmymaap",
                            "type": "checkbox",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Link",
                            "id": "link_mkmyeb4y",
                            "type": "link",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Email",
                            "id": "email_mkmymrsb",
                            "type": "email",
                            "settings_str": "{}",
                        },
                        {
                            "title": "Phone",
                            "id": "phone_mkmynw7g",
                            "type": "phone",
                            "settings_str": "{}",
                        },
                    ],
                }
            ]
        },
    }


@fixture
def response_fetch_items_by_board_id() -> dict[str, Any]:
    return {
        "data": {
            "boards": [
                {
                    "name": "Board with all types for testing",
                    "items_page": {
                        "cursor": None,
                        "items": [
                            {
                                "group": {"id": "topics", "title": "Group 1"},
                                "id": "10",
                                "name": "Item with values",
                                "column_values": [
                                    {
                                        "id": "person",
                                        "text": "John Doe, Peter Pan",
                                        "type": "people",
                                        "value": '{"changed_at":"2025-02-17T19:07:49.776Z","personsAndTeams":[{"id":1,"kind":"person"}, {"id":2,"kind":"person"}]}',
                                    },
                                    {
                                        "id": "status",
                                        "text": "Working on it",
                                        "type": "status",
                                        "value": '{"index":0,"post_id":null,"changed_at":"2019-03-01T17:24:57.321Z"}',
                                    },
                                    {
                                        "id": "dropdown_mkmyr6sf",
                                        "text": "a, b",
                                        "type": "dropdown",
                                        "value": '{"ids":[1,2]}',
                                    },
                                    {
                                        "id": "label_mkmytka4",
                                        "text": "Label 1",
                                        "type": "status",
                                        "value": '{"index":105,"post_id":null,"changed_at":"2025-02-07T09:52:41.753Z"}',
                                    },
                                    {
                                        "id": "date4",
                                        "text": "2025-02-10",
                                        "type": "date",
                                        "value": '{"date":"2025-02-10","icon":null,"changed_at":"2025-02-07T09:49:21.812Z"}',
                                    },
                                    {
                                        "id": "text_mkmyax8a",
                                        "text": "abc",
                                        "type": "text",
                                        "value": '"abc"',
                                    },
                                    {
                                        "id": "long_text_mkmy4rab",
                                        "text": "def",
                                        "type": "long_text",
                                        "value": '{"text":"def","changed_at":"2025-02-17T19:08:02.712Z"}',
                                    },
                                    {
                                        "id": "numbers_mkmyz9a4",
                                        "text": "10",
                                        "type": "numbers",
                                        "value": '"10"',
                                    },
                                    {
                                        "id": "files_mkmysy47",
                                        "text": "https://account-name.monday.com/docs/8426060102",
                                        "type": "file",
                                        "value": '{"files":[{"name":"THIS DOC IS FOR TESTING ONLY","fileId":"ea4b7fd6-e8ff-cadb-aad9-5d5053b8dc23","isImage":"false","fileType":"MONDAY_DOC","objectId":8426060102,"createdAt":1738921848389,"createdBy":"63044374","linkToFile":"https://account-name.monday.com/docs/8426060102"}]}',
                                    },
                                    {
                                        "id": "formula_mkmy4vct",
                                        "text": "",
                                        "type": "formula",
                                        "value": None,
                                    },
                                    {
                                        "id": "priority_mkmyqwh7",
                                        "text": "Critical ⚠️️",
                                        "type": "status",
                                        "value": '{"index":10,"post_id":null,"changed_at":"2025-02-07T09:53:26.320Z"}',
                                    },
                                    {
                                        "id": "connect_boards_mkmyc6sf",
                                        "text": None,
                                        "type": "board_relation",
                                        "value": '{"changed_at":"2025-02-07T09:55:26.603Z","linkedPulseIds":[{"linkedPulseId":8426052265}]}',
                                    },
                                    {
                                        "id": "mirror_mkmynj95",
                                        "text": None,
                                        "type": "mirror",
                                        "value": None,
                                    },
                                    {
                                        "id": "tags_mkmy81rw",
                                        "text": "A, B",
                                        "type": "tags",
                                        "value": '{"tag_ids":[25393416,25393417]}',
                                    },
                                    {
                                        "id": "check_mkmymaap",
                                        "text": "v",
                                        "type": "checkbox",
                                        "value": '{"checked":true,"changed_at":"2025-02-07T09:58:52.214Z"}',
                                    },
                                    {
                                        "id": "link_mkmyeb4y",
                                        "text": "https://somelink.nl - https://somelink.nl/",
                                        "type": "link",
                                        "value": '{"url":"https://somelink.nl/","text":"https://somelink.nl","changed_at":"2025-02-07T09:58:28.808Z"}',
                                    },
                                    {
                                        "id": "email_mkmymrsb",
                                        "text": "test@test.nl",
                                        "type": "email",
                                        "value": '{"text":"test@test.nl","email":"test@test.nl","changed_at":"2025-02-07T09:57:27.469Z"}',
                                    },
                                    {
                                        "id": "phone_mkmynw7g",
                                        "text": "31622222222",
                                        "type": "phone",
                                        "value": '{"phone":"31622222222","changed_at":"2025-02-17T19:08:18.375Z","countryShortName":"NL"}',
                                    },
                                ],
                            },
                            {
                                "group": {"id": "group_title", "title": "Group 2"},
                                "id": "20",
                                "name": "Item without values",
                                "column_values": [
                                    {
                                        "id": "person",
                                        "text": "",
                                        "type": "people",
                                        "value": None,
                                    },
                                    {
                                        "id": "status",
                                        "text": None,
                                        "type": "status",
                                        "value": None,
                                    },
                                    {
                                        "id": "dropdown_mkmyr6sf",
                                        "text": None,
                                        "type": "dropdown",
                                        "value": None,
                                    },
                                    {
                                        "id": "label_mkmytka4",
                                        "text": None,
                                        "type": "status",
                                        "value": None,
                                    },
                                    {
                                        "id": "date4",
                                        "text": "",
                                        "type": "date",
                                        "value": None,
                                    },
                                    {
                                        "id": "text_mkmyax8a",
                                        "text": "",
                                        "type": "text",
                                        "value": None,
                                    },
                                    {
                                        "id": "long_text_mkmy4rab",
                                        "text": "",
                                        "type": "long_text",
                                        "value": None,
                                    },
                                    {
                                        "id": "numbers_mkmyz9a4",
                                        "text": "",
                                        "type": "numbers",
                                        "value": None,
                                    },
                                    {
                                        "id": "files_mkmysy47",
                                        "text": "",
                                        "type": "file",
                                        "value": None,
                                    },
                                    {
                                        "id": "formula_mkmy4vct",
                                        "text": "",
                                        "type": "formula",
                                        "value": None,
                                    },
                                    {
                                        "id": "priority_mkmyqwh7",
                                        "text": None,
                                        "type": "status",
                                        "value": None,
                                    },
                                    {
                                        "id": "connect_boards_mkmyc6sf",
                                        "text": None,
                                        "type": "board_relation",
                                        "value": '{"changed_at":"2025-02-17T19:08:42.391Z"}',
                                    },
                                    {
                                        "id": "mirror_mkmynj95",
                                        "text": None,
                                        "type": "mirror",
                                        "value": None,
                                    },
                                    {
                                        "id": "tags_mkmy81rw",
                                        "text": "",
                                        "type": "tags",
                                        "value": '{"tag_ids":[]}',
                                    },
                                    {
                                        "id": "check_mkmymaap",
                                        "text": "",
                                        "type": "checkbox",
                                        "value": '{"checked":false}',
                                    },
                                    {
                                        "id": "link_mkmyeb4y",
                                        "text": "",
                                        "type": "link",
                                        "value": None,
                                    },
                                    {
                                        "id": "email_mkmymrsb",
                                        "text": "",
                                        "type": "email",
                                        "value": None,
                                    },
                                    {
                                        "id": "phone_mkmynw7g",
                                        "text": "",
                                        "type": "phone",
                                        "value": None,
                                    },
                                ],
                            },
                        ],
                    },
                }
            ]
        }
    }


@fixture
def dataframe_representation() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": ["10", "20"],
            "Name": ["Item with values", "Item without values"],
            "Group": ["Group 1", "Group 2"],
            "Person": ["1,2", None],
            "Status": ["Working on it", None],
            "Dropdown": [{"a", "b"}, {}],
            "Label": ["Label 1", None],
            "Date": [pd.Timestamp("2025-02-10 00:00:00"), pd.NaT],
            "Text": ["abc", None],
            "Long text": ["def", None],
            "Numbers": [10.0, None],
            "Priority": ["Critical ⚠️️", None],
            "Tags": [["A", "B"], None],
            "Check": [True, False],
            "Link": ["https://somelink.nl/", None],
            "Email": ["test@test.nl", None],
            "Phone": ["+31622222222 NL", None],
        }
    ).set_index("id")
