"""
UO Items Database Performance Analysis Script

This script analyzes the current integration between the UO Items Database
and the looting system, identifying performance optimization opportunities.
"""

import time
import sys
import os
from typing import Dict, List, Any, Tuple
import json

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.uo_items import UOItemDatabase, get_item_database
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the DexBot root directory")
    sys.exit(1)


class UOItemsPerformanceAnalyzer:
    """
    Analyzes performance characteristics of the UO Items Database
    in the context of looting system integration.
    """
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.results = {}
        self.db = None
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """
        Run comprehensive performance analysis.
        
        Returns:
            Dictionary containing all analysis results
        """
        print("=== UO Items Database Performance Analysis ===\n")
        
        # Database initialization benchmarks
        self._benchmark_initialization()
        
        # Query performance benchmarks
        self._benchmark_queries()
        
        # Memory usage analysis
        self._analyze_memory_usage()
        
        # Integration pattern analysis
        self._analyze_integration_patterns()
        
        # Cache efficiency analysis
        self._analyze_cache_efficiency()
        
        return self.results
    
    def _benchmark_initialization(self):
        """Benchmark database initialization time."""
        print("📊 Benchmarking Database Initialization...")
        
        # Cold initialization (first time)
        start_time = time.perf_counter()
        db1 = UOItemDatabase()
        cold_init_time = time.perf_counter() - start_time
        
        # Warm initialization (singleton pattern)
        start_time = time.perf_counter()
        db2 = get_item_database()
        warm_init_time = time.perf_counter() - start_time
        
        # Verify singleton behavior
        singleton_check = db2 is get_item_database()
        
        self.results['initialization'] = {
            'cold_init_time_ms': cold_init_time * 1000,
            'warm_init_time_ms': warm_init_time * 1000,
            'singleton_working': singleton_check,
            'speed_improvement': cold_init_time / warm_init_time if warm_init_time > 0 else float('inf')
        }
        
        self.db = db1
        
        print(f"  ✓ Cold initialization: {cold_init_time*1000:.2f}ms")
        print(f"  ✓ Warm initialization: {warm_init_time*1000:.2f}ms")
        print(f"  ✓ Singleton pattern: {'Working' if singleton_check else 'BROKEN'}")
        print()
    
    def _benchmark_queries(self):
        """Benchmark various query operations."""
        print("📊 Benchmarking Query Operations...")
        
        if not self.db:
            return
        
        query_results = {}
        
        # Test common item IDs used in looting
        test_item_ids = [3821, 3862, 3859, 3821, 3862]  # Some duplicates for cache testing
        test_names = ['gold', 'gem', 'reagent', 'potion', 'bandage']
        test_categories = ['currency', 'gems', 'reagents', 'potions']
        test_tiers = ['high', 'medium', 'low']
        
        # Benchmark ID lookups
        start_time = time.perf_counter()
        for item_id in test_item_ids * 100:  # Run 500 lookups
            self.db.get_item_by_id(item_id)
        id_lookup_time = time.perf_counter() - start_time
        query_results['id_lookup_per_ms'] = (id_lookup_time * 1000) / 500
        
        # Benchmark name lookups
        start_time = time.perf_counter()
        for name in test_names * 20:  # Run 100 lookups
            self.db.get_items_by_name(name)
        name_lookup_time = time.perf_counter() - start_time
        query_results['name_lookup_per_ms'] = (name_lookup_time * 1000) / 100
        
        # Benchmark category lookups
        start_time = time.perf_counter()
        for category in test_categories * 10:  # Run 40 lookups
            self.db.get_items_by_category(category)
        category_lookup_time = time.perf_counter() - start_time
        query_results['category_lookup_per_ms'] = (category_lookup_time * 1000) / 40
        
        # Benchmark value tier lookups
        start_time = time.perf_counter()
        for tier in test_tiers * 10:  # Run 30 lookups
            self.db.get_items_by_value_tier(tier)
        tier_lookup_time = time.perf_counter() - start_time
        query_results['tier_lookup_per_ms'] = (tier_lookup_time * 1000) / 30
        
        self.results['queries'] = query_results
        
        print(f"  ✓ ID lookup average: {query_results['id_lookup_per_ms']:.3f}ms")
        print(f"  ✓ Name lookup average: {query_results['name_lookup_per_ms']:.3f}ms")  
        print(f"  ✓ Category lookup average: {query_results['category_lookup_per_ms']:.3f}ms")
        print(f"  ✓ Tier lookup average: {query_results['tier_lookup_per_ms']:.3f}ms")
        print()
    
    def _analyze_memory_usage(self):
        """Analyze memory usage characteristics."""
        print("📊 Analyzing Memory Usage...")
        
        if not self.db:
            return
        
        # Get database statistics
        stats = self.db.get_database_stats()
        
        # Estimate memory usage (rough calculation)
        data_size = len(str(self.db.data))  # String representation size
        
        # Analyze lookup table sizes
        quick_lookup = self.db.data.get('quick_lookup', {})
        by_decimal_id = quick_lookup.get('by_decimal_id', {})
        by_name = quick_lookup.get('by_name', {})
        by_value_tier = quick_lookup.get('by_value_tier', {})
        
        memory_results = {
            'total_categories': stats['total_categories'],
            'total_items': stats['total_items'],
            'estimated_data_size_bytes': data_size,
            'lookup_tables': {
                'by_decimal_id_entries': len(by_decimal_id),
                'by_name_entries': len(by_name),
                'by_value_tier_entries': len(by_value_tier)
            }
        }
        
        self.results['memory'] = memory_results
        
        print(f"  ✓ Total categories: {stats['total_categories']}")
        print(f"  ✓ Total items: {stats['total_items']}")
        print(f"  ✓ Estimated data size: {data_size:,} bytes")
        print(f"  ✓ ID lookup entries: {len(by_decimal_id):,}")
        print(f"  ✓ Name lookup entries: {len(by_name):,}")
        print()
    
    def _analyze_integration_patterns(self):
        """Analyze how the database is used in the looting system."""
        print("📊 Analyzing Integration Patterns...")
        
        # Read the looting system file to analyze usage patterns
        looting_file = os.path.join('src', 'systems', 'looting.py')
        
        integration_analysis = {
            'usage_patterns': [],
            'optimization_opportunities': [],
            'potential_issues': []
        }
        
        try:
            with open(looting_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Analyze usage patterns
            if 'self.item_db.get_item_by_id(' in content:
                integration_analysis['usage_patterns'].append('Individual ID lookups')
                
            if 'self.item_db.get_items_by_category(' in content:
                integration_analysis['usage_patterns'].append('Category-based filtering')
                
            if 'self.item_db.find_items_by_name(' in content:
                integration_analysis['usage_patterns'].append('Name-based searching')
                
            if 'self.item_db.get_items_by_value_tier(' in content:
                integration_analysis['usage_patterns'].append('Value tier filtering')
            
            # Identify potential optimization opportunities
            id_lookup_count = content.count('self.item_db.get_item_by_id(')
            if id_lookup_count > 5:
                integration_analysis['optimization_opportunities'].append(
                    f'Multiple ID lookups detected ({id_lookup_count}) - consider batch operations'
                )
            
            # Check for potential caching opportunities
            if 'get_items_by_category' in content and 'cache' not in content.lower():
                integration_analysis['optimization_opportunities'].append(
                    'Category lookups could benefit from result caching'
                )
                
        except FileNotFoundError:
            integration_analysis['potential_issues'].append('Looting system file not found')
        
        self.results['integration'] = integration_analysis
        
        print(f"  ✓ Usage patterns found: {len(integration_analysis['usage_patterns'])}")
        for pattern in integration_analysis['usage_patterns']:
            print(f"    - {pattern}")
        
        if integration_analysis['optimization_opportunities']:
            print(f"  ⚡ Optimization opportunities: {len(integration_analysis['optimization_opportunities'])}")
            for opp in integration_analysis['optimization_opportunities']:
                print(f"    - {opp}")
        print()
    
    def _analyze_cache_efficiency(self):
        """Analyze potential cache efficiency improvements."""
        print("📊 Analyzing Cache Efficiency Potential...")
        
        if not self.db:
            return
        
        # Simulate looting scenarios to test cache patterns
        cache_analysis = {
            'repeated_lookups': 0,
            'unique_lookups': 0,
            'cache_hit_potential': 0.0
        }
        
        # Simulate common looting patterns
        common_items = [3821, 3862, 3859]  # Gold, Diamond, Ruby
        lookup_sequence = common_items * 10  # Repeated lookups like in real looting
        
        seen_items = set()
        for item_id in lookup_sequence:
            if item_id in seen_items:
                cache_analysis['repeated_lookups'] += 1
            else:
                cache_analysis['unique_lookups'] += 1
                seen_items.add(item_id)
        
        total_lookups = len(lookup_sequence)
        cache_analysis['cache_hit_potential'] = cache_analysis['repeated_lookups'] / total_lookups
        
        self.results['cache_efficiency'] = cache_analysis
        
        print(f"  ✓ Simulated {total_lookups} lookups")
        print(f"  ✓ Repeated lookups: {cache_analysis['repeated_lookups']}")
        print(f"  ✓ Cache hit potential: {cache_analysis['cache_hit_potential']:.1%}")
        print()
    
    def generate_report(self) -> str:
        """Generate a comprehensive performance report."""
        report = []
        report.append("# UO Items Database Performance Analysis Report")
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Initialization Performance
        init_data = self.results.get('initialization', {})
        report.append("## Initialization Performance")
        report.append(f"- Cold initialization: {init_data.get('cold_init_time_ms', 0):.2f}ms")
        report.append(f"- Warm initialization: {init_data.get('warm_init_time_ms', 0):.2f}ms")
        report.append(f"- Singleton pattern: {'✓ Working' if init_data.get('singleton_working') else '❌ Broken'}")
        report.append("")
        
        # Query Performance
        query_data = self.results.get('queries', {})
        report.append("## Query Performance (Average Times)")
        report.append(f"- ID lookup: {query_data.get('id_lookup_per_ms', 0):.3f}ms")
        report.append(f"- Name lookup: {query_data.get('name_lookup_per_ms', 0):.3f}ms")
        report.append(f"- Category lookup: {query_data.get('category_lookup_per_ms', 0):.3f}ms")
        report.append(f"- Value tier lookup: {query_data.get('tier_lookup_per_ms', 0):.3f}ms")
        report.append("")
        
        # Memory Usage
        memory_data = self.results.get('memory', {})
        report.append("## Memory Usage")
        report.append(f"- Total items: {memory_data.get('total_items', 0):,}")
        report.append(f"- Estimated size: {memory_data.get('estimated_data_size_bytes', 0):,} bytes")
        lookup_tables = memory_data.get('lookup_tables', {})
        report.append(f"- Lookup tables: {lookup_tables.get('by_decimal_id_entries', 0):,} ID entries")
        report.append("")
        
        # Integration Analysis
        integration_data = self.results.get('integration', {})
        report.append("## Integration Analysis")
        usage_patterns = integration_data.get('usage_patterns', [])
        if usage_patterns:
            report.append("### Current Usage Patterns")
            for pattern in usage_patterns:
                report.append(f"- {pattern}")
        
        opportunities = integration_data.get('optimization_opportunities', [])
        if opportunities:
            report.append("### Optimization Opportunities")
            for opp in opportunities:
                report.append(f"- {opp}")
        report.append("")
        
        # Cache Efficiency
        cache_data = self.results.get('cache_efficiency', {})
        report.append("## Cache Efficiency Analysis")
        report.append(f"- Cache hit potential: {cache_data.get('cache_hit_potential', 0):.1%}")
        report.append(f"- Repeated vs unique lookups: {cache_data.get('repeated_lookups', 0)} / {cache_data.get('unique_lookups', 0)}")
        report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        report.append("1. **Implement Bulk Lookup API** - Add batch operations for multiple item evaluations")
        report.append("2. **Add Result Caching** - Cache frequently accessed category and tier lookups")
        report.append("3. **Optimize Memory Usage** - Consider lazy loading for large datasets")
        report.append("4. **Add Performance Monitoring** - Track lookup times during extended sessions")
        
        return "\n".join(report)


def main():
    """Run the performance analysis."""
    analyzer = UOItemsPerformanceAnalyzer()
    
    try:
        # Run full analysis
        results = analyzer.run_full_analysis()
        
        # Generate and save report
        report = analyzer.generate_report()
        
        # Save results to files
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        
        # Save raw results as JSON
        results_file = f'tmp/uo_items_performance_results_{timestamp}.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        # Save formatted report
        report_file = f'tmp/uo_items_performance_report_{timestamp}.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("=" * 60)
        print("📊 PERFORMANCE ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Raw results saved to: {results_file}")
        print(f"Report saved to: {report_file}")
        print()
        print("KEY FINDINGS:")
        
        # Display key findings
        init_data = results.get('initialization', {})
        query_data = results.get('queries', {})
        cache_data = results.get('cache_efficiency', {})
        
        print(f"• Database initialization: {init_data.get('cold_init_time_ms', 0):.1f}ms")
        print(f"• Average ID lookup time: {query_data.get('id_lookup_per_ms', 0):.3f}ms")
        print(f"• Cache hit potential: {cache_data.get('cache_hit_potential', 0):.1%}")
        
        integration_data = results.get('integration', {})
        opportunities = integration_data.get('optimization_opportunities', [])
        if opportunities:
            print(f"• Optimization opportunities identified: {len(opportunities)}")
        
        print("\nReview the generated report for detailed analysis and recommendations.")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
