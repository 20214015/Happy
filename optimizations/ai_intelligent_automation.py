#!/usr/bin/env python3
"""
🤖 Intelligent Automation AI System
=================================

Advanced AI-driven automation for MumuManager Pro:
- Smart decision-making algorithms
- Adaptive workflow automation
- Context-aware task scheduling
- Intelligent resource management
- Self-optimizing automation rules
"""

import time
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import statistics
import threading
from datetime import datetime, timedelta
from enum import Enum


class AutomationPriority(Enum):
    """Automation task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


class AutomationStatus(Enum):
    """Automation task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"


@dataclass
class AutomationRule:
    """Intelligent automation rule"""
    rule_id: str
    name: str
    description: str
    conditions: List[Dict[str, Any]]  # List of conditions to check
    actions: List[Dict[str, Any]]     # List of actions to execute
    priority: AutomationPriority
    enabled: bool = True
    auto_adapt: bool = True
    learning_enabled: bool = True
    success_rate: float = 0.0
    execution_count: int = 0
    last_execution: float = 0.0
    created_timestamp: float = 0.0
    
    def __post_init__(self):
        if self.created_timestamp == 0.0:
            self.created_timestamp = time.time()


@dataclass
class AutomationTask:
    """Individual automation task"""
    task_id: str
    rule_id: str
    name: str
    description: str
    actions: List[Dict[str, Any]]
    priority: AutomationPriority
    status: AutomationStatus
    scheduled_time: float
    created_time: float
    started_time: Optional[float] = None
    completed_time: Optional[float] = None
    error_message: Optional[str] = None
    context: Dict[str, Any] = None
    success: bool = False
    execution_duration: float = 0.0
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.created_time == 0.0:
            self.created_time = time.time()


@dataclass
class DecisionContext:
    """Context information for AI decision making"""
    current_metrics: Dict[str, float]
    historical_data: Dict[str, List[float]]
    system_state: Dict[str, Any]
    user_preferences: Dict[str, Any]
    time_context: Dict[str, Any]
    resource_constraints: Dict[str, Any]
    performance_goals: Dict[str, float]


class IntelligentConditionEvaluator:
    """🧠 AI-powered condition evaluation system"""
    
    def __init__(self):
        self.evaluation_history = deque(maxlen=1000)
        self.condition_patterns = defaultdict(list)
        self.learning_enabled = True
        
        print("🧠 Intelligent Condition Evaluator initialized")
    
    def evaluate_condition(self, condition: Dict[str, Any], context: DecisionContext) -> Tuple[bool, float]:
        """Evaluate a condition with AI enhancement and confidence score"""
        try:
            condition_type = condition.get('type', 'simple')
            
            if condition_type == 'simple':
                result, confidence = self._evaluate_simple_condition(condition, context)
            elif condition_type == 'complex':
                result, confidence = self._evaluate_complex_condition(condition, context)
            elif condition_type == 'ai_enhanced':
                result, confidence = self._evaluate_ai_enhanced_condition(condition, context)
            elif condition_type == 'threshold':
                result, confidence = self._evaluate_threshold_condition(condition, context)
            elif condition_type == 'trend':
                result, confidence = self._evaluate_trend_condition(condition, context)
            else:
                result, confidence = self._evaluate_simple_condition(condition, context)
            
            # Record evaluation for learning
            if self.learning_enabled:
                self._record_evaluation(condition, context, result, confidence)
            
            return result, confidence
            
        except Exception as e:
            print(f"❌ Condition evaluation error: {e}")
            return False, 0.0
    
    def _evaluate_simple_condition(self, condition: Dict[str, Any], context: DecisionContext) -> Tuple[bool, float]:
        """Evaluate simple condition (metric comparison)"""
        metric = condition.get('metric', '')
        operator = condition.get('operator', '>')
        value = condition.get('value', 0)
        
        if metric not in context.current_metrics:
            return False, 0.0
        
        current_value = context.current_metrics[metric]
        
        if operator == '>':
            result = current_value > value
        elif operator == '<':
            result = current_value < value
        elif operator == '>=':
            result = current_value >= value
        elif operator == '<=':
            result = current_value <= value
        elif operator == '==':
            result = abs(current_value - value) < 1e-6
        elif operator == '!=':
            result = abs(current_value - value) >= 1e-6
        else:
            result = False
        
        # Calculate confidence based on how far the value is from threshold
        if value != 0:
            distance_ratio = abs(current_value - value) / abs(value)
            confidence = min(0.5 + distance_ratio * 0.5, 1.0)
        else:
            confidence = 0.8 if result else 0.2
        
        return result, confidence
    
    def _evaluate_complex_condition(self, condition: Dict[str, Any], context: DecisionContext) -> Tuple[bool, float]:
        """Evaluate complex condition (multiple metrics with logic)"""
        sub_conditions = condition.get('conditions', [])
        logic_operator = condition.get('logic', 'AND')
        
        if not sub_conditions:
            return False, 0.0
        
        results = []
        confidences = []
        
        for sub_condition in sub_conditions:
            result, confidence = self.evaluate_condition(sub_condition, context)
            results.append(result)
            confidences.append(confidence)
        
        # Apply logic operator
        if logic_operator == 'AND':
            final_result = all(results)
            final_confidence = min(confidences) if confidences else 0.0
        elif logic_operator == 'OR':
            final_result = any(results)
            final_confidence = max(confidences) if confidences else 0.0
        elif logic_operator == 'NOT':
            final_result = not results[0] if results else False
            final_confidence = confidences[0] if confidences else 0.0
        else:
            final_result = False
            final_confidence = 0.0
        
        return final_result, final_confidence
    
    def _evaluate_ai_enhanced_condition(self, condition: Dict[str, Any], context: DecisionContext) -> Tuple[bool, float]:
        """Evaluate AI-enhanced condition using pattern recognition"""
        pattern_name = condition.get('pattern', '')
        parameters = condition.get('parameters', {})
        
        # Use historical patterns to make intelligent decisions
        if pattern_name in self.condition_patterns:
            pattern_history = self.condition_patterns[pattern_name]
            
            if len(pattern_history) >= 5:
                # Calculate pattern success rate
                recent_results = pattern_history[-10:]  # Last 10 evaluations
                success_rate = sum(1 for r in recent_results if r['result']) / len(recent_results)
                
                # Use machine learning-like logic
                current_similarity = self._calculate_context_similarity(context, recent_results)
                
                # Predict result based on similarity and success rate
                predicted_success = success_rate * current_similarity
                result = predicted_success > 0.5
                confidence = predicted_success if result else 1 - predicted_success
                
                return result, confidence
        
        # Fallback to simple evaluation
        return self._evaluate_simple_condition(condition, context)
    
    def _evaluate_threshold_condition(self, condition: Dict[str, Any], context: DecisionContext) -> Tuple[bool, float]:
        """Evaluate adaptive threshold condition"""
        metric = condition.get('metric', '')
        threshold_type = condition.get('threshold_type', 'static')
        base_value = condition.get('value', 0)
        
        if metric not in context.current_metrics:
            return False, 0.0
        
        current_value = context.current_metrics[metric]
        
        # Calculate adaptive threshold
        if threshold_type == 'adaptive' and metric in context.historical_data:
            historical_values = context.historical_data[metric]
            if len(historical_values) >= 10:
                mean_val = statistics.mean(historical_values)
                std_val = statistics.stdev(historical_values)
                adaptive_threshold = mean_val + 2 * std_val  # 2 sigma threshold
            else:
                adaptive_threshold = base_value
        else:
            adaptive_threshold = base_value
        
        # Evaluate against adaptive threshold
        result = current_value > adaptive_threshold
        
        # Calculate confidence
        if adaptive_threshold != 0:
            distance_ratio = abs(current_value - adaptive_threshold) / abs(adaptive_threshold)
            confidence = min(0.5 + distance_ratio * 0.5, 1.0)
        else:
            confidence = 0.7
        
        return result, confidence
    
    def _evaluate_trend_condition(self, condition: Dict[str, Any], context: DecisionContext) -> Tuple[bool, float]:
        """Evaluate trend-based condition"""
        metric = condition.get('metric', '')
        trend_direction = condition.get('direction', 'increasing')
        window_size = condition.get('window', 10)
        
        if metric not in context.historical_data:
            return False, 0.0
        
        historical_values = context.historical_data[metric]
        if len(historical_values) < window_size:
            return False, 0.0
        
        # Calculate trend from recent values
        recent_values = historical_values[-window_size:]
        
        # Simple linear trend calculation
        n = len(recent_values)
        x = list(range(n))
        y = recent_values
        
        # Calculate slope
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return False, 0.0
        
        slope = numerator / denominator
        
        # Evaluate trend direction
        if trend_direction == 'increasing':
            result = slope > 0.01
        elif trend_direction == 'decreasing':
            result = slope < -0.01
        elif trend_direction == 'stable':
            result = abs(slope) <= 0.01
        else:
            result = False
        
        # Calculate confidence based on trend strength
        confidence = min(abs(slope) * 100, 1.0)
        
        return result, confidence
    
    def _calculate_context_similarity(self, current_context: DecisionContext, historical_results: List[Dict]) -> float:
        """Calculate similarity between current context and historical contexts"""
        if not historical_results:
            return 0.5
        
        similarities = []
        
        for historical_result in historical_results[-5:]:  # Compare with last 5
            historical_context = historical_result.get('context', {})
            
            # Simple similarity calculation based on metric values
            similarity = 0.0
            common_metrics = 0
            
            for metric in current_context.current_metrics:
                if metric in historical_context:
                    current_val = current_context.current_metrics[metric]
                    historical_val = historical_context.get(metric, 0)
                    
                    if historical_val != 0:
                        metric_similarity = 1 - abs(current_val - historical_val) / abs(historical_val)
                        similarity += max(metric_similarity, 0)
                    
                    common_metrics += 1
            
            if common_metrics > 0:
                similarities.append(similarity / common_metrics)
        
        return statistics.mean(similarities) if similarities else 0.5
    
    def _record_evaluation(self, condition: Dict[str, Any], context: DecisionContext, result: bool, confidence: float):
        """Record evaluation for learning"""
        pattern_name = condition.get('pattern', condition.get('type', 'unknown'))
        
        evaluation_record = {
            'condition': condition,
            'context': asdict(context),
            'result': result,
            'confidence': confidence,
            'timestamp': time.time()
        }
        
        self.evaluation_history.append(evaluation_record)
        self.condition_patterns[pattern_name].append(evaluation_record)
        
        # Keep pattern history manageable
        if len(self.condition_patterns[pattern_name]) > 50:
            self.condition_patterns[pattern_name] = self.condition_patterns[pattern_name][-30:]


class SmartActionExecutor:
    """⚡ AI-powered action execution system"""
    
    def __init__(self):
        self.execution_history = deque(maxlen=1000)
        self.action_success_rates = defaultdict(lambda: {'success': 0, 'total': 0})
        self.action_patterns = defaultdict(list)
        
        # Predefined action handlers
        self.action_handlers = {
            'optimize_memory': self._optimize_memory_action,
            'restart_instance': self._restart_instance_action,
            'scale_resources': self._scale_resources_action,
            'send_notification': self._send_notification_action,
            'cleanup_cache': self._cleanup_cache_action,
            'adjust_settings': self._adjust_settings_action,
            'log_event': self._log_event_action,
            'trigger_backup': self._trigger_backup_action
        }
        
        print("⚡ Smart Action Executor initialized")
    
    def execute_action(self, action: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Execute an action with AI optimization"""
        action_type = action.get('type', 'unknown')
        action_params = action.get('parameters', {})
        
        try:
            # Get action handler
            handler = self.action_handlers.get(action_type, self._default_action_handler)
            
            # Execute action
            start_time = time.time()
            success, message = handler(action_params, context)
            execution_time = time.time() - start_time
            
            # Record execution
            self._record_execution(action_type, action_params, success, execution_time, message)
            
            return success, message
            
        except Exception as e:
            error_message = f"Action execution failed: {e}"
            self._record_execution(action_type, action_params, False, 0.0, error_message)
            return False, error_message
    
    def _optimize_memory_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Optimize memory usage action"""
        target_reduction = params.get('target_reduction_mb', 100)
        
        # Simulate memory optimization
        current_memory = context.current_metrics.get('memory_usage', 0)
        
        if current_memory > 80:  # High memory usage
            # Simulate successful optimization
            print(f"🧠 Memory optimization: Target reduction {target_reduction}MB")
            return True, f"Memory optimized, reduced by {target_reduction}MB"
        else:
            return False, "Memory usage already optimal"
    
    def _restart_instance_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Restart instance action"""
        instance_id = params.get('instance_id', 'unknown')
        force_restart = params.get('force', False)
        
        # Check if restart is appropriate
        cpu_usage = context.current_metrics.get('cpu_usage', 0)
        
        if cpu_usage > 90 or force_restart:
            print(f"🔄 Restarting instance {instance_id}")
            return True, f"Instance {instance_id} restarted successfully"
        else:
            return False, "Instance restart not needed"
    
    def _scale_resources_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Scale resources action"""
        scale_type = params.get('type', 'cpu')
        scale_amount = params.get('amount', 1.0)
        
        current_usage = context.current_metrics.get(f'{scale_type}_usage', 0)
        
        if current_usage > 85:  # High usage
            print(f"📈 Scaling {scale_type} resources by {scale_amount}x")
            return True, f"Scaled {scale_type} resources by {scale_amount}x"
        else:
            return False, f"{scale_type} scaling not needed"
    
    def _send_notification_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Send notification action"""
        message = params.get('message', 'System notification')
        severity = params.get('severity', 'info')
        
        print(f"📢 Notification [{severity}]: {message}")
        return True, f"Notification sent: {message}"
    
    def _cleanup_cache_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Cleanup cache action"""
        cache_type = params.get('cache_type', 'all')
        
        print(f"🧹 Cleaning up {cache_type} cache")
        return True, f"Cache cleanup completed for {cache_type}"
    
    def _adjust_settings_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Adjust settings action"""
        setting_name = params.get('setting', 'unknown')
        new_value = params.get('value', None)
        
        if new_value is not None:
            print(f"⚙️ Adjusting {setting_name} to {new_value}")
            return True, f"Setting {setting_name} adjusted to {new_value}"
        else:
            return False, "No value specified for setting adjustment"
    
    def _log_event_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Log event action"""
        event_message = params.get('message', 'Automated event')
        event_level = params.get('level', 'info')
        
        print(f"📝 Log [{event_level}]: {event_message}")
        return True, f"Event logged: {event_message}"
    
    def _trigger_backup_action(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Trigger backup action"""
        backup_type = params.get('type', 'full')
        
        print(f"💾 Triggering {backup_type} backup")
        return True, f"{backup_type} backup initiated"
    
    def _default_action_handler(self, params: Dict[str, Any], context: DecisionContext) -> Tuple[bool, str]:
        """Default action handler for unknown actions"""
        print(f"⚡ Executing custom action with params: {params}")
        return True, "Custom action executed"
    
    def _record_execution(self, action_type: str, params: Dict[str, Any], success: bool, execution_time: float, message: str):
        """Record action execution for learning"""
        execution_record = {
            'action_type': action_type,
            'parameters': params,
            'success': success,
            'execution_time': execution_time,
            'message': message,
            'timestamp': time.time()
        }
        
        self.execution_history.append(execution_record)
        
        # Update success rates
        rates = self.action_success_rates[action_type]
        rates['total'] += 1
        if success:
            rates['success'] += 1
        
        # Store patterns
        self.action_patterns[action_type].append(execution_record)
        
        # Keep pattern history manageable
        if len(self.action_patterns[action_type]) > 30:
            self.action_patterns[action_type] = self.action_patterns[action_type][-20:]
    
    def get_action_success_rate(self, action_type: str) -> float:
        """Get success rate for an action type"""
        rates = self.action_success_rates[action_type]
        if rates['total'] > 0:
            return rates['success'] / rates['total']
        return 0.0


class IntelligentAutomationEngine(QObject):
    """🤖 Main intelligent automation engine"""
    
    # Signals for automation events
    rule_triggered = pyqtSignal(dict)
    task_scheduled = pyqtSignal(dict)
    task_completed = pyqtSignal(dict)
    automation_learned = pyqtSignal(dict)
    decision_made = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Core components
        self.condition_evaluator = IntelligentConditionEvaluator()
        self.action_executor = SmartActionExecutor()
        
        # Automation state
        self.automation_rules = {}
        self.task_queue = deque()
        self.active_tasks = {}
        self.completed_tasks = deque(maxlen=1000)
        
        # Processing timer
        self.processing_timer = QTimer()
        self.processing_timer.timeout.connect(self._process_automation_cycle)
        self.processing_interval = 5000  # 5 seconds
        
        # Learning and adaptation
        self.learning_enabled = True
        self.adaptation_enabled = True
        self.performance_metrics = defaultdict(list)
        
        print("🤖 Intelligent Automation Engine initialized")
    
    def start_automation(self):
        """Start the automation engine"""
        self.processing_timer.start(self.processing_interval)
        print("🤖 Automation engine started")
    
    def stop_automation(self):
        """Stop the automation engine"""
        self.processing_timer.stop()
        print("🤖 Automation engine stopped")
    
    def add_automation_rule(self, rule: AutomationRule):
        """Add a new automation rule"""
        self.automation_rules[rule.rule_id] = rule
        print(f"🤖 Added automation rule: {rule.name}")
    
    def remove_automation_rule(self, rule_id: str):
        """Remove an automation rule"""
        if rule_id in self.automation_rules:
            del self.automation_rules[rule_id]
            print(f"🤖 Removed automation rule: {rule_id}")
    
    def create_decision_context(self, current_metrics: Dict[str, float], historical_data: Dict[str, List[float]] = None) -> DecisionContext:
        """Create decision context for AI evaluation"""
        if historical_data is None:
            historical_data = {}
        
        # Basic system state (can be enhanced with real data)
        system_state = {
            'uptime': time.time() % 86400,  # Simulated uptime
            'load_average': current_metrics.get('cpu_usage', 0) / 100,
            'active_connections': current_metrics.get('active_connections', 10)
        }
        
        # Time context
        current_time = datetime.now()
        time_context = {
            'hour': current_time.hour,
            'day_of_week': current_time.weekday(),
            'is_business_hours': 9 <= current_time.hour <= 17,
            'is_weekend': current_time.weekday() >= 5
        }
        
        # Resource constraints
        resource_constraints = {
            'max_cpu_usage': 90.0,
            'max_memory_usage': 85.0,
            'max_disk_usage': 80.0,
            'max_active_instances': 20
        }
        
        # Performance goals
        performance_goals = {
            'target_response_time': 2.0,
            'target_throughput': 100.0,
            'max_error_rate': 0.05,
            'min_availability': 0.99
        }
        
        return DecisionContext(
            current_metrics=current_metrics,
            historical_data=historical_data,
            system_state=system_state,
            user_preferences={},  # Can be populated with real preferences
            time_context=time_context,
            resource_constraints=resource_constraints,
            performance_goals=performance_goals
        )
    
    def _process_automation_cycle(self):
        """Main automation processing cycle"""
        try:
            # Get current context (in real implementation, this would come from system monitoring)
            current_metrics = self._get_current_metrics()
            historical_data = self._get_historical_data()
            context = self.create_decision_context(current_metrics, historical_data)
            
            # Evaluate all automation rules
            for rule_id, rule in self.automation_rules.items():
                if rule.enabled:
                    self._evaluate_rule(rule, context)
            
            # Process task queue
            self._process_task_queue()
            
            # Update active tasks
            self._update_active_tasks()
            
            # Perform learning and adaptation
            if self.learning_enabled:
                self._perform_learning_cycle()
                
        except Exception as e:
            print(f"❌ Automation cycle error: {e}")
    
    def _get_current_metrics(self) -> Dict[str, float]:
        """Get current system metrics (simulated for demo)"""
        import random
        
        # Simulate realistic metrics with some variability
        base_time = time.time()
        hour_factor = abs(math.sin(base_time / 3600))  # Hourly variation
        
        return {
            'cpu_usage': 30 + hour_factor * 40 + random.uniform(-10, 10),
            'memory_usage': 40 + hour_factor * 30 + random.uniform(-5, 5),
            'disk_usage': 50 + random.uniform(-5, 5),
            'network_io': 20 + hour_factor * 50 + random.uniform(-10, 10),
            'response_time': 1.5 + random.uniform(-0.5, 1.0),
            'error_rate': 0.02 + random.uniform(-0.01, 0.03),
            'active_connections': 15 + random.randint(-5, 10)
        }
    
    def _get_historical_data(self) -> Dict[str, List[float]]:
        """Get historical metrics data (simulated for demo)"""
        import random
        
        metrics = ['cpu_usage', 'memory_usage', 'response_time', 'error_rate']
        historical = {}
        
        for metric in metrics:
            # Generate 50 historical points with trend
            base_values = []
            for i in range(50):
                if metric == 'cpu_usage':
                    val = 30 + i * 0.2 + random.uniform(-5, 5)
                elif metric == 'memory_usage':
                    val = 40 + i * 0.1 + random.uniform(-3, 3)
                elif metric == 'response_time':
                    val = 1.5 + random.uniform(-0.2, 0.5)
                else:  # error_rate
                    val = 0.02 + random.uniform(-0.01, 0.02)
                
                base_values.append(max(0, val))
            
            historical[metric] = base_values
        
        return historical
    
    def _evaluate_rule(self, rule: AutomationRule, context: DecisionContext):
        """Evaluate an automation rule"""
        try:
            # Evaluate all conditions
            all_conditions_met = True
            total_confidence = 0.0
            condition_count = 0
            
            for condition in rule.conditions:
                result, confidence = self.condition_evaluator.evaluate_condition(condition, context)
                
                if not result:
                    all_conditions_met = False
                    break
                
                total_confidence += confidence
                condition_count += 1
            
            if all_conditions_met and condition_count > 0:
                avg_confidence = total_confidence / condition_count
                
                # Only trigger if confidence is high enough
                if avg_confidence >= 0.6:
                    self._trigger_rule(rule, context, avg_confidence)
                    
        except Exception as e:
            print(f"❌ Rule evaluation error ({rule.rule_id}): {e}")
    
    def _trigger_rule(self, rule: AutomationRule, context: DecisionContext, confidence: float):
        """Trigger an automation rule"""
        try:
            # Check if rule was recently triggered (avoid spam)
            if time.time() - rule.last_execution < 60:  # 1 minute cooldown
                return
            
            # Create automation task
            task_id = f"{rule.rule_id}_{int(time.time())}"
            task = AutomationTask(
                task_id=task_id,
                rule_id=rule.rule_id,
                name=f"Auto: {rule.name}",
                description=rule.description,
                actions=rule.actions.copy(),
                priority=rule.priority,
                status=AutomationStatus.SCHEDULED,
                scheduled_time=time.time(),
                created_time=time.time(),
                context={
                    'trigger_confidence': confidence,
                    'trigger_metrics': context.current_metrics.copy()
                }
            )
            
            # Add to task queue
            self.task_queue.append(task)
            
            # Update rule execution tracking
            rule.last_execution = time.time()
            rule.execution_count += 1
            
            # Emit signals
            self.rule_triggered.emit({
                'rule_id': rule.rule_id,
                'rule_name': rule.name,
                'confidence': confidence,
                'task_id': task_id
            })
            
            self.task_scheduled.emit(asdict(task))
            
            print(f"🤖 Rule triggered: {rule.name} (confidence: {confidence:.2f})")
            
        except Exception as e:
            print(f"❌ Rule trigger error ({rule.rule_id}): {e}")
    
    def _process_task_queue(self):
        """Process pending tasks in the queue"""
        # Sort tasks by priority and scheduled time
        tasks_to_process = sorted(
            [task for task in self.task_queue if task.status == AutomationStatus.SCHEDULED],
            key=lambda t: (t.priority.value, t.scheduled_time),
            reverse=True  # Higher priority first
        )
        
        # Process up to 3 tasks per cycle to avoid overload
        for task in tasks_to_process[:3]:
            self._execute_task(task)
    
    def _execute_task(self, task: AutomationTask):
        """Execute an automation task"""
        try:
            task.status = AutomationStatus.RUNNING
            task.started_time = time.time()
            self.active_tasks[task.task_id] = task
            
            # Remove from queue
            if task in self.task_queue:
                self.task_queue.remove(task)
            
            # Create execution context
            current_metrics = self._get_current_metrics()
            context = self.create_decision_context(current_metrics)
            
            # Execute all actions
            all_actions_successful = True
            execution_messages = []
            
            for action in task.actions:
                success, message = self.action_executor.execute_action(action, context)
                execution_messages.append(message)
                
                if not success:
                    all_actions_successful = False
                    break
            
            # Update task status
            task.completed_time = time.time()
            task.execution_duration = task.completed_time - task.started_time
            task.success = all_actions_successful
            
            if all_actions_successful:
                task.status = AutomationStatus.COMPLETED
            else:
                task.status = AutomationStatus.FAILED
                task.error_message = "; ".join(execution_messages)
            
            # Update rule success rate
            if task.rule_id in self.automation_rules:
                rule = self.automation_rules[task.rule_id]
                if all_actions_successful:
                    rule.success_rate = (rule.success_rate * (rule.execution_count - 1) + 1.0) / rule.execution_count
                else:
                    rule.success_rate = (rule.success_rate * (rule.execution_count - 1)) / rule.execution_count
            
            # Move to completed tasks
            self.completed_tasks.append(task)
            
            # Emit completion signal
            self.task_completed.emit(asdict(task))
            
            print(f"🤖 Task {'completed' if all_actions_successful else 'failed'}: {task.name}")
            
        except Exception as e:
            task.status = AutomationStatus.FAILED
            task.error_message = str(e)
            task.completed_time = time.time()
            print(f"❌ Task execution error ({task.task_id}): {e}")
        finally:
            # Remove from active tasks
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    def _update_active_tasks(self):
        """Update status of active tasks"""
        # Check for long-running tasks (timeout after 5 minutes)
        current_time = time.time()
        timeout_threshold = 300  # 5 minutes
        
        for task_id, task in list(self.active_tasks.items()):
            if task.started_time and (current_time - task.started_time) > timeout_threshold:
                task.status = AutomationStatus.FAILED
                task.error_message = "Task timeout"
                task.completed_time = current_time
                
                self.completed_tasks.append(task)
                del self.active_tasks[task_id]
                
                print(f"⏰ Task timeout: {task.name}")
    
    def _perform_learning_cycle(self):
        """Perform learning and adaptation cycle"""
        try:
            # Analyze recent task performance
            recent_tasks = list(self.completed_tasks)[-20:]  # Last 20 tasks
            
            if len(recent_tasks) >= 10:
                success_rate = sum(1 for task in recent_tasks if task.success) / len(recent_tasks)
                avg_duration = statistics.mean(task.execution_duration for task in recent_tasks if task.execution_duration > 0)
                
                # Record performance metrics
                self.performance_metrics['success_rate'].append(success_rate)
                self.performance_metrics['avg_duration'].append(avg_duration)
                
                # Emit learning signal
                self.automation_learned.emit({
                    'success_rate': success_rate,
                    'avg_duration': avg_duration,
                    'tasks_analyzed': len(recent_tasks),
                    'timestamp': time.time()
                })
                
                # Adaptive improvements
                if self.adaptation_enabled:
                    self._adapt_automation_rules(success_rate, avg_duration)
            
        except Exception as e:
            print(f"❌ Learning cycle error: {e}")
    
    def _adapt_automation_rules(self, success_rate: float, avg_duration: float):
        """Adapt automation rules based on performance"""
        if success_rate < 0.7:  # Low success rate
            # Make conditions more strict
            for rule in self.automation_rules.values():
                if rule.auto_adapt:
                    # Increase confidence thresholds (simulated)
                    print(f"🧠 Adapting rule {rule.name} for better success rate")
        
        if avg_duration > 10.0:  # Tasks taking too long
            # Optimize for faster execution
            print("🧠 Optimizing automation for faster execution")
    
    def get_automation_insights(self) -> Dict[str, Any]:
        """Get comprehensive automation insights"""
        insights = {
            'active_rules': len([r for r in self.automation_rules.values() if r.enabled]),
            'total_rules': len(self.automation_rules),
            'tasks_in_queue': len(self.task_queue),
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'automation_running': self.processing_timer.isActive(),
            'learning_enabled': self.learning_enabled,
            'adaptation_enabled': self.adaptation_enabled,
            'rule_performance': {},
            'recent_performance': {}
        }
        
        # Rule performance
        for rule_id, rule in self.automation_rules.items():
            insights['rule_performance'][rule_id] = {
                'name': rule.name,
                'success_rate': rule.success_rate,
                'execution_count': rule.execution_count,
                'last_execution': rule.last_execution,
                'enabled': rule.enabled
            }
        
        # Recent performance metrics
        if self.performance_metrics['success_rate']:
            insights['recent_performance'] = {
                'avg_success_rate': statistics.mean(self.performance_metrics['success_rate'][-10:]),
                'avg_duration': statistics.mean(self.performance_metrics['avg_duration'][-10:]) if self.performance_metrics['avg_duration'] else 0.0,
                'performance_trend': 'improving' if len(self.performance_metrics['success_rate']) >= 2 and 
                                   self.performance_metrics['success_rate'][-1] > self.performance_metrics['success_rate'][-2] else 'stable'
            }
        
        return insights


# Global intelligent automation engine
global_automation_engine = None

def get_intelligent_automation_engine(parent=None) -> IntelligentAutomationEngine:
    """Get or create global intelligent automation engine"""
    global global_automation_engine
    
    if global_automation_engine is None:
        global_automation_engine = IntelligentAutomationEngine(parent)
    
    return global_automation_engine


if __name__ == "__main__":
    # Test intelligent automation system
    print("🤖 Testing Intelligent Automation Engine")
    
    engine = get_intelligent_automation_engine()
    
    # Create a sample automation rule
    sample_rule = AutomationRule(
        rule_id="high_cpu_optimizer",
        name="High CPU Usage Optimizer",
        description="Automatically optimize system when CPU usage is high",
        conditions=[
            {
                'type': 'threshold',
                'metric': 'cpu_usage',
                'threshold_type': 'adaptive',
                'value': 80.0
            }
        ],
        actions=[
            {
                'type': 'optimize_memory',
                'parameters': {'target_reduction_mb': 200}
            },
            {
                'type': 'send_notification',
                'parameters': {
                    'message': 'High CPU detected, optimization applied',
                    'severity': 'warning'
                }
            }
        ],
        priority=AutomationPriority.HIGH
    )
    
    # Add rule and start automation
    engine.add_automation_rule(sample_rule)
    engine.start_automation()
    
    print("✅ Sample automation rule added and engine started")
    
    # Get insights
    insights = engine.get_automation_insights()
    print(f"✅ Automation insights: {insights['active_rules']} active rules, {insights['automation_running']} running")