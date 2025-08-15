# ZipSearch Documentation

ZipSearch is a Python library for US zipcode lookups and geographic data queries. It provides a drop-in replacement for the `uszipcode` library with significantly improved performance through pre-built RAM indices.

## Overview

ZipSearch offers two primary interfaces:

- **SearchEngine**: Backwards compatible API matching the original uszipcode library
- **FastSearchEngine**: Optimized API with additional methods for high-performance applications

The library includes comprehensive data for all 42,724+ US zipcodes, including demographic, geographic, and administrative information.

## Installation

```bash
pip install zipsearch
```

## Quick Start

### Basic Usage

```python
from zipsearch import SearchEngine

search = SearchEngine()

# Zipcode lookup
zipcode = search.by_zipcode("10001")
print(f"{zipcode.major_city}, {zipcode.state}")  # New York, NY

# City and state lookup  
zipcodes = search.by_city_and_state("Chicago", "IL")
print(f"Found {len(zipcodes)} zipcodes")

# Coordinate-based search
nearby = search.by_coordinates(40.7128, -74.0060, radius=5)
print(f"Found {len(nearby)} zipcodes within 5 miles")
```

### Advanced Usage

```python
from zipsearch import FastSearchEngine

engine = FastSearchEngine()

# Batch processing
city_state_pairs = [("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL")]
results = engine.batch_city_state_lookup(city_state_pairs)

# Prefix search
manhattan_zips = engine.by_prefix("100")  # All 100xx zipcodes

# State-wide search
california_zips = engine.by_state("California")
```

## Migration from uszipcode

ZipSearch maintains full API compatibility with uszipcode. To migrate existing code:

```python
# Before
from uszipcode import SearchEngine

# After  
from zipsearch import SearchEngine

# All existing code continues to work unchanged
search = SearchEngine()
zipcode = search.by_zipcode("10001")
```

## Documentation

### API Reference

- **[FastSearchEngine API](api.md)** - High-performance optimized interface
- **[Legacy API](legacy.md)** - Backwards compatible uszipcode interface
- **[Zipcode Data](zip-data.md)** - Complete field reference and data structure

### Core Features

- **Direct Lookups**: Exact zipcode queries
- **Geographic Search**: City/state and coordinate-based queries
- **Batch Operations**: Efficient processing of multiple queries
- **Prefix Matching**: Find zipcodes by partial matches
- **Complete Data**: Demographics, boundaries, and administrative information

## Performance Characteristics

ZipSearch uses pre-built in-memory indices for fast lookups:

| Operation | Performance |
|-----------|-------------|
| Zipcode lookup | ~0.0003ms |
| City/state search | ~0.0005ms |
| Coordinate search | ~0.002ms |
| Initial load time | ~100ms |
| Memory usage | ~50MB |

## Data Structure

Each zipcode result includes:

```python
zipcode = search.by_zipcode("10001")

# Geographic data
print(zipcode.lat, zipcode.lng)           # Coordinates
print(zipcode.timezone)                   # Time zone
print(zipcode.bounds)                     # Geographic boundaries

# Administrative data
print(zipcode.major_city)                 # Primary city
print(zipcode.county)                     # County name
print(zipcode.state)                      # State abbreviation

# Demographic data
print(zipcode.population)                 # Population count
print(zipcode.median_home_value)          # Housing values
print(zipcode.median_household_income)    # Income data
```

[View complete field reference →](zip-data.md)

## Common Use Cases

- **Data Processing**: ETL pipelines and DataFrame enrichment
- **Web Applications**: Address validation and geographic lookups
- **Analytics**: Demographic analysis and geographic research  
- **APIs**: High-throughput zipcode services

## Technical Architecture

ZipSearch achieves performance improvements through:

1. **Pre-built Indices**: Data pre-processed into optimized Python dictionaries
2. **Memory Resident**: All data loaded into RAM at startup
3. **Direct Access**: Hash table lookups instead of database queries
4. **Specialized Indices**: Different index structures for different query patterns

The library has no external dependencies and is thread-safe for concurrent access.

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT License

---

**Getting Started:**

- [Installation and basic usage](#quick-start)
- [API documentation](api.md)
- [Migration guide](#migration-from-uszipcode)
- [Complete data reference](zip-data.md)