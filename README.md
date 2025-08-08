# ZipSearch

**Ultra-fast US zipcode lookup library with 100% backwards compatibility**

[![Compatibility](https://img.shields.io/badge/API-100%25_compatible-blue)](https://github.com/your-repo/zipsearch)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://github.com/your-repo/zipsearch)

ZipSearch is a drop-in replacement for [`uszipcode`](https://pypi.org/project/uszipcode) that delivers **>600x faster zipcode lookups** and **>50,000x faster city/state searches** by using pre-built RAM indices instead of SQLite queries.

## Key Features

- **Blazing Fast**: RAM-based O(1) lookups instead of SQLite queries
- **100% Compatible**: Drop-in replacement for `uszipcode` - no code changes needed
- **Complete Data**: All 42,724+ US zipcodes with demographics, coordinates, and boundaries
- **Multiple Search Types**: By zipcode, city/state, coordinates, prefix, and more
- **Batch Processing**: Optimized methods for bulk operations
- **Memory Efficient**: Pre-built indices loaded once at startup (11mb)

## Performance Comparison
![speed.png](media/speed.png)

## Installation

```bash
pip install zipsearch
```

## Quick Start

### Basic Usage (100% compatible with uszipcode)

```python
from zipsearch import SearchEngine

search = SearchEngine()

# Zipcode lookup
zipcode = search.by_zipcode("10001")
print(f"{zipcode.major_city}, {zipcode.state}")  # New York, NY

# City and state lookup  
zipcodes = search.by_city_and_state("Chicago", "IL")
print(f"Found {len(zipcodes)} zipcodes in Chicago")

# Coordinate-based search
nearby = search.by_coordinates(40.7128, -74.0060, radius=5)
print(f"Found {len(nearby)} zipcodes within 5 miles of NYC")
```

### Advanced Usage

```python
from zipsearch import FastSearchEngine

engine = FastSearchEngine()

# Batch processing for DataFrames
city_state_pairs = [("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL")]
results = engine.batch_city_state_lookup(city_state_pairs)

# Prefix search
manhattan_zips = engine.by_prefix("100")  # All 100xx zipcodes

# State-wide search
california_zips = engine.by_state("California")
```

## Complete API Reference

### SearchEngine (Backwards Compatible)

```python
search = SearchEngine()

# Single zipcode lookup
zipcode = search.by_zipcode("90210")

# City and state (handles full state names and abbreviations)
zipcodes = search.by_city_and_state("Beverly Hills", "California")
zipcodes = search.by_city_and_state("Beverly Hills", "CA")

# Coordinate search with radius (miles)
nearby = search.by_coordinates(34.0901, -118.4065, radius=10)

# Legacy query method (limited compatibility)
results = search.query(city="Austin", state="TX")
```

### FastSearchEngine (New Optimized API)

```python
engine = FastSearchEngine()

# All the same methods as SearchEngine, plus:
results = engine.by_city("Austin")  # Search by city across all states
results = engine.by_state("TX")     # All zipcodes in a state
results = engine.by_prefix("787")   # All zipcodes starting with 787

# Batch operations for ETL/DataFrame processing
batch_results = engine.batch_city_state_lookup([
    ("Austin", "TX"), 
    ("Houston", "TX"), 
    ("Dallas", "TX")
])
```

## 📊 Zipcode Data Fields

Each zipcode object contains comprehensive demographic and geographic data:

```python
zipcode = search.by_zipcode("10001")

# Geographic
print(zipcode.lat, zipcode.lng)           # 40.7505, -73.9934
print(zipcode.timezone)                   # Eastern
print(zipcode.radius_in_miles)            # 0.9090

# Administrative
print(zipcode.major_city)                 # New York
print(zipcode.county)                     # New York County
print(zipcode.state)                      # NY
print(zipcode.zipcode_type)              # STANDARD

# Demographics
print(zipcode.population)                 # 21102
print(zipcode.population_density)         # 23227.0
print(zipcode.median_home_value)          # 1000000
print(zipcode.median_household_income)    # 85066

# Area
print(zipcode.land_area_in_sqmi)         # 0.91
print(zipcode.water_area_in_sqmi)        # 0.0

# Boundaries
print(zipcode.bounds)                     # {'west': -74.0, 'east': -73.98, ...}

# Lists (JSON decoded)
print(zipcode.common_city_list)          # ['New York']
print(zipcode.area_code_list)            # ['212', '646', '332']
```

## Migration from uszipcode

**No code changes required!** Simply replace the import:

```python
# Before
from uszipcode import SearchEngine

# After  
from zipsearch import SearchEngine

# Everything else stays the same
search = SearchEngine()
zipcode = search.by_zipcode("10001")
```

### Performance Optimization Tips

For maximum performance in data processing workflows:

```python
# Use FastSearchEngine for new code
from zipsearch import FastSearchEngine
engine = FastSearchEngine()

# Use batch methods for DataFrame enrichment
results = engine.batch_city_state_lookup(city_state_pairs)

# Pre-load the engine once, reuse many times
class DataProcessor:
    def __init__(self):
        self.zipcode_engine = FastSearchEngine()  # Load once
    
    def enrich_dataframe(self, df):
        # Use self.zipcode_engine for all lookups
        pass
```

## Technical Architecture

### How It Works

1. **Pre-built Indices**: All zipcode data is pre-processed into optimized Python dictionaries
2. **Memory Loading**: Indices are loaded once at startup using pickle
3. **O(1) Lookups**: Direct dictionary access instead of SQL queries
4. **Smart Indexing**: Multiple index types for different search patterns:
   - `zipcode_index`: Direct zipcode → data mapping
   - `city_state_index`: (city, state) → [zipcodes] mapping  
   - `coordinate_grid`: Spatial grid for geographic searches

### Memory Usage

- **Index Size**: ~50MB RAM for all US zipcode data
- **Load Time**: ~100ms initial startup
- **Lookup Time**: ~0.0003ms per operation

### Data Sources

- Based on the same comprehensive dataset as `uszipcode`
- 42,724+ zipcodes with complete demographic and geographic data
- Regular updates to maintain data accuracy

## Requirements

- Python 3.7+
- No external dependencies for core functionality
- Compatible with pandas, numpy, and other data science libraries

## Benchmarks

Our comprehensive benchmarks show consistent performance improvements:

```
=== Zipcode Lookups ===
uszipcode:  100,000 ops in 17.57s  (5,692 ops/sec)
zipsearch: 1,000,000 ops in 0.26s  (3,827,112 ops/sec)
Speedup: 670x faster

=== City/State Lookups ===  
uszipcode:    2,500 ops in 74.36s    (34 ops/sec)
zipsearch: 1,000,000 ops in 0.58s   (1,740,366 ops/sec)
Speedup: 51,674x faster
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original `uszipcode` library for the comprehensive dataset and API design
- US Census Bureau for demographic data
- USPS for zipcode definitions

**⚡ Ready to make your zipcode lookups 670x faster? Install zipsearch today!**