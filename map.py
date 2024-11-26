# Imports.
# Local imports.
from biome import Biome, Entry
from enums import Months, Season, TimeOfDay, WeekDays
from npc import Npc
from player import Player
from utils import label_pixels, tl_map_set
from utils_settings import init_map_setting

# External imports.
from attrs import define, field


@define
class Map:
    # Time map attributes.
    year: int = field(default=249)
    month: int = field(default=Months.AURENAR.value)
    day: int = field(default=1)
    hour: int = field(default=6)

    morning_start: int = field(default=6)
    afternoon_start: int = field(default=12)
    evening_start: int = field(default=18)
    night_start: int = field(default=22)
    day_duration: int = field(default=24)
    week_duration: int = field(default=8)
    month_duration: int = field(default=64)
    year_duration: int = field(default=8)

    # Climate map attributes.
    temperature: int = field(default=15)
    length_of_seasons: int = field(default=2)

    # Map attributes.
    map_labels: list = field(default=None)
    map_init_settings: dict = field(default=None)
    map_settings: dict = field(default=None)
    npcs: dict = field(default=None)
    biomes: dict = field(default=None)
    mobs: dict = field(default=None)
    x_len: int = field(init=False)
    y_len: int = field(init=False)

    def __attrs_post_init__(self):
        if self.map_labels is None:
            self.map_labels = label_pixels("rsc/tile-00.png")

        if self.map_init_settings is None:
            pass

        if self.map_settings is None:
            self.map_settings = tl_map_set(self.map_labels, biomes=self.biomes)
            init_map_setting(ms=self.map_settings)

        if self.npcs is None:
            self.npcs = {}

        self.x_len = len(self.map_labels) - 1
        self.y_len = len(self.map_labels[0]) - 1

    @property
    def current_date(self) -> tuple[int, int, int]:
        return self.year, self.month, self.day

    @property
    def current_time_of_day(self) -> int:
        if self.night_start < self.morning_start:
            if self.night_start <= self.hour < self.morning_start:
                return TimeOfDay.NIGHT.value

        if self.morning_start <= self.hour < self.afternoon_start:
            return TimeOfDay.MORNING.value

        elif self.afternoon_start <= self.hour < self.evening_start:
            return TimeOfDay.AFTERNOON.value

        elif self.evening_start <= self.hour < self.night_start:
            return TimeOfDay.EVENING.value

        else:
            return TimeOfDay.NIGHT.value

    @property
    def current_time_of_day_name(self) -> str:
        return TimeOfDay(self.current_time_of_day).name

    @property
    def current_week_day(self) -> int:
        return WeekDays(self.day % self.week_duration).value

    @property
    def current_week_day_name(self) -> str:
        return WeekDays(self.day % self.week_duration).name

    @property
    def year_duration_days(self) -> int:
        return self.year_duration * self.month_duration

    @property
    def current_season(self):
        return [*Season][self.month // self.length_of_seasons]

    def add_hours(self, hours_to_add: int) -> None:
        hours_sum = self.hour + hours_to_add
        if hours_sum < self.day_duration:
            self.hour = hours_sum

        else:
            self.hour = hours_sum % self.day_duration
            self.add_days(days_to_add=hours_sum // self.day_duration)

    def add_days(self, days_to_add: int) -> None:
        days_sum = self.day + days_to_add
        if days_sum <= self.month_duration:
            self.day = days_sum

        else:
            self.day = days_sum % self.month_duration
            self.add_months(months_to_add=days_sum // self.month_duration)

    def add_months(self, months_to_add: int) -> None:
        months_sum = self.month + months_to_add
        if months_sum < self.year_duration:
            self.month = months_sum

        else:
            self.month = months_sum % self.year_duration
            self.year += months_sum // self.year_duration

    def get_start_hour_tod(self, time_of_day: int) -> int:
        if time_of_day == TimeOfDay.MORNING.value:
            return self.morning_start

        elif time_of_day == TimeOfDay.AFTERNOON.value:
            return self.afternoon_start

        elif time_of_day == TimeOfDay.EVENING.value:
            return self.evening_start

        else:
            return self.night_start

    def skip_to(self, time_of_day: int) -> None:
        time_of_day_start = self.get_start_hour_tod(time_of_day=time_of_day)

        if self.hour < time_of_day_start:
            self.add_hours(hours_to_add=time_of_day_start - self.hour)
        else:
            self.add_hours(hours_to_add=time_of_day_start + (self.day_duration - self.hour))

    def estimate_date(self, days: int) -> tuple[int, int, int]:
        sum_days = (self.day - 1) + days
        sum_months_days = self.month * self.month_duration
        sum_year_days = (self.year - 1) * self.year_duration_days
        sum_all_days = sum_days + sum_months_days + sum_year_days

        year = sum_all_days // self.year_duration_days
        days_left = sum_all_days % self.year_duration_days

        months = days_left // self.month_duration
        days = days_left % self.month_duration + 1

        return year + 1, months, days

    def is_major_date(self, first_date: tuple[int, int, int], second_date: tuple[int, int, int]):
        date_1 = (first_date[0] - 1) * self.year_duration_days + first_date[1] * self.month_duration + first_date[2]
        date_2 = (second_date[0] - 1) * self.year_duration_days + second_date[1] * self.month_duration + second_date[2]

        return date_1 < date_2

    def coords_from_place(self, place: Biome | Entry) -> tuple:
        return next((eval(k) for k, v in self.map_settings.items() if v == place), None)

    def check_room_expiration(self, player: Player, npc: Npc) -> iter:
        for item, date in self.npcs[npc].room_expirations.items():
            if item in player.inventory.items.keys():
                if self.is_major_date(date, self.current_date):
                    yield item

    def add_npc(self, npc_key: str, npc: Npc) -> None:
        self.npcs[npc_key] = npc

    def place_from_list(self, place_list: list) -> Biome | Entry | None:
        place = self.map_settings[place_list[0]]
        for site in place_list[1:]:
            place = place.entries[site]
        return place

    def refresh_npcs(self) -> None:
        for npc_key, npc in self.npcs.items():
            place = None
            if npc.place is not None:
                place = self.place_from_list(place_list=npc.place)

            if place is not None and npc_key in place.npc:
                place.npc.remove(npc_key)

            npc.refresh_temporal(hour=self.hour)
            if npc.place is not None:
                self.place_from_list(place_list=npc.place).npc.append(npc_key)
