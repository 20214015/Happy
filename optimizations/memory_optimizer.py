"""
Advanced Memory Optimization System
===================================

Comprehensive memory management and optimization for Happy application.
Implements memory pooling, garbage collection optimization, and resource tracking.

Author: GitHub Copilot
Date: August 26, 2025
Version: 1.0 - Production Ready
"""

import gc
import sys
import time
import weakref
import threading
from typing import Dict, List, Any, Optional, Type, Callable
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget


class MemoryTracker:
    """Tracks memory usage and provides insights"""
    
    def __init__(self):
        self.peak_memory = 0
        self.baseline_memory = 0
        self.measurements = []
        self.object_counts = {}
        
    def get_memory_usage(self) -> int:
        """Get current memory usage in bytes"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            # Fallback to sys.getsizeof for rough estimate
            return len(gc.get_objects()) * 64  # Rough estimate
    
    def record_measurement(self, label: str):
        """Record a memory measurement"""
        memory_usage = self.get_memory_usage()
        self.measurements.append({
            'label': label,
            'memory': memory_usage,
            'timestamp': time.time()
        })
        
        if memory_usage > self.peak_memory:
            self.peak_memory = memory_usage
            
        self._update_object_counts()
        
    def _update_object_counts(self):
        """Update object type counts"""
        objects = gc.get_objects()
        counts = {}
        
        for obj in objects:
            obj_type = type(obj).__name__
            counts[obj_type] = counts.get(obj_type, 0) + 1
            
        self.object_counts = counts
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Generate memory usage report"""
        current_memory = self.get_memory_usage()
        
        return {
            'current_mb': round(current_memory / 1024 / 1024, 2),
            'peak_mb': round(self.peak_memory / 1024 / 1024, 2),
            'baseline_mb': round(self.baseline_memory / 1024 / 1024, 2),
            'growth_mb': round((current_memory - self.baseline_memory) / 1024 / 1024, 2),
            'measurements': len(self.measurements),
            'top_objects': sorted(self.object_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }


class ObjectPool:
    """Generic object pool for memory optimization"""
    
    def __init__(self, factory: Callable, max_size: int = 50, initial_size: int = 5):
        self.factory = factory
        self.max_size = max_size
        self.available = []
        self.in_use = weakref.WeakSet()
        self.created_count = 0
        self.reused_count = 0
        self._lock = threading.Lock()
        
        # Pre-create initial objects
        for _ in range(initial_size):
            try:
                obj = self.factory()
                self.available.append(obj)
                self.created_count += 1
            except Exception:
                break
    
    def acquire(self):
        """Acquire object from pool"""
        with self._lock:
            if self.available:
                obj = self.available.pop()
                self.reused_count += 1
            else:
                obj = self.factory()
                self.created_count += 1
                
            self.in_use.add(obj)
            return obj
    
    def release(self, obj):
        """Release object back to pool"""
        with self._lock:
            if obj in self.in_use:
                self.in_use.discard(obj)
                
                if len(self.available) < self.max_size:
                    # Reset object state if possible
                    if hasattr(obj, 'reset'):
                        obj.reset()
                    elif hasattr(obj, 'clear'):
                        obj.clear()
                        
                    self.available.append(obj)
    
    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics"""
        return {
            'available': len(self.available),
            'in_use': len(self.in_use),
            'created': self.created_count,
            'reused': self.reused_count,
            'efficiency': round(self.reused_count / max(self.created_count, 1) * 100, 1)
        }


class WidgetPool(ObjectPool):
    """Specialized pool for Qt widgets"""
    
    def __init__(self, widget_class: Type[QWidget], max_size: int = 20):
        super().__init__(lambda: widget_class(), max_size, 3)
        self.widget_class = widget_class
    
    def release(self, widget: QWidget):
        """Release widget back to pool with proper cleanup"""
        if widget and not widget.isVisible():
            # Clean up widget state
            widget.hide()
            widget.setParent(None)
            widget.clearFocus()
            
            # Clear widget-specific state
            if hasattr(widget, 'clear'):
                widget.clear()
            
            super().release(widget)


class CacheManager:
    """Manages application caches with memory limits"""
    
    def __init__(self, max_total_size: int = 50 * 1024 * 1024):  # 50MB default
        self.caches = {}
        self.max_total_size = max_total_size
        self.current_size = 0
        self._lock = threading.Lock()
        
    def create_cache(self, name: str, max_size: int = 100, ttl: int = 3600):
        """Create a new cache instance"""
        with self._lock:
            if name not in self.caches:
                self.caches[name] = {
                    'data': {},
                    'access_times': {},
                    'max_size': max_size,
                    'ttl': ttl,
                    'hits': 0,
                    'misses': 0
                }
        
    def get(self, cache_name: str, key: str, default=None):
        """Get value from cache"""
        if cache_name not in self.caches:
            return default
            
        cache = self.caches[cache_name]
        current_time = time.time()
        
        if key in cache['data']:
            # Check TTL
            if current_time - cache['access_times'].get(key, 0) < cache['ttl']:
                cache['access_times'][key] = current_time
                cache['hits'] += 1
                return cache['data'][key]
            else:
                # Expired
                self._remove_from_cache(cache_name, key)
        
        cache['misses'] += 1
        return default
    
    def set(self, cache_name: str, key: str, value: Any):
        """Set value in cache"""
        if cache_name not in self.caches:
            self.create_cache(cache_name)
            
        cache = self.caches[cache_name]
        
        # Check size limits
        if len(cache['data']) >= cache['max_size']:
            self._evict_lru(cache_name)
        
        cache['data'][key] = value
        cache['access_times'][key] = time.time()
    
    def _remove_from_cache(self, cache_name: str, key: str):
        """Remove item from cache"""
        cache = self.caches[cache_name]
        if key in cache['data']:
            del cache['data'][key]
            del cache['access_times'][key]
    
    def _evict_lru(self, cache_name: str):
        """Evict least recently used item"""
        cache = self.caches[cache_name]
        if not cache['access_times']:
            return
            
        lru_key = min(cache['access_times'], key=cache['access_times'].get)
        self._remove_from_cache(cache_name, lru_key)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        stats = {}
        for name, cache in self.caches.items():
            total_requests = cache['hits'] + cache['misses']
            stats[name] = {
                'size': len(cache['data']),
                'max_size': cache['max_size'],
                'hits': cache['hits'],
                'misses': cache['misses'],
                'hit_rate': round(cache['hits'] / max(total_requests, 1) * 100, 1)
            }
        return stats
    
    def clear_expired(self):
        """Clear expired cache entries"""
        current_time = time.time()
        for cache_name, cache in self.caches.items():
            expired_keys = []
            for key, access_time in cache['access_times'].items():
                if current_time - access_time > cache['ttl']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_from_cache(cache_name, key)


class MemoryOptimizer(QObject):
    """Main memory optimization coordinator"""
    
    memory_warning = pyqtSignal(float)  # memory_usage_mb
    optimization_complete = pyqtSignal(dict)  # stats
    
    def __init__(self):
        super().__init__()
        self.tracker = MemoryTracker()
        self.pools = {}
        self.cache_manager = CacheManager()
        self.optimization_timer = QTimer()
        self.optimization_timer.timeout.connect(self._periodic_optimization)
        
        # Configuration
        self.config = {
            'gc_threshold': 100 * 1024 * 1024,  # 100MB
            'warning_threshold': 200 * 1024 * 1024,  # 200MB
            'optimization_interval': 30000,  # 30 seconds
            'aggressive_cleanup': False
        }
        
        # Record baseline
        self.tracker.baseline_memory = self.tracker.get_memory_usage()
        
    def create_object_pool(self, name: str, factory: Callable, max_size: int = 50) -> ObjectPool:
        """Create a new object pool"""
        pool = ObjectPool(factory, max_size)
        self.pools[name] = pool
        return pool
    
    def create_widget_pool(self, name: str, widget_class: Type[QWidget], max_size: int = 20) -> WidgetPool:
        """Create a new widget pool"""
        pool = WidgetPool(widget_class, max_size)
        self.pools[name] = pool
        return pool
    
    def get_pool(self, name: str) -> Optional[ObjectPool]:
        """Get existing pool by name"""
        return self.pools.get(name)
    
    def start_monitoring(self, interval_ms: int = 30000):
        """Start memory monitoring"""
        self.optimization_timer.start(interval_ms)
        self.tracker.record_measurement("monitoring_started")
        
    def stop_monitoring(self):
        """Stop memory monitoring"""
        self.optimization_timer.stop()
        
    def force_optimization(self):
        """Force immediate memory optimization"""
        self._periodic_optimization()
    
    def _periodic_optimization(self):
        """Perform periodic memory optimization"""
        current_memory = self.tracker.get_memory_usage()
        
        # Check for memory warning
        if current_memory > self.config['warning_threshold']:
            self.memory_warning.emit(current_memory / 1024 / 1024)
        
        # Perform optimization if needed
        if current_memory > self.config['gc_threshold']:
            self._perform_gc_optimization()
        
        # Clear expired cache entries
        self.cache_manager.clear_expired()
        
        # Record measurement
        self.tracker.record_measurement("periodic_optimization")
        
        # Emit optimization stats
        stats = self.get_optimization_stats()
        self.optimization_complete.emit(stats)
    
    def _perform_gc_optimization(self):
        """Perform garbage collection optimization"""
        # Force garbage collection
        collected = gc.collect()
        
        if self.config['aggressive_cleanup']:
            # Additional cleanup for aggressive mode
            gc.collect(0)  # Young generation
            gc.collect(1)  # Middle generation
            gc.collect(2)  # Old generation
        
        print(f"🧹 Garbage collection: {collected} objects collected")
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get comprehensive optimization statistics"""
        memory_report = self.tracker.get_memory_report()
        cache_stats = self.cache_manager.get_cache_stats()
        
        pool_stats = {}
        for name, pool in self.pools.items():
            pool_stats[name] = pool.get_stats()
        
        return {
            'memory': memory_report,
            'caches': cache_stats,
            'pools': pool_stats,
            'gc_stats': {
                'counts': gc.get_count(),
                'threshold': gc.get_threshold()
            }
        }
    
    def cleanup_on_exit(self):
        """Cleanup resources on application exit"""
        self.stop_monitoring()
        
        # Clear all caches
        for cache in self.cache_manager.caches.values():
            cache['data'].clear()
            cache['access_times'].clear()
        
        # Clear pools
        for pool in self.pools.values():
            pool.available.clear()
        
        # Final garbage collection
        self._perform_gc_optimization()
        
        print("🧹 Memory optimization cleanup complete")


# Global memory optimizer instance
_memory_optimizer = None

def get_memory_optimizer() -> MemoryOptimizer:
    """Get global memory optimizer instance"""
    global _memory_optimizer
    if _memory_optimizer is None:
        _memory_optimizer = MemoryOptimizer()
    return _memory_optimizer


def optimize_memory():
    """Convenient function to trigger memory optimization"""
    optimizer = get_memory_optimizer()
    optimizer.force_optimization()


def create_cached_function(cache_name: str, ttl: int = 3600):
    """Decorator to create cached functions"""
    def decorator(func):
        optimizer = get_memory_optimizer()
        optimizer.cache_manager.create_cache(cache_name, ttl=ttl)
        
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check cache first
            result = optimizer.cache_manager.get(cache_name, key)
            if result is not None:
                return result
            
            # Compute and cache result
            result = func(*args, **kwargs)
            optimizer.cache_manager.set(cache_name, key, result)
            return result
        
        return wrapper
    return decorator