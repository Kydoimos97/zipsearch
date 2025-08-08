#!/usr/bin/env python3
"""
Simple speed test comparison between old and new uszipcode implementations.
Generates visualization saved to ./media/speed.png
"""
import os
import time
import random
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from WrenchCL import logger
import uszipcode
import zipsearch

def generate_test_data():
    """Load real test data from indices.bin file."""
    logger.info("Loading real test data from indices.bin...")

    import pickle

    indices_path = r"./zipsearch/bin/indices.bin"

    try:
        with open(indices_path, 'rb') as f:
            all_indices = pickle.load(f)

        zipcode_index = all_indices['zipcode_index']
        city_state_index = all_indices['city_state_index']

        # Extract real zipcodes
        zipcodes = list(zipcode_index.keys())
        logger.info(f"Loaded {len(zipcodes):,} real zipcodes")

        # Extract real city/state pairs
        city_state_pairs = list(city_state_index.keys())
        logger.info(f"Loaded {len(city_state_pairs):,} real city/state pairs")

        return zipcodes, city_state_pairs

    except FileNotFoundError:
        logger.warning(f"indices.bin not found at {indices_path}, using fallback data")
        return generate_fallback_data()
    except Exception as e:
        logger.warning(f"Error loading indices.bin: {e}, using fallback data")
        return generate_fallback_data()

def generate_fallback_data():
    """Generate diverse test data if indices.bin not available."""
    logger.info("Generating fallback test data...")

    # Generate 100k diverse zipcodes
    zipcodes = [f"{random.randint(1000, 99999):05d}" for _ in range(100000)]

    # Generate 100k diverse city/state pairs
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
              "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
              "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
              "Seattle", "Denver", "Boston", "El Paso", "Detroit", "Nashville", "Portland",
              "Oklahoma City", "Las Vegas", "Louisville", "Baltimore", "Milwaukee"]

    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "WA", "CO", "MA", "OH", "NC",
              "TN", "OR", "OK", "NV", "KY", "MD", "WI", "NM", "IN", "MI", "NE", "ID", "WV"]

    city_state_pairs = [(random.choice(cities), random.choice(states)) for _ in range(100000)]

    logger.info(f"Generated {len(zipcodes):,} zipcodes and {len(city_state_pairs):,} city/state pairs")
    return zipcodes, city_state_pairs

def test_old_version():
    """Test old uszipcode version performance."""
    logger.info("Testing OLD uszipcode version...")

    import subprocess
    import sys

    try:
        # Import old version
        import uszipcode
        search = uszipcode.SearchEngine()

        zipcodes, city_state_pairs = generate_test_data()

        # Test zipcode lookups (reduced sample due to performance)
        zipcode_test_size = 100000  # 100k operations for zipcode lookups
        logger.info(f"Running {zipcode_test_size:,} zipcode lookups...")

        start_time = time.time()
        # Use real zipcode data, cycling through to get test_size operations
        zipcode_cycle = (zipcodes * ((zipcode_test_size // len(zipcodes)) + 1))[:zipcode_test_size]

        for i, zipcode in enumerate(zipcode_cycle):
            result = search.by_zipcode(zipcode)

            if (i + 1) % 10000 == 0:  # Report every 10k
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                logger.info(f"  {i+1:,}/{zipcode_test_size:,} complete ({rate:.0f} ops/sec)")

        zipcode_total_time = time.time() - start_time
        zipcode_per_op = zipcode_total_time / zipcode_test_size

        logger.info(f"Zipcode lookup: {zipcode_per_op*1000:.2f}ms per op, {zipcode_total_time:.2f}s total")

        # Test city/state lookups (much smaller sample - these are very slow)
        citystate_test_size = 500  # Only 5k operations for city/state lookups
        logger.info(f"Running {citystate_test_size:,} city/state lookups...")

        start_time = time.time()
        # Use real city/state data, cycling through to get test_size operations
        citystate_cycle = (city_state_pairs * ((citystate_test_size // len(city_state_pairs)) + 1))[:citystate_test_size]

        for i, (city, state) in enumerate(citystate_cycle):
            try:
                result = search.by_city_and_state(city, state)
            except Exception as e:
                logger.warning(f"Error in city/state lookup: {e}")
                logger.warning(f"  {city}, {state}")
            if (i + 1) % 100 == 0:  # Report every 1k for smaller test
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                logger.info(f"  {i+1:,}/{citystate_test_size:,} complete ({rate:.0f} ops/sec)")

        citystate_total_time = time.time() - start_time
        citystate_per_op = citystate_total_time / citystate_test_size

        logger.info(f"City/state lookup: {citystate_per_op*1000:.2f}ms per op, {citystate_total_time:.2f}s total")

        search.close()

        return {
            'zipcode_lookup_time': zipcode_per_op,
            'citystate_lookup_time': citystate_per_op,
            'total_zipcode_time': zipcode_total_time,
            'total_citystate_time': citystate_total_time,
        }

    except Exception as e:
        logger.warning(f"Could not test old version: {e}")
        logger.info("Using simulated results based on known SQL performance")
        raise

def test_new_version():
    """Test new uszipcode version performance."""
    logger.info("Testing NEW zipsearch version...")

    from zipsearch import SearchEngine

    search = SearchEngine()
    zipcodes, city_state_pairs = generate_test_data()

    # Test individual zipcode lookups (1M operations)
    test_size = 1000000
    logger.info(f"Running {test_size:,} zipcode lookups...")

    start_time = time.time()
    # Cycle through real zipcodes to get 1M operations
    zipcode_cycle = (zipcodes * ((test_size // len(zipcodes)) + 1))[:test_size]

    for i, zipcode in enumerate(zipcode_cycle):
        result = search.by_zipcode(zipcode)

        if (i + 1) % 100000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            logger.info(f"  {i+1:,}/1M complete ({rate:.0f} ops/sec)")

    zipcode_total_time = time.time() - start_time
    zipcode_per_op = zipcode_total_time / test_size

    logger.info(f"Zipcode lookup: {zipcode_per_op*1000:.4f}ms per op, {zipcode_total_time:.2f}s total")

    # Test individual city/state lookups (1M operations)
    logger.info(f"Running {test_size:,} city/state lookups...")

    start_time = time.time()
    # Cycle through real city/state pairs to get 1M operations
    citystate_cycle = (city_state_pairs * ((test_size // len(city_state_pairs)) + 1))[:test_size]

    for i, (city, state) in enumerate(citystate_cycle):
        result = search.by_city_and_state(city, state)

        if (i + 1) % 100000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            logger.info(f"  {i+1:,}/1M complete ({rate:.0f} ops/sec)")

    citystate_total_time = time.time() - start_time
    citystate_per_op = citystate_total_time / test_size

    logger.info(f"City/state lookup: {citystate_per_op*1000:.4f}ms per op, {citystate_total_time:.2f}s total")

    # Test batch operations
    batch_results = {}
    for batch_size in [10000, 50000, 100000, 500000]:
        logger.info(f"Running batch of {batch_size:,} operations...")

        start_time = time.time()
        # Use real data for batch operations, cycling if needed
        batch_data = (city_state_pairs * ((batch_size // len(city_state_pairs)) + 1))[:batch_size]
        results = search.batch_city_state_lookup(batch_data)
        batch_time = time.time() - start_time

        batch_results[batch_size] = {
            'total_time': batch_time,
            'per_op_time': batch_time / batch_size
        }

        logger.info(f"Batch {batch_size:,}: {batch_time:.2f}s total, {(batch_time/batch_size)*1000:.4f}ms per op")

    return {
        'zipcode_lookup_time': zipcode_per_op,
        'citystate_lookup_time': citystate_per_op,
        'total_zipcode_time': zipcode_total_time,
        'total_citystate_time': citystate_total_time,
        'batch_results': batch_results
    }

def create_visualization(old_results, new_results):
    """Create performance comparison charts focused on improvement."""

    # Set dark mode style
    plt.style.use('dark_background')

    fig = plt.figure(figsize=(18, 12))
    fig.patch.set_facecolor('#1e1e1e')

    # Colors - muted gray for old, vibrant green for new/improved
    old_color = '#666666'  # Muted gray for old/slow
    new_color = '#8f2323'  # Vibrant green for new/improved
    accent_color = '#ffffff'  # Orange accent for highlights

    # Create grid layout - 2x2 with different emphasis
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1], width_ratios=[1.5, 1])

    # 1. Main speedup comparison (focus on improvement)
    ax1 = fig.add_subplot(gs[0, :])

    operations = ['Zipcode Lookup', 'City/State Lookup']
    speedups = [
        old_results['zipcode_lookup_time'] / new_results['zipcode_lookup_time'],
        old_results['citystate_lookup_time'] / new_results['citystate_lookup_time']
    ]

    # Create horizontal bars showing speedup
    bars = ax1.barh(operations, speedups, color=[new_color, new_color],
                    alpha=0.9, height=0.6, edgecolor='white', linewidth=2)

    ax1.set_xlabel('Performance Improvement (x times faster)', fontsize=14, color='white', fontweight='bold')
    ax1.set_title('ZipSearch Performance Gains vs USZipcode', fontsize=18, fontweight='bold',
                  color='white', pad=25)
    ax1.grid(True, alpha=0.3, axis='x')
    ax1.set_facecolor('#2a2a2a')

    # Add speedup labels with emphasis
    for i, (bar, speedup) in enumerate(zip(bars, speedups)):
        width = bar.get_width()
        ax1.text(width + max(speedups) * 0.02, bar.get_y() + bar.get_height()/2,
                f'{speedup:.0f}x faster', ha='left', va='center',
                fontsize=16, color=accent_color, fontweight='bold')

        # Add baseline reference
        ax1.axvline(x=1, color=old_color, linestyle='--', alpha=0.7, linewidth=2)
        ax1.text(1, -0.3, 'USZipcode baseline', ha='center', va='top',
                color=accent_color, fontsize=10, style='italic')

    ax1.set_xlim(0, max(speedups) * 1.15)

    # 2. Time comparison with emphasis on new performance
    ax2 = fig.add_subplot(gs[1, 0])

    old_times_ms = [old_results['zipcode_lookup_time']*1000, old_results['citystate_lookup_time']*1000]
    new_times_ms = [new_results['zipcode_lookup_time']*1000, new_results['citystate_lookup_time']*1000]

    x = np.arange(len(operations))
    width = 0.35

    # Old times in muted color, new times prominent
    bars1 = ax2.bar(x - width/2, old_times_ms, width, label='USZipcode (old)',
                    color=old_color, alpha=0.6)
    bars2 = ax2.bar(x + width/2, new_times_ms, width, label='ZipSearch (new)',
                    color=new_color, alpha=0.9)

    ax2.set_ylabel('Time per Operation (ms)', fontsize=12, color='white')
    ax2.set_title('Response Time Comparison', fontsize=14, fontweight='bold', color='white')
    ax2.set_xticks(x)
    ax2.set_xticklabels(operations, fontsize=11)
    ax2.set_yscale('log')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.2)
    ax2.set_facecolor('#2a2a2a')

    # Add value labels - emphasize the new performance
    for bar, val in zip(bars1, old_times_ms):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height * 1.1, f'{val:.1f}ms',
                ha='center', va='bottom', fontsize=9, color=accent_color)

    for bar, val in zip(bars2, new_times_ms):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height * 1.1, f'{val:.4f}ms',
                ha='center', va='bottom', fontsize=10, color=accent_color, fontweight='bold')

    # 3. Linear extrapolation chart for large-scale operations
    ax3 = fig.add_subplot(gs[1, 1])

    # Operation counts for realistic large-scale scenarios
    op_counts = np.array([100000, 500000, 1000000, 5000000, 10000000])  # 100K to 10M

    # Calculate processing times in minutes for city/state (worst case)
    old_times_min = (op_counts * old_results['citystate_lookup_time']) / 60
    new_times_min = (op_counts * new_results['citystate_lookup_time']) / 60

    # Plot with emphasis on the new performance
    ax3.plot(op_counts/1000000, old_times_min, 'o-', color=old_color,
             linewidth=2, markersize=6, alpha=0.7, label='USZipcode')
    ax3.plot(op_counts/1000000, new_times_min, 'o-', color=new_color,
             linewidth=4, markersize=8, label='ZipSearch', markerfacecolor=new_color)

    ax3.set_xlabel('Operations (Millions)', fontsize=12, color='white')
    ax3.set_ylabel('Processing Time (Minutes)', fontsize=12, color='white')
    ax3.set_title('Large-Scale Processing Time', fontsize=13, fontweight='bold', color='white')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    ax3.set_facecolor('#2a2a2a')

    # Add some key data points with labels
    for i, (count, old_t, new_t) in enumerate(zip(op_counts, old_times_min, new_times_min)):
        if i % 2 == 0:  # Label every other point to avoid clutter
            if old_t > 60:  # Convert to hours if over 60 minutes
                ax3.annotate(f'{old_t/60:.1f}h',
                           (count/1000000, old_t), textcoords="offset points",
                           xytext=(0,10), ha='center', fontsize=8, color=accent_color)
            if new_t < 1:  # Show seconds if under 1 minute
                ax3.annotate(f'{new_t*60:.0f}s',
                           (count/1000000, new_t), textcoords="offset points",
                           xytext=(0,-15), ha='center', fontsize=8, color=accent_color, fontweight='bold')

    # Style all axes
    for ax in [ax1, ax2, ax3]:
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#555555')

    # Add overall summary text
    fig.text(0.02, 0.02,
             f'Summary: ZipSearch delivers {speedups[0]:.0f}x faster zipcode lookups and {speedups[1]:.0f}x faster city/state queries',
             fontsize=12, color=accent_color, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='#2a2a2a', alpha=0.8))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.08)  # Make room for summary text

    # Save chart
    media_dir = Path('')
    media_dir.mkdir(exist_ok=True)
    output_path = media_dir / 'speed.png'

    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1e1e1e')
    logger.info(f"Improved speed comparison chart saved to {output_path}")
    plt.show()

    return output_path

def main():
    """Run speed test comparison."""
    logger.info("Starting USZipcode speed test...")

    # Run tests
    old_results = test_old_version()
    new_results = test_new_version()

    # Create visualization
    chart_path = create_visualization(old_results, new_results)

    # Print summary
    speedup_zipcode = old_results['zipcode_lookup_time'] / new_results['zipcode_lookup_time']
    speedup_citystate = old_results['citystate_lookup_time'] / new_results['citystate_lookup_time']

    logger.info("=" * 50)
    logger.info("SPEED TEST COMPLETE!")
    logger.info(f"Zipcode lookup speedup: {speedup_zipcode:.0f}x faster")
    logger.info(f"City/state lookup speedup: {speedup_citystate:.0f}x faster")
    logger.info(f"Chart saved to: {chart_path}")

if __name__ == "__main__":
    main()