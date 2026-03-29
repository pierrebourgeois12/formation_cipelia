"""Tests pour les Tools du serveur Paris MCP"""

import pytest
from pathlib import Path
import sys

# Ajouter src au chemin pour les imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    get_location_weather,
    search_trees_by_species,
    get_trees_in_arrondissement,
    get_remarkable_trees
)


class TestWeatherTools:
    """Tests pour les outils météo"""

    @pytest.mark.asyncio
    async def test_get_location_weather_valid_coords(self):
        """Test avec des coordonnées valides (Paris)"""
        # Coordonnées de la Tour Eiffel
        result = await get_location_weather(48.8584, 2.2945)
        assert result is not None
        assert isinstance(result, str)
        assert "Météo" in result or "température" in result.lower()

    @pytest.mark.asyncio
    async def test_get_location_weather_format(self):
        """Test que le résultat a le bon format"""
        result = await get_location_weather(48.8584, 2.2945)
        # Vérifie que la réponse contient des emojis et des informations
        assert "🌤️" in result or "Température" in result or "°C" in result

    @pytest.mark.asyncio
    async def test_get_location_weather_different_locations(self):
        """Test avec différentes localisations"""
        # Paris
        result_paris = await get_location_weather(48.8584, 2.2945)
        # Lyon
        result_lyon = await get_location_weather(45.7640, 4.8357)
        
        assert result_paris is not None
        assert result_lyon is not None


class TestTreeTools:
    """Tests pour les outils d'arbres"""

    @pytest.mark.asyncio
    async def test_search_trees_common_species(self):
        """Test la recherche avec une espèce commune"""
        result = await search_trees_by_species("Platane", limit=5)
        assert result is not None
        assert isinstance(result, str)
        # Le résultat devrait mentionner soit des trouvailles soit l'impossibilité

    @pytest.mark.asyncio
    async def test_search_trees_with_limit(self):
        """Test avec limite de résultats"""
        result_small = await search_trees_by_species("Marronnier", limit=3)
        result_large = await search_trees_by_species("Marronnier", limit=10)
        assert result_small is not None
        assert result_large is not None

    @pytest.mark.asyncio
    async def test_get_trees_in_arrondissement(self):
        """Test la recherche par arrondissement"""
        result = await get_trees_in_arrondissement("PARIS 1ER ARRDT", limit=5)
        assert result is not None
        assert isinstance(result, str)
        # Le résultat devrait mentionner l'arrondissement

    @pytest.mark.asyncio
    async def test_get_remarkable_trees(self):
        """Test la récupération des arbres remarquables"""
        result = await get_remarkable_trees(limit=5)
        assert result is not None
        assert isinstance(result, str)
        assert "🌳" in result or "arbre" in result.lower()

    @pytest.mark.asyncio
    async def test_get_remarkable_trees_limit(self):
        """Test avec différentes limites"""
        result_small = await get_remarkable_trees(limit=3)
        result_large = await get_remarkable_trees(limit=20)
        assert len(result_small) >= 0
        assert len(result_large) >= len(result_small)


class TestToolErrorHandling:
    """Tests pour la gestion des erreurs"""

    @pytest.mark.asyncio
    async def test_search_trees_nonexistent_species(self):
        """Test avec une espèce qui n'existe probablement pas"""
        result = await search_trees_by_species("XyZzZ12345UnknownSpecies")
        assert result is not None
        # Devrait retourner un message d'erreur gracieux
        assert "Impossible" in result or "Aucun" in result or "trouvé" in result.lower()

    @pytest.mark.asyncio
    async def test_search_trees_empty_string(self):
        """Test avec une chaîne vide"""
        result = await search_trees_by_species("")
        assert result is not None  # Devrait retourner quelque chose, pas crasher

    @pytest.mark.asyncio
    async def test_search_trees_special_characters(self):
        """Test avec des caractères spéciaux"""
        result = await search_trees_by_species("Til%leul'", limit=5)
        assert result is not None  # Ne devrait pas crasher
