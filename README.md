# B.A.D.I. - Balanced Autonomous Digital Intelligence

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-alpha-orange)

## 🌟 Overview

B.A.D.I. (Balanced Autonomous Digital Intelligence) is an open-source AI assistant framework designed with a focus on:

- **Privacy-First Design**: Local-first architecture with optional cloud integration
- **Controlled Autonomy**: User consent and transparency at every step
- **Modular Architecture**: Extensible plugin system for capabilities
- **Multi-Modal Interaction**: CLI, API, and voice interfaces
- **Hybrid Intelligence**: Seamless switching between local and cloud AI models

## 🏗️ Architecture

B.A.D.I. is built on a layered architecture:

```
┌─────────────────────────────────────────────────┐
│          User Layer (Voice, Text, GUI)          │
├─────────────────────────────────────────────────┤
│     Interaction Layer (NLP, Voice, API)         │
├─────────────────────────────────────────────────┤
│  Core Layer (Router, Planner, Executor, Policy) │
├─────────────────────────────────────────────────┤
│        Module System (Extensible Plugins)       │
├─────────────────────────────────────────────────┤
│      System Layer (OS, Network Adapters)        │
├─────────────────────────────────────────────────┤
│   Memory System (SQL + Vector Store + Cache)    │
├─────────────────────────────────────────────────┤
│      AI Backends (Local, vLLM, Cloud APIs)      │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip and git installed
- (Optional) NVIDIA GPU with CUDA for faster inference

**Note:** Local LLM support is optional. We recommend starting with cloud APIs (OpenAI/Anthropic/Google) for the easiest setup. See [INSTALLATION_TROUBLESHOOTING.md](INSTALLATION_TROUBLESHOOTING.md) if you encounter issues.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/restonuct/BADI
cd badi
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** This installs base dependencies. Local LLM support (`llama-cpp-python`) is optional. For local models, see [INSTALLATION_TROUBLESHOOTING.md](INSTALLATION_TROUBLESHOOTING.md).

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your preferences
```

5. Run initial setup:
```bash
python -m badi.cli setup
```

6. Start chatting:
```bash
python -m badi.cli chat
```

## 📦 Features

### Current Capabilities

- ✅ **Conversational AI**: Natural language interaction with context awareness
- ✅ **Task Planning**: Multi-step task decomposition and execution
- ✅ **File Management**: Automated file organization and cleanup
- ✅ **Memory System**: Long-term memory with semantic search
- ✅ **Web Search**: Internet search with summarization
- ✅ **Multiple AI Backends**: Local (llama.cpp), vLLM, OpenAI, Anthropic, Google

### Planned Features

- 🔄 **Social Media Integration**: Post to Instagram, Twitter, LinkedIn
- 🔄 **Email Management**: Smart inbox processing and composition
- 🔄 **Calendar Integration**: Schedule management and reminders
- 🔄 **Voice Interaction**: Whisper-based STT and TTS
- 🔄 **Smart Home Control**: Integration with IoT devices
- 🔄 **Code Assistance**: Development workflow automation

## 🔧 Configuration

B.A.D.I. supports three operational modes:

1. **Local Mode**: Everything runs offline using local LLMs
2. **Cloud Mode**: Uses cloud APIs (OpenAI, Anthropic, etc.)
3. **Hybrid Mode**: Local by default, cloud for complex tasks

Configure via `.env`:

```env
BADI_MODE=hybrid  # local / cloud / hybrid
BADI_DB_PATH=./data/badi.db
BADI_VECTOR_DIR=./data/chroma
BADI_LOCAL_MODEL_PATH=./models/llama-3-8b-instruct-q4.gguf
```

## 🧩 Module System

B.A.D.I. uses a plugin-based module system. Create custom modules by extending the base class:

```python
from badi.modules.base import Module

class MyCustomModule(Module):
    name = "my_custom_module"
    description = "Does something useful"
    requires_confirmation = False
    
    async def run(self, **kwargs) -> dict:
        # Your implementation
        return {"status": "success", "result": "..."}
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [Module Development](docs/module-development.md)
- [API Reference](docs/api-reference.md)
- [Architecture Deep Dive](docs/architecture.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork and clone the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `pytest tests/`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [llama.cpp](https://github.com/ggerganov/llama.cpp) for local inference
- Vector storage powered by [ChromaDB](https://www.trychroma.com/)
- Inspired by the vision of balanced, ethical AI assistants

## 📞 Contact

- Project Issues: [GitHub Issues](https://github.com/yourusername/badi/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/badi/discussions)

## ⚠️ Disclaimer

B.A.D.I. is currently in **alpha** status. Use in production environments at your own risk. Always review and approve actions before execution, especially for file operations and system changes.

---

**Built with ❤️ for a more transparent, privacy-respecting AI future**
