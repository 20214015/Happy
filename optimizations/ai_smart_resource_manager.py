#!/usr/bin/env python3
"""
🧠 Smart Resource Management System
==================================

AI-powered intelligent resource allocation and optimization:
- Dynamic memory management
- Intelligent CPU scheduling
- Smart cache optimization
- Predictive resource scaling
- Adaptive resource allocation
"""

import time
import gc
import threading
import psutil
from typing import Dict, List, Any, Optional, Tuple, Callable
from collections import defaultdict, deque
from dataclasses import dataclass, field
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import statistics
import weakref
import sys


@dataclass
class ResourceProfile:
    """Resource usage profile for components"""
    component_id: str
    cpu_usage: float
    memory_usage: float
    io_usage: float
    priority: int  # 1 (low) to 10 (critical)
    last_used: float
    usage_frequency: float
    performance_impact: float


@dataclass
class ResourceAllocation:
    """Resource allocation decision"""
    component_id: str
    allocated_cpu: float
    allocated_memory: float
    allocated_io: float
    allocation_confidence: float
    expected_performance: float
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CacheEntry:
    """Smart cache entry with AI metadata"""
    key: str
    value: Any
    size: int
    access_count: int
    last_access: float
    creation_time: float
    access_pattern: List[float]
    predicted_next_access: float
    importance_score: float


class IntelligentMemoryManager:
    """🧠 AI-powered memory management with predictive optimization"""
    
    def __init__(self, max_memory_mb: int = 1024):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_usage = 0
        self.allocations = {}
        self.usage_history = deque(maxlen=1000)
        self.optimization_stats = {
            'allocations': 0,
            'deallocations': 0,
            'gc_triggers': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # AI components
        self.usage_predictor = MemoryUsagePredictor()
        self.smart_cache = SmartCache(max_size_mb=256)
        self.adaptive_gc = AdaptiveGarbageCollector()
        
        # Configuration
        self.auto_optimization = True
        self.gc_threshold = 0.85  # Trigger GC at 85% memory usage
        self.emergency_threshold = 0.95
        
        print("🧠 Intelligent Memory Manager initialized")
    
    def allocate_memory(self, component_id: str, size_bytes: int, 
                       priority: int = 5) -> bool:
        """Allocate memory with AI optimization"""
        try:
            # Check if allocation is possible
            if not self._can_allocate(size_bytes):
                # Try to free memory using AI optimization
                if not self._optimize_memory_for_allocation(size_bytes, priority):
                    print(f"❌ Memory allocation failed for {component_id}: {size_bytes} bytes")
                    return False
            
            # Record allocation
            self.allocations[component_id] = {
                'size': size_bytes,
                'priority': priority,
                'timestamp': time.time(),
                'access_count': 0
            }
            
            self.current_usage += size_bytes
            self.optimization_stats['allocations'] += 1
            
            # Update usage history for AI learning
            self.usage_history.append({
                'timestamp': time.time(),
                'total_usage': self.current_usage,
                'allocation_size': size_bytes,
                'component': component_id,
                'priority': priority
            })
            
            # Predictive optimization
            if self.auto_optimization:
                self._predictive_optimization()
            
            print(f"✅ Allocated {size_bytes} bytes for {component_id}")
            return True
            
        except Exception as e:
            print(f"❌ Memory allocation error: {e}")
            return False
    
    def deallocate_memory(self, component_id: str) -> bool:
        """Deallocate memory for component"""
        try:
            if component_id in self.allocations:
                allocation = self.allocations[component_id]
                self.current_usage -= allocation['size']
                del self.allocations[component_id]
                self.optimization_stats['deallocations'] += 1
                
                print(f"✅ Deallocated memory for {component_id}")
                return True
            else:
                print(f"⚠️ No allocation found for {component_id}")
                return False
                
        except Exception as e:
            print(f"❌ Memory deallocation error: {e}")
            return False
    
    def _can_allocate(self, size_bytes: int) -> bool:
        """Check if memory allocation is possible"""
        projected_usage = self.current_usage + size_bytes
        return projected_usage <= self.max_memory_bytes * self.gc_threshold
    
    def _optimize_memory_for_allocation(self, required_bytes: int, 
                                       priority: int) -> bool:
        """Optimize memory to make space for new allocation"""
        try:
            freed_bytes = 0
            
            # 1. Smart cache optimization
            freed_bytes += self.smart_cache.optimize_for_space(required_bytes)
            
            # 2. Release low-priority allocations
            if freed_bytes < required_bytes:
                freed_bytes += self._release_low_priority_allocations(
                    required_bytes - freed_bytes, priority
                )
            
            # 3. Adaptive garbage collection
            if freed_bytes < required_bytes:
                gc_freed = self.adaptive_gc.intelligent_gc()
                freed_bytes += gc_freed
                self.optimization_stats['gc_triggers'] += 1
            
            # 4. Emergency memory management
            if self.current_usage >= self.max_memory_bytes * self.emergency_threshold:
                freed_bytes += self._emergency_memory_cleanup()
            
            return freed_bytes >= required_bytes
            
        except Exception as e:
            print(f"❌ Memory optimization error: {e}")
            return False
    
    def _release_low_priority_allocations(self, required_bytes: int, 
                                         min_priority: int) -> int:
        """Release low-priority allocations to free memory"""
        freed_bytes = 0
        
        # Sort allocations by priority and last access
        allocation_items = list(self.allocations.items())
        allocation_items.sort(key=lambda x: (
            x[1]['priority'], 
            x[1].get('access_count', 0),
            -x[1]['timestamp']
        ))
        
        for component_id, allocation in allocation_items:
            if allocation['priority'] < min_priority:
                if self.deallocate_memory(component_id):
                    freed_bytes += allocation['size']
                    
                    if freed_bytes >= required_bytes:
                        break
        
        return freed_bytes
    
    def _emergency_memory_cleanup(self) -> int:
        """Emergency memory cleanup procedures"""
        print("🚨 Emergency memory cleanup triggered")
        
        freed_bytes = 0
        
        # Force garbage collection
        initial_objects = len(gc.get_objects())
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Estimate freed memory (rough approximation)
        objects_freed = initial_objects - final_objects
        estimated_freed = objects_freed * 100  # Rough estimate: 100 bytes per object
        freed_bytes += max(0, estimated_freed)
        
        # Clear all non-critical cache entries
        freed_bytes += self.smart_cache.emergency_clear()
        
        print(f"🚨 Emergency cleanup freed ~{freed_bytes} bytes")
        return freed_bytes
    
    def _predictive_optimization(self):
        """Predictive memory optimization using AI"""
        try:
            if len(self.usage_history) > 50:
                # Predict future memory usage
                prediction = self.usage_predictor.predict_usage(self.usage_history)
                
                # Proactive optimization if high usage predicted
                if prediction['predicted_peak'] > self.max_memory_bytes * 0.8:
                    print("🔮 Proactive memory optimization triggered")
                    self.smart_cache.proactive_cleanup(prediction)
                    
        except Exception as e:
            print(f"❌ Predictive optimization error: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        usage_percent = (self.current_usage / self.max_memory_bytes) * 100
        
        return {
            'current_usage_bytes': self.current_usage,
            'max_memory_bytes': self.max_memory_bytes,
            'usage_percent': usage_percent,
            'allocations_count': len(self.allocations),
            'optimization_stats': dict(self.optimization_stats),
            'cache_stats': self.smart_cache.get_stats(),
            'gc_stats': self.adaptive_gc.get_stats(),
            'components': list(self.allocations.keys())
        }


class MemoryUsagePredictor:
    """🔮 AI-powered memory usage prediction"""
    
    def __init__(self):
        self.prediction_window = 100
        self.pattern_memory = deque(maxlen=500)
    
    def predict_usage(self, usage_history: deque) -> Dict[str, Any]:
        """Predict future memory usage patterns"""
        if len(usage_history) < 20:
            return {'predicted_peak': 0, 'confidence': 0.0}
        
        try:
            recent_usage = list(usage_history)[-50:]
            
            # Extract usage values
            usage_values = [entry['total_usage'] for entry in recent_usage]
            
            # Simple trend analysis
            if len(usage_values) >= 10:
                recent_trend = statistics.mean(usage_values[-10:])
                older_trend = statistics.mean(usage_values[-20:-10])
                
                trend_direction = recent_trend - older_trend
                
                # Predict peak usage
                current_usage = usage_values[-1]
                predicted_peak = current_usage + (trend_direction * 2)
                
                # Calculate confidence based on trend consistency
                confidence = self._calculate_prediction_confidence(usage_values)
                
                return {
                    'predicted_peak': max(predicted_peak, current_usage),
                    'trend_direction': trend_direction,
                    'confidence': confidence,
                    'current_usage': current_usage
                }
            
        except Exception as e:
            print(f"❌ Memory prediction error: {e}")
        
        return {'predicted_peak': 0, 'confidence': 0.0}
    
    def _calculate_prediction_confidence(self, usage_values: List[float]) -> float:
        """Calculate prediction confidence based on pattern consistency"""
        if len(usage_values) < 10:
            return 0.5
        
        try:
            # Calculate variance in recent trends
            trends = []
            for i in range(5, len(usage_values) - 5):
                recent = statistics.mean(usage_values[i:i+5])
                older = statistics.mean(usage_values[i-5:i])
                trends.append(recent - older)
            
            if not trends:
                return 0.5
            
            # Lower variance = higher confidence
            trend_variance = statistics.variance(trends)
            confidence = 1.0 / (1.0 + trend_variance / 1000000)  # Normalize
            
            return min(max(confidence, 0.1), 0.9)
            
        except:
            return 0.5


class SmartCache:
    """🧠 AI-powered smart caching with predictive eviction"""
    
    def __init__(self, max_size_mb: int = 256):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size = 0
        self.entries: Dict[str, CacheEntry] = {}
        self.access_predictor = CacheAccessPredictor()
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size_optimizations': 0
        }
    
    def put(self, key: str, value: Any, importance: float = 0.5) -> bool:
        """Put item in smart cache with AI optimization"""
        try:
            # Estimate value size
            value_size = self._estimate_size(value)
            
            # Check if we need to make space
            if self.current_size + value_size > self.max_size_bytes:
                if not self._make_space_intelligent(value_size, importance):
                    return False
            
            # Create cache entry with AI metadata
            entry = CacheEntry(
                key=key,
                value=value,
                size=value_size,
                access_count=1,
                last_access=time.time(),
                creation_time=time.time(),
                access_pattern=[time.time()],
                predicted_next_access=time.time() + 3600,  # Default 1 hour
                importance_score=importance
            )
            
            # Remove existing entry if present
            if key in self.entries:
                self.current_size -= self.entries[key].size
            
            # Add new entry
            self.entries[key] = entry
            self.current_size += value_size
            
            return True
            
        except Exception as e:
            print(f"❌ Cache put error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from smart cache with AI learning"""
        if key in self.entries:
            entry = self.entries[key]
            
            # Update access pattern
            current_time = time.time()
            entry.access_count += 1
            entry.last_access = current_time
            entry.access_pattern.append(current_time)
            
            # Keep only recent access pattern
            if len(entry.access_pattern) > 20:
                entry.access_pattern = entry.access_pattern[-10:]
            
            # Update predicted next access
            entry.predicted_next_access = self.access_predictor.predict_next_access(
                entry.access_pattern
            )
            
            self.stats['hits'] += 1
            return entry.value
        else:
            self.stats['misses'] += 1
            return None
    
    def _make_space_intelligent(self, required_space: int, 
                               importance: float) -> bool:
        """Make space using AI-driven eviction strategy"""
        try:
            freed_space = 0
            current_time = time.time()
            
            # Score all entries for eviction priority
            eviction_candidates = []
            
            for key, entry in self.entries.items():
                # Calculate eviction score (higher = more likely to evict)
                eviction_score = self._calculate_eviction_score(entry, current_time)
                
                # Don't evict if importance is much higher than new item
                if entry.importance_score > importance * 1.5:
                    continue
                
                eviction_candidates.append((eviction_score, key, entry))
            
            # Sort by eviction score (highest first)
            eviction_candidates.sort(reverse=True)
            
            # Evict items until we have enough space
            for score, key, entry in eviction_candidates:
                if freed_space >= required_space:
                    break
                
                freed_space += entry.size
                self.current_size -= entry.size
                del self.entries[key]
                self.stats['evictions'] += 1
            
            return freed_space >= required_space
            
        except Exception as e:
            print(f"❌ Cache space optimization error: {e}")
            return False
    
    def _calculate_eviction_score(self, entry: CacheEntry, 
                                 current_time: float) -> float:
        """Calculate eviction priority score using AI"""
        # Time since last access (normalized)
        time_score = (current_time - entry.last_access) / 3600  # Hours
        
        # Access frequency (lower = higher eviction score)
        if len(entry.access_pattern) > 1:
            access_intervals = []
            for i in range(1, len(entry.access_pattern)):
                interval = entry.access_pattern[i] - entry.access_pattern[i-1]
                access_intervals.append(interval)
            
            avg_interval = statistics.mean(access_intervals)
            frequency_score = avg_interval / 3600  # Hours between accesses
        else:
            frequency_score = 24  # 24 hours if only accessed once
        
        # Size impact (larger items have higher eviction priority)
        size_score = entry.size / (1024 * 1024)  # MB
        
        # Predicted next access (sooner = lower eviction score)
        prediction_score = (entry.predicted_next_access - current_time) / 3600
        
        # Importance (lower importance = higher eviction score)
        importance_score = 1.0 - entry.importance_score
        
        # Combine scores with weights
        total_score = (
            time_score * 0.3 +
            frequency_score * 0.25 +
            size_score * 0.2 +
            prediction_score * 0.15 +
            importance_score * 0.1
        )
        
        return total_score
    
    def optimize_for_space(self, required_space: int) -> int:
        """Optimize cache to free specific amount of space"""
        freed_space = 0
        
        try:
            # Find least valuable entries
            current_time = time.time()
            candidates = []
            
            for key, entry in self.entries.items():
                score = self._calculate_eviction_score(entry, current_time)
                candidates.append((score, key, entry))
            
            # Sort by eviction score
            candidates.sort(reverse=True)
            
            # Remove entries until we free enough space
            for score, key, entry in candidates:
                if freed_space >= required_space:
                    break
                
                freed_space += entry.size
                self.current_size -= entry.size
                del self.entries[key]
                self.stats['evictions'] += 1
                self.stats['size_optimizations'] += 1
            
        except Exception as e:
            print(f"❌ Cache optimization error: {e}")
        
        return freed_space
    
    def proactive_cleanup(self, prediction: Dict[str, Any]):
        """Proactive cache cleanup based on AI predictions"""
        try:
            # If high memory usage predicted, preemptively clear low-value items
            confidence = prediction.get('confidence', 0.0)
            
            if confidence > 0.7:
                target_reduction = int(self.max_size_bytes * 0.2)  # 20% reduction
                self.optimize_for_space(target_reduction)
                print(f"🔮 Proactive cache cleanup: freed {target_reduction} bytes")
                
        except Exception as e:
            print(f"❌ Proactive cleanup error: {e}")
    
    def emergency_clear(self) -> int:
        """Emergency cache clearing"""
        freed_bytes = self.current_size
        self.entries.clear()
        self.current_size = 0
        return freed_bytes
    
    def _estimate_size(self, obj: Any) -> int:
        """Estimate object size in bytes"""
        try:
            return sys.getsizeof(obj)
        except:
            return 1024  # Default 1KB estimate
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        hit_rate = 0.0
        total_requests = self.stats['hits'] + self.stats['misses']
        if total_requests > 0:
            hit_rate = self.stats['hits'] / total_requests
        
        return {
            'current_size_bytes': self.current_size,
            'max_size_bytes': self.max_size_bytes,
            'usage_percent': (self.current_size / self.max_size_bytes) * 100,
            'entries_count': len(self.entries),
            'hit_rate': hit_rate,
            **self.stats
        }


class CacheAccessPredictor:
    """🔮 Predicts cache access patterns"""
    
    def predict_next_access(self, access_pattern: List[float]) -> float:
        """Predict when item will be accessed next"""
        if len(access_pattern) < 2:
            return time.time() + 3600  # Default 1 hour
        
        try:
            # Calculate intervals between accesses
            intervals = []
            for i in range(1, len(access_pattern)):
                interval = access_pattern[i] - access_pattern[i-1]
                intervals.append(interval)
            
            # Predict based on average interval
            if intervals:
                avg_interval = statistics.mean(intervals)
                last_access = access_pattern[-1]
                
                # Add some randomness based on variance
                if len(intervals) > 1:
                    variance = statistics.variance(intervals)
                    # Adjust prediction based on pattern consistency
                    consistency_factor = 1.0 / (1.0 + variance / (avg_interval ** 2))
                    predicted_interval = avg_interval * consistency_factor
                else:
                    predicted_interval = avg_interval
                
                return last_access + predicted_interval
            
        except Exception as e:
            print(f"❌ Access prediction error: {e}")
        
        return time.time() + 3600


class AdaptiveGarbageCollector:
    """🗑️ AI-powered adaptive garbage collection"""
    
    def __init__(self):
        self.gc_history = deque(maxlen=100)
        self.adaptive_threshold = 0.85
        self.stats = {
            'total_collections': 0,
            'objects_collected': 0,
            'time_spent': 0.0
        }
    
    def intelligent_gc(self) -> int:
        """Perform intelligent garbage collection"""
        start_time = time.time()
        initial_objects = len(gc.get_objects())
        
        # Adaptive garbage collection strategy
        if self._should_force_collection():
            # Force full collection for maximum cleanup
            gc.collect()
            gc.collect()  # Second pass for circular references
        else:
            # Standard collection
            gc.collect()
        
        final_objects = len(gc.get_objects())
        objects_collected = max(0, initial_objects - final_objects)
        collection_time = time.time() - start_time
        
        # Update statistics
        self.stats['total_collections'] += 1
        self.stats['objects_collected'] += objects_collected
        self.stats['time_spent'] += collection_time
        
        # Record collection result
        self.gc_history.append({
            'timestamp': start_time,
            'objects_collected': objects_collected,
            'collection_time': collection_time,
            'effectiveness': objects_collected / max(initial_objects, 1)
        })
        
        # Estimate freed memory (rough approximation)
        estimated_freed = objects_collected * 100  # Rough estimate
        
        print(f"🗑️ GC: collected {objects_collected} objects in {collection_time:.3f}s")
        return estimated_freed
    
    def _should_force_collection(self) -> bool:
        """Determine if force collection is needed"""
        if len(self.gc_history) < 5:
            return False
        
        # Check recent collection effectiveness
        recent_collections = list(self.gc_history)[-5:]
        avg_effectiveness = statistics.mean([gc['effectiveness'] for gc in recent_collections])
        
        # Force collection if recent collections were highly effective
        return avg_effectiveness > 0.1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get garbage collection statistics"""
        avg_effectiveness = 0.0
        if self.gc_history:
            avg_effectiveness = statistics.mean([gc['effectiveness'] for gc in self.gc_history])
        
        return {
            'total_collections': self.stats['total_collections'],
            'objects_collected': self.stats['objects_collected'],
            'time_spent': self.stats['time_spent'],
            'avg_effectiveness': avg_effectiveness,
            'adaptive_threshold': self.adaptive_threshold
        }


class SmartResourceManager(QObject):
    """🧠 Central AI-powered resource management system"""
    
    # Signals for resource events
    resource_allocated = pyqtSignal(dict)
    resource_optimized = pyqtSignal(dict)
    resource_alert = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Resource managers
        self.memory_manager = IntelligentMemoryManager(max_memory_mb=1024)
        self.cpu_scheduler = IntelligentCPUScheduler()
        self.io_optimizer = IntelligentIOOptimizer()
        
        # Resource monitoring
        self.resource_profiles = {}
        self.allocation_history = deque(maxlen=1000)
        self.optimization_timer = None
        
        # AI components
        self.resource_predictor = ResourcePredictor()
        self.allocation_optimizer = AllocationOptimizer()
        
        # Configuration
        self.auto_optimization_enabled = True
        self.optimization_interval = 30000  # 30 seconds
        
        print("🧠 Smart Resource Manager initialized")
    
    def start_resource_management(self):
        """Start intelligent resource management"""
        if self.parent():
            self.optimization_timer = QTimer(self.parent())
            self.optimization_timer.timeout.connect(self._optimization_cycle)
            self.optimization_timer.start(self.optimization_interval)
        
        print("🚀 Smart resource management started")
    
    def stop_resource_management(self):
        """Stop resource management"""
        if self.optimization_timer:
            self.optimization_timer.stop()
        print("⏹️ Resource management stopped")
    
    def register_component(self, component_id: str, resource_requirements: Dict[str, Any],
                          priority: int = 5) -> bool:
        """Register component with resource requirements"""
        try:
            profile = ResourceProfile(
                component_id=component_id,
                cpu_usage=resource_requirements.get('cpu', 0.0),
                memory_usage=resource_requirements.get('memory', 0),
                io_usage=resource_requirements.get('io', 0.0),
                priority=priority,
                last_used=time.time(),
                usage_frequency=0.0,
                performance_impact=resource_requirements.get('performance_impact', 0.5)
            )
            
            self.resource_profiles[component_id] = profile
            
            # Allocate initial resources
            allocation_success = self._allocate_resources(component_id, resource_requirements)
            
            if allocation_success:
                self.resource_allocated.emit({
                    'component_id': component_id,
                    'resources': resource_requirements,
                    'success': True
                })
            
            return allocation_success
            
        except Exception as e:
            print(f"❌ Component registration error: {e}")
            return False
    
    def unregister_component(self, component_id: str) -> bool:
        """Unregister component and free resources"""
        try:
            if component_id in self.resource_profiles:
                # Free allocated resources
                self.memory_manager.deallocate_memory(component_id)
                self.cpu_scheduler.unregister_component(component_id)
                self.io_optimizer.release_io_resources(component_id)
                
                # Remove profile
                del self.resource_profiles[component_id]
                
                print(f"✅ Component {component_id} unregistered")
                return True
            else:
                print(f"⚠️ Component {component_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Component unregistration error: {e}")
            return False
    
    def _allocate_resources(self, component_id: str, 
                           requirements: Dict[str, Any]) -> bool:
        """Allocate resources for component"""
        try:
            success = True
            
            # Memory allocation
            memory_bytes = requirements.get('memory', 0)
            if memory_bytes > 0:
                priority = self.resource_profiles[component_id].priority
                if not self.memory_manager.allocate_memory(component_id, memory_bytes, priority):
                    success = False
            
            # CPU scheduling
            cpu_weight = requirements.get('cpu', 0.0)
            if cpu_weight > 0:
                self.cpu_scheduler.register_component(component_id, cpu_weight)
            
            # IO resources
            io_requirements = requirements.get('io', 0.0)
            if io_requirements > 0:
                self.io_optimizer.allocate_io_resources(component_id, io_requirements)
            
            return success
            
        except Exception as e:
            print(f"❌ Resource allocation error: {e}")
            return False
    
    def _optimization_cycle(self):
        """AI-powered resource optimization cycle"""
        try:
            # Update resource usage patterns
            self._update_usage_patterns()
            
            # Predict future resource needs
            predictions = self.resource_predictor.predict_resource_needs(
                self.resource_profiles, self.allocation_history
            )
            
            # Optimize allocations based on predictions
            optimizations = self.allocation_optimizer.optimize_allocations(
                self.resource_profiles, predictions
            )
            
            # Apply optimizations
            for optimization in optimizations:
                self._apply_optimization(optimization)
            
            # Emit optimization event
            if optimizations:
                self.resource_optimized.emit({
                    'optimizations_count': len(optimizations),
                    'predictions': predictions,
                    'timestamp': time.time()
                })
            
        except Exception as e:
            print(f"❌ Optimization cycle error: {e}")
    
    def _update_usage_patterns(self):
        """Update usage patterns for AI learning"""
        current_time = time.time()
        
        for component_id, profile in self.resource_profiles.items():
            # Update usage frequency
            time_since_last = current_time - profile.last_used
            if time_since_last < 3600:  # Active within last hour
                profile.usage_frequency = min(profile.usage_frequency + 0.1, 1.0)
            else:
                profile.usage_frequency = max(profile.usage_frequency - 0.05, 0.0)
    
    def _apply_optimization(self, optimization: ResourceAllocation):
        """Apply resource optimization"""
        try:
            component_id = optimization.component_id
            
            # Update resource profile
            if component_id in self.resource_profiles:
                profile = self.resource_profiles[component_id]
                
                # Adjust allocations based on optimization
                if optimization.allocated_memory != profile.memory_usage:
                    # Reallocate memory if needed
                    memory_diff = optimization.allocated_memory - profile.memory_usage
                    if memory_diff > 0:
                        self.memory_manager.allocate_memory(component_id, int(memory_diff))
                    elif memory_diff < 0:
                        # Reduce allocation (simplified)
                        pass
                
                # Update CPU scheduling
                self.cpu_scheduler.update_component_weight(
                    component_id, optimization.allocated_cpu
                )
                
                print(f"🔧 Applied optimization for {component_id}")
            
        except Exception as e:
            print(f"❌ Optimization application error: {e}")
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get comprehensive resource summary"""
        return {
            'memory': self.memory_manager.get_memory_stats(),
            'cpu': self.cpu_scheduler.get_cpu_stats(),
            'io': self.io_optimizer.get_io_stats(),
            'components': len(self.resource_profiles),
            'total_allocations': len(self.allocation_history),
            'optimization_enabled': self.auto_optimization_enabled
        }


class IntelligentCPUScheduler:
    """🔄 AI-powered CPU scheduling and optimization"""
    
    def __init__(self):
        self.components = {}
        self.scheduling_history = deque(maxlen=500)
        self.cpu_stats = {
            'total_weight': 0.0,
            'scheduling_events': 0,
            'optimization_events': 0
        }
    
    def register_component(self, component_id: str, cpu_weight: float):
        """Register component for CPU scheduling"""
        self.components[component_id] = {
            'weight': cpu_weight,
            'last_scheduled': time.time(),
            'total_cpu_time': 0.0,
            'priority_boost': 0.0
        }
        self.cpu_stats['total_weight'] += cpu_weight
    
    def unregister_component(self, component_id: str):
        """Unregister component from CPU scheduling"""
        if component_id in self.components:
            self.cpu_stats['total_weight'] -= self.components[component_id]['weight']
            del self.components[component_id]
    
    def update_component_weight(self, component_id: str, new_weight: float):
        """Update component CPU weight"""
        if component_id in self.components:
            old_weight = self.components[component_id]['weight']
            self.components[component_id]['weight'] = new_weight
            self.cpu_stats['total_weight'] = self.cpu_stats['total_weight'] - old_weight + new_weight
    
    def get_cpu_stats(self) -> Dict[str, Any]:
        """Get CPU scheduling statistics"""
        return {
            'registered_components': len(self.components),
            'total_weight': self.cpu_stats['total_weight'],
            'scheduling_events': self.cpu_stats['scheduling_events'],
            'optimization_events': self.cpu_stats['optimization_events']
        }


class IntelligentIOOptimizer:
    """💾 AI-powered I/O optimization"""
    
    def __init__(self):
        self.io_allocations = {}
        self.io_stats = {
            'total_allocations': 0,
            'optimization_events': 0
        }
    
    def allocate_io_resources(self, component_id: str, io_weight: float):
        """Allocate I/O resources for component"""
        self.io_allocations[component_id] = {
            'weight': io_weight,
            'allocated_time': time.time()
        }
        self.io_stats['total_allocations'] += 1
    
    def release_io_resources(self, component_id: str):
        """Release I/O resources for component"""
        if component_id in self.io_allocations:
            del self.io_allocations[component_id]
    
    def get_io_stats(self) -> Dict[str, Any]:
        """Get I/O optimization statistics"""
        return {
            'active_allocations': len(self.io_allocations),
            'total_allocations': self.io_stats['total_allocations'],
            'optimization_events': self.io_stats['optimization_events']
        }


class ResourcePredictor:
    """🔮 AI-powered resource usage prediction"""
    
    def predict_resource_needs(self, profiles: Dict[str, ResourceProfile], 
                              history: deque) -> Dict[str, Any]:
        """Predict future resource needs"""
        predictions = {
            'memory_trend': 'stable',
            'cpu_trend': 'stable',
            'io_trend': 'stable',
            'peak_usage_time': time.time() + 3600,
            'confidence': 0.5
        }
        
        if len(history) > 20:
            # Simple trend analysis
            recent_allocations = list(history)[-20:]
            memory_usage = sum(profiles[comp_id].memory_usage for comp_id in profiles)
            
            # Predict trends based on historical data
            if memory_usage > 1024 * 1024 * 512:  # 512MB
                predictions['memory_trend'] = 'increasing'
            
            predictions['confidence'] = min(len(history) / 100.0, 0.9)
        
        return predictions


class AllocationOptimizer:
    """⚡ AI-powered resource allocation optimization"""
    
    def optimize_allocations(self, profiles: Dict[str, ResourceProfile], 
                           predictions: Dict[str, Any]) -> List[ResourceAllocation]:
        """Optimize resource allocations based on AI predictions"""
        optimizations = []
        
        try:
            for component_id, profile in profiles.items():
                # Calculate optimal allocation based on usage patterns
                optimal_memory = self._calculate_optimal_memory(profile, predictions)
                optimal_cpu = self._calculate_optimal_cpu(profile, predictions)
                optimal_io = self._calculate_optimal_io(profile, predictions)
                
                # Create optimization if significant improvement possible
                if self._optimization_worthwhile(profile, optimal_memory, optimal_cpu, optimal_io):
                    optimization = ResourceAllocation(
                        component_id=component_id,
                        allocated_cpu=optimal_cpu,
                        allocated_memory=optimal_memory,
                        allocated_io=optimal_io,
                        allocation_confidence=predictions.get('confidence', 0.5),
                        expected_performance=profile.performance_impact * 1.1
                    )
                    optimizations.append(optimization)
            
        except Exception as e:
            print(f"❌ Allocation optimization error: {e}")
        
        return optimizations
    
    def _calculate_optimal_memory(self, profile: ResourceProfile, 
                                 predictions: Dict[str, Any]) -> float:
        """Calculate optimal memory allocation"""
        base_memory = profile.memory_usage
        
        # Adjust based on usage frequency
        frequency_factor = 1.0 + (profile.usage_frequency * 0.2)
        
        # Adjust based on predictions
        if predictions.get('memory_trend') == 'increasing':
            trend_factor = 1.1
        elif predictions.get('memory_trend') == 'decreasing':
            trend_factor = 0.9
        else:
            trend_factor = 1.0
        
        return base_memory * frequency_factor * trend_factor
    
    def _calculate_optimal_cpu(self, profile: ResourceProfile, 
                              predictions: Dict[str, Any]) -> float:
        """Calculate optimal CPU allocation"""
        base_cpu = profile.cpu_usage
        
        # Adjust based on priority
        priority_factor = 0.8 + (profile.priority / 10.0) * 0.4
        
        return base_cpu * priority_factor
    
    def _calculate_optimal_io(self, profile: ResourceProfile, 
                             predictions: Dict[str, Any]) -> float:
        """Calculate optimal I/O allocation"""
        return profile.io_usage  # Simplified for now
    
    def _optimization_worthwhile(self, profile: ResourceProfile, 
                                optimal_memory: float, optimal_cpu: float, 
                                optimal_io: float) -> bool:
        """Check if optimization is worthwhile"""
        memory_diff = abs(optimal_memory - profile.memory_usage) / max(profile.memory_usage, 1)
        cpu_diff = abs(optimal_cpu - profile.cpu_usage) / max(profile.cpu_usage, 0.1)
        
        # Optimization worthwhile if difference > 10%
        return memory_diff > 0.1 or cpu_diff > 0.1


# Global smart resource manager
global_resource_manager = None

def get_smart_resource_manager(parent=None) -> SmartResourceManager:
    """Get or create global smart resource manager"""
    global global_resource_manager
    if global_resource_manager is None:
        global_resource_manager = SmartResourceManager(parent)
    return global_resource_manager


if __name__ == "__main__":
    # Test smart resource management
    print("🧠 Testing Smart Resource Management System")
    
    manager = SmartResourceManager()
    
    # Register test components
    manager.register_component("test_component_1", {
        'memory': 1024 * 1024,  # 1MB
        'cpu': 0.2,
        'io': 0.1,
        'performance_impact': 0.7
    }, priority=8)
    
    manager.register_component("test_component_2", {
        'memory': 2048 * 1024,  # 2MB
        'cpu': 0.3,
        'io': 0.2,
        'performance_impact': 0.5
    }, priority=5)
    
    # Start resource management
    manager.start_resource_management()
    
    # Simulate resource usage
    time.sleep(2)
    
    # Get resource summary
    summary = manager.get_resource_summary()
    print(f"\n📊 Resource Summary:")
    for category, stats in summary.items():
        if isinstance(stats, dict):
            print(f"   {category}:")
            for key, value in stats.items():
                print(f"      {key}: {value}")
        else:
            print(f"   {category}: {stats}")
    
    # Stop resource management
    manager.stop_resource_management()
    
    print("\n✅ Smart Resource Management system ready!")