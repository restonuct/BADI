# Quick Start Guide

Get B.A.D.I. running in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- 8GB RAM (16GB recommended for local LLM)
- pip and git installed

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/badi.git
cd badi
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install base dependencies (required)
pip install -r requirements.txt
```

**Note:** Local LLM support (`llama-cpp-python`) is optional and can be tricky to install. See [INSTALLATION_TROUBLESHOOTING.md](INSTALLATION_TROUBLESHOOTING.md) if you want local models. **We recommend starting with cloud mode** (easier setup, works immediately).

## Configuration

### Option A: Cloud Mode (Easiest - Recommended)

**Perfect for getting started quickly!** No model downloads, no compilation issues.

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add ONE of these API keys:

**Using OpenAI (GPT-4, ChatGPT):**
```env
BADI_MODE=cloud
OPENAI_API_KEY=sk-...
```
Get key at: https://platform.openai.com/api-keys

**Using Anthropic (Claude):**
```env
BADI_MODE=cloud
ANTHROPIC_API_KEY=sk-ant-...
```
Get key at: https://console.anthropic.com/

**Using Google (Gemini):**
```env
BADI_MODE=cloud
GEMINI_API_KEY=...
```
Get key at: https://makersuite.google.com/app/apikey

3. Done! Skip to "First Run" below.

---

### Option B: Local Mode (Privacy-First)

**For users who want offline capability and complete privacy.**

⚠️ **Important:** Local mode requires additional setup. See [INSTALLATION_TROUBLESHOOTING.md](INSTALLATION_TROUBLESHOOTING.md) for detailed instructions.

1. **Install llama-cpp-python** (separate step):
```bash
# Easiest method - use pre-built wheels:
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# See INSTALLATION_TROUBLESHOOTING.md for GPU support and other options
```

2. **Download a GGUF model** from HuggingFace. Recommended:

   **For 8GB RAM:**
   - Model: [Llama-2-7B-Chat-GGUF](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
   - File: `llama-2-7b-chat.Q4_K_M.gguf` (about 4GB)

   **For 16GB+ RAM:**
   - Model: [Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
   - File: `mistral-7b-instruct-v0.2.Q5_K_M.gguf` (about 5GB)

   Download and place in `./models/` folder:
   ```bash
   mkdir models
   # Download your chosen model file to this folder
   ```

3. **Configure `.env`:**
```bash
cp .env.example .env
```

Edit `.env`:
```env
BADI_MODE=local
BADI_LOCAL_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf
BADI_LOCAL_GPU_LAYERS=0  # Set to 20-30 if you have NVIDIA GPU
```

---

### Option C: Hybrid Mode (Best of Both)

**Recommended for experienced users.** Uses local for simple tasks, cloud for complex ones.

1. Set up BOTH local and cloud (follow steps above)
2. Configure `.env`:
```env
BADI_MODE=hybrid
BADI_LOCAL_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf
ANTHROPIC_API_KEY=sk-ant-...  # Fallback for complex tasks
```

## First Run

### 1. Run Setup

```bash
python -m badi.cli setup
```

This will:
- Initialize the database
- Create your user profile
- Verify configuration
- Check available backends

### 2. Start Chatting

```bash
python -m badi.cli chat
```

Try these example commands:
- "Hello, who are you?"
- "Scan my downloads folder"
- "Remember that I prefer dark mode"
- "What can you help me with?"

## Testing Installation

Verify everything works:

```bash
python -m badi.cli info
```

You should see:
- Your configuration mode
- Database paths
- List of enabled modules

## Common Issues

### "No AI backend available"
- **Solution**: Make sure you've set EITHER `OPENAI_API_KEY` (or similar) in `.env` OR installed `llama-cpp-python` and set `BADI_LOCAL_MODEL_PATH`
- **Quick fix**: Use cloud mode - it's easier!

### "llama-cpp-python won't install"
- **Solution**: Start with cloud mode instead! Or see [INSTALLATION_TROUBLESHOOTING.md](INSTALLATION_TROUBLESHOOTING.md) for detailed fixes
- **Quick fix**: 
  ```bash
  pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
  ```

### "Module not found" errors
- **Solution**: Activate virtual environment and run `pip install -r requirements.txt`

### "Model not found"
- **Solution**: Check that `BADI_LOCAL_MODEL_PATH` in `.env` points to an actual `.gguf` file
- **Or**: Switch to cloud mode (no model download needed!)

## Next Steps

1. **Explore Modules**: Check what B.A.D.I. can do
   ```bash
   python -m badi.cli info
   ```

2. **Create Custom Modules**: See [Module Development Guide](docs/module-development.md)

3. **Enable Voice**: Install voice dependencies
   ```bash
   pip install openai-whisper sounddevice
   ```

4. **API Access**: Run the web API
   ```bash
   uvicorn badi.interaction.api:app --reload
   ```

## Need Help?

- 📚 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/badi/issues)
- 💬 [Discussions](https://github.com/yourusername/badi/discussions)

## What's Next?

- **Tasks**: Try "organize my downloads folder"
- **Memory**: Tell B.A.D.I. your preferences
- **Customization**: Create your own modules
- **Integration**: Connect to your tools and services

Happy building! 🚀
