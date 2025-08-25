#!/usr/bin/env python3
"""
🔧 Intelligent Performance Monitoring System
===========================================

AI-powered real-time performance monitoring with:
- Adaptive resource optimization
- Intelligent anomaly detection
- Predictive performance analytics
- Dynamic system tuning
- Smart alert management
"""

import time
import psutil
import threading
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, field
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QThread
import statistics
import json
import os


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics"""
    timestamp: float
    cpu_usage: float
    memory_usage: float
    disk_io: Dict[str, float]
    network_io: Dict[str, float]
    process_count: int
    thread_count: int
    response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    user_satisfaction: float = 1.0


@dataclass
class PerformanceAlert:
    """Performance alert with AI classification"""
    alert_id: str
    timestamp: float
    severity: str  # 'low', 'medium', 'high', 'critical'
    category: str  # 'cpu', 'memory', 'disk', 'network', 'application'
    message: str
    metrics: PerformanceMetrics
    suggested_actions: List[str] = field(default_factory=list)
    confidence: float = 1.0
    auto_resolvable: bool = False


@dataclass
class OptimizationAction:
    """AI-suggested optimization action"""
    action_id: str
    action_type: str  # 'tune_parameter', 'scale_resource', 'restart_component', etc.
    target: str
    parameters: Dict[str, Any]
    expected_impact: float
    confidence: float
    risk_level: str  # 'low', 'medium', 'high'
    estimated_duration: float


class IntelligentPerformanceMonitor(QObject):
    """🔧 AI-powered performance monitoring with adaptive optimization"""
    
    # Signals for real-time updates
    metrics_updated = pyqtSignal(dict)
    alert_raised = pyqtSignal(dict)
    optimization_suggested = pyqtSignal(dict)
    anomaly_detected = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_interval = 1000  # 1 second
        self.metrics_history = deque(maxlen=3600)  # 1 hour of data
        self.alerts_history = deque(maxlen=1000)
        
        # AI components
        self.anomaly_detector = AnomalyDetector()
        self.optimization_engine = OptimizationEngine()
        self.adaptive_thresholds = AdaptiveThresholds()
        
        # Performance baselines
        self.performance_baselines = {}
        self.baseline_learning_period = 300  # 5 minutes
        self.baseline_established = False
        
        # Optimization state
        self.active_optimizations = {}
        self.optimization_history = deque(maxlen=500)
        
        # Monitoring timer
        self.monitor_timer = None
        
        # Configuration
        self.config = {
            'cpu_alert_threshold': 80.0,
            'memory_alert_threshold': 85.0,
            'disk_alert_threshold': 90.0,
            'response_time_threshold': 5.0,
            'auto_optimization_enabled': True,
            'anomaly_detection_enabled': True,
            'adaptive_thresholds_enabled': True
        }
        
        print("🔧 Intelligent Performance Monitor initialized")
    
    def start_monitoring(self, interval: int = 1000):
        """Start intelligent performance monitoring"""
        self.monitoring_interval = interval
        self.monitoring_active = True
        
        if self.parent():
            self.monitor_timer = QTimer(self.parent())
            self.monitor_timer.timeout.connect(self._monitoring_cycle)
            self.monitor_timer.start(self.monitoring_interval)
        
        print("🚀 Intelligent performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_timer:
            self.monitor_timer.stop()
        
        print("⏹️ Performance monitoring stopped")
    
    def _monitoring_cycle(self):
        """Main monitoring cycle with AI analysis"""
        try:
            # Collect performance metrics
            metrics = self._collect_performance_metrics()
            
            # Store metrics
            self.metrics_history.append(metrics)
            
            # AI-powered analysis
            self._analyze_performance(metrics)
            
            # Update baselines if learning
            if not self.baseline_established:
                self._update_baselines(metrics)
            
            # Emit metrics update
            self.metrics_updated.emit(self._metrics_to_dict(metrics))
            
        except Exception as e:
            print(f"❌ Monitoring cycle error: {e}")
    
    def _collect_performance_metrics(self) -> PerformanceMetrics:
        """Collect comprehensive performance metrics"""
        current_time = time.time()
        
        # CPU metrics
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Disk I/O metrics
        disk_io = psutil.disk_io_counters()
        disk_metrics = {
            'read_bytes': disk_io.read_bytes if disk_io else 0,
            'write_bytes': disk_io.write_bytes if disk_io else 0,
            'read_time': disk_io.read_time if disk_io else 0,
            'write_time': disk_io.write_time if disk_io else 0
        }
        
        # Network I/O metrics
        network_io = psutil.net_io_counters()
        network_metrics = {
            'bytes_sent': network_io.bytes_sent if network_io else 0,
            'bytes_recv': network_io.bytes_recv if network_io else 0,
            'packets_sent': network_io.packets_sent if network_io else 0,
            'packets_recv': network_io.packets_recv if network_io else 0
        }
        
        # Process metrics
        process_count = len(psutil.pids())
        
        # Thread count (approximate)
        try:
            current_process = psutil.Process()
            thread_count = current_process.num_threads()
        except:
            thread_count = 1
        
        # Application-specific metrics
        response_time = self._measure_response_time()
        throughput = self._calculate_throughput()
        error_rate = self._calculate_error_rate()
        
        return PerformanceMetrics(
            timestamp=current_time,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_io=disk_metrics,
            network_io=network_metrics,
            process_count=process_count,
            thread_count=thread_count,
            response_time=response_time,
            throughput=throughput,
            error_rate=error_rate
        )
    
    def _measure_response_time(self) -> float:
        """Measure application response time"""
        start_time = time.time()
        
        # Simulate a lightweight operation to measure responsiveness
        try:
            # Simple file system operation
            temp_file = "/tmp/perf_test.tmp"
            with open(temp_file, 'w') as f:
                f.write("test")
            os.remove(temp_file)
            
            return (time.time() - start_time) * 1000  # Return in milliseconds
        except:
            return 0.0
    
    def _calculate_throughput(self) -> float:
        """Calculate application throughput"""
        if len(self.metrics_history) < 2:
            return 0.0
        
        # Calculate operations per second based on metrics collection
        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 metrics
        if len(recent_metrics) >= 2:
            time_span = recent_metrics[-1].timestamp - recent_metrics[0].timestamp
            if time_span > 0:
                return len(recent_metrics) / time_span
        
        return 0.0
    
    def _calculate_error_rate(self) -> float:
        """Calculate application error rate"""
        # In a real application, this would track actual errors
        # For now, we'll estimate based on performance degradation
        if len(self.metrics_history) < 10:
            return 0.0
        
        recent_metrics = list(self.metrics_history)[-10:]
        high_cpu_count = sum(1 for m in recent_metrics if m.cpu_usage > 90)
        high_memory_count = sum(1 for m in recent_metrics if m.memory_usage > 90)
        
        error_rate = (high_cpu_count + high_memory_count) / (len(recent_metrics) * 2) * 100
        return min(error_rate, 100.0)
    
    def _analyze_performance(self, metrics: PerformanceMetrics):
        """AI-powered performance analysis"""
        try:
            # Anomaly detection
            if self.config['anomaly_detection_enabled']:
                anomalies = self.anomaly_detector.detect_anomalies(metrics, self.metrics_history)
                for anomaly in anomalies:
                    self.anomaly_detected.emit(anomaly)
            
            # Adaptive threshold analysis
            if self.config['adaptive_thresholds_enabled']:
                self.adaptive_thresholds.update_thresholds(metrics, self.metrics_history)
            
            # Alert generation
            alerts = self._generate_intelligent_alerts(metrics)
            for alert in alerts:
                self.alerts_history.append(alert)
                self.alert_raised.emit(self._alert_to_dict(alert))
            
            # Optimization suggestions
            if self.config['auto_optimization_enabled']:
                optimizations = self.optimization_engine.suggest_optimizations(metrics, self.metrics_history)
                for optimization in optimizations:
                    self.optimization_suggested.emit(self._optimization_to_dict(optimization))
                    
                    # Auto-apply low-risk optimizations
                    if optimization.risk_level == 'low' and optimization.confidence > 0.8:
                        self._apply_optimization(optimization)
            
        except Exception as e:
            print(f"❌ Performance analysis error: {e}")
    
    def _generate_intelligent_alerts(self, metrics: PerformanceMetrics) -> List[PerformanceAlert]:
        """Generate intelligent alerts based on AI analysis"""
        alerts = []
        current_time = time.time()
        
        # Adaptive thresholds
        cpu_threshold = self.adaptive_thresholds.get_threshold('cpu', self.config['cpu_alert_threshold'])
        memory_threshold = self.adaptive_thresholds.get_threshold('memory', self.config['memory_alert_threshold'])
        
        # CPU usage alert
        if metrics.cpu_usage > cpu_threshold:
            severity = 'critical' if metrics.cpu_usage > 95 else 'high' if metrics.cpu_usage > 85 else 'medium'
            
            alert = PerformanceAlert(
                alert_id=f"cpu_{int(current_time)}",
                timestamp=current_time,
                severity=severity,
                category='cpu',
                message=f"High CPU usage detected: {metrics.cpu_usage:.1f}%",
                metrics=metrics,
                suggested_actions=[
                    "Identify CPU-intensive processes",
                    "Scale up CPU resources",
                    "Optimize algorithms",
                    "Enable CPU throttling"
                ],
                confidence=0.9,
                auto_resolvable=(severity == 'medium')
            )
            alerts.append(alert)
        
        # Memory usage alert
        if metrics.memory_usage > memory_threshold:
            severity = 'critical' if metrics.memory_usage > 95 else 'high' if metrics.memory_usage > 90 else 'medium'
            
            alert = PerformanceAlert(
                alert_id=f"memory_{int(current_time)}",
                timestamp=current_time,
                severity=severity,
                category='memory',
                message=f"High memory usage detected: {metrics.memory_usage:.1f}%",
                metrics=metrics,
                suggested_actions=[
                    "Clear memory caches",
                    "Restart memory-intensive processes",
                    "Increase available memory",
                    "Optimize memory allocation"
                ],
                confidence=0.95,
                auto_resolvable=(severity == 'medium')
            )
            alerts.append(alert)
        
        # Response time alert
        if metrics.response_time > self.config['response_time_threshold']:
            severity = 'high' if metrics.response_time > 10.0 else 'medium'
            
            alert = PerformanceAlert(
                alert_id=f"response_time_{int(current_time)}",
                timestamp=current_time,
                severity=severity,
                category='application',
                message=f"Slow response time detected: {metrics.response_time:.1f}ms",
                metrics=metrics,
                suggested_actions=[
                    "Optimize database queries",
                    "Enable response caching",
                    "Scale application servers",
                    "Reduce payload sizes"
                ],
                confidence=0.8,
                auto_resolvable=False
            )
            alerts.append(alert)
        
        # Error rate alert
        if metrics.error_rate > 5.0:
            severity = 'critical' if metrics.error_rate > 20 else 'high' if metrics.error_rate > 10 else 'medium'
            
            alert = PerformanceAlert(
                alert_id=f"error_rate_{int(current_time)}",
                timestamp=current_time,
                severity=severity,
                category='application',
                message=f"High error rate detected: {metrics.error_rate:.1f}%",
                metrics=metrics,
                suggested_actions=[
                    "Check application logs",
                    "Restart failing components",
                    "Review recent deployments",
                    "Scale healthy instances"
                ],
                confidence=0.85,
                auto_resolvable=False
            )
            alerts.append(alert)
        
        return alerts
    
    def _update_baselines(self, metrics: PerformanceMetrics):
        """Update performance baselines during learning period"""
        if len(self.metrics_history) < self.baseline_learning_period:
            return
        
        # Calculate baselines from learning period
        learning_metrics = list(self.metrics_history)[-self.baseline_learning_period:]
        
        self.performance_baselines = {
            'cpu_avg': statistics.mean([m.cpu_usage for m in learning_metrics]),
            'cpu_std': statistics.stdev([m.cpu_usage for m in learning_metrics]) if len(learning_metrics) > 1 else 0,
            'memory_avg': statistics.mean([m.memory_usage for m in learning_metrics]),
            'memory_std': statistics.stdev([m.memory_usage for m in learning_metrics]) if len(learning_metrics) > 1 else 0,
            'response_time_avg': statistics.mean([m.response_time for m in learning_metrics]),
            'response_time_std': statistics.stdev([m.response_time for m in learning_metrics]) if len(learning_metrics) > 1 else 0,
            'throughput_avg': statistics.mean([m.throughput for m in learning_metrics]),
            'throughput_std': statistics.stdev([m.throughput for m in learning_metrics]) if len(learning_metrics) > 1 else 0
        }
        
        self.baseline_established = True
        print("📊 Performance baselines established")
    
    def _apply_optimization(self, optimization: OptimizationAction):
        """Apply automatic optimization"""
        try:
            optimization_id = optimization.action_id
            self.active_optimizations[optimization_id] = {
                'optimization': optimization,
                'start_time': time.time(),
                'status': 'applying'
            }
            
            # Execute optimization based on type
            success = False
            
            if optimization.action_type == 'adjust_polling_interval':
                success = self._adjust_polling_interval(optimization.parameters)
            elif optimization.action_type == 'clear_cache':
                success = self._clear_performance_cache()
            elif optimization.action_type == 'tune_thresholds':
                success = self._tune_thresholds(optimization.parameters)
            elif optimization.action_type == 'optimize_monitoring':
                success = self._optimize_monitoring_frequency(optimization.parameters)
            
            # Update optimization status
            self.active_optimizations[optimization_id]['status'] = 'completed' if success else 'failed'
            self.active_optimizations[optimization_id]['end_time'] = time.time()
            
            # Record in history
            self.optimization_history.append({
                'optimization': optimization,
                'success': success,
                'timestamp': time.time()
            })
            
            print(f"🔧 Applied optimization: {optimization.action_type} ({'Success' if success else 'Failed'})")
            
        except Exception as e:
            print(f"❌ Optimization application failed: {e}")
    
    def _adjust_polling_interval(self, parameters: Dict[str, Any]) -> bool:
        """Adjust monitoring polling interval"""
        try:
            new_interval = parameters.get('interval', self.monitoring_interval)
            if 500 <= new_interval <= 5000:  # Valid range
                self.monitoring_interval = new_interval
                if self.monitor_timer:
                    self.monitor_timer.setInterval(new_interval)
                return True
        except:
            pass
        return False
    
    def _clear_performance_cache(self) -> bool:
        """Clear performance monitoring cache"""
        try:
            # Keep recent metrics but clear older ones
            if len(self.metrics_history) > 100:
                recent_metrics = list(self.metrics_history)[-100:]
                self.metrics_history.clear()
                self.metrics_history.extend(recent_metrics)
            return True
        except:
            return False
    
    def _tune_thresholds(self, parameters: Dict[str, Any]) -> bool:
        """Tune alert thresholds"""
        try:
            for key, value in parameters.items():
                if key in self.config and isinstance(value, (int, float)):
                    self.config[key] = value
            return True
        except:
            return False
    
    def _optimize_monitoring_frequency(self, parameters: Dict[str, Any]) -> bool:
        """Optimize monitoring frequency based on system load"""
        try:
            if len(self.metrics_history) > 0:
                recent_cpu = self.metrics_history[-1].cpu_usage
                
                # Adjust monitoring frequency based on CPU load
                if recent_cpu > 80:
                    new_interval = 2000  # Slower monitoring under high load
                elif recent_cpu < 30:
                    new_interval = 500   # Faster monitoring under low load
                else:
                    new_interval = 1000  # Normal monitoring
                
                return self._adjust_polling_interval({'interval': new_interval})
        except:
            pass
        return False
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        if not self.metrics_history:
            return {}
        
        recent_metrics = list(self.metrics_history)[-60:]  # Last minute
        current_metrics = self.metrics_history[-1]
        
        summary = {
            'current': self._metrics_to_dict(current_metrics),
            'averages': {
                'cpu_usage': statistics.mean([m.cpu_usage for m in recent_metrics]),
                'memory_usage': statistics.mean([m.memory_usage for m in recent_metrics]),
                'response_time': statistics.mean([m.response_time for m in recent_metrics]),
                'throughput': statistics.mean([m.throughput for m in recent_metrics]),
                'error_rate': statistics.mean([m.error_rate for m in recent_metrics])
            },
            'trends': self._calculate_trends(recent_metrics),
            'anomalies': self.anomaly_detector.get_recent_anomalies(),
            'active_alerts': len([a for a in self.alerts_history if time.time() - a.timestamp < 300]),
            'active_optimizations': len(self.active_optimizations),
            'baseline_established': self.baseline_established,
            'monitoring_active': self.monitoring_active
        }
        
        return summary
    
    def _calculate_trends(self, metrics: List[PerformanceMetrics]) -> Dict[str, str]:
        """Calculate performance trends"""
        if len(metrics) < 10:
            return {}
        
        trends = {}
        
        # CPU trend
        cpu_values = [m.cpu_usage for m in metrics]
        cpu_trend = self._calculate_trend_direction(cpu_values)
        trends['cpu'] = cpu_trend
        
        # Memory trend
        memory_values = [m.memory_usage for m in metrics]
        memory_trend = self._calculate_trend_direction(memory_values)
        trends['memory'] = memory_trend
        
        # Response time trend
        response_time_values = [m.response_time for m in metrics]
        response_trend = self._calculate_trend_direction(response_time_values)
        trends['response_time'] = response_trend
        
        return trends
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction for a series of values"""
        if len(values) < 5:
            return 'stable'
        
        # Simple linear regression slope
        n = len(values)
        x_values = list(range(n))
        
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(values)
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'stable'
        
        slope = numerator / denominator
        
        if slope > 1.0:
            return 'increasing'
        elif slope < -1.0:
            return 'decreasing'
        else:
            return 'stable'
    
    def _metrics_to_dict(self, metrics: PerformanceMetrics) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            'timestamp': metrics.timestamp,
            'cpu_usage': metrics.cpu_usage,
            'memory_usage': metrics.memory_usage,
            'disk_io': metrics.disk_io,
            'network_io': metrics.network_io,
            'process_count': metrics.process_count,
            'thread_count': metrics.thread_count,
            'response_time': metrics.response_time,
            'throughput': metrics.throughput,
            'error_rate': metrics.error_rate,
            'user_satisfaction': metrics.user_satisfaction
        }
    
    def _alert_to_dict(self, alert: PerformanceAlert) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            'alert_id': alert.alert_id,
            'timestamp': alert.timestamp,
            'severity': alert.severity,
            'category': alert.category,
            'message': alert.message,
            'suggested_actions': alert.suggested_actions,
            'confidence': alert.confidence,
            'auto_resolvable': alert.auto_resolvable
        }
    
    def _optimization_to_dict(self, optimization: OptimizationAction) -> Dict[str, Any]:
        """Convert optimization to dictionary"""
        return {
            'action_id': optimization.action_id,
            'action_type': optimization.action_type,
            'target': optimization.target,
            'parameters': optimization.parameters,
            'expected_impact': optimization.expected_impact,
            'confidence': optimization.confidence,
            'risk_level': optimization.risk_level,
            'estimated_duration': optimization.estimated_duration
        }


class AnomalyDetector:
    """🔍 AI-powered anomaly detection for performance metrics"""
    
    def __init__(self):
        self.anomalies = deque(maxlen=100)
        self.sensitivity = 0.7
        self.learning_window = 50
    
    def detect_anomalies(self, current_metrics: PerformanceMetrics, 
                        history: deque) -> List[Dict[str, Any]]:
        """Detect performance anomalies"""
        anomalies = []
        
        if len(history) < self.learning_window:
            return anomalies
        
        try:
            # Statistical anomaly detection
            recent_history = list(history)[-self.learning_window:]
            
            # CPU anomaly
            cpu_anomaly = self._detect_statistical_anomaly(
                current_metrics.cpu_usage,
                [m.cpu_usage for m in recent_history],
                'cpu'
            )
            if cpu_anomaly:
                anomalies.append(cpu_anomaly)
            
            # Memory anomaly
            memory_anomaly = self._detect_statistical_anomaly(
                current_metrics.memory_usage,
                [m.memory_usage for m in recent_history],
                'memory'
            )
            if memory_anomaly:
                anomalies.append(memory_anomaly)
            
            # Response time anomaly
            response_anomaly = self._detect_statistical_anomaly(
                current_metrics.response_time,
                [m.response_time for m in recent_history],
                'response_time'
            )
            if response_anomaly:
                anomalies.append(response_anomaly)
            
        except Exception as e:
            print(f"❌ Anomaly detection error: {e}")
        
        return anomalies
    
    def _detect_statistical_anomaly(self, current_value: float, 
                                   historical_values: List[float], 
                                   metric_name: str) -> Optional[Dict[str, Any]]:
        """Detect statistical anomaly using Z-score"""
        if len(historical_values) < 10:
            return None
        
        try:
            mean_value = statistics.mean(historical_values)
            std_value = statistics.stdev(historical_values)
            
            if std_value == 0:
                return None
            
            z_score = abs(current_value - mean_value) / std_value
            
            # Anomaly threshold based on sensitivity
            threshold = 3.0 - (self.sensitivity * 1.5)  # Range: 1.5 to 3.0
            
            if z_score > threshold:
                anomaly = {
                    'metric': metric_name,
                    'current_value': current_value,
                    'expected_value': mean_value,
                    'z_score': z_score,
                    'severity': 'high' if z_score > 4.0 else 'medium',
                    'timestamp': time.time(),
                    'confidence': min(z_score / 5.0, 1.0)
                }
                
                self.anomalies.append(anomaly)
                return anomaly
        
        except Exception as e:
            print(f"❌ Statistical anomaly detection error: {e}")
        
        return None
    
    def get_recent_anomalies(self) -> List[Dict[str, Any]]:
        """Get recent anomalies"""
        current_time = time.time()
        recent_threshold = 300  # 5 minutes
        
        return [anomaly for anomaly in self.anomalies 
                if current_time - anomaly['timestamp'] < recent_threshold]


class AdaptiveThresholds:
    """📊 Adaptive threshold management based on historical performance"""
    
    def __init__(self):
        self.thresholds = {}
        self.adaptation_rate = 0.05
        self.min_samples = 50
    
    def update_thresholds(self, current_metrics: PerformanceMetrics, 
                         history: deque):
        """Update adaptive thresholds based on performance history"""
        if len(history) < self.min_samples:
            return
        
        try:
            recent_history = list(history)[-100:]  # Last 100 samples
            
            # CPU threshold adaptation
            cpu_values = [m.cpu_usage for m in recent_history]
            cpu_95th = statistics.quantiles(cpu_values, n=20)[18]  # 95th percentile
            self.thresholds['cpu'] = self._adapt_threshold(
                self.thresholds.get('cpu', 80.0),
                cpu_95th,
                self.adaptation_rate
            )
            
            # Memory threshold adaptation
            memory_values = [m.memory_usage for m in recent_history]
            memory_95th = statistics.quantiles(memory_values, n=20)[18]
            self.thresholds['memory'] = self._adapt_threshold(
                self.thresholds.get('memory', 85.0),
                memory_95th,
                self.adaptation_rate
            )
            
            # Response time threshold adaptation
            response_values = [m.response_time for m in recent_history if m.response_time > 0]
            if response_values:
                response_95th = statistics.quantiles(response_values, n=20)[18]
                self.thresholds['response_time'] = self._adapt_threshold(
                    self.thresholds.get('response_time', 5.0),
                    response_95th,
                    self.adaptation_rate
                )
            
        except Exception as e:
            print(f"❌ Threshold adaptation error: {e}")
    
    def _adapt_threshold(self, current_threshold: float, observed_95th: float, 
                        adaptation_rate: float) -> float:
        """Adapt threshold based on observed values"""
        # Gradually move threshold towards 95th percentile
        target_threshold = observed_95th * 1.1  # 10% above 95th percentile
        
        # Smooth adaptation
        adapted_threshold = current_threshold + (target_threshold - current_threshold) * adaptation_rate
        
        # Ensure reasonable bounds
        if 'cpu' in str(current_threshold) or 'memory' in str(current_threshold):
            adapted_threshold = max(50.0, min(95.0, adapted_threshold))
        elif 'response_time' in str(current_threshold):
            adapted_threshold = max(1.0, min(30.0, adapted_threshold))
        
        return adapted_threshold
    
    def get_threshold(self, metric: str, default: float) -> float:
        """Get adaptive threshold for metric"""
        return self.thresholds.get(metric, default)


class OptimizationEngine:
    """⚡ AI-powered optimization engine"""
    
    def __init__(self):
        self.optimization_history = deque(maxlen=200)
        self.success_rates = defaultdict(float)
    
    def suggest_optimizations(self, current_metrics: PerformanceMetrics, 
                            history: deque) -> List[OptimizationAction]:
        """Suggest AI-powered optimizations"""
        optimizations = []
        
        try:
            # High CPU optimization
            if current_metrics.cpu_usage > 80:
                optimizations.extend(self._suggest_cpu_optimizations(current_metrics, history))
            
            # High memory optimization
            if current_metrics.memory_usage > 85:
                optimizations.extend(self._suggest_memory_optimizations(current_metrics, history))
            
            # Slow response optimization
            if current_metrics.response_time > 5.0:
                optimizations.extend(self._suggest_response_optimizations(current_metrics, history))
            
            # Proactive optimizations
            optimizations.extend(self._suggest_proactive_optimizations(current_metrics, history))
            
        except Exception as e:
            print(f"❌ Optimization suggestion error: {e}")
        
        return optimizations
    
    def _suggest_cpu_optimizations(self, metrics: PerformanceMetrics, 
                                  history: deque) -> List[OptimizationAction]:
        """Suggest CPU optimizations"""
        optimizations = []
        
        # Reduce monitoring frequency under high CPU load
        optimization = OptimizationAction(
            action_id=f"cpu_opt_{int(time.time())}",
            action_type="optimize_monitoring",
            target="monitoring_system",
            parameters={"reduce_frequency": True, "target_cpu": 70.0},
            expected_impact=0.15,
            confidence=0.8,
            risk_level="low",
            estimated_duration=5.0
        )
        optimizations.append(optimization)
        
        return optimizations
    
    def _suggest_memory_optimizations(self, metrics: PerformanceMetrics, 
                                     history: deque) -> List[OptimizationAction]:
        """Suggest memory optimizations"""
        optimizations = []
        
        # Clear cache under high memory pressure
        optimization = OptimizationAction(
            action_id=f"mem_opt_{int(time.time())}",
            action_type="clear_cache",
            target="performance_cache",
            parameters={"cache_type": "metrics", "keep_recent": 100},
            expected_impact=0.20,
            confidence=0.9,
            risk_level="low",
            estimated_duration=2.0
        )
        optimizations.append(optimization)
        
        return optimizations
    
    def _suggest_response_optimizations(self, metrics: PerformanceMetrics, 
                                       history: deque) -> List[OptimizationAction]:
        """Suggest response time optimizations"""
        optimizations = []
        
        # Adjust polling interval for better responsiveness
        optimization = OptimizationAction(
            action_id=f"resp_opt_{int(time.time())}",
            action_type="adjust_polling_interval",
            target="monitoring_timer",
            parameters={"interval": 2000, "reason": "high_response_time"},
            expected_impact=0.25,
            confidence=0.7,
            risk_level="low",
            estimated_duration=1.0
        )
        optimizations.append(optimization)
        
        return optimizations
    
    def _suggest_proactive_optimizations(self, metrics: PerformanceMetrics, 
                                        history: deque) -> List[OptimizationAction]:
        """Suggest proactive optimizations"""
        optimizations = []
        
        if len(history) > 50:
            recent_metrics = list(history)[-50:]
            
            # Check for trending issues
            cpu_trend = [m.cpu_usage for m in recent_metrics]
            if len(cpu_trend) > 10:
                recent_avg = statistics.mean(cpu_trend[-10:])
                older_avg = statistics.mean(cpu_trend[-20:-10])
                
                if recent_avg > older_avg + 10:  # CPU trending up
                    optimization = OptimizationAction(
                        action_id=f"proactive_cpu_{int(time.time())}",
                        action_type="tune_thresholds",
                        target="cpu_threshold",
                        parameters={"cpu_alert_threshold": max(recent_avg + 5, 75)},
                        expected_impact=0.10,
                        confidence=0.6,
                        risk_level="low",
                        estimated_duration=1.0
                    )
                    optimizations.append(optimization)
        
        return optimizations


# Global intelligent performance monitor
global_performance_monitor = None

def get_intelligent_performance_monitor(parent=None) -> IntelligentPerformanceMonitor:
    """Get or create global intelligent performance monitor"""
    global global_performance_monitor
    if global_performance_monitor is None:
        global_performance_monitor = IntelligentPerformanceMonitor(parent)
    return global_performance_monitor


if __name__ == "__main__":
    # Test intelligent performance monitoring
    print("🔧 Testing Intelligent Performance Monitoring System")
    
    monitor = IntelligentPerformanceMonitor()
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Simulate monitoring for a few cycles
    import time
    for i in range(5):
        time.sleep(1)
        monitor._monitoring_cycle()
    
    # Get performance summary
    summary = monitor.get_performance_summary()
    print(f"\n📊 Performance Summary:")
    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for sub_key, sub_value in value.items():
                print(f"      {sub_key}: {sub_value}")
        else:
            print(f"   {key}: {value}")
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    print("\n✅ Intelligent Performance Monitoring system ready!")