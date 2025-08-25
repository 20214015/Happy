#!/usr/bin/env python3
"""
Test script to validate table update performance improvements
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from widgets import InstancesModel, InstancesProxy
from global_ai_tracker import GlobalAITracker

def test_table_performance():
    """Test the optimized table update performance"""
    
    print("🧪 Testing Table Update Performance Improvements")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Create model and table
    model = InstancesModel()
    proxy = InstancesProxy()
    proxy.setSourceModel(model)
    
    table = QTableView()
    table.setModel(proxy)
    
    # Create some test data
    test_instances = []
    for i in range(10):
        test_instances.append({
            'index': i,
            'info': {
                'name': f'MuMu-{i}',
                'is_process_started': i % 2 == 0,
                'adb_port': 16384 + i,
                'disk_size_bytes': 1000000 * (i + 1)
            }
        })
    
    # Set initial data
    model.set_rows(test_instances)
    print(f"✅ Created table with {model.rowCount()} instances")
    
    # Test GlobalAITracker with Model/View pattern
    tracker = GlobalAITracker()
    
    # Test batch updates
    print("\n🚀 Testing Batch Update Performance...")
    start_time = time.time()
    
    # Simulate multiple rapid updates
    for i in range(10):
        status = '🟢 Running' if i % 2 == 0 else '🔴 Stopped'
        data = {'cpu': 25.5 + i, 'memory': 40.0 + i}
        tracker.update_instance_in_table(table, i, status, data)
    
    # Force flush updates
    if hasattr(tracker, '_flush_table_updates'):
        tracker._flush_table_updates()
    
    update_time = time.time() - start_time
    print(f"✅ Batch updates completed in {update_time:.3f} seconds")
    
    # Test individual fast updates
    print("\n⚡ Testing Fast Instance Updates...")
    start_time = time.time()
    
    for i in range(10):
        model.update_instance_fast(i, {
            'ui_state': f'🟡 Status-{i}',
            'info': {'cpu_usage': 30.0 + i, 'memory_usage': 50.0 + i}
        })
    
    # Force apply pending updates
    if hasattr(model, '_apply_pending_updates'):
        model._apply_pending_updates()
    
    fast_update_time = time.time() - start_time
    print(f"✅ Fast updates completed in {fast_update_time:.3f} seconds")
    
    # Test data comparison efficiency
    print("\n🔍 Testing Data Comparison Efficiency...")
    start_time = time.time()
    
    dict1 = {'name': 'test', 'cpu': 25.5, 'pid': 12345, 'irrelevant': 'data'}
    dict2 = {'name': 'test', 'cpu': 25.5, 'pid': 54321, 'irrelevant': 'data'}  # pid different but ignored
    
    for _ in range(1000):
        result = model._are_dicts_equal(dict1, dict2)
    
    comparison_time = time.time() - start_time
    print(f"✅ 1000 comparisons completed in {comparison_time:.3f} seconds")
    print(f"   Result: {result} (should be True - ignoring PID changes)")
    
    print("\n📊 Performance Summary:")
    print(f"   - Batch updates: {update_time:.3f}s for 10 instances")
    print(f"   - Fast updates: {fast_update_time:.3f}s for 10 instances")
    print(f"   - Data comparison: {comparison_time:.3f}s for 1000 ops")
    
    # Performance expectations
    if update_time < 0.1 and fast_update_time < 0.1 and comparison_time < 0.1:
        print("✅ ALL PERFORMANCE TESTS PASSED")
        return True
    else:
        print("⚠️ Some performance tests exceeded expected thresholds")
        return False

if __name__ == "__main__":
    import os
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    success = test_table_performance()
    sys.exit(0 if success else 1)