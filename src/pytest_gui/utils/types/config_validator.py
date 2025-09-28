from typing import Literal

from pydantic import BaseModel, model_validator


class Argument(BaseModel):
    arg_name: str
    arg_type: Literal["select", "text_input"]
    options: list[str] | None = None
    placeholder: str | None = None

    @model_validator(mode="after")
    def check_arg_type(self):
        if self.arg_type == "select":
            if not self.options:
                raise ValueError("Argument with arg_type='select' must have 'options'")
            if self.placeholder is not None:
                raise ValueError("Argument with arg_type='select' must NOT have 'placeholder'")

        if self.arg_type == "text_input":
            if not self.placeholder:
                raise ValueError("Argument with arg_type='text_input' must have 'placeholder'")
            if self.options is not None:
                raise ValueError("Argument with arg_type='text_input' must NOT have 'options'")

        return self


class Test(BaseModel):
    label: str
    test_name: str | None = None
    markers: list[str] | None = None
    arguments: list[Argument] | None = None

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        has_test_name = self.test_name is not None
        has_markers = self.markers is not None

        if has_test_name == has_markers:  # If both are there, or neither is
            raise ValueError(
                f"Test '{self.label}' must have exactly one of 'test_name' or 'markers'",
            )
        return self


class Subcategory(BaseModel):
    label: str
    tests: list[Test]


class Category(BaseModel):
    label: str
    subcategories: list[Subcategory]


class Config(BaseModel):
    categories: list[Category]
