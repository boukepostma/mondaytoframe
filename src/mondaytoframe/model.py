import datetime
from enum import Enum
import json
import logging

from typing import Annotated, Literal, Optional, TypeAlias, Union

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_extra_types.country import CountryAlpha2
from phonenumbers import (
    parse as parse_phone_number,
    PhoneNumberFormat,
    format_number,
)
from typing import Any

logger = logging.getLogger(__name__)

ID: TypeAlias = str
JSON: TypeAlias = str
String: TypeAlias = str


class ColumnType(Enum):
    """
    The columns to create.
    """

    auto_number = "auto_number"
    board_relation = "board_relation"
    button = "button"
    checkbox = "checkbox"
    color_picker = "color_picker"
    country = "country"
    creation_log = "creation_log"
    date = "date"
    dependency = "dependency"
    doc = "doc"
    dropdown = "dropdown"
    email = "email"
    file = "file"
    formula = "formula"
    group = "group"
    hour = "hour"
    integration = "integration"
    item_assignees = "item_assignees"
    item_id = "item_id"
    last_updated = "last_updated"
    link = "link"
    location = "location"
    long_text = "long_text"
    mirror = "mirror"
    name = "name"
    numbers = "numbers"
    people = "people"
    person = "person"
    phone = "phone"
    progress = "progress"
    rating = "rating"
    status = "status"
    subtasks = "subtasks"
    tags = "tags"
    team = "team"
    text = "text"
    time_tracking = "time_tracking"
    timeline = "timeline"
    unsupported = "unsupported"
    vote = "vote"
    week = "week"
    world_clock = "world_clock"


SUPPORTED_COLUMN_TYPES = [
    ColumnType.email,
    ColumnType.date,
    ColumnType.text,
    ColumnType.link,
    ColumnType.people,
    ColumnType.status,
    ColumnType.name,
    ColumnType.checkbox,
    ColumnType.tags,
    ColumnType.long_text,
    ColumnType.phone,
    ColumnType.dropdown,
    ColumnType.numbers,
]


class SchemaColumn(BaseModel):
    title: String
    type: ColumnType
    id: str


class SchemaTags(BaseModel):
    id: ID
    name: String


class SchemaBoard(BaseModel):
    columns: list[SchemaColumn]
    tags: list[SchemaTags]

    @field_validator("columns", mode="after")
    @classmethod
    def validate_unique_column_titles(cls, value: list[SchemaColumn]):
        titles = [col.title for col in value]
        duplicates = [title for title in set(titles) if titles.count(title) > 1]
        if duplicates:
            raise ValueError(
                f"Duplicate column titles found in Monday board: {duplicates}"
            )
        return value


class SchemaData(BaseModel):
    boards: list[SchemaBoard]


class SchemaResponse(BaseModel):
    data: SchemaData


class ItemsByBoardColumn(BaseModel):
    title: String


class BaseColumnValue(BaseModel):
    id: ID
    model_config = ConfigDict(strict=False)


class ColumnValue(BaseColumnValue):
    text: Optional[String]
    type: Union[
        Literal["auto_number"],
        Literal["board_relation"],
        Literal["button"],
        Literal["color_picker"],
        Literal["country"],
        Literal["creation_log"],
        Literal["dependency"],
        Literal["doc"],
        Literal["email"],
        Literal["file"],
        Literal["formula"],
        Literal["group"],
        Literal["hour"],
        Literal["integration"],
        Literal["item_assignees"],
        Literal["item_id"],
        Literal["last_updated"],
        Literal["location"],
        Literal["long_text"],
        Literal["mirror"],
        Literal["name"],
        Literal["person"],
        Literal["progress"],
        Literal["rating"],
        Literal["status"],
        Literal["subtasks"],
        Literal["team"],
        Literal["text"],
        Literal["time_tracking"],
        Literal["timeline"],
        Literal["unsupported"],
        Literal["vote"],
        Literal["week"],
        Literal["world_clock"],
    ]
    value: Optional[JSON]

    @model_validator(mode="after")
    def email_text_and_value_are_equal(self) -> "ColumnValue":
        if (self.type == ColumnType.email) and self.value:
            as_dict = json.loads(self.value)
            if as_dict["text"] != as_dict["email"]:
                raise ValueError(
                    f"For e-mail columns, text must equal value. Now text='{self.text}' and value='{self.value}'"
                )
        return self


class LinkRaw(BaseModel):
    text: str
    url: str

    @model_validator(mode="after")
    def validate_link_equals_url(self) -> "LinkRaw":
        if self.text.rstrip("/") != self.url.rstrip("/"):
            raise ValueError(
                f"For link columns, text must equal url. Now text='{self.text}' and url='{self.url}'"
            )
        return self


class DateRaw(BaseModel):
    date: datetime.date | None = None
    time: datetime.time = Field(default_factory=lambda: datetime.time(0, 0, 0))

    @field_validator("time", mode="before")
    @classmethod
    def set_default_time_if_none(cls, v: Any):
        return datetime.time(0, 0, 0) if v is None else v


class DateColumnValue(BaseColumnValue):
    type: Literal["date"]
    text: Optional[String]
    value: Optional[DateRaw]

    @field_validator("value", mode="before")
    @classmethod
    def parse_json_string(cls, v: Any):
        if not isinstance(v, str):
            return v
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string for date value")


class LinkColumnValue(BaseColumnValue):
    type: Literal["link"]
    value: Optional[LinkRaw]

    @field_validator("value", mode="before")
    @classmethod
    def parse_json_string(cls, v: Any):
        if not isinstance(v, str):
            return v
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string for link value")


class PersonOrTeam(BaseModel):
    id: str
    kind: Literal["person", "team"]

    model_config = ConfigDict(strict=False, coerce_numbers_to_str=True)


class PeopleRaw(BaseModel):
    personsAndTeams: list[PersonOrTeam]


class PeopleColumnValue(BaseColumnValue):
    type: Literal["people"]
    value: Optional[PeopleRaw]

    @field_validator("value", mode="before")
    @classmethod
    def parse_json_string(cls, v: Any):
        if not isinstance(v, str):
            return v
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string for people value")


class CheckboxColumnValue(BaseColumnValue):
    type: Literal["checkbox"]
    text: Literal["v", ""] = Field(default="")


class TagValue(BaseModel):
    name: str


class TagsColumnValue(BaseColumnValue):
    type: Literal["tags"]
    tags: list[TagValue]


class PhoneRaw(BaseModel):
    phone: str
    countryShortName: CountryAlpha2

    @model_validator(mode="after")
    def parse_phone_number(self):
        try:
            # Use the country short name as the default region
            parsed_phone_number = parse_phone_number(self.phone, self.countryShortName)
            self.phone = format_number(parsed_phone_number, PhoneNumberFormat.E164)
            return self
        except Exception as e:
            raise ValueError(f"Error parsing phone number: {e}")


class PhoneColumnValue(BaseColumnValue):
    type: Literal["phone"]
    text: Optional[String]
    value: Optional[PhoneRaw]

    @field_validator("value", mode="before")
    @classmethod
    def parse_json_string(cls, v: Any):
        if not isinstance(v, str):
            return v
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string for phone value")


class DropdownValueOption(BaseModel):
    label: str


class DropdownColumnValue(BaseColumnValue):
    type: Literal["dropdown"]
    values: list[DropdownValueOption]


class NumberColumnValue(BaseColumnValue):
    type: Literal["numbers"]
    text: float = Field(default=np.nan)

    @field_validator("text", mode="before")
    @classmethod
    def empty_string_to_nan(cls, v: Any):
        if isinstance(v, str) and v == "":
            return np.nan
        return v


class ItemsByBoardGroup(BaseModel):
    title: String


class ItemsByBoardItem(BaseModel):
    group: ItemsByBoardGroup
    id: str
    name: str
    column_values: list[
        Annotated[
            Union[
                ColumnValue,
                DropdownColumnValue,
                NumberColumnValue,
                PhoneColumnValue,
                TagsColumnValue,
                CheckboxColumnValue,
                PeopleColumnValue,
                LinkColumnValue,
                DateColumnValue,
            ],
            Field(discriminator="type"),
        ]
    ]


class ItemsByBoardItemsPage(BaseModel):
    cursor: str | None
    items: list[ItemsByBoardItem]


class ItemsByBoardBoard(BaseModel):
    items_page: ItemsByBoardItemsPage


class ItemsByBoardData(BaseModel):
    boards: list[ItemsByBoardBoard]


class ItemsByBoardResponse(BaseModel):
    data: ItemsByBoardData


class BoardKind(Enum):
    private = "private"
    public = "public"
    share = "share"
