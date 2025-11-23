# Imports.
# Local imports.
from .enums import Colors

# External imports
from attrs import define, field


@define
class Region:
    # Basic attributes.
    name: str = field(default=None)
    description: str = field(default=None)
    color_label: tuple = field(default=None)
    id: str = field(default=None)

    def __attrs_post_init__(self):
        # Basic attributes.
        if self.name is None:
            self.name = "UNKNOWN"

        if self.description is None:
            self.description = "No description avaible."

        if self.color_label is None:
            self.color_label = Colors.RED.value

        if self.id is None:
            self.id = self.name.replace(" ", "_").lower()
