from dataclasses import dataclass
from typing import Dict, List, Optional


# noinspection PyUnusedName
@dataclass
class FastZipcode:
    """Complete zipcode data matching SQLite schema."""
    zipcode: str
    zipcode_type: Optional[str] = None
    major_city: Optional[str] = None
    post_office_city: Optional[str] = None
    common_city_list: Optional[List[str]] = None
    county: Optional[str] = None
    state: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    timezone: Optional[str] = None
    radius_in_miles: Optional[float] = None
    area_code_list: Optional[List[str]] = None
    population: Optional[int] = None
    population_density: Optional[float] = None
    land_area_in_sqmi: Optional[float] = None
    water_area_in_sqmi: Optional[float] = None
    housing_units: Optional[int] = None
    occupied_housing_units: Optional[int] = None
    median_home_value: Optional[int] = None
    median_household_income: Optional[int] = None
    bounds_west: Optional[float] = None
    bounds_east: Optional[float] = None
    bounds_north: Optional[float] = None
    bounds_south: Optional[float] = None

    # Backwards compatibility aliases
    @property
    def city(self) -> Optional[str]:
        """Alias for major_city to match original zipsearch API."""
        return self.major_city

    @property
    def bounds(self) -> Optional[Dict[str, float]]:
        """Return bounds as dict like original API."""
        if all(x is not None for x in [self.bounds_west, self.bounds_east, self.bounds_north, self.bounds_south]):
            return {
                'west': self.bounds_west,
                'east': self.bounds_east,
                'north': self.bounds_north,
                'south': self.bounds_south
            }
        return None