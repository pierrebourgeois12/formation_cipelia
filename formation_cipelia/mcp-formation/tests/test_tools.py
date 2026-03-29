"""Tests pour les tools"""

import pytest
from src.main import hello, calculate


@pytest.mark.asyncio
async def test_hello():
    """Test le tool hello"""
    result = await hello("Pierre")
    assert "Bonjour Pierre" in result
    assert "👋" in result


@pytest.mark.asyncio
async def test_calculate_add():
    """Test addition"""
    result = await calculate("add", 10, 5)
    assert "15" in result
    assert "+" in result


@pytest.mark.asyncio
async def test_calculate_subtract():
    """Test soustraction"""
    result = await calculate("subtract", 10, 5)
    assert "5" in result
    assert "-" in result


@pytest.mark.asyncio
async def test_calculate_multiply():
    """Test multiplication"""
    result = await calculate("multiply", 10, 5)
    assert "50" in result


@pytest.mark.asyncio
async def test_calculate_divide():
    """Test division"""
    result = await calculate("divide", 10, 5)
    assert "2" in result


@pytest.mark.asyncio
async def test_calculate_divide_by_zero():
    """Test division par zéro"""
    result = await calculate("divide", 10, 0)
    assert "zéro" in result.lower()


@pytest.mark.asyncio
async def test_calculate_invalid_operation():
    """Test opération invalide"""
    result = await calculate("invalid", 10, 5)
    assert "inconnue" in result.lower()
