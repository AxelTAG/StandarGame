# Imports.
# Local imports.
from globals import Months, Season, NPCS, BIOMES
from utils import label_pixels, tl_map_set


# External imports.
import numpy as np
import random

from attrs import define, field
from datetime import datetime


@define
class Map:
    # Time map attributes.
    year: int = field(default=249)
    month: int = field(default=Months.AURENAR.value)
    day: int = field(default=4)
    hour: int = field(default=6)

    # Climate map attributes.
    season: Season = field(default=Season.SUMMER.value)
    temperature: int = field(default=15)

    # Map attributes.
    map_labels: list = field(default=None)
    map_settings: dict = field(default=None)
    npcs: dict = field(default=NPCS.copy())
    biomes: dict = field(default=BIOMES.copy())
    x_len: int = field(init=False)
    y_len: int = field(init=False)

    def __attrs_post_init__(self):
        if self.map_labels is None:
            self.map_labels = label_pixels("rsc/tile-00.png")

        if self.map_settings is None:
            self.map_settings = tl_map_set(self.map_labels)
