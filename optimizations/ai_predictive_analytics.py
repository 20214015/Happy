#!/usr/bin/env python3
"""
📊 Advanced Predictive Analytics AI System
========================================

Next-generation predictive analytics for MumuManager Pro:
- Time series forecasting with machine learning
- Multi-dimensional trend analysis
- Real-time adaptive prediction models
- Statistical inference and confidence intervals
- Automated model selection and tuning
"""

import time
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import statistics
import math
import threading
from datetime import datetime, timedelta


@dataclass
class PredictiveModel:
    """Configuration for predictive models"""
    model_type: str  # 'linear', 'polynomial', 'exponential', 'arima', 'ensemble'
    lookback_window: int = 50
    forecast_horizon: int = 10
    confidence_level: float = 0.95
    auto_update: bool = True
    model_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.model_params is None:
            self.model_params = {}


@dataclass
class ForecastResult:
    """Predictive forecast result"""
    forecast_id: str
    metric_name: str
    predicted_values: List[float]
    confidence_intervals: List[Tuple[float, float]]
    timestamps: List[float]
    model_type: str
    accuracy_score: float
    trend_direction: str  # 'increasing', 'decreasing', 'stable'
    seasonal_pattern: bool
    anomaly_probability: float
    forecast_timestamp: float


@dataclass
class MetricTimeSeries:
    """Time series data for a specific metric"""
    metric_name: str
    values: deque
    timestamps: deque
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if not isinstance(self.values, deque):
            self.values = deque(self.values, maxlen=1000)
        if not isinstance(self.timestamps, deque):
            self.timestamps = deque(self.timestamps, maxlen=1000)


class AdvancedTimeSeries:
    """🕐 Advanced time series analysis and forecasting"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.series_data = {}  # metric_name -> MetricTimeSeries
        self.models = {}       # metric_name -> PredictiveModel
        self.forecast_cache = {}
        
        print("📊 Advanced Time Series Analytics initialized")
    
    def add_data_point(self, metric_name: str, value: float, timestamp: float = None, metadata: Dict[str, Any] = None):
        """Add a new data point to time series"""
        if timestamp is None:
            timestamp = time.time()
        
        if metric_name not in self.series_data:
            self.series_data[metric_name] = MetricTimeSeries(
                metric_name=metric_name,
                values=deque(maxlen=self.max_history),
                timestamps=deque(maxlen=self.max_history),
                metadata=metadata or {}
            )
        
        series = self.series_data[metric_name]
        series.values.append(value)
        series.timestamps.append(timestamp)
        
        # Update metadata
        if metadata:
            series.metadata.update(metadata)
    
    def fit_linear_trend(self, values: List[float]) -> Tuple[float, float, float]:
        """Fit linear trend and return slope, intercept, and R²"""
        if len(values) < 2:
            return 0.0, values[0] if values else 0.0, 0.0
        
        n = len(values)
        x = np.arange(n)
        y = np.array(values)
        
        # Linear regression
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        if denominator == 0:
            return 0.0, y_mean, 0.0
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # R² calculation
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        return slope, intercept, r_squared
    
    def detect_seasonality(self, values: List[float], period: int = 24) -> Tuple[bool, float]:
        """Detect seasonal patterns in time series"""
        if len(values) < period * 2:
            return False, 0.0
        
        # Simple autocorrelation at seasonal lag
        n = len(values)
        values_array = np.array(values)
        
        # Calculate autocorrelation at seasonal lag
        mean_val = np.mean(values_array)
        
        # Autocorrelation calculation
        numerator = 0.0
        denominator = 0.0
        
        for i in range(n - period):
            numerator += (values_array[i] - mean_val) * (values_array[i + period] - mean_val)
        
        for i in range(n):
            denominator += (values_array[i] - mean_val) ** 2
        
        if denominator == 0:
            return False, 0.0
        
        autocorr = numerator / denominator
        
        # Consider seasonal if autocorrelation > 0.3
        is_seasonal = autocorr > 0.3
        
        return is_seasonal, autocorr
    
    def exponential_smoothing(self, values: List[float], alpha: float = 0.3, horizon: int = 5) -> List[float]:
        """Simple exponential smoothing forecast"""
        if not values:
            return [0.0] * horizon
        
        # Initialize with first value
        smoothed = [values[0]]
        
        # Calculate smoothed values
        for i in range(1, len(values)):
            smoothed_val = alpha * values[i] + (1 - alpha) * smoothed[-1]
            smoothed.append(smoothed_val)
        
        # Forecast future values
        forecast = []
        last_smoothed = smoothed[-1]
        
        for _ in range(horizon):
            forecast.append(last_smoothed)
        
        return forecast
    
    def polynomial_forecast(self, values: List[float], degree: int = 2, horizon: int = 5) -> List[float]:
        """Polynomial trend extrapolation"""
        if len(values) < degree + 1:
            # Fallback to linear or constant
            if len(values) >= 2:
                return self.linear_forecast(values, horizon)
            else:
                return [values[0] if values else 0.0] * horizon
        
        n = len(values)
        x = np.arange(n)
        y = np.array(values)
        
        # Fit polynomial
        try:
            coeffs = np.polyfit(x, y, degree)
            
            # Generate forecasts
            future_x = np.arange(n, n + horizon)
            forecast = np.polyval(coeffs, future_x)
            
            return forecast.tolist()
            
        except Exception:
            # Fallback to exponential smoothing
            return self.exponential_smoothing(values, horizon=horizon)
    
    def linear_forecast(self, values: List[float], horizon: int = 5) -> List[float]:
        """Linear trend extrapolation"""
        slope, intercept, _ = self.fit_linear_trend(values)
        
        n = len(values)
        future_x = np.arange(n, n + horizon)
        forecast = slope * future_x + intercept
        
        return forecast.tolist()
    
    def adaptive_forecast(self, values: List[float], horizon: int = 5) -> Tuple[List[float], str]:
        """Adaptive forecasting that selects best model"""
        if len(values) < 10:
            forecast = self.exponential_smoothing(values, horizon=horizon)
            return forecast, 'exponential'
        
        # Try different models and select best
        models_to_try = [
            ('linear', lambda: self.linear_forecast(values, horizon)),
            ('polynomial', lambda: self.polynomial_forecast(values, 2, horizon)),
            ('exponential', lambda: self.exponential_smoothing(values, horizon=horizon))
        ]
        
        best_model = 'exponential'
        best_forecast = []
        best_score = float('inf')
        
        # Use last 20% of data for validation
        if len(values) >= 20:
            split_idx = int(len(values) * 0.8)
            train_data = values[:split_idx]
            test_data = values[split_idx:]
            
            for model_name, forecast_func in models_to_try:
                try:
                    if model_name == 'linear':
                        model_forecast = self.linear_forecast(train_data, len(test_data))
                    elif model_name == 'polynomial':
                        model_forecast = self.polynomial_forecast(train_data, 2, len(test_data))
                    else:
                        model_forecast = self.exponential_smoothing(train_data, horizon=len(test_data))
                    
                    # Calculate RMSE
                    if len(model_forecast) == len(test_data):
                        rmse = math.sqrt(np.mean([(pred - actual) ** 2 for pred, actual in zip(model_forecast, test_data)]))
                        
                        if rmse < best_score:
                            best_score = rmse
                            best_model = model_name
                            best_forecast = forecast_func()
                            
                except Exception:
                    continue
        
        # If no model was selected, use exponential smoothing
        if not best_forecast:
            best_forecast = self.exponential_smoothing(values, horizon=horizon)
            best_model = 'exponential'
        
        return best_forecast, best_model
    
    def calculate_confidence_intervals(self, values: List[float], forecast: List[float], confidence: float = 0.95) -> List[Tuple[float, float]]:
        """Calculate confidence intervals for forecast"""
        if len(values) < 5:
            # Wide intervals for limited data
            intervals = [(val * 0.8, val * 1.2) for val in forecast]
            return intervals
        
        # Calculate residuals from recent history
        n = len(values)
        recent_values = values[-min(20, n):]  # Use recent 20 points or all available
        
        # Simple moving average as baseline
        if len(recent_values) >= 3:
            baseline = sum(recent_values) / len(recent_values)
            residuals = [val - baseline for val in recent_values]
            std_error = statistics.stdev(residuals) if len(residuals) > 1 else abs(baseline * 0.1)
        else:
            std_error = abs(statistics.mean(recent_values) * 0.15) if recent_values else 1.0
        
        # Z-score for confidence level
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z_score = z_scores.get(confidence, 1.96)
        
        # Calculate intervals
        margin = z_score * std_error
        intervals = [(val - margin, val + margin) for val in forecast]
        
        return intervals


class PredictiveAnalyticsEngine(QObject):
    """🎯 Advanced predictive analytics engine"""
    
    # Signals for predictive analytics events
    forecast_generated = pyqtSignal(dict)
    model_updated = pyqtSignal(dict)
    anomaly_detected = pyqtSignal(dict)
    trend_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Time series manager
        self.time_series = AdvancedTimeSeries(max_history=1000)
        
        # Predictive models configuration
        self.models_config = {
            'cpu_usage': PredictiveModel('adaptive', lookback_window=50, forecast_horizon=10),
            'memory_usage': PredictiveModel('adaptive', lookback_window=40, forecast_horizon=8),
            'response_time': PredictiveModel('adaptive', lookback_window=30, forecast_horizon=6),
            'throughput': PredictiveModel('polynomial', lookback_window=60, forecast_horizon=12),
            'error_rate': PredictiveModel('exponential', lookback_window=20, forecast_horizon=5),
            'user_activity': PredictiveModel('adaptive', lookback_window=100, forecast_horizon=15)
        }
        
        # Analytics state
        self.forecasts = {}
        self.trend_analysis = {}
        self.anomaly_thresholds = {}
        self.last_forecasts = {}
        
        # Auto-forecast timer
        self.forecast_timer = QTimer()
        self.forecast_timer.timeout.connect(self._auto_forecast_cycle)
        self.forecast_interval = 30000  # 30 seconds
        
        print("🎯 Predictive Analytics Engine initialized")
    
    def start_predictive_analytics(self):
        """Start automatic predictive analytics"""
        self.forecast_timer.start(self.forecast_interval)
        print("🎯 Predictive analytics started")
    
    def stop_predictive_analytics(self):
        """Stop automatic predictive analytics"""
        self.forecast_timer.stop()
        print("🎯 Predictive analytics stopped")
    
    def add_metric_data(self, metric_name: str, value: float, timestamp: float = None, metadata: Dict[str, Any] = None):
        """Add metric data point for analysis"""
        self.time_series.add_data_point(metric_name, value, timestamp, metadata)
        
        # Update anomaly thresholds
        self._update_anomaly_thresholds(metric_name)
        
        # Check for anomalies
        self._check_anomaly(metric_name, value)
    
    def generate_forecast(self, metric_name: str, horizon: int = None) -> Optional[ForecastResult]:
        """Generate forecast for a specific metric"""
        if metric_name not in self.time_series.series_data:
            return None
        
        series = self.time_series.series_data[metric_name]
        if len(series.values) < 5:
            return None
        
        try:
            # Get model configuration
            model_config = self.models_config.get(metric_name, PredictiveModel('adaptive'))
            if horizon is None:
                horizon = model_config.forecast_horizon
            
            values = list(series.values)
            timestamps = list(series.timestamps)
            
            # Generate forecast based on model type
            if model_config.model_type == 'adaptive':
                predicted_values, model_used = self.time_series.adaptive_forecast(values, horizon)
            elif model_config.model_type == 'linear':
                predicted_values = self.time_series.linear_forecast(values, horizon)
                model_used = 'linear'
            elif model_config.model_type == 'polynomial':
                predicted_values = self.time_series.polynomial_forecast(values, 2, horizon)
                model_used = 'polynomial'
            elif model_config.model_type == 'exponential':
                predicted_values = self.time_series.exponential_smoothing(values, horizon=horizon)
                model_used = 'exponential'
            else:
                predicted_values, model_used = self.time_series.adaptive_forecast(values, horizon)
            
            # Calculate confidence intervals
            confidence_intervals = self.time_series.calculate_confidence_intervals(
                values, predicted_values, model_config.confidence_level
            )
            
            # Generate future timestamps
            if len(timestamps) >= 2:
                time_interval = (timestamps[-1] - timestamps[-2])
                future_timestamps = [timestamps[-1] + (i + 1) * time_interval for i in range(horizon)]
            else:
                future_timestamps = [time.time() + i * 60 for i in range(horizon)]  # 1-minute intervals
            
            # Analyze trends
            slope, _, r_squared = self.time_series.fit_linear_trend(values[-20:])  # Recent trend
            if slope > 0.01:
                trend_direction = 'increasing'
            elif slope < -0.01:
                trend_direction = 'decreasing'
            else:
                trend_direction = 'stable'
            
            # Detect seasonality
            is_seasonal, seasonal_strength = self.time_series.detect_seasonality(values)
            
            # Calculate anomaly probability
            recent_values = values[-5:]
            if recent_values:
                mean_recent = statistics.mean(recent_values)
                overall_mean = statistics.mean(values)
                deviation = abs(mean_recent - overall_mean) / (statistics.stdev(values) + 1e-8)
                anomaly_probability = min(deviation / 3.0, 1.0)  # Normalize to 0-1
            else:
                anomaly_probability = 0.0
            
            # Create forecast result
            forecast_result = ForecastResult(
                forecast_id=f"{metric_name}_{int(time.time())}",
                metric_name=metric_name,
                predicted_values=predicted_values,
                confidence_intervals=confidence_intervals,
                timestamps=future_timestamps,
                model_type=model_used,
                accuracy_score=r_squared,
                trend_direction=trend_direction,
                seasonal_pattern=is_seasonal,
                anomaly_probability=anomaly_probability,
                forecast_timestamp=time.time()
            )
            
            # Cache forecast
            self.forecasts[metric_name] = forecast_result
            self.last_forecasts[metric_name] = time.time()
            
            # Emit signal
            self.forecast_generated.emit(asdict(forecast_result))
            
            return forecast_result
            
        except Exception as e:
            print(f"❌ Forecast generation error ({metric_name}): {e}")
            return None
    
    def _auto_forecast_cycle(self):
        """Automatic forecasting cycle for all metrics"""
        try:
            for metric_name in self.time_series.series_data:
                # Check if forecast is needed (every 5 minutes or if no forecast exists)
                last_forecast = self.last_forecasts.get(metric_name, 0)
                if time.time() - last_forecast > 300:  # 5 minutes
                    self.generate_forecast(metric_name)
                    
        except Exception as e:
            print(f"❌ Auto-forecast cycle error: {e}")
    
    def _update_anomaly_thresholds(self, metric_name: str):
        """Update anomaly detection thresholds for a metric"""
        if metric_name not in self.time_series.series_data:
            return
        
        series = self.time_series.series_data[metric_name]
        values = list(series.values)
        
        if len(values) >= 10:
            mean_val = statistics.mean(values)
            std_val = statistics.stdev(values) if len(values) > 1 else abs(mean_val * 0.1)
            
            # Set thresholds at 2 and 3 standard deviations
            self.anomaly_thresholds[metric_name] = {
                'warning_lower': mean_val - 2 * std_val,
                'warning_upper': mean_val + 2 * std_val,
                'critical_lower': mean_val - 3 * std_val,
                'critical_upper': mean_val + 3 * std_val,
                'baseline': mean_val
            }
    
    def _check_anomaly(self, metric_name: str, value: float):
        """Check if a value is anomalous"""
        if metric_name not in self.anomaly_thresholds:
            return
        
        thresholds = self.anomaly_thresholds[metric_name]
        anomaly_info = None
        
        if value < thresholds['critical_lower'] or value > thresholds['critical_upper']:
            anomaly_info = {
                'metric': metric_name,
                'value': value,
                'severity': 'critical',
                'threshold_violated': 'critical',
                'baseline': thresholds['baseline'],
                'timestamp': time.time()
            }
        elif value < thresholds['warning_lower'] or value > thresholds['warning_upper']:
            anomaly_info = {
                'metric': metric_name,
                'value': value,
                'severity': 'warning',
                'threshold_violated': 'warning',
                'baseline': thresholds['baseline'],
                'timestamp': time.time()
            }
        
        if anomaly_info:
            self.anomaly_detected.emit(anomaly_info)
    
    def get_trend_analysis(self, metric_name: str, period_hours: int = 24) -> Dict[str, Any]:
        """Get comprehensive trend analysis for a metric"""
        if metric_name not in self.time_series.series_data:
            return {}
        
        series = self.time_series.series_data[metric_name]
        values = list(series.values)
        timestamps = list(series.timestamps)
        
        if len(values) < 5:
            return {}
        
        # Recent period analysis
        current_time = time.time()
        period_seconds = period_hours * 3600
        cutoff_time = current_time - period_seconds
        
        # Filter recent data
        recent_data = [(v, t) for v, t in zip(values, timestamps) if t >= cutoff_time]
        
        if not recent_data:
            recent_data = list(zip(values[-10:], timestamps[-10:]))  # Last 10 points as fallback
        
        recent_values = [v for v, t in recent_data]
        
        # Trend analysis
        slope, intercept, r_squared = self.time_series.fit_linear_trend(recent_values)
        
        # Volatility analysis
        volatility = statistics.stdev(recent_values) if len(recent_values) > 1 else 0.0
        
        # Seasonal analysis
        is_seasonal, seasonal_strength = self.time_series.detect_seasonality(values)
        
        # Performance change
        if len(recent_values) >= 5:
            first_half = recent_values[:len(recent_values)//2]
            second_half = recent_values[len(recent_values)//2:]
            
            first_mean = statistics.mean(first_half)
            second_mean = statistics.mean(second_half)
            
            if first_mean != 0:
                performance_change = ((second_mean - first_mean) / first_mean) * 100
            else:
                performance_change = 0.0
        else:
            performance_change = 0.0
        
        return {
            'metric_name': metric_name,
            'period_hours': period_hours,
            'trend_slope': slope,
            'trend_strength': r_squared,
            'trend_direction': 'increasing' if slope > 0.01 else 'decreasing' if slope < -0.01 else 'stable',
            'volatility': volatility,
            'seasonal_pattern': is_seasonal,
            'seasonal_strength': seasonal_strength,
            'performance_change_percent': performance_change,
            'data_points': len(recent_values),
            'analysis_timestamp': time.time()
        }
    
    def get_predictive_insights(self) -> Dict[str, Any]:
        """Get comprehensive predictive analytics insights"""
        insights = {
            'active_metrics': list(self.time_series.series_data.keys()),
            'forecasts_generated': len(self.forecasts),
            'models_configured': len(self.models_config),
            'anomaly_thresholds': len(self.anomaly_thresholds),
            'auto_forecasting': self.forecast_timer.isActive(),
            'recent_forecasts': {},
            'trend_summaries': {}
        }
        
        # Recent forecasts summary
        for metric_name, forecast in self.forecasts.items():
            insights['recent_forecasts'][metric_name] = {
                'model_type': forecast.model_type,
                'accuracy_score': forecast.accuracy_score,
                'trend_direction': forecast.trend_direction,
                'forecast_horizon': len(forecast.predicted_values),
                'anomaly_probability': forecast.anomaly_probability,
                'age_minutes': (time.time() - forecast.forecast_timestamp) / 60
            }
        
        # Trend summaries
        for metric_name in self.time_series.series_data:
            trend_analysis = self.get_trend_analysis(metric_name, 6)  # 6-hour analysis
            if trend_analysis:
                insights['trend_summaries'][metric_name] = {
                    'direction': trend_analysis['trend_direction'],
                    'strength': trend_analysis['trend_strength'],
                    'volatility': trend_analysis['volatility'],
                    'performance_change': trend_analysis['performance_change_percent']
                }
        
        return insights


# Global predictive analytics engine
global_predictive_engine = None

def get_predictive_analytics_engine(parent=None) -> PredictiveAnalyticsEngine:
    """Get or create global predictive analytics engine"""
    global global_predictive_engine
    
    if global_predictive_engine is None:
        global_predictive_engine = PredictiveAnalyticsEngine(parent)
    
    return global_predictive_engine


if __name__ == "__main__":
    # Test predictive analytics system
    print("🎯 Testing Predictive Analytics Engine")
    
    engine = get_predictive_analytics_engine()
    
    # Simulate time series data
    import random
    base_time = time.time()
    
    for i in range(100):
        # Simulate CPU usage with trend and noise
        cpu_value = 30 + i * 0.2 + random.uniform(-5, 5) + 10 * math.sin(i * 0.1)
        engine.add_metric_data('cpu_usage', cpu_value, base_time + i * 60)
        
        # Simulate memory usage
        memory_value = 40 + i * 0.1 + random.uniform(-3, 3)
        engine.add_metric_data('memory_usage', memory_value, base_time + i * 60)
    
    # Generate forecasts
    cpu_forecast = engine.generate_forecast('cpu_usage', horizon=5)
    memory_forecast = engine.generate_forecast('memory_usage', horizon=5)
    
    if cpu_forecast:
        print(f"✅ CPU forecast: {cpu_forecast.trend_direction} trend, {cpu_forecast.model_type} model")
    
    if memory_forecast:
        print(f"✅ Memory forecast: {memory_forecast.trend_direction} trend, {memory_forecast.model_type} model")
    
    # Get insights
    insights = engine.get_predictive_insights()
    print(f"✅ Predictive insights: {len(insights['active_metrics'])} metrics analyzed")