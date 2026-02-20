# B.A.D.I. Architecture

## Overview

B.A.D.I. (Balanced Autonomous Digital Intelligence) is built on a layered architecture that separates concerns and enables modularity, extensibility, and controlled autonomy.

## System Layers

### 1. User Layer
**Purpose**: Interface between humans and the system

- **Voice Interface**: Speech-to-text (Whisper) for natural voice interaction
- **Text Interface**: CLI and API for text-based interaction  
- **GUI**: Web-based interface (planned)

### 2. Interaction Layer
**Purpose**: Normalize inputs and format outputs

**Components:**
- `nlp.py`: Natural language processing and intent detection
- `cli.py`: Command-line interface implementation
- `api.py`: REST API endpoints (FastAPI)
- `voice.py`: Voice interaction handlers

**Responsibilities:**
- Parse user inputs
- Detect intents (chat vs task)
- Format responses for different channels
- Handle multi-modal inputs

### 3. Core Layer
**Purpose**: Intelligence and decision-making

**Components:**
- `router.py`: Routes requests to appropriate handlers
- `planner.py`: Decomposes tasks into executable plans
- `executor.py`: Executes plans with parallel support
- `policy.py`: Enforces permissions and confirmations

**Flow:**
```
Request → Context Enrichment → Intent Classification
    ↓
Simple Query → Chat Handler → Response
    ↓
Complex Task → Planner → Plan → Executor → Response
```

### 4. Module System
**Purpose**: Extensible capabilities

**Base Classes:**
- `Module`: Abstract base for all modules
- `ModuleCapability`: Defines what a module can do
- `ModuleParameter`: Parameter definitions

**Built-in Modules:**
- `system_control`: File operations
- `memory_tools`: Preferences and memories
- `web_search`: Internet search (planned)

**Module Registration:**
```python
from badi.modules.base import Module, register_module

class MyModule(Module):
    name = "my_module"
    # ... implementation
    
register_module(MyModule())
```

### 5. System Layer
**Purpose**: OS and network adapters

**Adapters:**
- `os_adapter.py`: File system, process management
- `http_adapter.py`: HTTP requests
- Platform-specific implementations

### 6. Memory System
**Purpose**: Long-term storage and retrieval

**Components:**
- **Relational DB** (SQLite + SQLAlchemy):
  - User profiles
  - Conversation history
  - Task records
  - Preferences
  
- **Vector Store** (ChromaDB):
  - Semantic search
  - Context retrieval
  - Document embeddings

**Memory Flow:**
```
User Message → Save to DB → Generate Embedding → Store in Vector DB
             ↓
Context Needed → Vector Search + Recent History → Context
```

### 7. AI Backend Layer
**Purpose**: Model abstraction and selection

**Backends:**
- `local_llama_cpp.py`: Local GGUF models
- `local_vllm.py`: vLLM server
- `cloud_backend.py`: OpenAI, Anthropic, Gemini

**Selection Logic:**
```
Task Request
    ↓
Mode Check (local/cloud/hybrid)
    ↓
Availability Check
    ↓
Fallback Logic
    ↓
Selected Backend
```

## Data Flow

### Chat Flow
```
User: "Tell me about AI"
    ↓
[Interaction Layer] Parse & Normalize
    ↓
[Core - Router] Classify as chat
    ↓
[Memory] Fetch recent context
    ↓
[AI Backend] Generate response
    ↓
[Memory] Save interaction
    ↓
[Interaction Layer] Format response
    ↓
User: [Response]
```

### Task Flow
```
User: "Organize my downloads"
    ↓
[Interaction Layer] Parse & Normalize
    ↓
[Core - Router] Classify as task
    ↓
[Core - Planner] Create execution plan:
    1. Scan downloads
    2. Categorize files
    3. Move to folders
    ↓
[Core - Policy] Check permissions
    ↓
[Core - Executor] Execute steps (parallel where possible)
    ↓
[Modules] system_control.scan_directory()
           system_control.organize_by_type()
    ↓
[Memory] Save task record
    ↓
[Core - Router] Generate summary
    ↓
User: "Organized 47 files into 5 categories"
```

## Key Design Principles

### 1. Privacy-First
- Local-first execution by default
- Explicit cloud API calls only when needed
- User controls all data

### 2. Controlled Autonomy
- Confirmation for destructive operations
- Clear permission boundaries
- User always in control

### 3. Modularity
- Loosely coupled components
- Plugin-based modules
- Easy to extend and customize

### 4. Transparency
- Clear logging
- Explainable plans
- Visible decision-making

### 5. Flexibility
- Multiple AI backends
- Configurable behavior
- Hybrid execution modes

## Extension Points

### Adding New Modules
1. Create new file in `badi/modules/`
2. Inherit from `Module` base class
3. Define capabilities and parameters
4. Implement `run()` method
5. Register with `register_module()`

### Adding New AI Backends
1. Implement backend class with `chat()` method
2. Add to backend selector logic
3. Update configuration options

### Adding New Interfaces
1. Create interface in `badi/interaction/`
2. Use `RequestRouter` for processing
3. Format responses appropriately

## Configuration

### Environment Variables
All configuration via `.env` file and `BADIConfig` class.

### Runtime Configuration
- Module enable/disable
- Backend selection
- Permission settings
- Resource limits

## Security Considerations

1. **File Access**: Modules declare allowed directories
2. **Network**: Optional network isolation
3. **API Keys**: Environment-only, never in code
4. **Confirmations**: Required for dangerous operations
5. **Sandboxing**: Future: module-level sandboxes

## Performance Optimization

1. **Lazy Loading**: Modules load on first use
2. **Caching**: Backend instances cached
3. **Parallel Execution**: Steps run concurrently when safe
4. **Vector Search**: Optimized with indexes

## Future Architecture Plans

- **Multi-User Support**: User isolation and permissions
- **Plugin Marketplace**: Community modules
- **Advanced Memory**: Hierarchical memory systems
- **Distributed Execution**: Multi-machine orchestration
- **Fine-Grained Sandboxing**: Per-module security

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Language | Python 3.10+ |
| Web Framework | FastAPI, Uvicorn |
| CLI | Click |
| Database | SQLite, SQLAlchemy |
| Vector Store | ChromaDB |
| Local LLM | llama.cpp |
| GPU LLM | vLLM |
| Cloud APIs | OpenAI, Anthropic, Google |
| Voice | Whisper |
| Async | asyncio |
| Config | Pydantic |

## Diagrams

### Component Interaction
```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│  Interaction Layer          │
│  (CLI, API, Voice)          │
└──────┬──────────────────────┘
       │
┌──────▼──────────────────────┐
│  Core Layer                 │
│  Router → Planner/Executor  │
└──────┬──────────────────────┘
       │
       ├────────┬─────────┬────────┐
       │        │         │        │
┌──────▼────┐ ┌▼─────┐ ┌▼────┐  ┌▼───────┐
│  Modules  │ │Memory│ │ AI  │  │System  │
│           │ │      │ │Back │  │Adapter │
└───────────┘ └──────┘ └─────┘  └────────┘
```

This architecture enables B.A.D.I. to be powerful yet controllable, private yet capable, and simple yet extensible.
