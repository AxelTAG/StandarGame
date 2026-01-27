# Imports.
# Local imports.
from .enums import Colors

# External imports
from attrs import define, field, fields, has


@define
class Region:
    # Basic attributes.
    name: str = field(default=None)
    description: str = field(default=None)
    color_label: tuple = field(default=None)
    id: str = field(default=None)

    # Update attributes.
    __updatable__: tuple[str, ...] = field(init=False, repr=False, default=())
    __migration_map__: dict[str, str] = field(init=False, repr=False, factory=dict)

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

    # Update methods.
    def update_from_instance(self, old):
        if has(old.__class__):
            old_attrs = {f.name: getattr(old, f.name, None) for f in fields(old.__class__)}
        else:
            old_attrs = {
                name: getattr(old, name)
                for name in dir(old)
                if not name.startswith("__") and hasattr(old, name)
            }

        for attr, value in old_attrs.items():
            new_attr = self.__migration_map__.get(attr, attr)

            if new_attr in self.__updatable__:
                setattr(self, new_attr, value)

        self._after_migration(old=old)

    @staticmethod
    def _after_migration(old) -> None:
        pass
