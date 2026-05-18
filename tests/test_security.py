"""🔒 Test Security"""

import pytest
from src.utils.security import mask_secret

def test_mask_github_token():
    text = "Error: ghp_abc123secrettoken"
    result = mask_secret(text)
    assert "ghp_" in result
    assert "abc123secrettoken" not in result

def test_mask_docker_token():
    text = "Error: dckr_pat_supersecret"
    result = mask_secret(text)
    assert "dckr_pat_" in result
    assert "supersecret" not in result
