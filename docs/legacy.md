# Legacy API

The legacy API provides 100% backwards compatibility with the original `uszipcode` library. This ensures that existing code can migrate to ZipSearch without any modifications.

## Overview

The `SearchEngine` class maintains the exact same interface as the original `uszipcode.SearchEngine`, but with dramatically improved performance through pre-built RAM indices.

## Migration

Simply change your import statement:

```python
# Before
from uszipcode import SearchEngine

# After  
from zipsearch import SearchEngine

# Everything else stays exactly the same
search = SearchEngine()
zipcode = search.by_zipcode("10001")
```

## Query Method

The `query` method provides the most flexible search interface, supporting multiple search patterns and filters in a single call.

::: zipsearch.boilerplate.SearchEngine.query

## Performance Notes

While the legacy API maintains full compatibility, consider using the new `FastSearchEngine` class for optimal performance:

- Direct method calls (`by_zipcode`, `by_city_and_state`) are faster than the generic `query` method
- Batch operations are available for ETL workflows
- Simplified parameter handling reduces overhead

## Examples

### Basic Searches

```python
from zipsearch import SearchEngine

search = SearchEngine()

# Single zipcode lookup
results = search.query(zipcode="90210")

# City and state search
results = search.query(city="Beverly Hills", state="CA")

# Coordinate search
results = search.query(lat=34.0901, lng=-118.4065, radius=10)
```

### Advanced Filtering

```python
# Demographic filtering
results = search.query(
    state="CA",
    population_lower=50000,
    population_upper=100000,
    returns=20
)

# Prefix search
results = search.query(prefix="902", returns=10)
```

### Compatibility Notes

- Complex demographic queries are simplified but functional
- All original parameter names and types are supported
- Return objects maintain identical structure and properties
- Error handling behavior matches original implementation