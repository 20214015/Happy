#!/usr/bin/env python3
"""
🧠 AI-POWERED PREDICTIVE OPTIMIZATION - Phase 4.1 Implementation
Advanced machine learning system for user behavior prediction and resource optimization
"""

import time
import json
import threading
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QThread
import statistics
import random

@dataclass
class UserAction:
    """Represents a user action for pattern analysis"""
    action_type: str  # 'click', 'search', 'refresh', 'filter', etc.
    target: str       # Target element/component
    timestamp: float  # When action occurred
    context: Dict[str, Any]  # Additional context data
    duration: float = 0.0    # How long action took

@dataclass
class PredictionResult:
    """Result of AI prediction"""
    action_type: str
    confidence: float  # 0.0 to 1.0
    predicted_time: float  # When likely to occur
    suggested_preload: List[str]  # Resources to preload

class UsagePatternAnalyzer:
    """🧠 Analyzes user behavior patterns using machine learning techniques"""
    
    def __init__(self):
        self.action_history: deque = deque(maxlen=1000)  # Store last 1000 actions
        self.pattern_cache: Dict[str, Any] = {}
        self.sequence_patterns: Dict[str, List[float]] = defaultdict(list)
        self.timing_patterns: Dict[str, List[float]] = defaultdict(list)
        
        # Pattern recognition settings
        self.min_pattern_length = 2
        self.max_pattern_length = 5
        self.confidence_threshold = 0.6
        
        print("🧠 AI Pattern Analyzer initialized")
    
    def record_action(self, action: UserAction):
        """Record user action for pattern analysis"""
        self.action_history.append(action)
        
        # Update sequence patterns
        self._update_sequence_patterns(action)
        
        # Update timing patterns
        self._update_timing_patterns(action)
        
        # Invalidate cache for real-time learning
        if len(self.action_history) % 10 == 0:  # Every 10 actions
            self._update_pattern_cache()
    
    def _update_sequence_patterns(self, action: UserAction):
        """Update sequence-based patterns"""
        if len(self.action_history) < 2:
            return
        
        # Look for patterns in last few actions
        recent_actions = list(self.action_history)[-self.max_pattern_length:]
        
        for i in range(len(recent_actions) - 1):
            current_action = recent_actions[i].action_type
            next_action = action.action_type
            
            sequence_key = f"{current_action}->{next_action}"
            self.sequence_patterns[sequence_key].append(action.timestamp)
    
    def _update_timing_patterns(self, action: UserAction):
        """Update timing-based patterns"""
        # Record time intervals between similar actions
        similar_actions = [a for a in self.action_history 
                          if a.action_type == action.action_type]
        
        if len(similar_actions) >= 2:
            last_similar = similar_actions[-2]
            interval = action.timestamp - last_similar.timestamp
            self.timing_patterns[action.action_type].append(interval)
    
    def _update_pattern_cache(self):
        """Update pattern recognition cache"""
        try:
            # Analyze most common sequences
            sequence_frequencies = {}
            for sequence, timestamps in self.sequence_patterns.items():
                if len(timestamps) >= 3:  # Minimum occurrences
                    sequence_frequencies[sequence] = len(timestamps)
            
            # Analyze timing patterns
            timing_averages = {}
            for action_type, intervals in self.timing_patterns.items():
                if len(intervals) >= 3:
                    timing_averages[action_type] = {
                        'avg_interval': statistics.mean(intervals),
                        'std_dev': statistics.stdev(intervals) if len(intervals) > 1 else 0,
                        'min_interval': min(intervals),
                        'max_interval': max(intervals)
                    }
            
            self.pattern_cache = {
                'sequence_frequencies': sequence_frequencies,
                'timing_averages': timing_averages,
                'total_actions': len(self.action_history),
                'last_updated': time.time()
            }
            
        except Exception as e:
            print(f"❌ Pattern cache update failed: {e}")
    
    def get_pattern_insights(self) -> Dict[str, Any]:
        """Get current pattern analysis insights"""
        if not self.pattern_cache:
            self._update_pattern_cache()
        
        return {
            'patterns': self.pattern_cache,
            'recent_actions': len(self.action_history),
            'learning_status': 'active' if len(self.action_history) > 20 else 'learning'
        }

class PerformancePredictionEngine:
    """🎯 Predicts user actions and performance bottlenecks"""
    
    def __init__(self, pattern_analyzer: UsagePatternAnalyzer):
        self.pattern_analyzer = pattern_analyzer
        self.prediction_model = {}
        self.confidence_weights = {
            'sequence': 0.4,
            'timing': 0.3,
            'frequency': 0.2,
            'context': 0.1
        }
        
        print("🎯 AI Prediction Engine initialized")
    
    def train_model(self):
        """Train prediction model based on current patterns"""
        patterns = self.pattern_analyzer.get_pattern_insights()
        
        if patterns['recent_actions'] < 10:
            return False  # Not enough data
        
        # Train sequence prediction
        self._train_sequence_model(patterns['patterns'])
        
        # Train timing prediction
        self._train_timing_model(patterns['patterns'])
        
        print(f"🧠 AI Model trained with {patterns['recent_actions']} actions")
        return True
    
    def _train_sequence_model(self, patterns: Dict[str, Any]):
        """Train sequence-based prediction model"""
        sequence_freq = patterns.get('sequence_frequencies', {})
        
        # Create probability matrix for action sequences
        self.prediction_model['sequences'] = {}
        
        for sequence, frequency in sequence_freq.items():
            if '->' in sequence:
                current_action, next_action = sequence.split('->')
                confidence = min(frequency / 10.0, 1.0)  # Normalize confidence
                
                if current_action not in self.prediction_model['sequences']:
                    self.prediction_model['sequences'][current_action] = {}
                
                self.prediction_model['sequences'][current_action][next_action] = confidence
    
    def _train_timing_model(self, patterns: Dict[str, Any]):
        """Train timing-based prediction model"""
        timing_avg = patterns.get('timing_averages', {})
        
        self.prediction_model['timing'] = timing_avg
    
    def predict_next_actions(self, current_action: str, num_predictions: int = 3) -> List[PredictionResult]:
        """Predict user's next likely actions"""
        predictions = []
        
        if 'sequences' not in self.prediction_model:
            return predictions
        
        # Get sequence-based predictions
        if current_action in self.prediction_model['sequences']:
            next_actions = self.prediction_model['sequences'][current_action]
            
            # Sort by confidence and take top predictions
            sorted_actions = sorted(next_actions.items(), 
                                  key=lambda x: x[1], reverse=True)
            
            current_time = time.time()
            
            for next_action, confidence in sorted_actions[:num_predictions]:
                # Predict timing based on historical patterns
                predicted_time = self._predict_action_timing(next_action, current_time)
                
                # Suggest resources to preload
                suggested_preload = self._suggest_preload_resources(next_action)
                
                prediction = PredictionResult(
                    action_type=next_action,
                    confidence=confidence,
                    predicted_time=predicted_time,
                    suggested_preload=suggested_preload
                )
                
                predictions.append(prediction)
        
        return predictions
    
    def _predict_action_timing(self, action_type: str, current_time: float) -> float:
        """Predict when action is likely to occur"""
        if 'timing' not in self.prediction_model:
            return current_time + 5.0  # Default 5 second prediction
        
        timing_data = self.prediction_model['timing'].get(action_type)
        if timing_data:
            avg_interval = timing_data.get('avg_interval', 5.0)
            return current_time + avg_interval
        
        return current_time + 5.0
    
    def _suggest_preload_resources(self, action_type: str) -> List[str]:
        """Suggest resources to preload for predicted action"""
        preload_map = {
            'refresh': ['instance_data', 'status_cache'],
            'search': ['search_index', 'filter_cache'],
            'filter': ['filter_options', 'filtered_data'],
            'select': ['detail_view', 'context_menu'],
            'start': ['start_commands', 'process_monitor'],
            'stop': ['stop_commands', 'cleanup_tasks']
        }
        
        return preload_map.get(action_type, [])

class AdaptiveOptimizer:
    """⚡ Adaptive resource optimizer based on AI predictions"""
    
    def __init__(self):
        self.resource_cache: Dict[str, Any] = {}
        self.preload_queue: List[str] = []
        self.optimization_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'preload_successes': 0,
            'preload_failures': 0
        }
        
        print("⚡ Adaptive Optimizer initialized")
    
    def prepare_resources(self, predicted_action: PredictionResult):
        """Prepare resources based on AI prediction"""
        try:
            for resource in predicted_action.suggested_preload:
                self._preload_resource(resource, predicted_action.confidence)
            
            self.optimization_stats['preload_successes'] += 1
            
        except Exception as e:
            print(f"❌ Resource preparation failed: {e}")
            self.optimization_stats['preload_failures'] += 1
    
    def _preload_resource(self, resource_type: str, confidence: float):
        """Preload specific resource type"""
        if confidence < 0.3:  # Skip low-confidence predictions
            return
        
        current_time = time.time()
        
        # Simulate resource preloading based on type
        if resource_type == 'instance_data':
            self.resource_cache['instance_data'] = {
                'data': 'preloaded_instance_data',
                'timestamp': current_time,
                'confidence': confidence
            }
        elif resource_type == 'search_index':
            self.resource_cache['search_index'] = {
                'index': 'preloaded_search_index',
                'timestamp': current_time,
                'confidence': confidence
            }
        elif resource_type == 'status_cache':
            self.resource_cache['status_cache'] = {
                'statuses': 'preloaded_statuses',
                'timestamp': current_time,
                'confidence': confidence
            }
        
        print(f"📦 Preloaded {resource_type} (confidence: {confidence:.2f})")
    
    def get_cached_resource(self, resource_type: str) -> Optional[Any]:
        """Get cached resource if available"""
        if resource_type in self.resource_cache:
            cached = self.resource_cache[resource_type]
            
            # Check if cache is still fresh (5 minutes max)
            if time.time() - cached['timestamp'] < 300:
                self.optimization_stats['cache_hits'] += 1
                return cached['data']
            else:
                # Remove stale cache
                del self.resource_cache[resource_type]
        
        self.optimization_stats['cache_misses'] += 1
        return None
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization performance statistics"""
        total_requests = (self.optimization_stats['cache_hits'] + 
                         self.optimization_stats['cache_misses'])
        
        hit_rate = (self.optimization_stats['cache_hits'] / max(1, total_requests)) * 100
        
        return {
            'cache_hit_rate': hit_rate,
            'total_preloads': (self.optimization_stats['preload_successes'] + 
                              self.optimization_stats['preload_failures']),
            'preload_success_rate': (self.optimization_stats['preload_successes'] / 
                                   max(1, self.optimization_stats['preload_successes'] + 
                                       self.optimization_stats['preload_failures'])) * 100,
            'cached_resources': len(self.resource_cache),
            **self.optimization_stats
        }

class AIPerformanceOptimizer(QObject):
    """🧠 Enhanced AI-Powered Performance Optimization System with Advanced ML"""
    
    # Signals for UI integration
    prediction_ready = pyqtSignal(list)  # List of PredictionResult
    optimization_applied = pyqtSignal(dict)  # Optimization stats
    learning_progress = pyqtSignal(str)  # Learning status updates
    performance_alert = pyqtSignal(dict)  # Performance alerts
    resource_optimized = pyqtSignal(dict)  # Resource optimization events
    anomaly_detected = pyqtSignal(dict)  # Anomaly detection alerts
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize enhanced AI components
        self.pattern_analyzer = UsagePatternAnalyzer()
        self.prediction_engine = PerformancePredictionEngine(self.pattern_analyzer)
        self.adaptive_optimizer = AdaptiveOptimizer()
        
        # Enhanced ML components
        try:
            from .ai_enhanced_ml import get_enhanced_ml_components
            self.enhanced_analyzer, self.enhanced_predictor = get_enhanced_ml_components()
            self.enhanced_ml_available = True
            print("✅ Enhanced ML components loaded")
        except ImportError:
            self.enhanced_ml_available = False
            self.enhanced_analyzer = None
            self.enhanced_predictor = None
            print("⚠️ Enhanced ML components not available")
        
        # Intelligent monitoring
        try:
            from .ai_intelligent_monitor import get_intelligent_performance_monitor
            self.performance_monitor = get_intelligent_performance_monitor(parent)
            self.intelligent_monitoring_available = True
            print("✅ Intelligent performance monitor loaded")
        except ImportError:
            self.performance_monitor = None
            self.intelligent_monitoring_available = False
            print("⚠️ Intelligent monitoring not available")
        
        # Smart resource management
        try:
            from .ai_smart_resource_manager import get_smart_resource_manager
            self.resource_manager = get_smart_resource_manager(parent)
            self.smart_resources_available = True
            print("✅ Smart resource manager loaded")
        except ImportError:
            self.resource_manager = None
            self.smart_resources_available = False
            print("⚠️ Smart resource management not available")
        
        # Learning state
        self.learning_enabled = True
        self.prediction_enabled = True
        self.enhanced_features_enabled = True
        self.last_action = None
        
        # Initialize advanced AI systems
        self._initialize_advanced_ai_systems()
        
        # Monitoring timer
        self.monitor_timer = None
        self.prediction_interval = 10000  # 10 seconds
        
        # Enhanced configuration
        self.config = {
            'enhanced_ml_enabled': self.enhanced_ml_available,
            'intelligent_monitoring_enabled': self.intelligent_monitoring_available,
            'smart_resources_enabled': self.smart_resources_available,
            'auto_optimization_level': 'adaptive',  # 'basic', 'adaptive', 'aggressive'
            'learning_rate': 0.01,
            'confidence_threshold': 0.6
        }
        
        # Connect enhanced signals if available
        self._connect_enhanced_signals()
        
        print("🧠 Enhanced AI Performance Optimizer initialized")
    
    def _connect_enhanced_signals(self):
        """Connect signals from enhanced AI components"""
        try:
            if self.performance_monitor:
                self.performance_monitor.metrics_updated.connect(
                    lambda metrics: self._on_performance_metrics(metrics)
                )
                self.performance_monitor.alert_raised.connect(
                    lambda alert: self.performance_alert.emit(alert)
                )
                self.performance_monitor.anomaly_detected.connect(
                    lambda anomaly: self.anomaly_detected.emit(anomaly)
                )
            
            if self.resource_manager:
                self.resource_manager.resource_optimized.connect(
                    lambda opt: self.resource_optimized.emit(opt)
                )
                
        except Exception as e:
            print(f"❌ Signal connection error: {e}")
    
    def _on_performance_metrics(self, metrics: Dict[str, Any]):
        """Handle performance metrics from intelligent monitor"""
        try:
            # Convert metrics to enhanced user action for learning
            if self.enhanced_ml_available and self.learning_enabled:
                from .ai_enhanced_ml import EnhancedUserAction
                
                action = EnhancedUserAction(
                    action_type="performance_update",
                    target="system",
                    timestamp=metrics.get('timestamp', time.time()),
                    context={
                        'cpu_usage': metrics.get('cpu_usage', 0),
                        'memory_usage': metrics.get('memory_usage', 0),
                        'response_time': metrics.get('response_time', 0),
                        'throughput': metrics.get('throughput', 0)
                    },
                    duration=0.0,
                    session_id="performance_monitoring",
                    performance_impact=self._calculate_performance_impact(metrics),
                    user_satisfaction=self._estimate_user_satisfaction(metrics)
                )
                
                self.enhanced_analyzer.record_enhanced_action(action)
                
        except Exception as e:
            print(f"❌ Performance metrics handling error: {e}")
    
    def _calculate_performance_impact(self, metrics: Dict[str, Any]) -> float:
        """Calculate performance impact from metrics"""
        cpu = metrics.get('cpu_usage', 0) / 100.0
        memory = metrics.get('memory_usage', 0) / 100.0
        response_time = min(metrics.get('response_time', 0) / 1000.0, 1.0)  # Normalize to seconds
        
        # Higher values indicate negative performance impact
        impact = (cpu * 0.4 + memory * 0.4 + response_time * 0.2)
        return max(0.0, min(1.0, impact))
    
    def _estimate_user_satisfaction(self, metrics: Dict[str, Any]) -> float:
        """Estimate user satisfaction from performance metrics"""
        cpu = metrics.get('cpu_usage', 0)
        memory = metrics.get('memory_usage', 0)
        response_time = metrics.get('response_time', 0)
        
        # Calculate satisfaction score (inverse of performance impact)
        if cpu < 50 and memory < 60 and response_time < 1000:
            return 0.9  # High satisfaction
        elif cpu < 70 and memory < 80 and response_time < 3000:
            return 0.7  # Medium satisfaction
        elif cpu < 90 and memory < 90 and response_time < 5000:
            return 0.4  # Low satisfaction
        else:
            return 0.2  # Very low satisfaction

    def start_ai_optimization(self, prediction_interval: int = 10000):
        """Start enhanced AI-powered optimization system"""
        self.prediction_interval = prediction_interval
        
        # Start intelligent monitoring if available
        if self.intelligent_monitoring_available and self.performance_monitor:
            self.performance_monitor.start_monitoring(interval=2000)  # 2 second monitoring
            print("🔧 Intelligent performance monitoring started")
        
        # Start smart resource management if available
        if self.smart_resources_available and self.resource_manager:
            self.resource_manager.start_resource_management()
            print("🧠 Smart resource management started")
        
        # Start prediction cycle
        if self.parent():
            self.monitor_timer = QTimer(self.parent())
            self.monitor_timer.timeout.connect(self._enhanced_prediction_cycle)
            self.monitor_timer.start(self.prediction_interval)
            
            self.learning_progress.emit("🧠 Enhanced AI Optimization started")
            print("🚀 Enhanced AI Performance Optimization active")
    
    def stop_ai_optimization(self):
        """Stop AI optimization system"""
        if self.monitor_timer:
            self.monitor_timer.stop()
        
        if self.performance_monitor:
            self.performance_monitor.stop_monitoring()
        
        if self.resource_manager:
            self.resource_manager.stop_resource_management()
        
        self.learning_progress.emit("⏹️ AI Optimization stopped")
        print("⏹️ AI optimization stopped")

    def record_user_action(self, action_type: str, target: str, 
                          context: Optional[Dict[str, Any]] = None):
        """Record user action for both basic and enhanced AI learning"""
        if not self.learning_enabled:
            return
        
        current_time = time.time()
        action_context = context or {}
        
        # Record in basic pattern analyzer
        action = UserAction(
            action_type=action_type,
            target=target,
            timestamp=current_time,
            context=action_context,
            duration=0.0
        )
        
        self.pattern_analyzer.record_action(action)
        self.last_action = action
        
        # Record in enhanced analyzer if available
        if self.enhanced_ml_available and self.enhanced_analyzer:
            try:
                from .ai_enhanced_ml import EnhancedUserAction
                
                enhanced_action = EnhancedUserAction(
                    action_type=action_type,
                    target=target,
                    timestamp=current_time,
                    context=action_context,
                    duration=action_context.get('duration', 0.0),
                    session_id=action_context.get('session_id', 'default'),
                    performance_impact=action_context.get('performance_impact', 0.5),
                    user_satisfaction=action_context.get('user_satisfaction', 1.0)
                )
                
                self.enhanced_analyzer.record_enhanced_action(enhanced_action)
                
            except Exception as e:
                print(f"❌ Enhanced action recording error: {e}")

    def track_user_action(self, action_data: Dict[str, Any]):
        """Track user action from dictionary data with enhanced features"""
        if not self.learning_enabled:
            return
            
        action_type = action_data.get('type', 'unknown')
        target = action_data.get('action', 'unknown')
        context = {
            'instance_count': action_data.get('instance_count', 0),
            'timestamp': action_data.get('timestamp', time.time()),
            'duration': action_data.get('duration', 0.0),
            'performance_impact': action_data.get('performance_impact', 0.5),
            'user_satisfaction': action_data.get('user_satisfaction', 1.0)
        }
        
        self.record_user_action(action_type, target, context)
        
        # Enhanced ML training if enough data
        if self.enhanced_ml_available:
            if len(self.enhanced_analyzer.action_history) % 25 == 0:
                self._train_enhanced_models_async()
        else:
            # Basic model training
            if len(self.pattern_analyzer.action_history) % 20 == 0:
                self._train_model_async()

    def _train_enhanced_models_async(self):
        """Train enhanced ML models asynchronously"""
        def train():
            try:
                if self.enhanced_predictor:
                    success = self.enhanced_predictor.train_enhanced_models()
                    if success:
                        self.learning_progress.emit("🧠 Enhanced AI Models updated")
                        print("✅ Enhanced ML models trained successfully")
                        
            except Exception as e:
                print(f"❌ Enhanced model training error: {e}")
        
        # Run training in background thread
        thread = threading.Thread(target=train, daemon=True)
        thread.start()

    def _train_model_async(self):
        """Train basic AI model asynchronously"""
        def train():
            success = self.prediction_engine.train_model()
            if success:
                self.learning_progress.emit("🧠 AI Model updated")
        
        # Run training in background thread
        thread = threading.Thread(target=train, daemon=True)
        thread.start()

    def _enhanced_prediction_cycle(self):
        """Enhanced AI prediction and optimization cycle"""
        if not self.prediction_enabled or not self.last_action:
            return
        
        try:
            predictions = []
            
            # Get enhanced predictions if available
            if self.enhanced_ml_available and self.enhanced_predictor:
                enhanced_predictions = self.enhanced_predictor.predict_next_actions_enhanced(
                    self.last_action.action_type,
                    self.last_action.context,
                    num_predictions=3
                )
                
                # Convert enhanced predictions to basic format for compatibility
                for pred in enhanced_predictions:
                    basic_pred = PredictionResult(
                        action_type=pred.action_type,
                        confidence=pred.confidence,
                        predicted_time=pred.predicted_time,
                        suggested_preload=pred.suggested_optimizations[:2]  # Take first 2
                    )
                    predictions.append(basic_pred)
            
            # Fallback to basic predictions
            if not predictions:
                predictions = self.prediction_engine.predict_next_actions(
                    self.last_action.action_type, num_predictions=3
                )
            
            if predictions:
                # Apply optimizations based on predictions
                for prediction in predictions:
                    # Use higher confidence threshold for enhanced predictions
                    confidence_threshold = self.config.get('confidence_threshold', 0.6)
                    if prediction.confidence > confidence_threshold:
                        self.adaptive_optimizer.prepare_resources(prediction)
                
                # Emit signals for UI updates
                self.prediction_ready.emit(predictions)
                
                # Get optimization stats
                stats = self.adaptive_optimizer.get_optimization_stats()
                self.optimization_applied.emit(stats)
                
                # Enhanced logging
                if self.enhanced_ml_available:
                    print(f"🎯 Enhanced predictions: {len(predictions)} actions predicted")
                
        except Exception as e:
            print(f"❌ Enhanced AI prediction cycle failed: {e}")

    def get_ai_insights(self) -> Dict[str, Any]:
        """Get comprehensive AI system insights including enhanced features"""
        basic_insights = self._get_basic_insights()
        
        # Add enhanced insights if available
        if self.enhanced_ml_available and self.enhanced_analyzer:
            try:
                enhanced_insights = self.enhanced_analyzer.get_advanced_insights()
                basic_insights['enhanced_ml'] = enhanced_insights
                
                if self.enhanced_predictor:
                    model_performance = self.enhanced_predictor.get_model_performance()
                    basic_insights['model_performance'] = model_performance
                    
            except Exception as e:
                print(f"❌ Enhanced insights error: {e}")
        
        # Add performance monitoring insights
        if self.intelligent_monitoring_available and self.performance_monitor:
            try:
                perf_summary = self.performance_monitor.get_performance_summary()
                basic_insights['performance_monitoring'] = perf_summary
            except Exception as e:
                print(f"❌ Performance monitoring insights error: {e}")
        
        # Add resource management insights
        if self.smart_resources_available and self.resource_manager:
            try:
                resource_summary = self.resource_manager.get_resource_summary()
                basic_insights['resource_management'] = resource_summary
            except Exception as e:
                print(f"❌ Resource management insights error: {e}")
        
        # Add neural network insights
        try:
            from .ai_neural_network import get_deep_learning_system
            dl_system = get_deep_learning_system()
            dl_insights = dl_system.get_deep_learning_insights()
            basic_insights['deep_learning'] = dl_insights
        except Exception as e:
            print(f"⚠️ Deep learning insights not available: {e}")
        
        # Add predictive analytics insights
        try:
            from .ai_predictive_analytics import get_predictive_analytics_engine
            pred_engine = get_predictive_analytics_engine()
            pred_insights = pred_engine.get_predictive_insights()
            basic_insights['predictive_analytics'] = pred_insights
        except Exception as e:
            print(f"⚠️ Predictive analytics insights not available: {e}")
        
        # Add intelligent automation insights
        try:
            from .ai_intelligent_automation import get_intelligent_automation_engine
            auto_engine = get_intelligent_automation_engine()
            auto_insights = auto_engine.get_automation_insights()
            basic_insights['intelligent_automation'] = auto_insights
        except Exception as e:
            print(f"⚠️ Intelligent automation insights not available: {e}")
        
        return basic_insights
    
    def _get_basic_insights(self) -> Dict[str, Any]:
        """Get basic AI insights"""
        pattern_insights = self.pattern_analyzer.get_pattern_insights()
        optimization_stats = self.adaptive_optimizer.get_optimization_stats()
        
        return {
            'ai_status': 'active' if self.learning_enabled else 'disabled',
            'learning_progress': pattern_insights['learning_status'],
            'total_actions_learned': pattern_insights['recent_actions'],
            'prediction_accuracy': optimization_stats['cache_hit_rate'],
            'optimization_performance': optimization_stats,
            'system_health': 'excellent' if optimization_stats['cache_hit_rate'] > 70 else 'good',
            'enhanced_features': {
                'enhanced_ml': self.enhanced_ml_available,
                'intelligent_monitoring': self.intelligent_monitoring_available,
                'smart_resources': self.smart_resources_available
            },
            'configuration': dict(self.config)
        }

    def register_component_resources(self, component_id: str, 
                                   resource_requirements: Dict[str, Any],
                                   priority: int = 5) -> bool:
        """Register component with smart resource management"""
        if self.smart_resources_available and self.resource_manager:
            return self.resource_manager.register_component(
                component_id, resource_requirements, priority
            )
        return True  # Succeed gracefully if not available
    
    def unregister_component_resources(self, component_id: str) -> bool:
        """Unregister component from resource management"""
        if self.smart_resources_available and self.resource_manager:
            return self.resource_manager.unregister_component(component_id)
        return True  # Succeed gracefully if not available

    def set_optimization_level(self, level: str):
        """Set AI optimization level: 'basic', 'adaptive', 'aggressive'"""
        self.config['auto_optimization_level'] = level
        
        if level == 'basic':
            self.config['confidence_threshold'] = 0.8
            self.prediction_interval = 15000  # 15 seconds
        elif level == 'adaptive':
            self.config['confidence_threshold'] = 0.6
            self.prediction_interval = 10000  # 10 seconds
        elif level == 'aggressive':
            self.config['confidence_threshold'] = 0.4
            self.prediction_interval = 5000   # 5 seconds
        
        # Update timer if running
        if self.monitor_timer and self.monitor_timer.isActive():
            self.monitor_timer.setInterval(self.prediction_interval)
        
        self.learning_progress.emit(f"🔧 Optimization level set to {level}")

    def toggle_enhanced_features(self, enabled: bool):
        """Enable/disable enhanced AI features"""
        self.enhanced_features_enabled = enabled
        self.config['enhanced_ml_enabled'] = enabled and self.enhanced_ml_available
        self.config['intelligent_monitoring_enabled'] = enabled and self.intelligent_monitoring_available
        self.config['smart_resources_enabled'] = enabled and self.smart_resources_available
        
        status = "enabled" if enabled else "disabled"
        self.learning_progress.emit(f"🧠 Enhanced AI features {status}")
    
    def toggle_learning(self, enabled: bool):
        """Enable/disable AI learning"""
        self.learning_enabled = enabled
        status = "enabled" if enabled else "disabled"
        self.learning_progress.emit(f"🧠 AI Learning {status}")
    
    def toggle_predictions(self, enabled: bool):
        """Enable/disable AI predictions"""
        self.prediction_enabled = enabled
        if not enabled and self.monitor_timer:
            self.monitor_timer.stop()
        elif enabled and self.monitor_timer:
            self.monitor_timer.start(self.prediction_interval)
    
    def _initialize_advanced_ai_systems(self):
        """Initialize advanced AI systems (neural networks, predictive analytics, automation)"""
        try:
            # Initialize neural network system
            from .ai_neural_network import get_deep_learning_system
            self.deep_learning_system = get_deep_learning_system(self.parent())
            self.deep_learning_available = True
            print("✅ Deep learning system initialized")
        except Exception as e:
            self.deep_learning_system = None
            self.deep_learning_available = False
            print(f"⚠️ Deep learning system not available: {e}")
        
        try:
            # Initialize predictive analytics engine
            from .ai_predictive_analytics import get_predictive_analytics_engine
            self.predictive_engine = get_predictive_analytics_engine(self.parent())
            self.predictive_analytics_available = True
            print("✅ Predictive analytics engine initialized")
        except Exception as e:
            self.predictive_engine = None
            self.predictive_analytics_available = False
            print(f"⚠️ Predictive analytics not available: {e}")
        
        try:
            # Initialize intelligent automation engine
            from .ai_intelligent_automation import get_intelligent_automation_engine
            self.automation_engine = get_intelligent_automation_engine(self.parent())
            self.intelligent_automation_available = True
            print("✅ Intelligent automation engine initialized")
        except Exception as e:
            self.automation_engine = None
            self.intelligent_automation_available = False
            print(f"⚠️ Intelligent automation not available: {e}")

# Global AI optimizer instance
global_ai_optimizer = None

def get_ai_optimizer(parent=None) -> AIPerformanceOptimizer:
    """Get or create global AI optimizer"""
    global global_ai_optimizer
    if global_ai_optimizer is None:
        global_ai_optimizer = AIPerformanceOptimizer(parent)
    return global_ai_optimizer

def is_ai_optimization_available() -> bool:
    """Check if AI optimization is available"""
    return True  # Always available for software-based AI

if __name__ == "__main__":
    # Test AI optimization system
    print("🧠 Testing AI Performance Optimization System")
    
    # Create test optimizer
    ai_optimizer = AIPerformanceOptimizer()
    
    # Simulate user actions for learning
    test_actions = [
        ('refresh', 'instance_table', {'filter': 'all'}),
        ('search', 'search_box', {'query': 'test'}),
        ('filter', 'status_filter', {'status': 'running'}),
        ('refresh', 'instance_table', {'filter': 'running'}),
        ('select', 'instance_row', {'index': 1}),
        ('start', 'action_button', {'instance_id': 1}),
        ('refresh', 'instance_table', {'filter': 'all'}),
    ]
    
    # Record actions for learning
    for action_type, target, context in test_actions:
        ai_optimizer.record_user_action(action_type, target, context)
        time.sleep(0.1)  # Small delay between actions
    
    # Get AI insights
    insights = ai_optimizer.get_ai_insights()
    print(f"\n🧠 AI INSIGHTS:")
    for key, value in insights.items():
        print(f"   {key}: {value}")
    
    # Test predictions
    if len(ai_optimizer.pattern_analyzer.action_history) > 5:
        predictions = ai_optimizer.prediction_engine.predict_next_actions('refresh')
        print(f"\n🎯 PREDICTIONS for 'refresh':")
        for pred in predictions:
            print(f"   {pred.action_type} (confidence: {pred.confidence:.2f})")
    
    print("\n✅ AI Performance Optimization system ready!")
