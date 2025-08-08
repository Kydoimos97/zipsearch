#!/usr/bin/env python3
"""
build_fast_indices.py

Run once: python build_fast_indices.py
Generates: /bin/indices.bin
"""

import pickle
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Import utils directly to avoid circular imports
from zipsearch.utils import _decode_blob


@dataclass
class FastZipcode:
    """Local copy of FastZipcode for building indices (avoids circular imports)."""
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


def build_fast_indices(sqlite_path: str = None):
    """Build single optimized index file."""

    # Find SQLite database
    if sqlite_path is None:
        possible_paths = [
            "simple_db.sqlite",
            "~/.zipsearch/simple_db.sqlite",
            Path.home() / ".zipsearch" / "simple_db.sqlite"
        ]

        for path in possible_paths:
            if Path(path).expanduser().exists():
                sqlite_path = str(Path(path).expanduser())
                break

        if sqlite_path is None:
            raise FileNotFoundError("simple_db.sqlite not found")

    # Create output directory
    # output_dir = Path("bin")
    # output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Building fast indices from {sqlite_path}")

    # Load all data from SQLite
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT zipcode, zipcode_type, major_city, post_office_city, common_city_list,
               county, state, lat, lng, timezone, radius_in_miles, area_code_list,
               population, population_density, land_area_in_sqmi, water_area_in_sqmi,
               housing_units, occupied_housing_units, median_home_value, 
               median_household_income, bounds_west, bounds_east, bounds_north, bounds_south
        FROM simple_zipcode
    """)

    # Build all indices
    zipcode_index = {}
    city_state_index = {}
    coordinate_grid = {}

    for row in cursor.fetchall():
        # Unpack all 24 fields
        (zipcode, zipcode_type, major_city, post_office_city, common_city_list_blob,
         county, state, lat, lng, timezone, radius_in_miles, area_code_list_blob,
         population, population_density, land_area_in_sqmi, water_area_in_sqmi,
         housing_units, occupied_housing_units, median_home_value,
         median_household_income, bounds_west, bounds_east, bounds_north, bounds_south) = row

        # Create FastZipcode dataclass
        zipcode_data = FastZipcode(
            zipcode=zipcode.zfill(5) if zipcode else None,
            zipcode_type=zipcode_type,
            major_city=major_city.strip().title() if major_city else None,
            post_office_city=post_office_city.strip().title() if post_office_city else None,
            common_city_list=_decode_blob(common_city_list_blob),
            county=county,
            state=state.strip().upper() if state else None,
            lat=lat,
            lng=lng,
            timezone=timezone,
            radius_in_miles=radius_in_miles,
            area_code_list=_decode_blob(area_code_list_blob),
            population=population,
            population_density=population_density,
            land_area_in_sqmi=land_area_in_sqmi,
            water_area_in_sqmi=water_area_in_sqmi,
            housing_units=housing_units,
            occupied_housing_units=occupied_housing_units,
            median_home_value=median_home_value,
            median_household_income=median_household_income,
            bounds_west=bounds_west,
            bounds_east=bounds_east,
            bounds_north=bounds_north,
            bounds_south=bounds_south
        )

        # Primary zipcode index
        if zipcode_data.zipcode:
            zipcode_index[zipcode_data.zipcode] = zipcode_data.__dict__

        # City/state index
        if zipcode_data.major_city and zipcode_data.state:
            key = (zipcode_data.major_city, zipcode_data.state)
            if key not in city_state_index:
                city_state_index[key] = []
            city_state_index[key].append(zipcode_data.__dict__)

        # Spatial grid index
        if zipcode_data.lat is not None and zipcode_data.lng is not None:
            lat_grid = int(zipcode_data.lat * 10)
            lng_grid = int(zipcode_data.lng * 10)
            grid_key = (lat_grid, lng_grid)
            if grid_key not in coordinate_grid:
                coordinate_grid[grid_key] = []
            coordinate_grid[grid_key].append(zipcode_data.__dict__)

    conn.close()

    # Save single combined index file
    all_indices = {
        'zipcode_index': zipcode_index,
        'city_state_index': city_state_index,
        'coordinate_grid': coordinate_grid
    }

    output_file = Path("indices.bin")
    with open(output_file, 'wb') as f:
        pickle.dump(all_indices, f, protocol=pickle.HIGHEST_PROTOCOL)

    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"Built fast indices: {len(zipcode_index)} zipcodes, {size_mb:.1f}MB")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    import sys
    sqlite_path = sys.argv[1] if len(sys.argv) > 1 else None
    build_fast_indices(sqlite_path)