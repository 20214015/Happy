"""
Managers Package
================

Modular managers for different aspects of the MumuM application.
Extracted from the monolithic main_window.py to improve maintainability.
"""

from .instance_manager import InstanceManager
from .automation_manager import AutomationManager
from .ui_manager import UIManager
from .event_manager import EventManager

__all__ = [
    'InstanceManager',
    'AutomationManager', 
    'UIManager',
    'EventManager'
]