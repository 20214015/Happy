"""
Enhanced Application Launcher
============================

Clean application startup with comprehensive warning suppression and optimization.
Addresses all Qt plugin warnings and provides professional application experience.

Author: GitHub Copilot Assistant
Date: August 26, 2025
Version: 1.0 - Clean Startup
"""

import sys
import os
import io
import contextlib
from typing import List


class StartupWarningFilter:
    """Professional startup warning filter for clean console output"""
    
    def __init__(self):
        self.filtered_patterns = [
            "propagateSizeHints",
            "This plugin does not support",
            "QWindowsWindow::setGeometry",
            "QWindowsContext::windowsProc",
            "QXcbConnection: XCB error"
        ]
        self.original_stderr = None
        self.original_stdout = None
        
    def should_filter_message(self, message: str) -> bool:
        """Check if message should be filtered"""
        return any(pattern in message for pattern in self.filtered_patterns)
    
    def start_filtering(self):
        """Start filtering warnings"""
        self.original_stderr = sys.stderr
        self.original_stdout = sys.stdout
        
        sys.stderr = FilteredStream(self.original_stderr, self.should_filter_message)
        # Don't filter stdout, only stderr for warnings
        
    def stop_filtering(self):
        """Stop filtering and restore original streams"""
        if self.original_stderr:
            sys.stderr = self.original_stderr
        if self.original_stdout:
            sys.stdout = self.original_stdout


class FilteredStream:
    """Stream wrapper that filters specific warning messages"""
    
    def __init__(self, original_stream, filter_func):
        self.original_stream = original_stream
        self.filter_func = filter_func
        self.buffer = ""
        
    def write(self, text):
        # Buffer the text to handle multi-line messages
        self.buffer += text
        
        # Check for complete lines
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            self.buffer = lines[-1]  # Keep incomplete line in buffer
            
            for line in lines[:-1]:
                if line and not self.filter_func(line):
                    self.original_stream.write(line + '\n')
        
        return len(text)
    
    def flush(self):
        # Flush any remaining buffer content
        if self.buffer and not self.filter_func(self.buffer):
            self.original_stream.write(self.buffer)
            self.buffer = ""
        self.original_stream.flush()
        
    def __getattr__(self, name):
        return getattr(self.original_stream, name)


@contextlib.contextmanager
def clean_startup():
    """Context manager for clean application startup"""
    filter_manager = StartupWarningFilter()
    filter_manager.start_filtering()
    
    try:
        yield filter_manager
    finally:
        filter_manager.stop_filtering()


def launch_application_cleanly():
    """Launch the MumuManager Pro application with clean console output"""
    print("🚀 Starting MumuManager Pro...")
    
    with clean_startup():
        # Import and run the main application components
        try:
            import main
            print("✅ Application startup completed cleanly")
        except Exception as e:
            print(f"❌ Application startup error: {e}")
            raise


if __name__ == "__main__":
    # Test the warning filter
    print("🧪 Testing warning filter...")
    
    with clean_startup() as filter_manager:
        # Simulate Qt warnings
        print("This should appear")
        print("This plugin does not support propagateSizeHints()", file=sys.stderr)
        print("This should also appear")
        print("Another normal message", file=sys.stderr)
        
    print("🧪 Warning filter test completed")