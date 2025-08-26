"""
UI Performance Optimization System
=================================

Comprehensive UI performance optimizations including widget caching,
event filtering, and progressive rendering for Happy application.

Author: GitHub Copilot
Date: August 26, 2025
Version: 1.0 - Production Ready
"""

import time
import weakref
from typing import Dict, List, Any, Optional, Set, Type
from PyQt6.QtCore import QObject, QTimer, QEvent, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QApplication, QProgressBar, QLabel, 
                           QPushButton, QLineEdit, QTextEdit, QComboBox)
from PyQt6.QtGui import QPainter, QPixmap


class WidgetCache:
    """Cache for frequently used widgets to reduce allocation overhead"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.caches = {}  # widget_type -> list of available widgets
        self.in_use = weakref.WeakSet()
        
    def get_widget(self, widget_type: Type[QWidget], parent: QWidget = None) -> QWidget:
        """Get widget from cache or create new one"""
        type_name = widget_type.__name__
        
        if type_name not in self.caches:
            self.caches[type_name] = []
        
        cache = self.caches[type_name]
        
        # Try to reuse cached widget
        for widget in cache:
            if widget not in self.in_use and widget.parent() is None:
                cache.remove(widget)
                widget.setParent(parent)
                self.in_use.add(widget)
                
                # Reset widget state
                self._reset_widget_state(widget)
                return widget
        
        # Create new widget if cache empty
        widget = widget_type(parent)
        self.in_use.add(widget)
        return widget
    
    def return_widget(self, widget: QWidget):
        """Return widget to cache"""
        if widget in self.in_use:
            self.in_use.discard(widget)
            
            type_name = widget.__class__.__name__
            if type_name not in self.caches:
                self.caches[type_name] = []
            
            cache = self.caches[type_name]
            
            if len(cache) < self.max_size:
                # Clean up widget before caching
                widget.setParent(None)
                widget.hide()
                self._reset_widget_state(widget)
                cache.append(widget)
            else:
                # Cache full, delete widget
                widget.deleteLater()
    
    def _reset_widget_state(self, widget: QWidget):
        """Reset widget to default state"""
        try:
            widget.setEnabled(True)
            widget.setVisible(True)
            widget.setStyleSheet("")
            
            # Reset specific widget types
            if isinstance(widget, QLabel):
                widget.setText("")
                widget.setPixmap(QPixmap())
            elif isinstance(widget, QPushButton):
                widget.setText("")
                widget.setCheckable(False)
                widget.setChecked(False)
            elif isinstance(widget, QLineEdit):
                widget.clear()
                widget.setReadOnly(False)
            elif isinstance(widget, QTextEdit):
                widget.clear()
                widget.setReadOnly(False)
            elif isinstance(widget, QComboBox):
                widget.clear()
            elif isinstance(widget, QProgressBar):
                widget.setValue(0)
                widget.setRange(0, 100)
        except Exception:
            pass  # Ignore reset errors


class EventFilter(QObject):
    """Optimized event filter to reduce unnecessary processing"""
    
    def __init__(self):
        super().__init__()
        self.filtered_events = {
            QEvent.Type.MouseMove,
            QEvent.Type.HoverMove,
            QEvent.Type.Paint,
            QEvent.Type.UpdateRequest
        }
        self.event_counts = {}
        self.last_filter_time = time.time()
        
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filter unnecessary events"""
        event_type = event.type()
        
        # Count events for monitoring
        self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1
        
        current_time = time.time()
        
        # Throttle high-frequency events
        if event_type == QEvent.Type.MouseMove:
            # Limit mouse move events to 60fps
            if current_time - self.last_filter_time < 1.0 / 60.0:
                return True
            self.last_filter_time = current_time
        
        elif event_type == QEvent.Type.HoverMove:
            # Limit hover events to 30fps
            if current_time - self.last_filter_time < 1.0 / 30.0:
                return True
            self.last_filter_time = current_time
        
        return False
    
    def get_event_stats(self) -> Dict[str, int]:
        """Get event filtering statistics"""
        return {str(event_type): count for event_type, count in self.event_counts.items()}


class ProgressiveRenderer:
    """Renders UI components progressively to avoid blocking"""
    
    def __init__(self):
        self.render_queue = []
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._process_render_queue)
        self.render_timer.setInterval(16)  # ~60fps
        self.max_renders_per_frame = 3
        
    def add_render_task(self, widget: QWidget, render_func: callable, priority: int = 0):
        """Add widget to progressive rendering queue"""
        self.render_queue.append({
            'widget': widget,
            'render_func': render_func,
            'priority': priority,
            'added_time': time.time()
        })
        
        # Sort by priority
        self.render_queue.sort(key=lambda x: x['priority'], reverse=True)
        
        if not self.render_timer.isActive():
            self.render_timer.start()
    
    def _process_render_queue(self):
        """Process rendering queue progressively"""
        renders_this_frame = 0
        
        while self.render_queue and renders_this_frame < self.max_renders_per_frame:
            task = self.render_queue.pop(0)
            
            try:
                # Check if widget still exists
                if task['widget'] and not task['widget'].isHidden():
                    task['render_func']()
                    renders_this_frame += 1
            except Exception as e:
                print(f"⚠️ Render task failed: {e}")
        
        if not self.render_queue:
            self.render_timer.stop()


class UIPerformanceMonitor:
    """Monitors UI performance metrics"""
    
    def __init__(self):
        self.frame_times = []
        self.last_frame_time = time.time()
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self._measure_frame_time)
        self.fps_timer.setInterval(16)  # 60fps measurement
        self.monitoring = False
        
    def start_monitoring(self):
        """Start UI performance monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.fps_timer.start()
            self.last_frame_time = time.time()
    
    def stop_monitoring(self):
        """Stop UI performance monitoring"""
        if self.monitoring:
            self.monitoring = False
            self.fps_timer.stop()
    
    def _measure_frame_time(self):
        """Measure frame rendering time"""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        self.frame_times.append(frame_time)
        
        # Keep only recent measurements
        if len(self.frame_times) > 300:  # 5 seconds at 60fps
            self.frame_times = self.frame_times[-300:]
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get UI performance statistics"""
        if not self.frame_times:
            return {}
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        max_frame_time = max(self.frame_times)
        min_frame_time = min(self.frame_times)
        
        return {
            'avg_fps': 1.0 / avg_frame_time if avg_frame_time > 0 else 0,
            'avg_frame_time_ms': avg_frame_time * 1000,
            'max_frame_time_ms': max_frame_time * 1000,
            'min_frame_time_ms': min_frame_time * 1000,
            'frame_samples': len(self.frame_times)
        }


class UIOptimizer(QObject):
    """Main UI optimization coordinator"""
    
    optimization_applied = pyqtSignal(str, dict)  # optimization_type, stats
    
    def __init__(self):
        super().__init__()
        self.widget_cache = WidgetCache()
        self.event_filter = EventFilter()
        self.progressive_renderer = ProgressiveRenderer()
        self.performance_monitor = UIPerformanceMonitor()
        
        self.optimized_widgets = weakref.WeakSet()
        self.optimization_stats = {
            'widgets_cached': 0,
            'events_filtered': 0,
            'progressive_renders': 0,
            'memory_saved_mb': 0
        }
        
    def optimize_widget(self, widget: QWidget, enable_caching: bool = True, 
                       filter_events: bool = True) -> QWidget:
        """Apply comprehensive optimizations to a widget"""
        
        if widget in self.optimized_widgets:
            return widget  # Already optimized
        
        # Apply event filtering
        if filter_events:
            widget.installEventFilter(self.event_filter)
            self.optimization_stats['events_filtered'] += 1
        
        # Enable widget caching awareness
        if enable_caching:
            self._setup_widget_caching(widget)
        
        # Apply specific optimizations based on widget type
        self._apply_widget_specific_optimizations(widget)
        
        # Track optimized widget
        self.optimized_widgets.add(widget)
        
        print(f"✅ Widget optimized: {widget.__class__.__name__}")
        return widget
    
    def _setup_widget_caching(self, widget: QWidget):
        """Setup widget for caching support"""
        # Add custom properties for cache management
        widget.setProperty("cache_enabled", True)
        widget.setProperty("optimization_applied", True)
        
        self.optimization_stats['widgets_cached'] += 1
    
    def _apply_widget_specific_optimizations(self, widget: QWidget):
        """Apply optimizations specific to widget type"""
        
        if isinstance(widget, QTextEdit):
            # Optimize text editor
            widget.setAcceptRichText(False)  # Plain text is faster
            widget.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
            
        elif isinstance(widget, QComboBox):
            # Optimize combo box
            widget.setMaxVisibleItems(20)  # Limit visible items
            
        elif isinstance(widget, QProgressBar):
            # Optimize progress bar
            widget.setTextVisible(False)  # Remove text for better performance
    
    def create_optimized_widget(self, widget_type: Type[QWidget], 
                              parent: QWidget = None, **kwargs) -> QWidget:
        """Create a new optimized widget"""
        widget = self.widget_cache.get_widget(widget_type, parent)
        
        # Apply any additional properties
        for key, value in kwargs.items():
            if hasattr(widget, key):
                setattr(widget, key, value)
        
        # Optimize the widget
        self.optimize_widget(widget)
        
        return widget
    
    def return_widget_to_cache(self, widget: QWidget):
        """Return widget to cache when no longer needed"""
        if widget.property("cache_enabled"):
            self.widget_cache.return_widget(widget)
    
    def add_progressive_render_task(self, widget: QWidget, render_func: callable, 
                                  priority: int = 0):
        """Add widget to progressive rendering"""
        self.progressive_renderer.add_render_task(widget, render_func, priority)
        self.optimization_stats['progressive_renders'] += 1
    
    def start_performance_monitoring(self):
        """Start UI performance monitoring"""
        self.performance_monitor.start_monitoring()
    
    def stop_performance_monitoring(self):
        """Stop UI performance monitoring"""
        self.performance_monitor.stop_monitoring()
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        
        event_stats = self.event_filter.get_event_stats()
        performance_stats = self.performance_monitor.get_performance_stats()
        
        return {
            'optimization_stats': self.optimization_stats,
            'event_stats': event_stats,
            'performance_stats': performance_stats,
            'optimized_widgets': len(self.optimized_widgets),
            'cache_stats': {
                'total_cached': sum(len(cache) for cache in self.widget_cache.caches.values()),
                'in_use': len(self.widget_cache.in_use),
                'cache_types': list(self.widget_cache.caches.keys())
            }
        }
    
    def apply_global_ui_optimizations(self, app: QApplication):
        """Apply global UI optimizations to the application"""
        
        # Set global style optimizations
        app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_DisableWindowContextHelpButton, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_CompressHighFrequencyEvents, True)
        
        # Install global event filter
        app.installEventFilter(self.event_filter)
        
        # Start performance monitoring
        self.start_performance_monitoring()
        
        self.optimization_applied.emit("global_ui", {
            "attributes_set": 3,
            "event_filter_installed": True,
            "monitoring_started": True
        })
        
        print("✅ Global UI optimizations applied")
    
    def cleanup(self):
        """Cleanup UI optimizer resources"""
        self.stop_performance_monitoring()
        
        # Clear caches
        for cache in self.widget_cache.caches.values():
            cache.clear()
        
        print("🧹 UI optimizer cleanup complete")


# Global UI optimizer instance
_ui_optimizer = None

def get_ui_optimizer() -> UIOptimizer:
    """Get global UI optimizer instance"""
    global _ui_optimizer
    if _ui_optimizer is None:
        _ui_optimizer = UIOptimizer()
    return _ui_optimizer


def optimize_widget_performance(widget: QWidget, enable_caching: bool = True, 
                               filter_events: bool = True) -> QWidget:
    """Convenient function to optimize widget performance"""
    optimizer = get_ui_optimizer()
    return optimizer.optimize_widget(widget, enable_caching, filter_events)


def create_optimized_widget(widget_type: Type[QWidget], parent: QWidget = None, 
                          **kwargs) -> QWidget:
    """Create a new optimized widget"""
    optimizer = get_ui_optimizer()
    return optimizer.create_optimized_widget(widget_type, parent, **kwargs)


def apply_global_ui_optimizations(app: QApplication):
    """Apply global UI optimizations"""
    optimizer = get_ui_optimizer()
    optimizer.apply_global_ui_optimizations(app)