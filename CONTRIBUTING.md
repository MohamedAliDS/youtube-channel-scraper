# Contributing to YouTube Channel Scraper

Thank you for your interest in contributing! We welcome contributions of all kinds.

## 🤝 Types of Contributions

- **Bug reports** - Found a problem? Let us know
- **Feature requests** - Have an idea? Share it
- **Code improvements** - Fork and submit a PR
- **Documentation** - Help us improve docs
- **Examples** - Share your use cases

## 🐛 Reporting Bugs

Before creating a bug report, please search existing issues first.

When reporting a bug, include:
- **Title**: Clear, descriptive
- **Description**: What happened and what should happen
- **Steps to reproduce**: Detailed steps
- **Environment**: Python version, OS, Chrome version
- **Logs**: Error messages and stack traces

Example:
```
Title: Selenium timeout when searching non-English channel names

Description:
When searching for channels with non-ASCII characters (e.g., "123테스트"),
the scraper times out after 15 seconds.

Steps:
1. Create Excel file with channel name "123테스트"
2. Run 01_channel_search_and_urls.ipynb
3. Wait for timeout

Environment:
- Python 3.10
- Chrome 120.0.6099
- Windows 11
```

## 💡 Feature Requests

Suggest features using GitHub Issues with the `enhancement` label.

Include:
- **Use case**: Why do you need this?
- **Proposed solution**: How should it work?
- **Alternatives**: Other approaches considered?

Example:
```
Title: Add support for batch processing from CSV files

Use case: Current implementation only accepts Excel files, 
but some users prefer CSV format.

Proposed solution:
- Add CSV support to DataProcessor.read_file()
- Auto-detect format by file extension
- Support both comma and semicolon delimiters

Alternative: Just convert CSV to Excel beforehand
```

## 🔧 Setting Up Development Environment

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/02_youtube_channel_scraper.git
cd 02_youtube_channel_scraper
```

### 2. Create Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Install Dependencies (with dev tools)
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### 4. Make Changes
- Follow the coding style (see below)
- Add tests for new features
- Update documentation

### 5. Test Your Changes
```bash
# Run unit tests
pytest tests/

# Check code style
black src/ tests/
flake8 src/ tests/
```

### 6. Commit & Push
```bash
git add .
git commit -m "feat: add CSV file support"
git push origin feature/your-feature-name
```

### 7. Create Pull Request
- Go to GitHub and click "New Pull Request"
- Clear title and description
- Link related issues

## 📝 Code Style

### Python Style Guide (PEP 8)

```python
# Good: Clear variable names
average_views = 125000
social_media_links = []

# Bad: Unclear abbreviations
avg_vw = 125000
sm_links = []
```

### Documentation

Every function should have a docstring:

```python
def search_channels(self, channel_names: List[str]) -> List[Dict]:
    """
    Search for multiple channels in parallel.
    
    Args:
        channel_names: List of channel names to search
        
    Returns:
        List of dicts with 'alias' and 'channel_url' keys
        
    Raises:
        ValueError: If channel_names is empty
        
    Example:
        >>> scraper = YouTubeScraper(max_workers=4)
        >>> results = scraper.search_channels(["MrBeast", "PewDiePie"])
        >>> print(results[0]["channel_url"])
        'https://www.youtube.com/@MrBeast'
    """
```

### Imports

Group imports:
```python
# 1. Standard library
import os
import logging
from pathlib import Path
from typing import List, Dict

# 2. Third-party
import pandas as pd
from selenium import webdriver

# 3. Local
from . import config
from . import selenium_utils
```

## ✅ Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] New features have tests
- [ ] Tests pass: `pytest`
- [ ] No linting errors: `flake8`
- [ ] Code formatted: `black`
- [ ] README updated if needed
- [ ] Commit messages are clear
- [ ] No sensitive data in commits

## 📚 Documentation

Help improve our docs:

1. **README** - Quick start and overview
2. **Docstrings** - Function documentation
3. **Notebooks** - Tutorial examples
4. **Comments** - Complex code sections
5. **CONTRIBUTING** - This file!

## 🧪 Testing

All new features should have tests:

```python
# tests/test_youtube_scraper.py
import pytest
from src.youtube_scraper import YouTubeScraper

def test_search_single_channel():
    scraper = YouTubeScraper(max_workers=1)
    result = scraper.search_single_channel("test_channel")
    
    assert result is not None or result is None  # Should always complete
    if result is not None:
        assert "youtube.com" in result

def test_search_channels_multiple():
    scraper = YouTubeScraper(max_workers=2)
    results = scraper.search_channels(["MrBeast", "PewDiePie"])
    
    assert len(results) == 2
    assert all("channel_url" in r for r in results)
```

## 🚀 Release Process

We follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

Example: `v1.2.3`

## 📞 Questions?

- Check existing issues/PRs first
- Ask in GitHub Discussions
- See README FAQ section
- Review code comments

## 🙏 Thank You!

Your contributions make this project better for everyone. Thank you for helping!

---

**Happy Contributing!** 🎉
