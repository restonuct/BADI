"""
B.A.D.I. - Balanced Autonomous Digital Intelligence

An open-source AI assistant framework with privacy-first design,
controlled autonomy, and modular architecture.
"""

__version__ = "0.1.0-alpha"
__author__ = "B.A.D.I. Contributors"
__license__ = "MIT"

from badi.config import get_config, reload_config

__all__ = ["get_config", "reload_config", "__version__"]
