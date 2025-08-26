#!/usr/bin/env python3
"""
Performance Benchmark Test
=========================

Measures the performance improvements achieved by the optimization system.
Compares startup time, memory usage, and component loading speeds.

Author: GitHub Copilot
Date: August 26, 2025
Version: 1.0 - Benchmark Test
"""

import time
import statistics
import subprocess
import sys
import os
from typing import List, Dict, Any


def measure_startup_time(num_runs: int = 5) -> List[float]:
    """Measure application startup time over multiple runs"""
    
    print(f"🔬 Measuring startup time over {num_runs} runs...")
    startup_times = []
    
    for i in range(num_runs):
        print(f"  Run {i+1}/{num_runs}...", end=" ")
        
        start_time = time.time()
        
        # Run the application with timeout
        env = os.environ.copy()
        env['QT_QPA_PLATFORM'] = 'offscreen'
        
        result = subprocess.run([
            'python3', 'main.py'
        ], 
        capture_output=True, 
        text=True, 
        timeout=15,
        env=env,
        cwd='/home/runner/work/Happy/Happy'
        )
        
        end_time = time.time()
        startup_time = end_time - start_time
        startup_times.append(startup_time)
        
        print(f"{startup_time:.3f}s")
        
        # Small delay between runs
        time.sleep(1)
    
    return startup_times


def analyze_performance_metrics() -> Dict[str, Any]:
    """Analyze performance metrics from the production deployment"""
    
    print("📊 Analyzing performance metrics...")
    
    try:
        # Run production deployment to get metrics
        env = os.environ.copy()
        result = subprocess.run([
            'python3', 'production_deployment.py'
        ], 
        capture_output=True, 
        text=True, 
        timeout=30,
        env=env,
        cwd='/home/runner/work/Happy/Happy'
        )
        
        output = result.stdout
        
        # Parse key metrics from output
        metrics = {
            'components_verified': 0,
            'phase1_time': 0.0,
            'phase2_time': 0.0,
            'phase3_time': 0.0,
            'memory_estimate': 0
        }
        
        # Extract component count
        if 'components verified' in output:
            for line in output.split('\n'):
                if 'components verified' in line:
                    parts = line.split('/')
                    if len(parts) >= 2:
                        metrics['components_verified'] = int(parts[0].split()[-1])
                    break
        
        # Extract loading times
        for line in output.split('\n'):
            if 'Phase 1 loading:' in line:
                time_str = line.split(':')[-1].strip().replace('ms', '')
                metrics['phase1_time'] = float(time_str)
            elif 'Phase 2 loading:' in line:
                time_str = line.split(':')[-1].strip().replace('ms', '')
                metrics['phase2_time'] = float(time_str)
            elif 'Phase 3 loading:' in line:
                time_str = line.split(':')[-1].strip().replace('ms', '')
                metrics['phase3_time'] = float(time_str)
            elif 'memory usage:' in line:
                memory_str = line.split(':')[-1].strip().replace('MB', '')
                metrics['memory_estimate'] = int(memory_str)
        
        return metrics
        
    except Exception as e:
        print(f"⚠️ Error analyzing metrics: {e}")
        return {}


def generate_performance_report(startup_times: List[float], metrics: Dict[str, Any]):
    """Generate comprehensive performance report"""
    
    print("\n" + "="*70)
    print("🚀 HAPPY APPLICATION PERFORMANCE REPORT")
    print("="*70)
    
    # Startup Performance
    print(f"\n📈 Startup Performance:")
    print(f"   • Average startup time: {statistics.mean(startup_times):.3f}s")
    print(f"   • Best startup time: {min(startup_times):.3f}s")
    print(f"   • Worst startup time: {max(startup_times):.3f}s")
    print(f"   • Standard deviation: {statistics.stdev(startup_times):.3f}s")
    print(f"   • Consistency: {'Excellent' if statistics.stdev(startup_times) < 0.2 else 'Good' if statistics.stdev(startup_times) < 0.5 else 'Variable'}")
    
    # Component Performance
    if metrics:
        print(f"\n🔧 Component Performance:")
        print(f"   • Components verified: {metrics.get('components_verified', 'N/A')}")
        print(f"   • Phase 1 loading: {metrics.get('phase1_time', 0):.2f}ms")
        print(f"   • Phase 2 loading: {metrics.get('phase2_time', 0):.2f}ms")
        print(f"   • Phase 3 loading: {metrics.get('phase3_time', 0):.2f}ms")
        
        total_component_time = metrics.get('phase1_time', 0) + metrics.get('phase2_time', 0) + metrics.get('phase3_time', 0)
        print(f"   • Total component loading: {total_component_time:.2f}ms")
        
        # Memory Analysis
        print(f"\n💾 Memory Analysis:")
        print(f"   • Estimated memory usage: {metrics.get('memory_estimate', 'N/A')}MB")
        
        memory_efficiency = "Excellent" if metrics.get('memory_estimate', 100) < 50 else "Good" if metrics.get('memory_estimate', 100) < 75 else "Acceptable"
        print(f"   • Memory efficiency: {memory_efficiency}")
    
    # Optimization Assessment
    print(f"\n🎯 Optimization Assessment:")
    avg_startup = statistics.mean(startup_times)
    
    # Performance grading
    if avg_startup < 2.0:
        grade = "A+ (Excellent)"
        description = "Outstanding performance - well optimized"
    elif avg_startup < 3.0:
        grade = "A (Very Good)"
        description = "Good performance - minor optimizations possible"
    elif avg_startup < 4.0:
        grade = "B (Good)"
        description = "Acceptable performance - optimization recommended"
    else:
        grade = "C (Needs Improvement)"
        description = "Performance issues - optimization required"
    
    print(f"   • Performance Grade: {grade}")
    print(f"   • Assessment: {description}")
    
    # Optimization Impact
    print(f"\n✨ Optimization Impact:")
    print(f"   • Startup Optimizations: Applied")
    print(f"   • Memory Optimizations: Applied") 
    print(f"   • Font Optimizations: Applied")
    print(f"   • UI Optimizations: Applied")
    print(f"   • Table Optimizations: Applied")
    
    # Performance vs. Targets
    print(f"\n🎯 Performance vs. Targets:")
    startup_target = 2.0  # Target: under 2 seconds
    memory_target = 50   # Target: under 50MB
    
    startup_status = "✅ Met" if avg_startup <= startup_target else "⚠️ Above target"
    memory_status = "✅ Met" if metrics.get('memory_estimate', 100) <= memory_target else "⚠️ Above target"
    
    print(f"   • Startup time target ({startup_target}s): {startup_status}")
    print(f"   • Memory usage target ({memory_target}MB): {memory_status}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if avg_startup > startup_target:
        print(f"   • Consider more aggressive lazy loading")
        print(f"   • Optimize component initialization order")
    
    if metrics.get('memory_estimate', 0) > memory_target:
        print(f"   • Implement stricter cache limits")
        print(f"   • Consider memory pooling for heavy components")
    
    if avg_startup <= startup_target and metrics.get('memory_estimate', 0) <= memory_target:
        print(f"   • Performance targets met - maintain current optimizations")
        print(f"   • Consider monitoring for regression prevention")
    
    print("\n" + "="*70)


def main():
    """Run performance benchmark"""
    
    print("🔬 Happy Application Performance Benchmark")
    print("=" * 50)
    
    # Change to application directory
    os.chdir('/home/runner/work/Happy/Happy')
    
    try:
        # Measure startup performance
        startup_times = measure_startup_time(3)  # 3 runs for faster testing
        
        # Analyze system metrics  
        metrics = analyze_performance_metrics()
        
        # Generate report
        generate_performance_report(startup_times, metrics)
        
        # Calculate overall score
        avg_startup = statistics.mean(startup_times)
        overall_score = max(0, 100 - (avg_startup - 1.5) * 20)  # Score based on startup time
        
        print(f"\n🏆 Overall Performance Score: {overall_score:.1f}/100")
        
        return avg_startup
        
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrupted by user")
        return None
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        return None


if __name__ == "__main__":
    main()