# Contributing to B.A.D.I.

Thank you for your interest in contributing to B.A.D.I.! We welcome contributions from the community.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   ggit clone https://github.com/restonuct/BADI
   cd badi
   ```
3. **Set up development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .  # Install in editable mode
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes**:
   ```bash
   pytest tests/
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Coding Standards

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Add tests for new features
- Keep functions focused and modular

## Module Development

To create a new module:

1. Create a new file in `badi/modules/your_module.py`
2. Inherit from `Module` base class
3. Define capabilities with clear descriptions
4. Implement the `run()` method
5. Register the module: `register_module(YourModule())`
6. Add tests in `tests/modules/test_your_module.py`

Example:
```python
from badi.modules.base import Module, ModuleCapability, register_module

class MyModule(Module):
    name = "my_module"
    description = "What this module does"
    capabilities = [
        ModuleCapability(
            name="do_something",
            description="Does something useful",
            parameters=[...]
        )
    ]
    
    async def run(self, capability: str, **kwargs):
        # Implementation
        pass

register_module(MyModule())
```

## Testing

We use pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=badi tests/

# Run specific test file
pytest tests/modules/test_system_control.py
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new code
- Update docs/ for architectural changes

## Code Review Process

1. All submissions require review
2. We'll provide constructive feedback
3. Address review comments promptly
4. Maintain a respectful, collaborative tone

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Join our community channels (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
