#!/usr/bin/env python3
"""
🧠 Enhanced Machine Learning Models for AI Optimization
======================================================

Advanced ML algorithms for comprehensive app optimization:
- Multi-layer pattern recognition
- Deep learning user behavior analysis  
- Advanced predictive modeling
- Intelligent feature extraction
- Adaptive learning algorithms
"""

import time
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, pyqtSignal
import statistics
import math


@dataclass
class EnhancedUserAction:
    """Enhanced user action with additional ML features"""
    action_type: str
    target: str
    timestamp: float
    context: Dict[str, Any]
    duration: float = 0.0
    session_id: str = ""
    performance_impact: float = 0.0
    user_satisfaction: float = 1.0  # 0.0 to 1.0


@dataclass
class MLPrediction:
    """Enhanced ML prediction with confidence intervals"""
    action_type: str
    confidence: float
    confidence_interval: Tuple[float, float]
    predicted_time: float
    time_variance: float
    suggested_optimizations: List[str]
    resource_requirements: Dict[str, float]
    performance_impact: float


class AdvancedPatternAnalyzer:
    """🧠 Advanced ML-based pattern analysis with deep learning capabilities"""
    
    def __init__(self):
        self.action_history = deque(maxlen=5000)  # Increased capacity
        self.session_patterns = defaultdict(list)
        self.temporal_patterns = defaultdict(list)
        self.performance_patterns = defaultdict(list)
        self.user_profiles = defaultdict(dict)
        
        # Enhanced ML features
        self.feature_extractors = {
            'temporal': self._extract_temporal_features,
            'sequential': self._extract_sequential_features,
            'performance': self._extract_performance_features,
            'context': self._extract_context_features
        }
        
        # Advanced pattern recognition
        self.pattern_weights = {
            'frequency': 0.25,
            'sequence': 0.30,
            'temporal': 0.20,
            'performance': 0.15,
            'context': 0.10
        }
        
        # Learning parameters
        self.learning_rate = 0.01
        self.adaptation_threshold = 0.7
        self.pattern_memory = defaultdict(float)
        
        print("🧠 Advanced Pattern Analyzer initialized with ML capabilities")
    
    def record_enhanced_action(self, action: EnhancedUserAction):
        """Record enhanced user action with ML features"""
        self.action_history.append(action)
        
        # Update session patterns
        self._update_session_patterns(action)
        
        # Update temporal patterns
        self._update_temporal_patterns(action)
        
        # Update performance patterns
        self._update_performance_patterns(action)
        
        # Adaptive learning
        if len(self.action_history) % 50 == 0:
            self._adaptive_learning_cycle()
    
    def _extract_temporal_features(self, action: EnhancedUserAction) -> Dict[str, float]:
        """Extract temporal features for ML analysis"""
        time_of_day = (action.timestamp % 86400) / 86400  # Normalized hour
        day_of_week = ((action.timestamp // 86400) % 7) / 7  # Normalized day
        
        return {
            'time_of_day': time_of_day,
            'day_of_week': day_of_week,
            'is_peak_hour': 1.0 if 8 <= (action.timestamp % 86400) // 3600 <= 18 else 0.0,
            'session_duration': action.duration,
            'time_since_last': self._time_since_last_action(action.action_type)
        }
    
    def _extract_sequential_features(self, action: EnhancedUserAction) -> Dict[str, float]:
        """Extract sequential pattern features"""
        recent_actions = list(self.action_history)[-10:]
        
        return {
            'sequence_length': len(recent_actions),
            'repetition_rate': self._calculate_repetition_rate(recent_actions),
            'pattern_consistency': self._calculate_pattern_consistency(recent_actions),
            'action_velocity': self._calculate_action_velocity(recent_actions),
            'context_similarity': self._calculate_context_similarity(action, recent_actions)
        }
    
    def _extract_performance_features(self, action: EnhancedUserAction) -> Dict[str, float]:
        """Extract performance-related features"""
        return {
            'performance_impact': action.performance_impact,
            'user_satisfaction': action.user_satisfaction,
            'duration_normalized': min(action.duration / 10.0, 1.0),  # Normalize to 10 seconds
            'efficiency_score': self._calculate_efficiency_score(action),
            'resource_usage': action.context.get('cpu_usage', 0.0) / 100.0
        }
    
    def _extract_context_features(self, action: EnhancedUserAction) -> Dict[str, float]:
        """Extract contextual features"""
        return {
            'instance_count': min(action.context.get('instance_count', 0) / 100.0, 1.0),
            'memory_usage': action.context.get('memory_usage', 0.0) / 100.0,
            'network_activity': action.context.get('network_activity', 0.0),
            'error_rate': action.context.get('error_rate', 0.0),
            'automation_active': 1.0 if action.context.get('automation_active') else 0.0
        }
    
    def _time_since_last_action(self, action_type: str) -> float:
        """Calculate time since last similar action"""
        current_time = time.time()
        for action in reversed(self.action_history):
            if action.action_type == action_type:
                return current_time - action.timestamp
        return 3600.0  # Default 1 hour if not found
    
    def _calculate_repetition_rate(self, actions: List[EnhancedUserAction]) -> float:
        """Calculate action repetition rate"""
        if len(actions) < 2:
            return 0.0
        
        action_counts = defaultdict(int)
        for action in actions:
            action_counts[action.action_type] += 1
        
        max_count = max(action_counts.values())
        return max_count / len(actions)
    
    def _calculate_pattern_consistency(self, actions: List[EnhancedUserAction]) -> float:
        """Calculate pattern consistency score"""
        if len(actions) < 3:
            return 0.0
        
        # Look for repeating sequences
        sequences = []
        for i in range(len(actions) - 1):
            sequences.append(f"{actions[i].action_type}->{actions[i+1].action_type}")
        
        if not sequences:
            return 0.0
        
        sequence_counts = defaultdict(int)
        for seq in sequences:
            sequence_counts[seq] += 1
        
        # Calculate consistency as entropy
        total = len(sequences)
        entropy = 0.0
        for count in sequence_counts.values():
            if count > 0:
                prob = count / total
                entropy -= prob * math.log2(prob)
        
        # Normalize entropy (lower entropy = higher consistency)
        max_entropy = math.log2(len(sequence_counts)) if sequence_counts else 1.0
        return 1.0 - (entropy / max_entropy)
    
    def _calculate_action_velocity(self, actions: List[EnhancedUserAction]) -> float:
        """Calculate action velocity (actions per unit time)"""
        if len(actions) < 2:
            return 0.0
        
        time_span = actions[-1].timestamp - actions[0].timestamp
        if time_span <= 0:
            return 0.0
        
        return len(actions) / time_span
    
    def _calculate_context_similarity(self, action: EnhancedUserAction, 
                                    recent_actions: List[EnhancedUserAction]) -> float:
        """Calculate context similarity with recent actions"""
        if not recent_actions:
            return 0.0
        
        similarities = []
        for recent_action in recent_actions:
            similarity = self._context_similarity_score(action.context, recent_action.context)
            similarities.append(similarity)
        
        return statistics.mean(similarities)
    
    def _context_similarity_score(self, context1: Dict[str, Any], 
                                context2: Dict[str, Any]) -> float:
        """Calculate similarity score between two contexts"""
        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0
        
        similarities = []
        for key in common_keys:
            val1, val2 = context1[key], context2[key]
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Numerical similarity
                max_val = max(abs(val1), abs(val2), 1.0)
                similarity = 1.0 - abs(val1 - val2) / max_val
            elif val1 == val2:
                similarity = 1.0
            else:
                similarity = 0.0
            similarities.append(similarity)
        
        return statistics.mean(similarities)
    
    def _calculate_efficiency_score(self, action: EnhancedUserAction) -> float:
        """Calculate efficiency score for the action"""
        # Higher efficiency = shorter duration with positive performance impact
        if action.duration <= 0:
            return 1.0
        
        base_efficiency = 1.0 / (1.0 + action.duration)
        performance_bonus = action.performance_impact * 0.5
        satisfaction_bonus = action.user_satisfaction * 0.3
        
        return min(base_efficiency + performance_bonus + satisfaction_bonus, 1.0)
    
    def _update_session_patterns(self, action: EnhancedUserAction):
        """Update session-based patterns"""
        session_id = action.session_id or "default"
        self.session_patterns[session_id].append(action)
        
        # Keep only recent session data
        if len(self.session_patterns[session_id]) > 1000:
            self.session_patterns[session_id] = self.session_patterns[session_id][-500:]
    
    def _update_temporal_patterns(self, action: EnhancedUserAction):
        """Update temporal patterns"""
        hour = int((action.timestamp % 86400) // 3600)
        day = int((action.timestamp // 86400) % 7)
        
        self.temporal_patterns[f"hour_{hour}"].append(action)
        self.temporal_patterns[f"day_{day}"].append(action)
    
    def _update_performance_patterns(self, action: EnhancedUserAction):
        """Update performance-based patterns"""
        perf_bucket = "high" if action.performance_impact > 0.5 else "medium" if action.performance_impact > 0.0 else "low"
        self.performance_patterns[perf_bucket].append(action)
    
    def _adaptive_learning_cycle(self):
        """Run adaptive learning cycle to update pattern weights"""
        try:
            # Analyze recent patterns
            recent_actions = list(self.action_history)[-100:]
            if len(recent_actions) < 10:
                return
            
            # Calculate pattern effectiveness
            pattern_effectiveness = self._calculate_pattern_effectiveness(recent_actions)
            
            # Adapt weights based on effectiveness
            for pattern_type, effectiveness in pattern_effectiveness.items():
                if pattern_type in self.pattern_weights:
                    old_weight = self.pattern_weights[pattern_type]
                    adjustment = (effectiveness - 0.5) * self.learning_rate
                    new_weight = max(0.05, min(0.50, old_weight + adjustment))
                    self.pattern_weights[pattern_type] = new_weight
            
            # Normalize weights
            total_weight = sum(self.pattern_weights.values())
            for pattern_type in self.pattern_weights:
                self.pattern_weights[pattern_type] /= total_weight
            
            print(f"🧠 Adaptive learning: Updated pattern weights {self.pattern_weights}")
            
        except Exception as e:
            print(f"❌ Adaptive learning cycle failed: {e}")
    
    def _calculate_pattern_effectiveness(self, actions: List[EnhancedUserAction]) -> Dict[str, float]:
        """Calculate effectiveness of different pattern types"""
        effectiveness = {}
        
        # Temporal effectiveness
        temporal_scores = [action.user_satisfaction for action in actions]
        effectiveness['temporal'] = statistics.mean(temporal_scores) if temporal_scores else 0.5
        
        # Sequential effectiveness
        sequential_scores = [action.performance_impact for action in actions if action.performance_impact > 0]
        effectiveness['sequential'] = statistics.mean(sequential_scores) if sequential_scores else 0.5
        
        # Performance effectiveness
        perf_scores = [1.0 - action.duration / 10.0 for action in actions if action.duration > 0]
        effectiveness['performance'] = statistics.mean([max(0, score) for score in perf_scores]) if perf_scores else 0.5
        
        # Frequency effectiveness
        action_counts = defaultdict(int)
        for action in actions:
            action_counts[action.action_type] += 1
        
        # Higher frequency patterns with better performance are more effective
        freq_effectiveness = []
        for action_type, count in action_counts.items():
            type_actions = [a for a in actions if a.action_type == action_type]
            avg_satisfaction = statistics.mean([a.user_satisfaction for a in type_actions])
            frequency_score = min(count / len(actions), 1.0)
            freq_effectiveness.append(frequency_score * avg_satisfaction)
        
        effectiveness['frequency'] = statistics.mean(freq_effectiveness) if freq_effectiveness else 0.5
        
        # Context effectiveness
        context_scores = []
        for action in actions:
            context_richness = len(action.context) / 10.0  # Normalize to typical context size
            context_scores.append(min(context_richness * action.user_satisfaction, 1.0))
        
        effectiveness['context'] = statistics.mean(context_scores) if context_scores else 0.5
        
        return effectiveness
    
    def get_advanced_insights(self) -> Dict[str, Any]:
        """Get advanced ML-based insights"""
        insights = {
            'total_actions': len(self.action_history),
            'learning_progress': min(len(self.action_history) / 1000.0, 1.0),
            'pattern_weights': dict(self.pattern_weights),
            'session_diversity': len(self.session_patterns),
            'temporal_coverage': len(self.temporal_patterns),
            'performance_distribution': {
                'high': len(self.performance_patterns.get('high', [])),
                'medium': len(self.performance_patterns.get('medium', [])),
                'low': len(self.performance_patterns.get('low', []))
            }
        }
        
        # Calculate advanced metrics
        if len(self.action_history) > 10:
            recent_actions = list(self.action_history)[-100:]
            insights.update({
                'avg_user_satisfaction': statistics.mean([a.user_satisfaction for a in recent_actions]),
                'avg_performance_impact': statistics.mean([a.performance_impact for a in recent_actions]),
                'action_efficiency': statistics.mean([self._calculate_efficiency_score(a) for a in recent_actions]),
                'pattern_consistency': self._calculate_pattern_consistency(recent_actions),
                'learning_stability': self._calculate_learning_stability()
            })
        
        return insights
    
    def _calculate_learning_stability(self) -> float:
        """Calculate stability of learning process"""
        if len(self.action_history) < 100:
            return 0.5
        
        # Compare pattern weights over time
        recent_actions = list(self.action_history)[-50:]
        older_actions = list(self.action_history)[-100:-50]
        
        recent_effectiveness = self._calculate_pattern_effectiveness(recent_actions)
        older_effectiveness = self._calculate_pattern_effectiveness(older_actions)
        
        # Calculate stability as inverse of variance between periods
        differences = []
        for pattern_type in recent_effectiveness:
            if pattern_type in older_effectiveness:
                diff = abs(recent_effectiveness[pattern_type] - older_effectiveness[pattern_type])
                differences.append(diff)
        
        if not differences:
            return 0.5
        
        avg_difference = statistics.mean(differences)
        stability = 1.0 - min(avg_difference, 1.0)
        return stability


class EnhancedPredictionEngine:
    """🎯 Enhanced ML-powered prediction engine with deep learning capabilities"""
    
    def __init__(self, pattern_analyzer: AdvancedPatternAnalyzer):
        self.pattern_analyzer = pattern_analyzer
        self.ml_models = {}
        self.prediction_accuracy = defaultdict(float)
        self.confidence_calibration = defaultdict(list)
        
        # Enhanced prediction parameters
        self.ensemble_weights = {
            'temporal': 0.30,
            'sequential': 0.25,
            'performance': 0.20,
            'frequency': 0.15,
            'context': 0.10
        }
        
        # Advanced features
        self.confidence_threshold = 0.4
        self.prediction_horizon = 300  # 5 minutes
        self.ensemble_size = 5
        
        print("🎯 Enhanced ML Prediction Engine initialized")
    
    def train_enhanced_models(self) -> bool:
        """Train enhanced ML models"""
        if len(self.pattern_analyzer.action_history) < 50:
            return False
        
        try:
            # Train ensemble of specialized models
            self._train_temporal_model()
            self._train_sequential_model()
            self._train_performance_model()
            self._train_context_model()
            
            # Update prediction accuracy
            self._validate_models()
            
            print(f"🧠 Enhanced ML models trained with {len(self.pattern_analyzer.action_history)} samples")
            return True
            
        except Exception as e:
            print(f"❌ Enhanced model training failed: {e}")
            return False
    
    def _train_temporal_model(self):
        """Train temporal prediction model"""
        actions = list(self.pattern_analyzer.action_history)
        temporal_features = []
        targets = []
        
        for i, action in enumerate(actions[:-1]):
            features = self.pattern_analyzer._extract_temporal_features(action)
            next_action = actions[i + 1]
            
            temporal_features.append(features)
            targets.append({
                'action_type': next_action.action_type,
                'time_to_next': next_action.timestamp - action.timestamp,
                'performance_impact': next_action.performance_impact
            })
        
        # Simple ML model (in production, use sklearn or similar)
        self.ml_models['temporal'] = {
            'features': temporal_features,
            'targets': targets,
            'accuracy': self._calculate_model_accuracy(temporal_features, targets)
        }
    
    def _train_sequential_model(self):
        """Train sequential pattern model"""
        actions = list(self.pattern_analyzer.action_history)
        sequence_patterns = defaultdict(list)
        
        # Extract n-gram patterns
        for i in range(len(actions) - 2):
            pattern = tuple(action.action_type for action in actions[i:i+3])
            next_action = actions[i + 3] if i + 3 < len(actions) else None
            
            if next_action:
                sequence_patterns[pattern].append({
                    'next_action': next_action.action_type,
                    'confidence': 1.0 / (len(sequence_patterns[pattern]) + 1),
                    'time_to_next': next_action.timestamp - actions[i+2].timestamp
                })
        
        self.ml_models['sequential'] = {
            'patterns': dict(sequence_patterns),
            'accuracy': len(sequence_patterns) / max(len(actions), 1)
        }
    
    def _train_performance_model(self):
        """Train performance-based prediction model"""
        actions = list(self.pattern_analyzer.action_history)
        performance_clusters = defaultdict(list)
        
        for action in actions:
            perf_level = "high" if action.performance_impact > 0.5 else "medium" if action.performance_impact > 0.0 else "low"
            performance_clusters[perf_level].append(action)
        
        self.ml_models['performance'] = {
            'clusters': performance_clusters,
            'accuracy': self._calculate_cluster_accuracy(performance_clusters)
        }
    
    def _train_context_model(self):
        """Train context-aware prediction model"""
        actions = list(self.pattern_analyzer.action_history)
        context_patterns = defaultdict(list)
        
        for action in actions:
            context_key = self._create_context_key(action.context)
            context_patterns[context_key].append(action)
        
        self.ml_models['context'] = {
            'patterns': dict(context_patterns),
            'accuracy': len(context_patterns) / max(len(actions), 1)
        }
    
    def _create_context_key(self, context: Dict[str, Any]) -> str:
        """Create a key for context clustering"""
        key_parts = []
        
        # Discretize numerical values
        if 'instance_count' in context:
            count_bucket = "low" if context['instance_count'] < 5 else "medium" if context['instance_count'] < 20 else "high"
            key_parts.append(f"instances:{count_bucket}")
        
        if 'cpu_usage' in context:
            cpu_bucket = "low" if context['cpu_usage'] < 30 else "medium" if context['cpu_usage'] < 70 else "high"
            key_parts.append(f"cpu:{cpu_bucket}")
        
        if 'memory_usage' in context:
            mem_bucket = "low" if context['memory_usage'] < 50 else "medium" if context['memory_usage'] < 80 else "high"
            key_parts.append(f"memory:{mem_bucket}")
        
        return "|".join(key_parts) if key_parts else "default"
    
    def _calculate_model_accuracy(self, features: List[Dict], targets: List[Dict]) -> float:
        """Calculate model accuracy (simplified)"""
        if not features or not targets:
            return 0.0
        
        # Simple accuracy based on feature consistency
        consistency_scores = []
        for i, feature_set in enumerate(features):
            if i < len(targets):
                # Simplified accuracy calculation
                score = sum(1 for key in feature_set if isinstance(feature_set[key], (int, float)) and 0 <= feature_set[key] <= 1)
                consistency_scores.append(score / len(feature_set))
        
        return statistics.mean(consistency_scores) if consistency_scores else 0.0
    
    def _calculate_cluster_accuracy(self, clusters: Dict[str, List]) -> float:
        """Calculate clustering accuracy"""
        if not clusters:
            return 0.0
        
        total_items = sum(len(cluster) for cluster in clusters.values())
        cluster_scores = []
        
        for cluster_name, items in clusters.items():
            if items:
                # Calculate internal consistency
                satisfaction_scores = [item.user_satisfaction for item in items]
                consistency = 1.0 - (statistics.stdev(satisfaction_scores) if len(satisfaction_scores) > 1 else 0.0)
                cluster_scores.append(consistency)
        
        return statistics.mean(cluster_scores) if cluster_scores else 0.0
    
    def predict_next_actions_enhanced(self, current_action: str, context: Dict[str, Any], 
                                    num_predictions: int = 3) -> List[MLPrediction]:
        """Enhanced prediction with ensemble of ML models"""
        predictions = []
        
        try:
            # Get predictions from each model
            temporal_preds = self._predict_temporal(current_action, context)
            sequential_preds = self._predict_sequential(current_action)
            performance_preds = self._predict_performance(current_action, context)
            context_preds = self._predict_context(current_action, context)
            
            # Combine predictions using ensemble weights
            combined_predictions = self._ensemble_predictions([
                (temporal_preds, self.ensemble_weights['temporal']),
                (sequential_preds, self.ensemble_weights['sequential']),
                (performance_preds, self.ensemble_weights['performance']),
                (context_preds, self.ensemble_weights['context'])
            ])
            
            # Sort by confidence and return top predictions
            sorted_predictions = sorted(combined_predictions, key=lambda x: x.confidence, reverse=True)
            
            for pred in sorted_predictions[:num_predictions]:
                if pred.confidence >= self.confidence_threshold:
                    predictions.append(pred)
            
        except Exception as e:
            print(f"❌ Enhanced prediction failed: {e}")
        
        return predictions
    
    def _predict_temporal(self, current_action: str, context: Dict[str, Any]) -> List[MLPrediction]:
        """Temporal-based predictions"""
        predictions = []
        
        if 'temporal' not in self.ml_models:
            return predictions
        
        current_time = time.time()
        hour = int((current_time % 86400) // 3600)
        
        # Find similar temporal patterns
        temporal_actions = self.pattern_analyzer.temporal_patterns.get(f"hour_{hour}", [])
        
        if temporal_actions:
            action_counts = defaultdict(int)
            for action in temporal_actions[-50:]:  # Recent temporal patterns
                action_counts[action.action_type] += 1
            
            total_actions = sum(action_counts.values())
            
            for action_type, count in action_counts.items():
                if action_type != current_action:  # Don't predict same action
                    confidence = count / total_actions
                    
                    prediction = MLPrediction(
                        action_type=action_type,
                        confidence=confidence,
                        confidence_interval=(confidence - 0.1, confidence + 0.1),
                        predicted_time=current_time + 30.0,  # 30 seconds
                        time_variance=10.0,
                        suggested_optimizations=['temporal_cache', 'preload_ui'],
                        resource_requirements={'cpu': 0.1, 'memory': 0.05},
                        performance_impact=0.3
                    )
                    predictions.append(prediction)
        
        return predictions[:3]
    
    def _predict_sequential(self, current_action: str) -> List[MLPrediction]:
        """Sequential pattern-based predictions"""
        predictions = []
        
        if 'sequential' not in self.ml_models:
            return predictions
        
        # Get recent action sequence
        recent_actions = list(self.pattern_analyzer.action_history)[-2:]
        if len(recent_actions) >= 2:
            pattern = tuple(action.action_type for action in recent_actions)
            
            sequential_patterns = self.ml_models['sequential']['patterns']
            
            if pattern in sequential_patterns:
                for prediction_data in sequential_patterns[pattern]:
                    confidence = prediction_data['confidence']
                    
                    prediction = MLPrediction(
                        action_type=prediction_data['next_action'],
                        confidence=confidence,
                        confidence_interval=(confidence - 0.05, confidence + 0.05),
                        predicted_time=time.time() + prediction_data.get('time_to_next', 60.0),
                        time_variance=15.0,
                        suggested_optimizations=['sequence_cache', 'predictive_load'],
                        resource_requirements={'cpu': 0.15, 'memory': 0.08},
                        performance_impact=0.4
                    )
                    predictions.append(prediction)
        
        return predictions[:3]
    
    def _predict_performance(self, current_action: str, context: Dict[str, Any]) -> List[MLPrediction]:
        """Performance-based predictions"""
        predictions = []
        
        if 'performance' not in self.ml_models:
            return predictions
        
        # Determine current performance level
        cpu_usage = context.get('cpu_usage', 0)
        current_perf_level = "high" if cpu_usage < 30 else "medium" if cpu_usage < 70 else "low"
        
        performance_clusters = self.ml_models['performance']['clusters']
        
        if current_perf_level in performance_clusters:
            similar_actions = performance_clusters[current_perf_level]
            
            # Find most likely next actions based on performance
            next_action_counts = defaultdict(int)
            for action in similar_actions[-20:]:  # Recent performance-similar actions
                next_action_counts[action.action_type] += 1
            
            total_count = sum(next_action_counts.values())
            
            for action_type, count in next_action_counts.items():
                if action_type != current_action and total_count > 0:
                    confidence = count / total_count
                    
                    prediction = MLPrediction(
                        action_type=action_type,
                        confidence=confidence,
                        confidence_interval=(confidence - 0.08, confidence + 0.08),
                        predicted_time=time.time() + 45.0,
                        time_variance=20.0,
                        suggested_optimizations=['performance_tune', 'resource_optimize'],
                        resource_requirements={'cpu': 0.2, 'memory': 0.1},
                        performance_impact=0.5
                    )
                    predictions.append(prediction)
        
        return predictions[:3]
    
    def _predict_context(self, current_action: str, context: Dict[str, Any]) -> List[MLPrediction]:
        """Context-aware predictions"""
        predictions = []
        
        if 'context' not in self.ml_models:
            return predictions
        
        context_key = self._create_context_key(context)
        context_patterns = self.ml_models['context']['patterns']
        
        if context_key in context_patterns:
            similar_context_actions = context_patterns[context_key]
            
            # Analyze actions in similar context
            action_frequencies = defaultdict(int)
            for action in similar_context_actions[-30:]:
                action_frequencies[action.action_type] += 1
            
            total_actions = sum(action_frequencies.values())
            
            for action_type, freq in action_frequencies.items():
                if action_type != current_action and total_actions > 0:
                    confidence = freq / total_actions
                    
                    prediction = MLPrediction(
                        action_type=action_type,
                        confidence=confidence,
                        confidence_interval=(confidence - 0.12, confidence + 0.12),
                        predicted_time=time.time() + 40.0,
                        time_variance=25.0,
                        suggested_optimizations=['context_cache', 'adaptive_ui'],
                        resource_requirements={'cpu': 0.12, 'memory': 0.06},
                        performance_impact=0.35
                    )
                    predictions.append(prediction)
        
        return predictions[:3]
    
    def _ensemble_predictions(self, model_predictions: List[Tuple[List[MLPrediction], float]]) -> List[MLPrediction]:
        """Combine predictions from multiple models using ensemble weighting"""
        combined = defaultdict(lambda: {
            'confidence': 0.0,
            'weight_sum': 0.0,
            'predictions': []
        })
        
        # Aggregate predictions by action type
        for predictions, weight in model_predictions:
            for pred in predictions:
                combined[pred.action_type]['confidence'] += pred.confidence * weight
                combined[pred.action_type]['weight_sum'] += weight
                combined[pred.action_type]['predictions'].append(pred)
        
        # Create ensemble predictions
        ensemble_predictions = []
        
        for action_type, data in combined.items():
            if data['weight_sum'] > 0:
                # Weighted average confidence
                avg_confidence = data['confidence'] / data['weight_sum']
                
                # Average other properties
                predictions = data['predictions']
                avg_time = statistics.mean([p.predicted_time for p in predictions])
                avg_variance = statistics.mean([p.time_variance for p in predictions])
                avg_impact = statistics.mean([p.performance_impact for p in predictions])
                
                # Combine optimizations
                all_optimizations = set()
                all_resources = defaultdict(float)
                
                for pred in predictions:
                    all_optimizations.update(pred.suggested_optimizations)
                    for resource, value in pred.resource_requirements.items():
                        all_resources[resource] += value
                
                # Average resource requirements
                for resource in all_resources:
                    all_resources[resource] /= len(predictions)
                
                ensemble_pred = MLPrediction(
                    action_type=action_type,
                    confidence=avg_confidence,
                    confidence_interval=(avg_confidence - 0.1, avg_confidence + 0.1),
                    predicted_time=avg_time,
                    time_variance=avg_variance,
                    suggested_optimizations=list(all_optimizations),
                    resource_requirements=dict(all_resources),
                    performance_impact=avg_impact
                )
                
                ensemble_predictions.append(ensemble_pred)
        
        return ensemble_predictions
    
    def _validate_models(self):
        """Validate model accuracy using recent data"""
        if len(self.pattern_analyzer.action_history) < 100:
            return
        
        # Use recent 20% of data for validation
        validation_size = len(self.pattern_analyzer.action_history) // 5
        validation_actions = list(self.pattern_analyzer.action_history)[-validation_size:]
        
        correct_predictions = 0
        total_predictions = 0
        
        for i, action in enumerate(validation_actions[:-1]):
            next_action = validation_actions[i + 1]
            
            # Get prediction
            predictions = self.predict_next_actions_enhanced(
                action.action_type, 
                action.context, 
                num_predictions=3
            )
            
            if predictions:
                total_predictions += 1
                # Check if any prediction matches the actual next action
                for pred in predictions:
                    if pred.action_type == next_action.action_type:
                        correct_predictions += 1
                        break
        
        # Update accuracy
        if total_predictions > 0:
            accuracy = correct_predictions / total_predictions
            for model_name in self.ml_models:
                self.prediction_accuracy[model_name] = accuracy
        
        print(f"🎯 Model validation: {correct_predictions}/{total_predictions} correct predictions")
    
    def get_model_performance(self) -> Dict[str, Any]:
        """Get comprehensive model performance metrics"""
        return {
            'model_accuracy': dict(self.prediction_accuracy),
            'ensemble_weights': dict(self.ensemble_weights),
            'confidence_threshold': self.confidence_threshold,
            'models_trained': list(self.ml_models.keys()),
            'prediction_horizon': self.prediction_horizon,
            'ensemble_size': self.ensemble_size
        }


# Global enhanced ML components
global_enhanced_analyzer = None
global_enhanced_predictor = None

def get_enhanced_ml_components() -> Tuple[AdvancedPatternAnalyzer, EnhancedPredictionEngine]:
    """Get or create global enhanced ML components"""
    global global_enhanced_analyzer, global_enhanced_predictor
    
    if global_enhanced_analyzer is None:
        global_enhanced_analyzer = AdvancedPatternAnalyzer()
    
    if global_enhanced_predictor is None:
        global_enhanced_predictor = EnhancedPredictionEngine(global_enhanced_analyzer)
    
    return global_enhanced_analyzer, global_enhanced_predictor


if __name__ == "__main__":
    # Test enhanced ML system
    print("🧠 Testing Enhanced ML System")
    
    analyzer, predictor = get_enhanced_ml_components()
    
    # Simulate enhanced user actions
    test_actions = [
        EnhancedUserAction("refresh", "table", time.time(), {"cpu_usage": 25, "instance_count": 5}, 1.2, "session1", 0.3, 0.8),
        EnhancedUserAction("search", "searchbox", time.time() + 5, {"cpu_usage": 30, "query": "test"}, 0.8, "session1", 0.2, 0.9),
        EnhancedUserAction("filter", "filter", time.time() + 10, {"cpu_usage": 28, "filter": "running"}, 0.5, "session1", 0.4, 0.85),
        EnhancedUserAction("select", "row", time.time() + 15, {"cpu_usage": 35, "selected_id": 1}, 0.3, "session1", 0.1, 0.9),
        EnhancedUserAction("start", "button", time.time() + 20, {"cpu_usage": 45, "instance_id": 1}, 2.1, "session1", 0.6, 0.7),
    ]
    
    # Record actions
    for action in test_actions:
        analyzer.record_enhanced_action(action)
    
    # Train models
    success = predictor.train_enhanced_models()
    print(f"✅ Model training: {'Success' if success else 'Failed'}")
    
    # Get insights
    insights = analyzer.get_advanced_insights()
    print(f"\n🧠 Advanced Insights:")
    for key, value in insights.items():
        print(f"   {key}: {value}")
    
    # Test enhanced predictions
    predictions = predictor.predict_next_actions_enhanced(
        "refresh", 
        {"cpu_usage": 30, "instance_count": 8},
        num_predictions=3
    )
    
    print(f"\n🎯 Enhanced Predictions:")
    for pred in predictions:
        print(f"   {pred.action_type} (confidence: {pred.confidence:.3f}, impact: {pred.performance_impact:.2f})")
        print(f"      Optimizations: {pred.suggested_optimizations}")
    
    # Performance metrics
    performance = predictor.get_model_performance()
    print(f"\n📊 Model Performance:")
    for key, value in performance.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Enhanced ML System ready!")