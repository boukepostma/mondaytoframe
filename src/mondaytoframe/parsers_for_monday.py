from datetime import datetime

from mondaytoframe.model import ColumnType, PhoneRaw


def parse_email_for_monday(v: str):
    return {"email": v, "text": v} if v else None


def parse_date_for_monday(v: datetime):
    # Make sure to convert to UTC
    if not v == v or v is None:
        return None
    return {"date": v.strftime("%Y-%m-%d"), "time": v.strftime("%H:%M:%S")}


def parse_text_for_monday(v: str):
    return v if v else None


def parse_link_for_monday(v: str):
    return {"text": v, "url": v} if v else None


def parse_people_for_monday(v: str):
    if not v:
        return None
    return v


def parse_status_for_monday(v: str):
    if not v:
        return None
    return {"label": v}


def parse_name_for_monday(v: str):
    if not v:
        return None
    return v


def parse_checkbox_for_monday(v: bool):
    if v:
        return {"checked": "true"}
    return None


def parse_tags_for_monday(v: list[str]):
    return {"tag_ids": [int(s) for s in v]} if v else None


def parse_long_text_for_monday(v: str):
    return v if v else None


def parse_phone_for_monday(v: str):
    if not v:
        return None
    phone, country = v.split(" ", maxsplit=1)
    return PhoneRaw(phone=phone, countryShortName=country).model_dump()


def parse_dropdown_for_monday(v: str):
    return {"labels": v.split(",")} if v else None


def parse_numbers_for_monday(v: str):
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
    # ColumnType.dropdown: parse_dropdown_for_monday,
    ColumnType.numbers: parse_numbers_for_monday,
    "Name": parse_name_for_monday,
}
