# MumuManager Pro - GitHub Copilot Instructions

MumuManager Pro is a PyQt6-based desktop application for managing MuMu Android emulator instances. It features AI-powered performance optimization, automation management, and modular component architecture.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap Environment and Dependencies
**Run these commands in exact order - NEVER CANCEL, wait for completion:**

1. **Install system dependencies** (Linux/Ubuntu - takes 3-5 minutes, NEVER CANCEL):
```bash
sudo apt-get update && sudo apt-get install -y \
  libgl1-mesa-dev libglib2.0-0 libxkbcommon-x11-0 \
  libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xfixes0
```

2. **Install Python dependencies** (takes 2-3 minutes, NEVER CANCEL):
```bash
pip3 install PyQt6 psutil qtawesome numpy matplotlib PyQt6-Charts
```

3. **Verify installation**:
```bash
python3 -c "import PyQt6, psutil, qtawesome, numpy, matplotlib; print('All dependencies installed')"
```

### Build and Run Application

**CRITICAL ENVIRONMENT NOTE**: This application requires GUI components. In headless environments, ALWAYS use:
```bash
export QT_QPA_PLATFORM=offscreen
```

**Application startup** (takes 2-3 seconds, NEVER CANCEL):
```bash
cd /path/to/repository
QT_QPA_PLATFORM=offscreen python3 main.py
```

**Production verification** (takes ~0.3 seconds):
```bash
python3 production_deployment.py
```

### Testing and Validation

**NEVER CANCEL**: Set timeout to 30+ minutes for any test commands.

**Run production deployment verification**:
```bash
python3 production_deployment.py
```
- Expected time: 0.3 seconds
- Verifies all Phase 1, 2, and 3 components
- Checks system requirements and dependencies
- Generates deployment report

**Run integration tests**:
```bash
QT_QPA_PLATFORM=offscreen python3 main_window_integration_patch.py
```
- Expected time: 2-3 seconds  
- Tests optimization component integration
- May show warnings about missing EventTypes attributes (known issue)

**Component loading performance test**:
```bash
QT_QPA_PLATFORM=offscreen timeout 10 python3 main.py
```
- Expected startup time: 2-3 seconds
- Component loading: 18-50ms per phase
- Should show successful initialization logs

### Validation Requirements

**MANDATORY: Run complete validation after making changes:**

**Full Validation Workflow** (takes ~5 seconds total):
```bash
echo "=== COMPREHENSIVE VALIDATION TEST ===" && \
echo "1. Dependencies check..." && \
python3 -c "import PyQt6, psutil, qtawesome, numpy, matplotlib, PyQt6.QtCharts; print('✅ All dependencies OK')" && \
echo "2. Production verification..." && \
python3 production_deployment.py | grep -E "(Overall Status|verified|missing)" | head -3 && \
echo "3. Component integration..." && \
QT_QPA_PLATFORM=offscreen python3 -c "from main_window import MainWindow; print('✅ MainWindow integration OK')" 2>/dev/null && \
echo "4. Individual component tests..." && \
QT_QPA_PLATFORM=offscreen python3 -c "from components.dashboard_component import create_dashboard_component; print('✅ Dashboard component OK')" && \
QT_QPA_PLATFORM=offscreen python3 -c "from optimizations.ai_optimizer import AIPerformanceOptimizer; print('✅ AI optimizer OK')" && \
echo "5. Qt platform test..." && \
QT_QPA_PLATFORM=offscreen python3 -c "from PyQt6.QtWidgets import QApplication; print('✅ Qt platform OK')" && \
echo "=== ALL TESTS PASSED ==="
```

**Individual Test Commands:**

1. **Application Startup Test** (3 seconds, NEVER CANCEL):
```bash
QT_QPA_PLATFORM=offscreen timeout 10 python3 main.py 2>&1 | grep -E "(✅|❌|⚠️)"
```
- Must show "✅ MainWindow created successfully"
- Must show "✅ MainWindow shown, starting app loop..."

2. **Production Verification Test** (0.3 seconds):
```bash
python3 production_deployment.py | grep "Overall Status"
```
- Should show status (verified/issues/needs attention)
- Check component verification results

3. **Component Integration Test** (2 seconds):
```bash
QT_QPA_PLATFORM=offscreen python3 -c "
from main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)
window = MainWindow()
print('Integration test passed')
"
```

## User Scenario Testing

**MANUAL VALIDATION REQUIREMENT**: After building and running the application, you MUST test actual functionality through complete user scenarios.

### Core User Workflows to Test

**Note**: These scenarios run with `QT_QPA_PLATFORM=offscreen` so you cannot interact with GUI, but you can verify the application logic and component initialization.

1. **Application Launch and Component Loading**:
```bash
QT_QPA_PLATFORM=offscreen timeout 10 python3 main.py 2>&1 | tee startup_log.txt
# Verify: Check for component initialization messages
grep -E "✅.*initialized|✅.*created" startup_log.txt
```

2. **Production Deployment Validation**:
```bash
python3 production_deployment.py
# Verify: Check overall status and component verification results
# Expected: See verification results for Phase 1, 2, 3 components
```

3. **Module Import Verification**:
```bash
# Test critical imports work individually
QT_QPA_PLATFORM=offscreen python3 -c "
from optimizations.ai_optimizer import AIPerformanceOptimizer  
from components.dashboard_component import create_dashboard_component
print('Core modules import successfully')
"
```

4. **Service Layer Testing**:
```bash
QT_QPA_PLATFORM=offscreen python3 -c "
from services.service_manager import ServiceManager
from core.event_manager import EventManager  
from core.state_manager import StateManager
print('Service layer components available')
"
```

### Expected Behavior
- Application should start within 3 seconds
- All Phase 1, 2 components should verify successfully  
- Phase 3 may show warnings (known issue with EventTypes)
- Dashboard component should create successfully
- AI optimizer should initialize without errors

## Architecture Overview

### Key Components
- **`main.py`**: Application entry point with font loading and theme application
- **`main_window.py`**: Main application window with modular component integration
- **`production_deployment.py`**: Comprehensive system verification and deployment validation
- **Services** (`services/`): ServiceManager, centralized service management
- **Core** (`core/`): EventManager, StateManager for event-driven architecture  
- **Components** (`components/`): Modular UI components (dashboard, control panel, status, performance monitor, settings)
- **Optimizations** (`optimizations/`): AI optimizer, performance monitoring, smart templates
- **Managers** (`managers/`): AutomationManager for script and instance management

### Phase Architecture
- **Phase 1**: Service Integration (ServiceManager, EventManager, StateManager)
- **Phase 2**: Modular Components (Dashboard, Control Panel, Status)  
- **Phase 3**: Production Features (Performance Monitor, Settings, Deployment)

## System Requirements

**Minimum Requirements** (verified by production_deployment.py):
- **CPU**: 2+ cores
- **Memory**: 4GB+ RAM  
- **Python**: 3.8+ (tested on 3.12.3)
- **OS**: Linux (Ubuntu/Debian tested)

**Performance Expectations** (measured timings):
- Application startup: 3 seconds (use `timeout 10` minimum)
- Component loading: 18-50ms per phase
- Memory usage: ~60MB estimated
- Production verification: 0.3 seconds

## Critical Development Guidelines

### NEVER Cancel Commands
**CRITICAL**: These operations MUST complete - set timeouts appropriately:
- **Dependency installation**: 5+ minutes (use `timeout 300`)
- **Application startup**: 10+ seconds (use `timeout 15`)
- **Production verification**: 5+ seconds (use `timeout 10`)
- **Component integration tests**: 5+ seconds (use `timeout 10`)

### Environment Setup
**ALWAYS** export QT_QPA_PLATFORM=offscreen before running any PyQt6 commands in headless environments.

### Code Changes Validation
**ALWAYS run these commands after making changes**:
1. `python3 production_deployment.py` - Verify component integrity
2. `QT_QPA_PLATFORM=offscreen timeout 10 python3 main.py` - Test startup
3. Check for Python import errors and Qt platform issues

### Known Issues and Workarounds
- **GUI in headless**: Must use `QT_QPA_PLATFORM=offscreen`
- **Missing fonts**: Some JetBrains Mono variants missing in `assets/fonts/` (non-critical)
- **EventTypes attributes**: Some Phase 3 components may show warnings about missing EventTypes attributes (known integration issue)
- **libEGL.so.1 error**: Install system Qt dependencies as shown above

## Common Commands Reference

### Quick Development Cycle
```bash
# 1. Verify environment
python3 production_deployment.py

# 2. Test changes
QT_QPA_PLATFORM=offscreen timeout 10 python3 main.py

# 3. Check specific component
QT_QPA_PLATFORM=offscreen python3 -c "from components.dashboard_component import create_dashboard_component; print('Dashboard OK')"
```

### Debugging Commands
```bash
# Check dependencies
python3 -c "import PyQt6, psutil, qtawesome, numpy, matplotlib, PyQt6.QtCharts; print('All OK')"

# Verify component loading
python3 -c "from main_window import MainWindow; print('MainWindow import OK')"

# Test Qt platform
QT_QPA_PLATFORM=offscreen python3 -c "from PyQt6.QtWidgets import QApplication; print('Qt OK')"
```

## File Locations

### Frequently Modified Files
- **`main.py`**: Application entry point
- **`main_window.py`**: Main window implementation  
- **`components/`**: UI component implementations
- **`optimizations/`**: Performance optimization modules
- **`services/`**: Core service implementations

### Configuration Files
- **`automation_settings.json`**: Automation configuration
- **`constants.py`**: Application constants and enums

### Validation Files  
- **`production_deployment.py`**: Comprehensive system verification
- **`main_window_integration_patch.py`**: Integration testing

Always check `production_deployment.py` first to understand current system state and component status.

## Final Validation Checklist

**Before completing any development task, run this complete validation:**

```bash
echo "=== FINAL VALIDATION OF ALL INSTRUCTIONS ==="
echo "Testing dependency check..."
python3 -c "import PyQt6, psutil, qtawesome, numpy, matplotlib, PyQt6.QtCharts; print('✅ Dependencies OK')"

echo "Testing production verification..."
python3 production_deployment.py | grep "Overall Status" 

echo "Testing component integration..."
QT_QPA_PLATFORM=offscreen python3 -c "
from main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)
window = MainWindow()
print('✅ Integration test passed')
" 2>/dev/null

echo "Testing service layer..."
QT_QPA_PLATFORM=offscreen python3 -c "
from services.service_manager import ServiceManager
from core.event_manager import EventManager  
from core.state_manager import StateManager
print('✅ Service layer OK')
"

echo "Testing module imports..."
QT_QPA_PLATFORM=offscreen python3 -c "
from optimizations.ai_optimizer import AIPerformanceOptimizer  
from components.dashboard_component import create_dashboard_component
print('✅ Core modules OK')
" 2>/dev/null

echo "=== ALL INSTRUCTION COMMANDS VALIDATED ==="
```

**Expected Results:**
- All ✅ messages should appear
- "Overall Status" should show current system state
- Integration test should pass with component initialization logs
- No critical import errors should occur

This validation takes ~5-10 seconds total and confirms the entire development environment is working correctly.