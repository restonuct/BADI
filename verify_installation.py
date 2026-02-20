#!/usr/bin/env python3
"""
B.A.D.I. Installation Verification Script

Run this script to verify your B.A.D.I. installation is complete and working.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} is too old. Need 3.10+")
        return False

def check_dependencies():
    """Check required dependencies"""
    print_header("Checking Dependencies")
    
    required = [
        "pydantic",
        "click",
        "sqlalchemy",
        "chromadb",
        "fastapi"
    ]
    
    optional = [
        ("llama_cpp", "llama-cpp-python (for local LLM)"),
        ("openai", "OpenAI SDK"),
        ("anthropic", "Anthropic SDK"),
        ("google.generativeai", "Google Gemini SDK")
    ]
    
    all_ok = True
    
    # Required
    for package in required:
        try:
            __import__(package)
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} - REQUIRED")
            all_ok = False
    
    # Optional
    print("\nOptional dependencies:")
    for package, name in optional:
        try:
            __import__(package)
            print_success(f"{name}")
        except ImportError:
            print_warning(f"{name} - not installed (optional)")
    
    return all_ok

def check_project_structure():
    """Check project structure"""
    print_header("Checking Project Structure")
    
    required_paths = [
        "badi/__init__.py",
        "badi/config.py",
        "badi/cli.py",
        "badi/memory/db.py",
        "badi/memory/vector_store.py",
        "badi/core/router.py",
        "badi/core/planner.py",
        "badi/core/executor.py",
        "badi/modules/base.py",
        "badi/modules/system_control.py",
        "badi/ai_backends/__init__.py",
        "README.md",
        "requirements.txt",
        ".env.example"
    ]
    
    all_ok = True
    for path in required_paths:
        if Path(path).exists():
            print_success(path)
        else:
            print_error(f"{path} - MISSING")
            all_ok = False
    
    return all_ok

def check_configuration():
    """Check configuration"""
    print_header("Checking Configuration")
    
    if Path(".env").exists():
        print_success(".env file exists")
        try:
            from badi.config import get_config
            config = get_config()
            print_success(f"Configuration loaded: mode={config.mode}")
            return True
        except Exception as e:
            print_error(f"Error loading config: {e}")
            return False
    else:
        print_warning(".env not found (copy from .env.example)")
        return False

def check_imports():
    """Check all B.A.D.I. imports"""
    print_header("Checking B.A.D.I. Imports")
    
    imports = [
        "badi",
        "badi.config",
        "badi.memory",
        "badi.core",
        "badi.modules",
        "badi.ai_backends"
    ]
    
    all_ok = True
    for module in imports:
        try:
            __import__(module)
            print_success(f"{module}")
        except Exception as e:
            print_error(f"{module}: {e}")
            all_ok = False
    
    return all_ok

def check_backends():
    """Check AI backends availability"""
    print_header("Checking AI Backends")
    
    try:
        from badi.ai_backends import get_selector
        selector = get_selector()
        backends = selector.list_available_backends()
        
        available_count = sum(backends.values())
        
        for name, available in backends.items():
            if available:
                print_success(f"{name} backend configured")
            else:
                print_warning(f"{name} backend not configured")
        
        if available_count == 0:
            print_error("No AI backends configured!")
            print("\n  Configure at least one:")
            print("  - Local: Set BADI_LOCAL_MODEL_PATH in .env")
            print("  - Cloud: Set API key (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)")
            return False
        else:
            print_success(f"\n{available_count} backend(s) available")
            return True
            
    except Exception as e:
        print_error(f"Error checking backends: {e}")
        return False

def run_basic_test():
    """Run a basic functionality test"""
    print_header("Running Basic Functionality Test")
    
    try:
        # Test database
        from badi.memory import init_db, get_db, get_or_create_user
        init_db()
        db = get_db()
        user = get_or_create_user(db, name="Test User")
        print_success(f"Database: User created (ID: {user.id})")
        
        # Test vector store
        from badi.memory import get_vector_store
        vs = get_vector_store()
        print_success(f"Vector store: {vs.count('conversations')} entries")
        
        # Test module registry
        from badi.modules import MODULE_REGISTRY
        modules = MODULE_REGISTRY.list_enabled_modules()
        print_success(f"Modules: {len(modules)} registered ({', '.join(modules)})")
        
        return True
        
    except Exception as e:
        print_error(f"Functionality test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   B.A.D.I. Installation Verification                      ║
    ║   Balanced Autonomous Digital Intelligence                ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Configuration", check_configuration),
        ("Imports", check_imports),
        ("AI Backends", check_backends),
        ("Basic Functionality", run_basic_test)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Check '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Installation is complete and working!")
        print("\nNext steps:")
        print("  1. python -m badi.cli setup")
        print("  2. python -m badi.cli chat")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nRefer to QUICKSTART.md for detailed installation instructions.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
