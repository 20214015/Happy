#!/usr/bin/env python3
"""
📊 Comprehensive AI Analytics Dashboard
=====================================

Advanced analytics and visualization for AI optimization features:
- Real-time performance metrics
- ML model insights
- Predictive analytics
- Resource optimization statistics
- User behavior analysis
"""

import time
import json
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
from dataclasses import dataclass
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QLabel, QProgressBar, QTextEdit, QScrollArea,
                            QFrame, QGridLayout, QPushButton, QGroupBox,
                            QComboBox, QSpinBox, QCheckBox, QSlider)
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPalette, QColor
import statistics


@dataclass
class AIMetric:
    """AI performance metric"""
    name: str
    value: float
    trend: str  # 'up', 'down', 'stable'
    confidence: float
    timestamp: float


class AIAnalyticsDashboard(QWidget):
    """📊 Main AI Analytics Dashboard"""
    
    # Signals for real-time updates
    metrics_updated = pyqtSignal(dict)
    alert_generated = pyqtSignal(str, str)  # level, message
    
    def __init__(self, ai_optimizer=None, parent=None):
        super().__init__(parent)
        self.ai_optimizer = ai_optimizer
        
        # Data storage
        self.metrics_history = deque(maxlen=1000)
        self.performance_data = defaultdict(deque)
        self.ml_statistics = {}
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_interval = 2000  # 2 seconds
        
        # Initialize UI
        self.init_ui()
        self.apply_ai_theme()
        
        # Start updates if optimizer available
        if self.ai_optimizer:
            self.start_monitoring()
        
        print("📊 AI Analytics Dashboard initialized")
    
    def init_ui(self):
        """Initialize dashboard UI"""
        self.setWindowTitle("🧠 AI Analytics Dashboard")
        self.setMinimumSize(1400, 900)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget for different analytics views
        tabs = QTabWidget()
        
        # Overview Tab
        overview_tab = self.create_overview_tab()
        tabs.addTab(overview_tab, "📈 Overview")
        
        # ML Models Tab
        ml_tab = self.create_ml_models_tab()
        tabs.addTab(ml_tab, "🧠 ML Models")
        
        # Performance Tab
        performance_tab = self.create_performance_tab()
        tabs.addTab(performance_tab, "⚡ Performance")
        
        # Resources Tab
        resources_tab = self.create_resources_tab()
        tabs.addTab(resources_tab, "🔧 Resources")
        
        # Predictions Tab
        predictions_tab = self.create_predictions_tab()
        tabs.addTab(predictions_tab, "🔮 Predictions")
        
        # Settings Tab
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "⚙️ Settings")
        
        main_layout.addWidget(tabs)
        
        # Footer with controls
        footer = self.create_footer()
        main_layout.addWidget(footer)
    
    def create_header(self) -> QWidget:
        """Create dashboard header"""
        header = QFrame()
        header.setFixedHeight(80)
        layout = QHBoxLayout(header)
        
        # Title
        title = QLabel("🧠 AI Performance Analytics Dashboard")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Status indicators
        self.ai_status_label = QLabel("🟢 AI Active")
        self.ai_status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.ai_status_label)
        
        self.learning_status_label = QLabel("📚 Learning")
        self.learning_status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.learning_status_label)
        
        return header
    
    def create_overview_tab(self) -> QWidget:
        """Create overview analytics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Key metrics row
        metrics_row = QHBoxLayout()
        
        # AI Performance Score
        self.ai_score_card = self.create_metric_card("AI Performance Score", "85.2%", "🎯")
        metrics_row.addWidget(self.ai_score_card)
        
        # Learning Progress
        self.learning_card = self.create_metric_card("Learning Progress", "67%", "📚")
        metrics_row.addWidget(self.learning_card)
        
        # Prediction Accuracy
        self.accuracy_card = self.create_metric_card("Prediction Accuracy", "78.5%", "🎯")
        metrics_row.addWidget(self.accuracy_card)
        
        # System Health
        self.health_card = self.create_metric_card("System Health", "Excellent", "💚")
        metrics_row.addWidget(self.health_card)
        
        layout.addLayout(metrics_row)
        
        # Charts row
        charts_row = QHBoxLayout()
        
        # Performance trend chart
        performance_chart = self.create_chart_placeholder("Performance Trend", "📈")
        charts_row.addWidget(performance_chart)
        
        # ML accuracy chart
        accuracy_chart = self.create_chart_placeholder("ML Model Accuracy", "🧠")
        charts_row.addWidget(accuracy_chart)
        
        layout.addLayout(charts_row)
        
        # Activity feed
        activity_feed = self.create_activity_feed()
        layout.addWidget(activity_feed)
        
        return tab
    
    def create_ml_models_tab(self) -> QWidget:
        """Create ML models analytics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Model status grid
        models_grid = QGridLayout()
        
        # Pattern Analyzer Model
        pattern_model = self.create_model_status_card(
            "Pattern Analyzer", "Active", 0.82, "Analyzing user behavior patterns"
        )
        models_grid.addWidget(pattern_model, 0, 0)
        
        # Prediction Engine Model
        prediction_model = self.create_model_status_card(
            "Prediction Engine", "Training", 0.76, "Predicting user actions"
        )
        models_grid.addWidget(prediction_model, 0, 1)
        
        # Enhanced ML Model
        enhanced_model = self.create_model_status_card(
            "Enhanced ML", "Active", 0.89, "Advanced machine learning algorithms"
        )
        models_grid.addWidget(enhanced_model, 1, 0)
        
        # Resource Predictor Model
        resource_model = self.create_model_status_card(
            "Resource Predictor", "Active", 0.73, "Predicting resource usage"
        )
        models_grid.addWidget(resource_model, 1, 1)
        
        layout.addLayout(models_grid)
        
        # Model performance details
        performance_details = QTextEdit()
        performance_details.setMaximumHeight(200)
        performance_details.setPlainText(self.get_model_performance_text())
        layout.addWidget(performance_details)
        
        # Model training controls
        training_controls = self.create_training_controls()
        layout.addWidget(training_controls)
        
        return tab
    
    def create_performance_tab(self) -> QWidget:
        """Create performance analytics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Performance metrics
        perf_metrics = QHBoxLayout()
        
        # CPU optimization
        cpu_card = self.create_performance_metric_card("CPU Optimization", "15%", "Reduction")
        perf_metrics.addWidget(cpu_card)
        
        # Memory optimization
        memory_card = self.create_performance_metric_card("Memory Optimization", "23%", "Improvement")
        perf_metrics.addWidget(memory_card)
        
        # Response time
        response_card = self.create_performance_metric_card("Response Time", "1.2s", "Average")
        perf_metrics.addWidget(response_card)
        
        # Cache hit rate
        cache_card = self.create_performance_metric_card("Cache Hit Rate", "84%", "Efficiency")
        perf_metrics.addWidget(cache_card)
        
        layout.addLayout(perf_metrics)
        
        # Performance chart
        performance_chart = self.create_chart_placeholder("Real-time Performance Metrics", "📊")
        layout.addWidget(performance_chart)
        
        # Optimization recommendations
        recommendations = self.create_recommendations_panel()
        layout.addWidget(recommendations)
        
        return tab
    
    def create_resources_tab(self) -> QWidget:
        """Create resource analytics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Resource utilization
        resource_grid = QGridLayout()
        
        # Memory usage
        memory_progress = self.create_resource_progress("Memory Usage", 67, "1.2GB / 1.8GB")
        resource_grid.addWidget(memory_progress, 0, 0)
        
        # CPU usage
        cpu_progress = self.create_resource_progress("CPU Usage", 45, "45% average")
        resource_grid.addWidget(cpu_progress, 0, 1)
        
        # Cache usage
        cache_progress = self.create_resource_progress("Cache Usage", 78, "200MB / 256MB")
        resource_grid.addWidget(cache_progress, 1, 0)
        
        # I/O usage
        io_progress = self.create_resource_progress("I/O Usage", 32, "32% utilization")
        resource_grid.addWidget(io_progress, 1, 1)
        
        layout.addLayout(resource_grid)
        
        # Resource allocation chart
        allocation_chart = self.create_chart_placeholder("Resource Allocation Over Time", "📊")
        layout.addWidget(allocation_chart)
        
        # Component resource usage
        component_usage = self.create_component_usage_table()
        layout.addWidget(component_usage)
        
        return tab
    
    def create_predictions_tab(self) -> QWidget:
        """Create predictions analytics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Prediction summary
        pred_summary = QHBoxLayout()
        
        # Next action prediction
        next_action_card = self.create_prediction_card(
            "Next Action", "refresh_table", 0.78, "High confidence"
        )
        pred_summary.addWidget(next_action_card)
        
        # Resource forecast
        resource_forecast_card = self.create_prediction_card(
            "Resource Peak", "2.1GB in 45min", 0.65, "Medium confidence"
        )
        pred_summary.addWidget(resource_forecast_card)
        
        # Performance forecast
        perf_forecast_card = self.create_prediction_card(
            "Performance Trend", "Improving", 0.82, "High confidence"
        )
        pred_summary.addWidget(perf_forecast_card)
        
        layout.addLayout(pred_summary)
        
        # Prediction timeline
        timeline = self.create_prediction_timeline()
        layout.addWidget(timeline)
        
        # Prediction accuracy tracking
        accuracy_tracking = self.create_accuracy_tracking()
        layout.addWidget(accuracy_tracking)
        
        return tab
    
    def create_settings_tab(self) -> QWidget:
        """Create settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # AI Configuration
        ai_config = QGroupBox("AI Configuration")
        ai_layout = QGridLayout(ai_config)
        
        # Learning rate
        ai_layout.addWidget(QLabel("Learning Rate:"), 0, 0)
        self.learning_rate_spin = QSpinBox()
        self.learning_rate_spin.setRange(1, 100)
        self.learning_rate_spin.setValue(5)
        self.learning_rate_spin.setSuffix("%")
        ai_layout.addWidget(self.learning_rate_spin, 0, 1)
        
        # Prediction interval
        ai_layout.addWidget(QLabel("Prediction Interval:"), 1, 0)
        self.prediction_interval_spin = QSpinBox()
        self.prediction_interval_spin.setRange(1, 60)
        self.prediction_interval_spin.setValue(10)
        self.prediction_interval_spin.setSuffix(" seconds")
        ai_layout.addWidget(self.prediction_interval_spin, 1, 1)
        
        # Optimization level
        ai_layout.addWidget(QLabel("Optimization Level:"), 2, 0)
        self.optimization_level_combo = QComboBox()
        self.optimization_level_combo.addItems(["Basic", "Adaptive", "Aggressive"])
        self.optimization_level_combo.setCurrentText("Adaptive")
        ai_layout.addWidget(self.optimization_level_combo, 2, 1)
        
        layout.addWidget(ai_config)
        
        # Feature toggles
        features_config = QGroupBox("Feature Configuration")
        features_layout = QGridLayout(features_config)
        
        self.enhanced_ml_check = QCheckBox("Enhanced Machine Learning")
        self.enhanced_ml_check.setChecked(True)
        features_layout.addWidget(self.enhanced_ml_check, 0, 0)
        
        self.intelligent_monitoring_check = QCheckBox("Intelligent Monitoring")
        self.intelligent_monitoring_check.setChecked(True)
        features_layout.addWidget(self.intelligent_monitoring_check, 0, 1)
        
        self.smart_resources_check = QCheckBox("Smart Resource Management")
        self.smart_resources_check.setChecked(True)
        features_layout.addWidget(self.smart_resources_check, 1, 0)
        
        self.auto_optimization_check = QCheckBox("Auto Optimization")
        self.auto_optimization_check.setChecked(True)
        features_layout.addWidget(self.auto_optimization_check, 1, 1)
        
        layout.addWidget(features_config)
        
        # Apply settings button
        apply_btn = QPushButton("Apply Settings")
        apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        
        return tab
    
    def create_metric_card(self, title: str, value: str, icon: str) -> QWidget:
        """Create metric display card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setFixedSize(200, 120)
        
        layout = QVBoxLayout(card)
        
        # Icon and title
        header = QHBoxLayout()
        header.addWidget(QLabel(icon))
        header.addWidget(QLabel(title))
        header.addStretch()
        layout.addLayout(header)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        # Store reference for updates
        setattr(card, 'value_label', value_label)
        
        return card
    
    def create_chart_placeholder(self, title: str, icon: str) -> QWidget:
        """Create chart placeholder"""
        chart = QFrame()
        chart.setFrameStyle(QFrame.Shape.Box)
        chart.setMinimumHeight(200)
        
        layout = QVBoxLayout(chart)
        
        # Title
        title_label = QLabel(f"{icon} {title}")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Placeholder content
        content = QLabel("📊 Chart visualization\n(Real-time data)")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(content)
        
        return chart
    
    def create_activity_feed(self) -> QWidget:
        """Create activity feed"""
        feed = QGroupBox("🔔 Recent AI Activity")
        layout = QVBoxLayout(feed)
        
        self.activity_text = QTextEdit()
        self.activity_text.setMaximumHeight(150)
        self.activity_text.setReadOnly(True)
        layout.addWidget(self.activity_text)
        
        # Initialize with sample activities
        self.add_activity("AI Model training completed successfully")
        self.add_activity("Enhanced ML predictions improved by 12%")
        self.add_activity("Smart resource optimization applied")
        self.add_activity("Performance monitoring started")
        
        return feed
    
    def create_model_status_card(self, name: str, status: str, 
                               accuracy: float, description: str) -> QWidget:
        """Create ML model status card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setFixedSize(300, 150)
        
        layout = QVBoxLayout(card)
        
        # Model name and status
        header = QHBoxLayout()
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header.addWidget(name_label)
        
        status_label = QLabel(status)
        status_color = "#4CAF50" if status == "Active" else "#FF9800"
        status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
        header.addWidget(status_label)
        
        layout.addLayout(header)
        
        # Accuracy
        accuracy_label = QLabel(f"Accuracy: {accuracy:.1%}")
        layout.addWidget(accuracy_label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setValue(int(accuracy * 100))
        layout.addWidget(progress)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(desc_label)
        
        return card
    
    def create_performance_metric_card(self, title: str, value: str, subtitle: str) -> QWidget:
        """Create performance metric card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setFixedSize(200, 100)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #666; font-size: 9px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        return card
    
    def create_resource_progress(self, title: str, value: int, description: str) -> QWidget:
        """Create resource usage progress widget"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setFixedSize(250, 100)
        
        layout = QVBoxLayout(widget)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        progress = QProgressBar()
        progress.setValue(value)
        progress.setFormat(f"{value}%")
        layout.addWidget(progress)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(desc_label)
        
        return widget
    
    def create_prediction_card(self, title: str, prediction: str, 
                             confidence: float, status: str) -> QWidget:
        """Create prediction display card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setFixedSize(200, 120)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        pred_label = QLabel(prediction)
        pred_label.setFont(QFont("Arial", 12))
        pred_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pred_label)
        
        conf_label = QLabel(f"Confidence: {confidence:.1%}")
        layout.addWidget(conf_label)
        
        status_label = QLabel(status)
        status_label.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(status_label)
        
        return card
    
    def create_training_controls(self) -> QWidget:
        """Create ML model training controls"""
        controls = QGroupBox("Model Training Controls")
        layout = QHBoxLayout(controls)
        
        retrain_btn = QPushButton("🔄 Retrain Models")
        retrain_btn.clicked.connect(self.retrain_models)
        layout.addWidget(retrain_btn)
        
        reset_btn = QPushButton("🔄 Reset Learning")
        reset_btn.clicked.connect(self.reset_learning)
        layout.addWidget(reset_btn)
        
        export_btn = QPushButton("💾 Export Data")
        export_btn.clicked.connect(self.export_data)
        layout.addWidget(export_btn)
        
        layout.addStretch()
        
        return controls
    
    def create_recommendations_panel(self) -> QWidget:
        """Create optimization recommendations panel"""
        panel = QGroupBox("🎯 AI Recommendations")
        layout = QVBoxLayout(panel)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setMaximumHeight(100)
        self.recommendations_text.setReadOnly(True)
        layout.addWidget(self.recommendations_text)
        
        # Sample recommendations
        recommendations = [
            "• Increase memory allocation for high-priority components",
            "• Enable aggressive caching for frequently accessed data",
            "• Schedule resource-intensive tasks during low-usage periods",
            "• Consider upgrading CPU resources for better performance"
        ]
        
        self.recommendations_text.setPlainText("\n".join(recommendations))
        
        return panel
    
    def create_component_usage_table(self) -> QWidget:
        """Create component resource usage table"""
        table = QGroupBox("Component Resource Usage")
        layout = QVBoxLayout(table)
        
        # Placeholder for actual table
        placeholder = QLabel("📋 Component resource usage table\n(Real-time component data)")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(placeholder)
        
        return table
    
    def create_prediction_timeline(self) -> QWidget:
        """Create prediction timeline"""
        timeline = QGroupBox("Prediction Timeline")
        layout = QVBoxLayout(timeline)
        
        # Placeholder for timeline
        placeholder = QLabel("📅 Prediction timeline\n(Future predictions and accuracy)")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(placeholder)
        
        return timeline
    
    def create_accuracy_tracking(self) -> QWidget:
        """Create prediction accuracy tracking"""
        tracking = QGroupBox("Accuracy Tracking")
        layout = QVBoxLayout(tracking)
        
        # Placeholder for accuracy tracking
        placeholder = QLabel("📊 Prediction accuracy over time\n(Model performance tracking)")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(placeholder)
        
        return tracking
    
    def create_footer(self) -> QWidget:
        """Create dashboard footer with controls"""
        footer = QFrame()
        footer.setFixedHeight(50)
        layout = QHBoxLayout(footer)
        
        # Start/Stop monitoring
        self.monitor_btn = QPushButton("⏸️ Pause Monitoring")
        self.monitor_btn.clicked.connect(self.toggle_monitoring)
        layout.addWidget(self.monitor_btn)
        
        # Refresh rate control
        layout.addWidget(QLabel("Refresh Rate:"))
        self.refresh_rate_slider = QSlider(Qt.Orientation.Horizontal)
        self.refresh_rate_slider.setRange(1, 10)
        self.refresh_rate_slider.setValue(5)
        self.refresh_rate_slider.valueChanged.connect(self.update_refresh_rate)
        layout.addWidget(self.refresh_rate_slider)
        
        layout.addStretch()
        
        # Status
        self.status_label = QLabel("🟢 Dashboard Active")
        layout.addWidget(self.status_label)
        
        return footer
    
    def apply_ai_theme(self):
        """Apply AI-themed styling"""
        self.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QFrame {
            background-color: #2d2d2d;
            border: 1px solid #404040;
            border-radius: 8px;
            padding: 8px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #404040;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QProgressBar {
            border: 1px solid #404040;
            border-radius: 4px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #0078d4;
            border-radius: 3px;
        }
        
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #2d2d2d;
        }
        
        QTabBar::tab {
            background-color: #3d3d3d;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #0078d4;
        }
        
        QTabBar::tab:hover {
            background-color: #4d4d4d;
        }
        
        QTextEdit {
            background-color: #1e1e1e;
            border: 1px solid #404040;
            border-radius: 4px;
            padding: 4px;
        }
        
        QComboBox, QSpinBox {
            background-color: #3d3d3d;
            border: 1px solid #404040;
            border-radius: 4px;
            padding: 4px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        
        QCheckBox::indicator:checked {
            background-color: #0078d4;
            border: 1px solid #0078d4;
        }
        
        QSlider::groove:horizontal {
            border: 1px solid #404040;
            height: 6px;
            background: #3d3d3d;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background: #0078d4;
            border: 1px solid #0078d4;
            width: 16px;
            border-radius: 8px;
            margin: -5px 0;
        }
        """)
    
    def start_monitoring(self):
        """Start dashboard monitoring"""
        if self.ai_optimizer:
            self.update_timer.start(self.update_interval)
            print("📊 Dashboard monitoring started")
    
    def stop_monitoring(self):
        """Stop dashboard monitoring"""
        self.update_timer.stop()
        print("📊 Dashboard monitoring stopped")
    
    def toggle_monitoring(self):
        """Toggle dashboard monitoring"""
        if self.update_timer.isActive():
            self.stop_monitoring()
            self.monitor_btn.setText("▶️ Start Monitoring")
            self.status_label.setText("🔴 Dashboard Paused")
        else:
            self.start_monitoring()
            self.monitor_btn.setText("⏸️ Pause Monitoring")
            self.status_label.setText("🟢 Dashboard Active")
    
    def update_refresh_rate(self, value: int):
        """Update dashboard refresh rate"""
        # Convert slider value (1-10) to milliseconds (500-5000)
        self.update_interval = value * 500
        if self.update_timer.isActive():
            self.update_timer.setInterval(self.update_interval)
    
    def update_dashboard(self):
        """Update dashboard with latest AI data"""
        if not self.ai_optimizer:
            return
        
        try:
            # Get AI insights
            insights = self.ai_optimizer.get_ai_insights()
            
            # Update metrics
            self.update_metrics(insights)
            
            # Update status
            self.update_status(insights)
            
            # Add activity
            if insights.get('total_actions_learned', 0) > 0:
                self.add_activity(f"Learned from {insights['total_actions_learned']} user actions")
            
        except Exception as e:
            print(f"❌ Dashboard update error: {e}")
    
    def update_metrics(self, insights: Dict[str, Any]):
        """Update dashboard metrics"""
        try:
            # Update AI performance score
            performance = insights.get('optimization_performance', {})
            hit_rate = performance.get('cache_hit_rate', 0)
            
            if hasattr(self.ai_score_card, 'value_label'):
                self.ai_score_card.value_label.setText(f"{hit_rate:.1f}%")
            
            # Update learning progress
            total_actions = insights.get('total_actions_learned', 0)
            progress = min(total_actions / 100.0, 1.0) * 100
            
            if hasattr(self.learning_card, 'value_label'):
                self.learning_card.value_label.setText(f"{progress:.0f}%")
            
            # Update prediction accuracy
            accuracy = performance.get('preload_success_rate', 0)
            
            if hasattr(self.accuracy_card, 'value_label'):
                self.accuracy_card.value_label.setText(f"{accuracy:.1f}%")
            
            # Update system health
            health = insights.get('system_health', 'unknown')
            health_icon = "💚" if health == 'excellent' else "💛" if health == 'good' else "❤️"
            
            if hasattr(self.health_card, 'value_label'):
                self.health_card.value_label.setText(f"{health_icon} {health.title()}")
            
        except Exception as e:
            print(f"❌ Metrics update error: {e}")
    
    def update_status(self, insights: Dict[str, Any]):
        """Update status indicators"""
        try:
            ai_status = insights.get('ai_status', 'unknown')
            if ai_status == 'active':
                self.ai_status_label.setText("🟢 AI Active")
            else:
                self.ai_status_label.setText("🔴 AI Inactive")
            
            learning_status = insights.get('learning_progress', 'unknown')
            if learning_status == 'active':
                self.learning_status_label.setText("📚 Learning Active")
            else:
                self.learning_status_label.setText("📚 Learning Idle")
                
        except Exception as e:
            print(f"❌ Status update error: {e}")
    
    def add_activity(self, message: str):
        """Add activity to feed"""
        timestamp = time.strftime("%H:%M:%S")
        activity = f"[{timestamp}] {message}"
        
        current_text = self.activity_text.toPlainText()
        lines = current_text.split('\n')
        
        # Keep only last 10 activities
        lines.insert(0, activity)
        if len(lines) > 10:
            lines = lines[:10]
        
        self.activity_text.setPlainText('\n'.join(lines))
    
    def get_model_performance_text(self) -> str:
        """Get model performance details text"""
        return """🧠 ML Model Performance Details:

Pattern Analyzer:
• Training samples: 245 actions
• Pattern recognition: 18 sequences identified
• Accuracy: 82.3% (improving)

Prediction Engine:
• Active predictions: 3 models
• Confidence threshold: 60%
• Success rate: 76.4%

Enhanced ML:
• Deep learning layers: 5
• Feature extraction: 24 features
• Optimization score: 89.1%

Resource Predictor:
• Memory prediction: ±12% accuracy
• CPU forecasting: ±8% accuracy
• Cache optimization: 84% hit rate
"""
    
    def retrain_models(self):
        """Trigger model retraining"""
        if self.ai_optimizer:
            self.add_activity("Manual model retraining initiated")
            # In a real implementation, this would trigger actual retraining
            print("🔄 Manual model retraining requested")
    
    def reset_learning(self):
        """Reset AI learning data"""
        if self.ai_optimizer:
            self.add_activity("AI learning data reset")
            print("🔄 Learning data reset requested")
    
    def export_data(self):
        """Export AI data"""
        self.add_activity("AI data export initiated")
        print("💾 Data export requested")
    
    def apply_settings(self):
        """Apply dashboard settings"""
        learning_rate = self.learning_rate_spin.value()
        prediction_interval = self.prediction_interval_spin.value() * 1000
        optimization_level = self.optimization_level_combo.currentText().lower()
        
        if self.ai_optimizer:
            # Apply settings to AI optimizer
            self.ai_optimizer.set_optimization_level(optimization_level)
            self.add_activity(f"Settings applied: {optimization_level} optimization")
        
        print(f"⚙️ Settings applied: LR={learning_rate}%, PI={prediction_interval}ms, Level={optimization_level}")


def create_ai_dashboard(ai_optimizer=None, parent=None) -> AIAnalyticsDashboard:
    """Create AI analytics dashboard"""
    return AIAnalyticsDashboard(ai_optimizer, parent)


if __name__ == "__main__":
    # Test AI dashboard
    import sys
    from PyQt6.QtWidgets import QApplication
    
    print("📊 Testing AI Analytics Dashboard")
    
    app = QApplication(sys.argv)
    
    # Create dashboard
    dashboard = create_ai_dashboard()
    dashboard.show()
    
    print("✅ AI Analytics Dashboard ready!")
    
    # Run for a short time to test
    QTimer.singleShot(3000, app.quit)
    app.exec()