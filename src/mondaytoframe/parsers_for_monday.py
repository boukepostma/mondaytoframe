from datetime import datetime

from pydantic import validate_call

from mondaytoframe.model import ColumnType, PhoneRaw


@validate_call
def parse_email_for_monday(v: str | None):
    return {"email": v, "text": v} if v else None


@validate_call
def parse_date_for_monday(v: datetime | None):
    # Make sure to convert to UTC
    if not v == v or v is None:
        return None
    return {"date": v.strftime("%Y-%m-%d"), "time": v.strftime("%H:%M:%S")}


@validate_call
def parse_text_for_monday(v: str | None):
    return v if v else None


@validate_call
def parse_link_for_monday(v: str | None):
    return {"text": v, "url": v} if v else None


@validate_call
def parse_people_for_monday(v: str | None):
    if not v:
        return None
    return v


@validate_call
def parse_status_for_monday(v: str | None):
    if not v:
        return None
    return {"label": v}


@validate_call
def parse_checkbox_for_monday(v: bool | None):
    if v:
        return {"checked": "true"}
    return None


@validate_call
def parse_tags_for_monday(v: list[int] | None):
    return {"tag_ids": v} if v else None


@validate_call
def parse_long_text_for_monday(v: str | None):
    return v if v else None


@validate_call
def parse_phone_for_monday(v: str | None):
    if not v:
        return None
    phone, country = v.split(" ", maxsplit=1)
    return PhoneRaw(phone=phone, countryShortName=country).model_dump()


@validate_call
def parse_dropdown_for_monday(v: list[str] | None):
    return {"labels": list(v)} if v else None


@validate_call
def parse_numbers_for_monday(v: float | None):
    return str(v) if v == v and v is not None else None


PARSERS_FOR_MONDAY = {
    ColumnType.email: parse_email_for_monday,
    ColumnType.date: parse_date_for_monday,
    ColumnType.text: parse_text_for_monday,
    ColumnType.link: parse_link_for_monday,
    ColumnType.people: parse_people_for_monday,
    ColumnType.status: parse_status_for_monday,
    ColumnType.checkbox: parse_checkbox_for_monday,
    ColumnType.tags: parse_tags_for_monday,
    ColumnType.long_text: parse_long_text_for_monday,
    ColumnType.phone: parse_phone_for_monday,
    ColumnType.dropdown: parse_dropdown_for_monday,
    ColumnType.numbers: parse_numbers_for_monday,
}
