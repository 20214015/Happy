"""
Startup Performance Report Generator
===================================

Generates comprehensive startup performance reports for MumuManager Pro.
Provides detailed analysis of component loading times and optimization opportunities.

Author: GitHub Copilot
Date: August 26, 2025
Version: 1.0 - Performance Enhancement
"""

import time
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class StartupPerformanceReporter:
    """Generates detailed startup performance reports"""
    
    def __init__(self):
        self.startup_metrics = {}
        self.session_start = time.time()
        self.component_timings = []
        self.optimization_recommendations = []
        
    def record_component_timing(self, component_name: str, load_time: float, category: str = "component"):
        """Record timing for a component load"""
        timing_data = {
            'component': component_name,
            'load_time': load_time,
            'category': category,
            'timestamp': time.time() - self.session_start
        }
        self.component_timings.append(timing_data)
        
        # Generate optimization recommendations
        if load_time > 0.050:  # > 50ms
            self.optimization_recommendations.append(
                f"⚠️ {component_name} took {load_time:.3f}s - Consider async loading"
            )
        elif load_time > 0.100:  # > 100ms
            self.optimization_recommendations.append(
                f"❌ {component_name} took {load_time:.3f}s - Needs optimization"
            )
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        total_startup_time = time.time() - self.session_start
        
        # Calculate statistics
        if self.component_timings:
            load_times = [t['load_time'] for t in self.component_timings]
            avg_load_time = sum(load_times) / len(load_times)
            max_load_time = max(load_times)
            total_component_time = sum(load_times)
        else:
            avg_load_time = max_load_time = total_component_time = 0
        
        # Performance grade
        if total_startup_time < 2.0:
            performance_grade = "A+ Excellent"
        elif total_startup_time < 3.0:
            performance_grade = "A Good"
        elif total_startup_time < 5.0:
            performance_grade = "B Fair"
        else:
            performance_grade = "C Needs Improvement"
        
        report = {
            'session_info': {
                'timestamp': datetime.now().isoformat(),
                'total_startup_time': round(total_startup_time, 3),
                'performance_grade': performance_grade
            },
            'component_statistics': {
                'total_components': len(self.component_timings),
                'total_component_time': round(total_component_time, 3),
                'average_load_time': round(avg_load_time, 3),
                'slowest_component_time': round(max_load_time, 3),
                'component_overhead_percentage': round((total_component_time / total_startup_time) * 100, 1) if total_startup_time > 0 else 0
            },
            'component_timings': self.component_timings,
            'optimization_recommendations': self.optimization_recommendations,
            'performance_insights': self._generate_insights(total_startup_time, avg_load_time)
        }
        
        return report
    
    def _generate_insights(self, total_time: float, avg_load_time: float) -> List[str]:
        """Generate performance insights"""
        insights = []
        
        if total_time < 2.0:
            insights.append("🎉 Excellent startup performance - under 2 seconds!")
        elif total_time < 3.0:
            insights.append("✅ Good startup performance - within acceptable range")
        else:
            insights.append("⚠️ Startup time could be improved with optimization")
        
        if avg_load_time < 0.020:  # 20ms
            insights.append("🚀 Component loading is highly optimized")
        elif avg_load_time < 0.050:  # 50ms
            insights.append("✅ Component loading performance is good")
        else:
            insights.append("🔧 Consider optimizing component loading strategies")
        
        component_count = len(self.component_timings)
        if component_count > 10:
            insights.append(f"📊 {component_count} components loaded - consider lazy loading for non-critical components")
        
        return insights
    
    def save_report(self, filepath: Optional[str] = None) -> str:
        """Save performance report to file"""
        if not filepath:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"startup_performance_report_{timestamp}.json"
        
        report = self.generate_performance_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def print_summary(self):
        """Print performance summary to console"""
        report = self.generate_performance_report()
        session = report['session_info']
        stats = report['component_statistics']
        
        print(f"\n📊 STARTUP PERFORMANCE SUMMARY")
        print(f"=" * 50)
        print(f"🕒 Total Startup Time: {session['total_startup_time']}s")
        print(f"🏆 Performance Grade: {session['performance_grade']}")
        print(f"📦 Components Loaded: {stats['total_components']}")
        print(f"⚡ Average Load Time: {stats['average_load_time']}s")
        print(f"🐌 Slowest Component: {stats['slowest_component_time']}s")
        
        if report['optimization_recommendations']:
            print(f"\n🔧 Optimization Recommendations:")
            for rec in report['optimization_recommendations'][:3]:
                print(f"  {rec}")
        
        print(f"\n💡 Performance Insights:")
        for insight in report['performance_insights']:
            print(f"  {insight}")
        print(f"=" * 50)

# Global instance for easy access
_global_reporter = None

def get_startup_performance_reporter() -> StartupPerformanceReporter:
    """Get global startup performance reporter instance"""
    global _global_reporter
    if _global_reporter is None:
        _global_reporter = StartupPerformanceReporter()
    return _global_reporter

def record_startup_timing(component_name: str, load_time: float, category: str = "component"):
    """Record component timing in global reporter"""
    reporter = get_startup_performance_reporter()
    reporter.record_component_timing(component_name, load_time, category)

def print_startup_summary():
    """Print startup performance summary"""
    reporter = get_startup_performance_reporter()
    reporter.print_summary()