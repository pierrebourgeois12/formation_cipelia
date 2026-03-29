"""Tests pour les Resources du serveur Paris MCP"""

import pytest
from pathlib import Path
import sys
import json

# Ajouter src au chemin
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    get_paris_guide,
    get_arrondissements_data,
    get_monuments
)


class TestResourcesExist:
    """Tests pour vérifier que les ressources existent et sont accessibles"""

    @pytest.mark.asyncio
    async def test_paris_guide_resource(self):
        """Test que la ressource guide Paris existe"""
        resource = await get_paris_guide()
        assert resource is not None
        assert resource.uri == "uri://paris/guide"
        assert "Paris" in resource.name or "guide" in resource.name.lower()
        assert resource.contents is not None
        assert len(resource.contents) > 0

    @pytest.mark.asyncio
    async def test_paris_guide_content_format(self):
        """Test le format du contenu du guide"""
        resource = await get_paris_guide()
        content = resource.contents
        assert isinstance(content, str)
        assert len(content) > 10  # Doit avoir du contenu

    @pytest.mark.asyncio
    async def test_arrondissements_resource(self):
        """Test que la ressource arrondissements existe"""
        resource = await get_arrondissements_data()
        assert resource is not None
        assert resource.uri == "uri://paris/arrondissements"
        assert "arrondissement" in resource.name.lower()
        assert resource.mimeType == "application/json"

    @pytest.mark.asyncio
    async def test_arrondissements_json_format(self):
        """Test que les données arrondissements sont du JSON valide"""
        resource = await get_arrondissements_data()
        try:
            data = json.loads(resource.contents)
            assert "arrondissements" in data
            assert isinstance(data["arrondissements"], list)
            assert len(data["arrondissements"]) > 0
        except json.JSONDecodeError:
            pytest.fail("Les données arrondissements ne sont pas du JSON valide")

    @pytest.mark.asyncio
    async def test_monuments_resource(self):
        """Test que la ressource monuments existe"""
        resource = await get_monuments()
        assert resource is not None
        assert resource.uri == "uri://paris/monuments"
        assert "monument" in resource.name.lower()
        assert resource.contents is not None


class TestResourceContent:
    """Tests pour vérifier la qualité du contenu des ressources"""

    @pytest.mark.asyncio
    async def test_guide_contains_key_information(self):
        """Test que le guide contient des infos clés sur Paris"""
        resource = await get_paris_guide()
        content = resource.contents.lower()
        
        # Vérifier quelques éléments clés
        key_topics = ["paris", "métro", "arrondissement"]
        found_topics = [topic for topic in key_topics if topic in content]
        assert len(found_topics) > 0, f"Guide doit mentionner: {key_topics}"

    @pytest.mark.asyncio
    async def test_monuments_contains_structures(self):
        """Test que les monuments contiennent des monuments connus"""
        resource = await get_monuments()
        content = resource.contents.lower()
        
        # Monuments parisiens connus
        monuments = ["eiffel", "louvre", "notre-dame", "arc"]
        found = [m for m in monuments if m in content]
        assert len(found) > 0, "Devrait contenir les monuments parisiens connus"

    @pytest.mark.asyncio
    async def test_arrondissements_structure(self):
        """Test la structure des données arrondissements"""
        resource = await get_arrondissements_data()
        data = json.loads(resource.contents)
        
        # Chaque arrondissement devrait avoir certains champs
        if data["arrondissements"]:
            first_arr = data["arrondissements"][0]
            assert "numero" in first_arr
            assert "nom" in first_arr
            # Attractions est optionnel mais souhaitable
            if "attractions" in first_arr:
                assert isinstance(first_arr["attractions"], list)


class TestResourceMetadata:
    """Tests pour les métadonnées des ressources"""

    @pytest.mark.asyncio
    async def test_resource_mime_types(self):
        """Test que chaque ressource a le bon MIME type"""
        guide = await get_paris_guide()
        assert guide.mimeType == "text/plain"
        
        arrondissements = await get_arrondissements_data()
        assert arrondissements.mimeType == "application/json"
        
        monuments = await get_monuments()
        assert monuments.mimeType == "text/plain"

    @pytest.mark.asyncio
    async def test_resource_uris_unique(self):
        """Test que chaque ressource a un URI unique"""
        guide = await get_paris_guide()
        arrondissements = await get_arrondissements_data()
        monuments = await get_monuments()
        
        uris = [guide.uri, arrondissements.uri, monuments.uri]
        assert len(uris) == len(set(uris)), "Les URIs doivent être uniques"
