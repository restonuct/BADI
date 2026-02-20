"""Basic tests for B.A.D.I."""

def test_import():
    """Test that package can be imported"""
    import badi
    assert badi.__version__ == "0.1.0-alpha"

def test_config():
    """Test configuration loading"""
    from badi.config import get_config
    config = get_config()
    assert config is not None
    assert config.mode in ["local", "cloud", "hybrid"]
