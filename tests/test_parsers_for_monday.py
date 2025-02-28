import numpy as np
import pytest
from datetime import datetime
from mondaytoframe.parsers_for_monday import (
    parse_email_for_monday,
    parse_date_for_monday,
    parse_text_for_monday,
    parse_link_for_monday,
    parse_people_for_monday,
    parse_status_for_monday,
    parse_checkbox_for_monday,
    parse_tags_for_monday,
    parse_long_text_for_monday,
    parse_phone_for_monday,
    parse_dropdown_for_monday,
    parse_numbers_for_monday,
)
from deepdiff import DeepDiff


parameters = [
    (
        parse_email_for_monday,
        "test@example.com",
        {"email": "test@example.com", "text": "test@example.com"},
    ),
    (parse_email_for_monday, "", None),
    (parse_email_for_monday, None, None),
    (
        parse_date_for_monday,
        datetime(2025, 2, 10, 14, 30),
        {"date": "2025-02-10", "time": "14:30:00"},
    ),
    (parse_date_for_monday, None, None),
    (parse_text_for_monday, "some text", "some text"),
    (parse_text_for_monday, "", None),
    (parse_text_for_monday, None, None),
    (
        parse_link_for_monday,
        "https://example.com",
        {"text": "https://example.com", "url": "https://example.com"},
    ),
    (parse_link_for_monday, "", None),
    (parse_link_for_monday, None, None),
    (parse_people_for_monday, "1,2", "1,2"),
    (parse_people_for_monday, "", None),
    (parse_people_for_monday, None, None),
    (parse_status_for_monday, "Working on it", {"label": "Working on it"}),
    (parse_status_for_monday, "", None),
    (parse_status_for_monday, None, None),
    (parse_checkbox_for_monday, True, {"checked": "true"}),
    (parse_checkbox_for_monday, False, None),
    # TODO: raise error if checkbox is empty
    (parse_tags_for_monday, ["1", "2"], {"tag_ids": [1, 2]}),
    (parse_tags_for_monday, "", None),
    (parse_tags_for_monday, None, None),
    (parse_long_text_for_monday, "long text", "long text"),
    (parse_long_text_for_monday, "", None),
    (parse_long_text_for_monday, None, None),
    (
        parse_phone_for_monday,
        "31622222222 NL",
        {"phone": "+31622222222", "countryShortName": "NL"},
    ),
    (parse_phone_for_monday, "", None),
    (parse_phone_for_monday, None, None),
    (parse_dropdown_for_monday, ["label1", "label2"], {"labels": ["label1", "label2"]}),
    (parse_dropdown_for_monday, "", None),
    (parse_dropdown_for_monday, None, None),
    (parse_numbers_for_monday, 10.0, "10.0"),
    (parse_numbers_for_monday, 10, "10"),
    (parse_numbers_for_monday, np.nan, None),
    (parse_numbers_for_monday, None, None),
]


@pytest.mark.parametrize("func,input_value,expected", parameters)
def test_parsers_for_monday(func, input_value, expected):
    assert not DeepDiff(
        func(input_value),
        expected,
        ignore_nan_inequality=True,
        ignore_string_type_changes=True,
    )
