# Installation Troubleshooting Guide

## ⚡ Quick Start (No Local LLM Issues!)

**RECOMMENDED:** Start with cloud mode to avoid `llama-cpp-python` installation issues:

```bash
# 1. Install base requirements (works everywhere)
pip install -r requirements.txt

# 2. Configure for cloud mode
cp .env.example .env

# 3. Edit .env and set:
BADI_MODE=cloud
OPENAI_API_KEY=your-key-here
# OR
ANTHROPIC_API_KEY=your-key-here
# OR
GEMINI_API_KEY=your-key-here

# 4. Done! Start using BADI
python -m badi.cli setup
python -m badi.cli chat
```

This avoids ALL local LLM installation issues and gets you running immediately!

---

## 🔧 Installing Local LLM Support (Optional)

If you want to run models locally (privacy-first), here are solutions for common issues:

### Problem: llama-cpp-python Won't Install

**Root Cause:** Requires C++ compiler and CMake to build from source.

### Solution 1: Use Pre-built Wheels (Easiest)

```bash
# CPU only - Works on Windows/Mac/Linux
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### Solution 2: Install Build Tools First

#### Windows:
```bash
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++"

# Then install llama-cpp-python
pip install llama-cpp-python
```

#### Mac:
```bash
# Install Xcode Command Line Tools
xcode-select --install

# For Apple Silicon (M1/M2/M3) with GPU support:
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential cmake

# Fedora/RHEL
sudo dnf install gcc-c++ cmake

# Then install
pip install llama-cpp-python
```

### Solution 3: Use Docker (Advanced)

If compilation still fails, use Docker:

```bash
docker pull ghcr.io/abetlen/llama-cpp-python:latest
```

### Solution 4: Skip Local LLM Entirely

Just use cloud APIs! They're faster, don't require setup, and work immediately:

```python
# In .env
BADI_MODE=cloud
OPENAI_API_KEY=sk-...
```

---

## 🎯 Recommended Installation Path

### For Beginners:
1. ✅ Install base requirements: `pip install -r requirements.txt`
2. ✅ Use cloud mode (OpenAI/Anthropic/Gemini)
3. ✅ Try BADI immediately
4. ⏭️ Add local LLM later if desired

### For Privacy-Focused Users:
1. ✅ Install build tools for your OS (see above)
2. ✅ Install llama-cpp-python using pre-built wheels
3. ✅ Download a GGUF model file
4. ✅ Configure BADI for local mode

### For Developers:
1. ✅ Start with cloud mode for testing
2. ✅ Get BADI working first
3. ✅ Add local LLM support later
4. ✅ Contribute improvements!

---

## 🐛 Common Issues & Solutions

### Issue 1: "error: Microsoft Visual C++ 14.0 or greater is required"

**Platform:** Windows

**Solution:**
```bash
# Download and install Visual Studio Build Tools:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Select "Desktop development with C++" workload
```

### Issue 2: "fatal error: Python.h: No such file or directory"

**Platform:** Linux

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# Fedora/RHEL
sudo dnf install python3-devel
```

### Issue 3: "CMake not found"

**Solution:**
```bash
# Install CMake
pip install cmake

# Or use system package manager:
# Mac: brew install cmake
# Ubuntu: sudo apt-get install cmake
# Windows: Download from cmake.org
```

### Issue 4: Compilation takes forever / runs out of memory

**Solution:**
```bash
# Use pre-built wheels instead
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### Issue 5: "No module named 'llama_cpp'"

**This is OK!** BADI works without local LLM. Just use cloud mode:

```env
# .env
BADI_MODE=cloud
OPENAI_API_KEY=your-key
```

---

## 🚀 Alternative: Use Cloud Mode (Recommended)

You don't need local LLM at all! Cloud APIs are:
- ✅ **Faster** to set up (no compilation)
- ✅ **Easier** (no build tools needed)
- ✅ **More powerful** (GPT-4, Claude 3.5, etc.)
- ✅ **Always updated** (latest models)

### Get API Keys:

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create an account
3. Generate API key
4. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Anthropic (Claude):**
1. Go to https://console.anthropic.com/
2. Create account
3. Get API key
4. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Google (Gemini):**
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env`: `GEMINI_API_KEY=...`

Then just:
```bash
python -m badi.cli chat
```

---

## 🎓 Understanding the Issue

`llama-cpp-python` is a **Python binding** to llama.cpp (C++ library). It needs to:
1. Compile C++ code
2. Link to Python
3. Optimize for your CPU/GPU

This requires:
- C++ compiler
- CMake build system
- Python development headers

**That's a lot of setup!** That's why we recommend starting with cloud mode.

---

## 🔄 Hybrid Approach (Best of Both Worlds)

Start with cloud, add local later:

```env
# .env
BADI_MODE=hybrid

# Cloud for complex tasks
ANTHROPIC_API_KEY=sk-ant-...

# Local for simple tasks (add later)
BADI_LOCAL_MODEL_PATH=./models/model.gguf
```

BADI will use local when it can, cloud when needed!

---

## ✅ Verification

After installation, verify what's working:

```bash
python verify_installation.py
```

This will show:
- ✅ Which backends are available
- ✅ What's working
- ⚠️ What's optional

---

## 🆘 Still Stuck?

### Option 1: Skip Local LLM
Use cloud mode - it's easier and works great!

### Option 2: Use Docker
Avoid all compilation issues:
```bash
docker build -t badi .
docker run -it badi
```

### Option 3: Ask for Help
Open an issue on GitHub with:
- Your OS and version
- Python version
- Error message
- What you tried

---

## 📊 Installation Success Rates

Based on typical experiences:

| Method | Success Rate | Time |
|--------|--------------|------|
| Cloud mode | 99% | 2 min |
| Pre-built wheels | 90% | 5 min |
| Build from source | 70% | 10-30 min |
| Docker | 95% | 5 min |

**Recommendation:** Start with cloud mode!

---

## 🎯 Summary

**Quick Path (Recommended):**
```bash
pip install -r requirements.txt
# Use cloud API - Done!
```

**Privacy Path:**
```bash
pip install -r requirements.txt
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
# Download GGUF model - Done!
```

**Hybrid Path:**
```bash
pip install -r requirements.txt
# Start with cloud, add local later
```

**You don't need local LLM to use BADI!** 🚀

---

## 📞 Support Resources

- 📖 Official llama-cpp-python docs: https://github.com/abetlen/llama-cpp-python
- 🎥 Installation videos: Search YouTube for "llama-cpp-python install"
- 💬 Community: GitHub Discussions
- 🐛 Issues: GitHub Issues

---

**Remember:** Cloud mode works perfectly and is actually **recommended for getting started**. You can always add local LLM support later!
