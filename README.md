# ZipSearch

**Ultra-fast US zipcode lookup library with 100% backwards compatibility**



ZipSearch is a drop-in replacement for [`uszipcode`](https://pypi.org/project/uszipcode) that delivers **>600x faster zipcode lookups** and **>50,000x faster city/state searches** by using pre-built RAM indices instead of SQLite queries.

---

### [ReadTheDocs](https://zipsearch.readthedocs.io/en/latest)

---

## Key Features

- **Blazing Fast**: RAM-based O(1) lookups instead of SQLite queries
- **100% Compatible**: Drop-in replacement for `uszipcode` - no code changes needed
- **Complete Data**: All 42,724+ US zipcodes with demographics, coordinates, and boundaries
- **Multiple Search Types**: By zipcode, city/state, coordinates, prefix, and more
- **Batch Processing**: Optimized methods for bulk operations
- **Memory Efficient**: Pre-built indices loaded once at startup (11mb)

## Performance Comparison

![speed.png](https://github.com/Kydoimos97/zipsearch/blob/main/media/speed.png?raw=true)

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

- Python 3.11+
- No external dependencies

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

MIT License

## Acknowledgments

- Original `uszipcode` library for the comprehensive dataset and API design
- US Census Bureau for demographic data
- USPS for zipcode definitions

**⚡ Ready to make your zipcode lookups 670x faster? Install zipsearch today!**
