# Imports.
# Local imports.
from .biome import Biome, Entry
from .enums import Months, Season, TimeOfDay, WeekDays
from .npc import Npc
from .player import Player
from .utils import label_pixels, tl_map_set
from .utils_settings import init_map_setting
from .globals import MAP_TILE_PATH

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
    npcs: dict[str, Npc] = field(default=None)
    biomes: dict = field(default=None)
    entries: dict = field(default=None)
    mobs: dict = field(default=None)
    x_len: int = field(init=False)
    y_len: int = field(init=False)

    # Others.
    last_hour: int = field(default=6)

    def __attrs_post_init__(self):
        if self.map_labels is None:
            self.map_labels = label_pixels(MAP_TILE_PATH)

        if self.map_init_settings is None:
            pass

        if self.map_settings is None:
            self.map_settings = tl_map_set(tl_map=self.map_labels,
                                           biomes=self.biomes)
            init_map_setting(ms=self.map_settings)

        if self.npcs is None:
            self.npcs = {}

        self.x_len = len(self.map_labels) - 1
        self.y_len = len(self.map_labels[0]) - 1

    # Control methods.
    def get_label(self, x: int, y: int) -> str:
        return self.map_labels[y][x]

    def get_current_biome_name(self, x: int, y: int) -> str:
        return self.map_settings[(x, y)].name[self.current_month]

    # Time methods.
    @property
    def get_hours(self):
        sum_days = (self.day - 1)
        sum_months_days = self.month * self.month_duration
        sum_year_days = (self.year - 1) * self.year_duration_days
        sum_all_days = sum_days + sum_months_days + sum_year_days

        return sum_all_days * 24 + self.hour

    @property
    def current_date(self) -> tuple[int, int, int]:
        return self.year, self.month, self.day

    @property
    def current_time_of_day(self) -> int:
        return self.time_of_day_from_hour(hour=self.hour)

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
    def current_month(self) -> int:
        return self.month

    @property
    def current_season(self):
        return [*Season][self.month // self.length_of_seasons]

    @property
    def year_duration_days(self) -> int:
        return self.year_duration * self.month_duration

    def time_of_day_from_hour(self, hour: int) -> int:
        if self.night_start < self.morning_start:
            if self.night_start <= hour < self.morning_start:
                return TimeOfDay.NIGHT.value

        if self.morning_start <= hour < self.afternoon_start:
            return TimeOfDay.MORNING.value

        elif self.afternoon_start <= hour < self.evening_start:
            return TimeOfDay.AFTERNOON.value

        elif self.evening_start <= hour < self.night_start:
            return TimeOfDay.EVENING.value

        else:
            return TimeOfDay.NIGHT.value

    def add_hours(self, hours_to_add: int) -> None:
        self.last_hour = self.hour
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
        if first_date is None or second_date is None:
            return None

        date_1 = (first_date[0] - 1) * self.year_duration_days + first_date[1] * self.month_duration + first_date[2]
        date_2 = (second_date[0] - 1) * self.year_duration_days + second_date[1] * self.month_duration + second_date[2]
        return date_1 < date_2

    # Place methods.
    def place_from_list(self, place_list: list) -> Biome | Entry:
        place = self.map_settings[place_list[0]]
        for site in place_list[1:]:
            place = place.entries[site]

        if place is None:
            raise ValueError(f"{place_list} is not a place.")
        return place

    def neighbors_from_coord(self, coord: tuple):
        neighbors = []
        x, y = coord
        if y > 0:
            neighbors.append(self.map_settings[(x, y - 1)])
        if x < self.x_len:
            neighbors.append(self.map_settings[(x + 1, y)])
        if y < self.y_len:
            neighbors.append(self.map_settings[(x, y + 1)])
        if x > 0:
            neighbors.append(self.map_settings[(x - 1, y)])
        return neighbors

    def get_region_name(self, x: int, y: int) -> str:
        return "NAIWAT"

    # Npc methods.
    def check_room_expiration(self, player: Player, npc: str) -> iter:
        for item, date in self.npcs[npc].room_expirations.items():
            if item in player.inventory.items.keys():
                if self.is_major_date(date, self.current_date):
                    yield item

    def add_npc(self, npc_key: str, npc: Npc) -> None:
        self.npcs[npc_key] = npc

    def refresh_npcs(self) -> None:
        time_of_days, hours_time_of_days = [], []
        for hour in [h % 24 for h in range(self.last_hour, self.hour + 1)]:
            time_of_day = self.time_of_day_from_hour(hour=hour)
            if time_of_day not in time_of_days:
                time_of_days.append(time_of_day)
                hours_time_of_days.append(hour)

        for npc_key, npc in self.npcs.items():
            place = None
            if npc.place is not None:
                place = self.place_from_list(place_list=npc.place)

            if place is not None and npc_key in place.npcs:
                place.remove_npc(npc=npc_key)

            for hour in hours_time_of_days:
                npc.refresh_temporal(hour=hour)

            if npc.place is not None:
                self.place_from_list(place_list=npc.place).add_npc(npc=npc_key)

    # Refreshing methods.
    def refresh_biomes(self):
        for biome in self.map_settings.values():
            biome.refresh_biome(day=self.day,
                                neighboors=self.neighbors_from_coord(coord=biome.coordinates))

    def refresh_map(self) -> None:
        self.refresh_npcs()
        self.refresh_biomes()

    # Player control methods.
    def get_avaible_moves(self, player: Player) -> list:
        active_moves = [0, 0, 0, 0]
        month = self.current_month
        current_tile = self.map_labels[player.y][player.x]
        if not player.outside:
            return active_moves

        directions = [
            (0, -1, 0),  # North
            (1, 0, 1),  # East
            (0, 1, 2),  # South
            (-1, 0, 3)  # West
        ]

        for dx, dy, idx in directions:
            nx, ny = player.x + dx, player.y + dy

            if not (0 <= nx < self.y_len and 0 <= ny < self.x_len):
                continue

            ms_tile = self.map_settings[(nx, ny)]

            if not ms_tile.is_accessible_from(biome=current_tile):
                continue

            label_tile = self.map_labels[ny][nx]
            if not player.place.is_accessible_to(biome=label_tile):
                continue

            all_req = all(player.has(item=req) for req in ms_tile.get_req(month=month))
            all_status = player.status in ms_tile.get_status(month=month)

            if all_req and all_status:
                active_moves[idx] = 1

        return active_moves
