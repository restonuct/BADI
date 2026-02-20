# Deploying B.A.D.I. to GitHub

This guide walks you through deploying the B.A.D.I. project as an open-source repository on GitHub.

## Prerequisites

- Git installed on your system
- GitHub account
- SSH key configured with GitHub (or use HTTPS)

## Step 1: Initialize Git Repository

From the project root directory:

```bash
cd badi-project
git init
```

## Step 2: Create .gitignore

Already created - verify it exists:
```bash
cat .gitignore
```

## Step 3: Create Initial Commit

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: B.A.D.I. v0.1.0-alpha

- Complete modular architecture
- Local and cloud AI backend support
- Module system with file management and memory
- CLI interface
- SQLite + ChromaDB memory system
- Full documentation and quick start guide"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `badi`
3. Description: "B.A.D.I. - Balanced Autonomous Digital Intelligence: An open-source AI assistant framework"
4. Choose: **Public** (for open source)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 5: Link Local to GitHub

GitHub will show you commands. Use these (replace with your username):

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/badi.git

# Or with SSH:
git remote add origin git@github.com:YOUR_USERNAME/badi.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 6: Configure Repository Settings

On GitHub repository page:

### Add Topics
Settings → General → Topics:
- `ai`
- `artificial-intelligence`
- `assistant`
- `chatbot`
- `llm`
- `local-llm`
- `python`
- `open-source`

### Enable Discussions
Settings → Features → ✓ Discussions

### Add Description
Settings → General → About:
- Description: "Privacy-first AI assistant with local-first execution and modular architecture"
- Website: (if you have one)
- ✓ Releases
- ✓ Packages

## Step 7: Create Release

1. Go to Releases → Create a new release
2. Tag: `v0.1.0-alpha`
3. Title: `B.A.D.I. v0.1.0 Alpha Release`
4. Description:
```markdown
## 🎉 First Alpha Release!

B.A.D.I. (Balanced Autonomous Digital Intelligence) is now available for early adopters and contributors.

### ✨ Features
- 🔒 Privacy-first design with local-first execution
- 🧩 Modular architecture with extensible plugins
- 🤖 Multiple AI backend support (local, OpenAI, Anthropic, Google)
- 💾 Sophisticated memory system (SQL + vector embeddings)
- 📁 File management and automation capabilities
- 🎯 Task planning and execution
- 💬 Conversational interface

### 📦 Installation

pip install -r requirements.txt

### 🚀 Quick Start
See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

### ⚠️ Alpha Status
This is an alpha release. APIs may change. Not recommended for production use.

### 📝 Documentation
- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)

### 🙏 Contributors
Thank you to all early contributors!

**Full Changelog**: Initial release
```

5. ✓ Set as a pre-release
6. Click "Publish release"

## Step 8: Add README Badges

Update README.md with your repository URL:

```markdown
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-alpha-orange)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/badi)](https://github.com/YOUR_USERNAME/badi/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/badi)](https://github.com/YOUR_USERNAME/badi/issues)
```

Commit and push:
```bash
git add README.md
git commit -m "Add repository badges"
git push
```

## Step 9: Create GitHub Actions (Optional)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest tests/
```

## Step 10: Promote Your Project

### On GitHub
- ⭐ Star your own repository
- 📌 Pin it to your profile

### Social Media
Share on:
- Reddit: r/Python, r/MachineLearning, r/LocalLLaMA
- Twitter/X with hashtags: #AI #OpenSource #Python #LLM
- Hacker News (Show HN)
- Dev.to / Hashnode blog post

### Communities
- Add to Awesome lists
- Post in relevant Discord/Slack communities
- Share in AI/ML forums

## Step 11: Set Up Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`

## Step 12: Add Contributing Guidelines

Already created in `CONTRIBUTING.md` - verify it's complete.

## Step 13: Ongoing Maintenance

### Regular Tasks
- [ ] Respond to issues within 48 hours
- [ ] Review pull requests promptly
- [ ] Update documentation as needed
- [ ] Create milestone releases
- [ ] Maintain CHANGELOG.md

### Version Updates
```bash
# Update version in setup.py and __init__.py
# Create new release on GitHub
# Tag the commit
git tag v0.2.0
git push origin v0.2.0
```

## Troubleshooting

### Push Rejected
```bash
git pull origin main --rebase
git push origin main
```

### Large Files
If you have model files:
```bash
# Use Git LFS
git lfs install
git lfs track "*.gguf"
git add .gitattributes
git commit -m "Add Git LFS support"
```

Or better: Don't commit models, document where to download them.

## License Verification

Ensure LICENSE file contains MIT License and your name/year.

## Security

- Never commit `.env` files with API keys
- Verify `.gitignore` is comprehensive
- Use GitHub security scanning
- Add security policy (SECURITY.md)

## Success Checklist

- [x] Repository created and public
- [x] README with clear description
- [x] Quick start guide
- [x] Contributing guidelines
- [x] License file
- [x] .gitignore configured
- [x] Initial release created
- [x] Documentation complete
- [x] Topics/tags added
- [ ] GitHub Actions (optional)
- [ ] Community features enabled
- [ ] Social promotion completed

## Next Steps

1. Watch for stars and issues
2. Engage with community
3. Iterate based on feedback
4. Build contributor community
5. Create roadmap for v1.0

Congratulations! Your project is now open source! 🎉
