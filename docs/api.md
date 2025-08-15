# ZipSearch API

The `FastSearchEngine` provides the high-performance core of ZipSearch with an optimized API designed for maximum speed and efficiency.

## Quick Start

```python
from zipsearch import FastSearchEngine

# Initialize once, reuse many times
engine = FastSearchEngine()

# Fast exact lookups
zipcode = engine.by_zipcode("10001")

# Optimized city/state search
zipcodes = engine.by_city_and_state("New York", "NY")

# Batch processing for DataFrames
pairs = [("Chicago", "IL"), ("Houston", "TX"), ("Phoenix", "AZ")]
results = engine.batch_city_state_lookup(pairs)
```

## API Reference

::: zipsearch.FastSearchEngine
    options:
      members:
        - __init__
        - by_zipcode
        - by_city_and_state
        - by_coordinates
        - by_city
        - by_state
        - by_prefix
        - batch_city_state_lookup
        - close
      show_source: false
      heading_level: 3
      show_root_heading: false

## Usage Patterns

### Single Lookups

For individual zipcode lookups, use the direct methods:

```python
engine = FastSearchEngine()

# Most common pattern - exact zipcode lookup
zipcode = engine.by_zipcode("90210")
if zipcode:
    print(f"{zipcode.city}, {zipcode.state}")
```

### Bulk Processing

For processing large datasets, use batch methods:

```python
# DataFrame enrichment example
import pandas as pd

df = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago'],
    'state': ['NY', 'CA', 'IL']
})

# Batch lookup all city/state pairs
city_state_pairs = list(zip(df['city'], df['state']))
results = engine.batch_city_state_lookup(city_state_pairs)

# Add zipcode data to DataFrame
df['zipcodes'] = [results.get((city, state), []) for city, state in city_state_pairs]
```

### Geographic Search

For location-based queries:

```python
# Find all zipcodes within 25 miles of coordinates
lat, lng = 40.7128, -74.0060  # NYC coordinates
nearby_zipcodes = engine.by_coordinates(lat, lng, radius=25)

# Results are automatically sorted by distance
for zipcode in nearby_zipcodes[:10]:  # Closest 10
    print(f"{zipcode.zipcode}: {zipcode.city} ({zipcode.major_city})")
```

### State and Regional Analysis

For broader geographic analysis:

```python
# Get all zipcodes in a state
texas_zipcodes = engine.by_state("TX")
print(f"Texas has {len(texas_zipcodes)} zipcodes")

# Regional prefix search
southwest_zips = engine.by_prefix("85")  # Arizona area codes
```

## Best Practices

### Memory Management

```python
# Initialize once per application/process
class ZipcodeService:
    def __init__(self):
        self.engine = FastSearchEngine()  # Load indices once
    
    def lookup_zipcode(self, zipcode):
        return self.engine.by_zipcode(zipcode)
    
    def enrich_addresses(self, addresses):
        # Use batch methods for multiple lookups
        city_state_pairs = [(addr['city'], addr['state']) for addr in addresses]
        return self.engine.batch_city_state_lookup(city_state_pairs)
```

### Error Handling

```python
# Always check for None results
zipcode = engine.by_zipcode("invalid")
if zipcode is None:
    print("Zipcode not found")

# Handle empty results gracefully
zipcodes = engine.by_city_and_state("NonexistentCity", "XX")
if not zipcodes:
    print("No zipcodes found for this city/state")
```

### Performance Optimization

```python
# Cache the engine instance
engine = FastSearchEngine()

# Use specific methods instead of generic query
# Good: engine.by_zipcode("10001")
# Avoid: SearchEngine().query(zipcode="10001")

# Batch process when possible
# Good: engine.batch_city_state_lookup(pairs)
# Avoid: [engine.by_city_and_state(c, s) for c, s in pairs]
```