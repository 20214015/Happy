"""
Advanced Startup Optimizer
=========================

Comprehensive startup performance optimization for Happy application.
Implements progressive loading, memory pooling, and lazy initialization.

Author: GitHub Copilot
Date: August 26, 2025
Version: 1.0 - Production Ready
"""

import time
import threading
import functools
import weakref
from typing import Dict, Any, List, Callable, Optional, Union
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QThread, QMutex
from PyQt6.QtWidgets import QApplication


class StartupProfiler:
    """Profiles startup performance and provides insights"""
    
    def __init__(self):
        self.metrics = {}
        self.total_startup_time = 0
        self.critical_path_time = 0
        
    def record_component_time(self, component: str, load_time: float, critical: bool = False):
        """Record component loading time"""
        self.metrics[component] = {
            'time': load_time,
            'critical': critical,
            'timestamp': time.time()
        }
        
        if critical:
            self.critical_path_time += load_time
            
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        total_time = sum(metric['time'] for metric in self.metrics.values())
        critical_time = sum(metric['time'] for metric in self.metrics.values() if metric['critical'])
        
        return {
            'total_components': len(self.metrics),
            'total_time': total_time,
            'critical_path_time': critical_time,
            'average_time': total_time / len(self.metrics) if self.metrics else 0,
            'slowest_component': max(self.metrics.items(), key=lambda x: x[1]['time']) if self.metrics else None,
            'optimization_potential': total_time - critical_time
        }


class MemoryPool:
    """Simple memory pool for frequently allocated objects"""
    
    def __init__(self, initial_size: int = 100):
        self._pools = {}
        self._initial_size = initial_size
        self._mutex = QMutex()
        
    def get_pool(self, obj_type: str, factory: Callable) -> List[Any]:
        """Get or create object pool for specific type"""
        with QMutex():
            if obj_type not in self._pools:
                self._pools[obj_type] = {
                    'factory': factory,
                    'available': [],
                    'in_use': weakref.WeakSet()
                }
                
                # Pre-allocate objects
                for _ in range(min(10, self._initial_size)):
                    try:
                        obj = factory()
                        self._pools[obj_type]['available'].append(obj)
                    except Exception:
                        break
                        
            return self._pools[obj_type]
    
    def acquire(self, obj_type: str, factory: Callable) -> Any:
        """Acquire object from pool"""
        pool = self.get_pool(obj_type, factory)
        
        if pool['available']:
            obj = pool['available'].pop()
        else:
            obj = factory()
            
        pool['in_use'].add(obj)
        return obj
    
    def release(self, obj_type: str, obj: Any):
        """Release object back to pool"""
        if obj_type in self._pools:
            pool = self._pools[obj_type]
            if obj in pool['in_use']:
                pool['in_use'].discard(obj)
                if len(pool['available']) < 50:  # Limit pool size
                    pool['available'].append(obj)


class LazyImportManager:
    """Manages lazy imports to speed up startup"""
    
    def __init__(self):
        self._imports = {}
        self._import_lock = threading.Lock()
        
    def register_lazy_import(self, module_name: str, import_path: str):
        """Register a module for lazy import"""
        self._imports[module_name] = {
            'path': import_path,
            'module': None,
            'imported': False
        }
        
    def get_module(self, module_name: str):
        """Get module, importing if necessary"""
        if module_name not in self._imports:
            raise ImportError(f"Module {module_name} not registered for lazy import")
            
        import_info = self._imports[module_name]
        
        if not import_info['imported']:
            with self._import_lock:
                if not import_info['imported']:  # Double-check locking
                    try:
                        import_info['module'] = __import__(import_info['path'], fromlist=[''])
                        import_info['imported'] = True
                    except ImportError as e:
                        print(f"⚠️ Failed to lazy import {module_name}: {e}")
                        return None
                        
        return import_info['module']


class ComponentLoader(QObject):
    """Handles progressive component loading"""
    
    component_loaded = pyqtSignal(str, float)  # component_name, load_time
    all_components_loaded = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.loading_queue = []
        self.loaded_components = {}
        self.load_timer = QTimer()
        self.load_timer.timeout.connect(self._load_next_component)
        
    def add_component(self, name: str, loader_func: Callable, priority: int = 0, critical: bool = False):
        """Add component to loading queue"""
        self.loading_queue.append({
            'name': name,
            'loader': loader_func,
            'priority': priority,
            'critical': critical,
            'loaded': False
        })
        
        # Sort by priority (higher priority loads first)
        self.loading_queue.sort(key=lambda x: x['priority'], reverse=True)
        
    def start_loading(self, interval_ms: int = 50):
        """Start progressive loading"""
        if self.loading_queue:
            self.load_timer.start(interval_ms)
            
    def _load_next_component(self):
        """Load next component in queue"""
        if not self.loading_queue:
            self.load_timer.stop()
            self.all_components_loaded.emit()
            return
            
        component = None
        for i, comp in enumerate(self.loading_queue):
            if not comp['loaded']:
                component = comp
                self.loading_queue[i]['loaded'] = True
                break
                
        if component:
            start_time = time.time()
            try:
                result = component['loader']()
                load_time = time.time() - start_time
                
                self.loaded_components[component['name']] = {
                    'result': result,
                    'load_time': load_time,
                    'critical': component['critical']
                }
                
                self.component_loaded.emit(component['name'], load_time)
                
            except Exception as e:
                print(f"❌ Failed to load component {component['name']}: {e}")
                
        # Check if all components are loaded
        if all(comp['loaded'] for comp in self.loading_queue):
            self.load_timer.stop()
            self.all_components_loaded.emit()


class StartupOptimizer(QObject):
    """Main startup optimization coordinator"""
    
    optimization_complete = pyqtSignal(dict)  # performance_report
    
    def __init__(self):
        super().__init__()
        self.profiler = StartupProfiler()
        self.memory_pool = MemoryPool()
        self.lazy_imports = LazyImportManager()
        self.component_loader = ComponentLoader()
        
        # Connect signals
        self.component_loader.component_loaded.connect(self._on_component_loaded)
        self.component_loader.all_components_loaded.connect(self._on_all_components_loaded)
        
        # Configuration
        self.config = {
            'max_parallel_loads': 3,
            'component_load_interval': 25,  # ms
            'memory_pool_size': 50,
            'lazy_import_threshold': 0.1  # seconds
        }
        
    def measure_performance(self, component_name: str, critical: bool = False):
        """Decorator to measure component performance"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    load_time = time.time() - start_time
                    self.profiler.record_component_time(component_name, load_time, critical)
                    
                    if load_time > 0.5:  # Log slow components
                        print(f"🐌 Slow component detected: {component_name} ({load_time:.3f}s)")
                    elif load_time < 0.1:
                        print(f"⚡ Fast component: {component_name} ({load_time:.3f}s)")
                    else:
                        print(f"✅ Component loaded: {component_name} ({load_time:.3f}s)")
                        
                    return result
                except Exception as e:
                    load_time = time.time() - start_time
                    print(f"❌ Component failed: {component_name} after {load_time:.3f}s: {e}")
                    raise
            return wrapper
        return decorator
    
    def defer_non_critical_loading(self, components: List[tuple]):
        """Setup deferred loading for non-critical components"""
        for name, loader_func, priority in components:
            self.component_loader.add_component(name, loader_func, priority, critical=False)
            
    def setup_lazy_imports(self):
        """Setup commonly used lazy imports"""
        lazy_imports = [
            ('matplotlib', 'matplotlib.pyplot'),
            ('numpy', 'numpy'),
            ('qtawesome', 'qtawesome'),
            ('json', 'json'),
            ('sqlite3', 'sqlite3')
        ]
        
        for name, path in lazy_imports:
            self.lazy_imports.register_lazy_import(name, path)
    
    def optimize_qt_application(self, app: QApplication):
        """Apply Qt-specific optimizations"""
        if not app:
            return
            
        # Optimize Qt application settings
        app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
        
        # Optimize rendering
        app.setAttribute(Qt.ApplicationAttribute.AA_CompressHighFrequencyEvents, True)
        
        print("✅ Qt application optimizations applied")
    
    def start_progressive_loading(self):
        """Start the progressive loading process"""
        self.setup_lazy_imports()
        self.component_loader.start_loading(self.config['component_load_interval'])
        
    def _on_component_loaded(self, component_name: str, load_time: float):
        """Handle component loaded event"""
        # You can add additional logic here, like updating a progress bar
        pass
    
    def _on_all_components_loaded(self):
        """Handle all components loaded event"""
        report = self.profiler.get_performance_report()
        self.optimization_complete.emit(report)
        
        print("🎉 All components loaded successfully!")
        print(f"📊 Performance Summary:")
        print(f"   - Total components: {report['total_components']}")
        print(f"   - Total time: {report['total_time']:.3f}s")
        print(f"   - Critical path: {report['critical_path_time']:.3f}s")
        print(f"   - Average time: {report['average_time']:.3f}s")
        
        if report['slowest_component']:
            name, info = report['slowest_component']
            print(f"   - Slowest: {name} ({info['time']:.3f}s)")


def create_startup_optimizer() -> StartupOptimizer:
    """Factory function to create startup optimizer"""
    return StartupOptimizer()


# Global instance
_startup_optimizer = None

def get_startup_optimizer() -> StartupOptimizer:
    """Get global startup optimizer instance"""
    global _startup_optimizer
    if _startup_optimizer is None:
        _startup_optimizer = create_startup_optimizer()
    return _startup_optimizer