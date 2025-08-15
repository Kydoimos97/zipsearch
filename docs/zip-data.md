# Zipcode Data Reference

The `FastZipcode` dataclass contains comprehensive demographic, geographic, and administrative data for each US zipcode. This page documents all available fields and their meanings.

## FastZipcode Class

::: zipsearch.FastZipcode
    options:
      show_source: false
      heading_level: 3

## Field Reference

### Administrative Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `zipcode` | `str` | 5-digit zipcode | `"10001"` |
| `zipcode_type` | `Optional[str]` | Type classification | `"STANDARD"`, `"PO BOX"`, `"UNIQUE"` |
| `major_city` | `Optional[str]` | Primary city name | `"New York"` |
| `post_office_city` | `Optional[str]` | Official post office city | `"New York"` |
| `common_city_list` | `Optional[List[str]]` | Alternative city names | `["New York", "Manhattan"]` |
| `county` | `Optional[str]` | County name | `"New York County"` |
| `state` | `Optional[str]` | 2-letter state abbreviation | `"NY"` |

### Geographic Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `lat` | `Optional[float]` | Latitude in decimal degrees | `40.7505` |
| `lng` | `Optional[float]` | Longitude in decimal degrees | `-73.9934` |
| `timezone` | `Optional[str]` | Timezone name | `"Eastern"` |
| `radius_in_miles` | `Optional[float]` | Approximate radius coverage | `0.9090` |
| `bounds_west` | `Optional[float]` | Western boundary longitude | `-74.0` |
| `bounds_east` | `Optional[float]` | Eastern boundary longitude | `-73.98` |
| `bounds_north` | `Optional[float]` | Northern boundary latitude | `40.76` |
| `bounds_south` | `Optional[float]` | Southern boundary latitude | `40.74` |

### Area Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `land_area_in_sqmi` | `Optional[float]` | Land area in square miles | `0.91` |
| `water_area_in_sqmi` | `Optional[float]` | Water area in square miles | `0.0` |

### Communication Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `area_code_list` | `Optional[List[str]]` | Phone area codes | `["212", "646", "332"]` |

### Demographic Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `population` | `Optional[int]` | Total population | `21102` |
| `population_density` | `Optional[float]` | People per square mile | `23227.0` |
| `housing_units` | `Optional[int]` | Total housing units | `12476` |
| `occupied_housing_units` | `Optional[int]` | Occupied housing units | `11031` |

### Economic Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `median_home_value` | `Optional[int]` | Median home value in USD | `1000000` |
| `median_household_income` | `Optional[int]` | Median household income in USD | `85066` |

## Backwards Compatibility Properties

For compatibility with the original uszipcode API, the following properties are available:

### city Property

```python
@property
def city(self) -> Optional[str]:
    """Alias for major_city to match original zipsearch API."""
    return self.major_city
```

**Usage:**
```python
zipcode = engine.by_zipcode("10001")
print(zipcode.city)        # "New York" (alias)
print(zipcode.major_city)  # "New York" (direct field)
```

### bounds Property

```python
@property
def bounds(self) -> Optional[Dict[str, float]]:
    """Return bounds as dict like original API."""
```

**Usage:**
```python
zipcode = engine.by_zipcode("10001")
print(zipcode.bounds)
# {'west': -74.0, 'east': -73.98, 'north': 40.76, 'south': 40.74}

# Or access individual bounds
print(zipcode.bounds_west)   # -74.0
print(zipcode.bounds_east)   # -73.98
print(zipcode.bounds_north)  # 40.76
print(zipcode.bounds_south)  # 40.74
```

## Usage Examples

### Basic Data Access

```python
from zipsearch import FastSearchEngine

engine = FastSearchEngine()
zipcode = engine.by_zipcode("90210")

# Administrative information
print(f"Zipcode: {zipcode.zipcode}")
print(f"City: {zipcode.major_city}")
print(f"State: {zipcode.state}")
print(f"County: {zipcode.county}")
print(f"Type: {zipcode.zipcode_type}")

# Geographic information
print(f"Coordinates: {zipcode.lat}, {zipcode.lng}")
print(f"Timezone: {zipcode.timezone}")
print(f"Area: {zipcode.land_area_in_sqmi} sq mi")
```

### Demographic Analysis

```python
# Population and housing data
if zipcode.population:
    print(f"Population: {zipcode.population:,}")
    print(f"Density: {zipcode.population_density:.1f} people/sq mi")
    
if zipcode.median_household_income:
    print(f"Median Income: ${zipcode.median_household_income:,}")
    
if zipcode.median_home_value:
    print(f"Median Home Value: ${zipcode.median_home_value:,}")

# Housing statistics
if zipcode.housing_units and zipcode.occupied_housing_units:
    occupancy_rate = zipcode.occupied_housing_units / zipcode.housing_units
    print(f"Occupancy Rate: {occupancy_rate:.1%}")
```

### Geographic Boundaries

```python
# Using the bounds property
bounds = zipcode.bounds
if bounds:
    width_miles = (bounds['east'] - bounds['west']) * 69  # Rough conversion
    height_miles = (bounds['north'] - bounds['south']) * 69
    print(f"Approximate size: {width_miles:.1f} x {height_miles:.1f} miles")

# Direct boundary access
if all(x is not None for x in [zipcode.bounds_north, zipcode.bounds_south]):
    lat_range = zipcode.bounds_north - zipcode.bounds_south
    print(f"Latitude range: {lat_range:.4f} degrees")
```

### List Fields

```python
# Area codes
if zipcode.area_code_list:
    print(f"Area codes: {', '.join(zipcode.area_code_list)}")

# Alternative city names
if zipcode.common_city_list:
    print(f"Also known as: {', '.join(zipcode.common_city_list)}")
```

## Data Validation

Most fields are optional and may be `None` for certain zipcodes. Always check for `None` values:

```python
# Safe access pattern
zipcode = engine.by_zipcode("12345")

if zipcode is None:
    print("Zipcode not found")
else:
    # Check individual fields
    if zipcode.population:
        print(f"Population: {zipcode.population}")
    else:
        print("Population data not available")
    
    if zipcode.lat and zipcode.lng:
        print(f"Coordinates: {zipcode.lat}, {zipcode.lng}")
    else:
        print("Coordinate data not available")
```

## Data Sources

The zipcode data is sourced from:

- **US Census Bureau**: Population, demographics, and housing data
- **USPS**: Official zipcode definitions and classifications  
- **Geographic Data**: Coordinate and boundary information
- **Economic Data**: Income and home value statistics

All data fields maintain compatibility with the original uszipcode dataset structure.