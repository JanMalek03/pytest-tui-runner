from typing import Literal, NotRequired, TypedDict


class Argument(TypedDict):
    """Arguments for special tests.

    Normal tests will only run/not run,
    but special tests will run with arguments specified using the widget
    """

    name: str
    """The name of the argument, used for identification and display."""

    arg_type: Literal["select", "text_input"]
    """The type of the input widget for the argument.

    - "select": renders a dropdown with multiple options.
    - "text_input": renders a text input field.
    """

    options: NotRequired[list[str]]
    """A list of selectable options.

    Required only if `arg_type` is "select".
    """

    placeholder: NotRequired[str]
    """Placeholder text shown in the input field.

    Used only if `arg_type` is "text_input".
    """


class Test(TypedDict):
    """Represents an individual test definition within a subcategory."""

    name: str
    """The display name of the test."""

    markers: list[str]
    """A list of pytest markers assigned to this test.

    Used for filtering and categorizing test behavior.
    """

    type: Literal["normal", "special"]
    """The type of test.

    - "normal": standard test with no extra parameters.
                It's like a function with no argument, it just either runs or it doesn't
    - "special": test that requires user input via arguments.
                As well as functions with arguments that need to be specified.
                These arguments are specified in `arguments`
    """

    arguments: NotRequired[list[Argument]]
    """Optional list of input arguments for tests of type "special"."""


class Subcategory(TypedDict):
    """Logical grouping of related tests within a category."""

    name: str
    """The name of the subcategory (e.g., 'Login', 'Navigation')."""
    tests: list[Test]
    """A list of individual tests under this subcategory."""


class Category(TypedDict):
    """Top-level grouping for tests, typically representing a domain or module."""

    name: str
    """The name of the category (e.g., 'Unit Tests', 'Images')."""
    subcategories: list[Subcategory]
    """A list of subcategories contained within this category."""


class TestConfig(TypedDict):
    """The root structure of the configuration file.

    Describes the complete hierarchy of categories, subcategories, and tests.
    This format is expected to be loaded from a YAML or JSON file.

    Example:
    --------
    Example YAML structure this type represents:

        categories:
          - name: "Unit Tests"
            subcategories:
              - name: "Login"
                tests:
                  - name: "Login button visible"
                    markers: ["login"]
                    type: "normal"
                  - name: "Login with credentials"
                    markers: ["login"]
                    type: "special"
                    arguments:
                      - name: "username"
                        arg_type: "text_input"
                        placeholder: "Enter username"
                      - name: "role"
                        arg_type: "select"
                        options: ["admin", "user", "guest"]
    """

    categories: list[Category]
    """List of all top-level categories defined in the configuration."""
