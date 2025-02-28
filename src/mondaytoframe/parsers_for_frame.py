from datetime import datetime
import json
from typing import Any

import pandas as pd
from pydantic import validate_call
from mondaytoframe.model import ColumnType
from mondaytoframe.model import (
    DateRaw,
    DropdownRaw,
    PeopleRaw,
    ColumnValue,
    PhoneRaw,
)
import numpy as np


@validate_call()
def parse_email_for_df(v: ColumnValue) -> Any:
    return v.text if v.text else None


@validate_call()
def parse_date_for_df(v: ColumnValue) -> Any:
    if v.value is None:
        return pd.NaT
    validated = DateRaw.model_validate_json(v.value)
    return datetime.combine(validated.date, validated.time)


@validate_call()
def parse_text_for_df(v: ColumnValue):
    return v.text if v.text else None


@validate_call()
def parse_link_for_df(v: ColumnValue):
    if v.value is None:
        return None
    return json.loads(v.value)["url"]


@validate_call()
def parse_people_for_df(v: ColumnValue):
    if not v.value:
        return None
    validated = PeopleRaw.model_validate_json(v.value)
    return ",".join([str(v.id) for v in validated.personsAndTeams])


@validate_call()
def parse_status_for_df(v: ColumnValue):
    return v.text


@validate_call()
def parse_checkbox_for_df(v: ColumnValue) -> bool:
    return True if v.text else False


@validate_call()
def parse_tags_for_df(v: ColumnValue):
    return v.text.split(", ") if v.text else None


@validate_call()
def parse_long_text_for_df(v: ColumnValue):
    return v.text if v.text else None


@validate_call()
def parse_phone_for_df(v: ColumnValue):
    if v.value is None:
        return None
    validated = PhoneRaw.model_validate_json(v.value)
    return f"{validated.phone} {validated.countryShortName}"


@validate_call()
def parse_dropdown_for_df(v: ColumnValue):
    if v.value is None or v.text is None:
        return {}
    validated = DropdownRaw.model_validate_json(v.value)
    if v.text.count(",") + 1 != len(validated.ids):
        raise ValueError(
            "Make sure the labels in Monday do not contain commas: labels with commas are not supported."
        )
    return set(v.text.split(", "))


@validate_call()
def parse_numbers_for_df(v: ColumnValue):
    if not v.text:
        return np.nan
    return float(v.text)


PARSERS_FOR_DF = {
    ColumnType.email: parse_email_for_df,
    ColumnType.date: parse_date_for_df,
    ColumnType.text: parse_text_for_df,
    ColumnType.link: parse_link_for_df,
    ColumnType.people: parse_people_for_df,
    ColumnType.status: parse_status_for_df,
    ColumnType.checkbox: parse_checkbox_for_df,
    ColumnType.tags: parse_tags_for_df,
    ColumnType.long_text: parse_long_text_for_df,
    ColumnType.phone: parse_phone_for_df,
    ColumnType.dropdown: parse_dropdown_for_df,
    ColumnType.numbers: parse_numbers_for_df,
}
