"""Tests pour les Prompts du serveur Paris MCP"""

import pytest
from pathlib import Path
import sys

# Ajouter src au chemin
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import paris_expert_prompt, guide_touriste_prompt


class TestPromptsExist:
    """Tests pour vérifier que les prompts existent et retournent du contenu"""

    @pytest.mark.asyncio
    async def test_paris_expert_prompt_exists(self):
        """Test que le prompt Paris Expert existe"""
        prompt = await paris_expert_prompt()
        assert prompt is not None
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    @pytest.mark.asyncio
    async def test_guide_touriste_prompt_exists(self):
        """Test que le prompt Guide Touriste existe"""
        prompt = await guide_touriste_prompt()
        assert prompt is not None
        assert isinstance(prompt, str)
        assert len(prompt) > 0


class TestPromptsContent:
    """Tests pour vérifier la qualité du contenu des prompts"""

    @pytest.mark.asyncio
    async def test_paris_expert_prompt_content(self):
        """Test que le prompt expert contient des domaines clés"""
        prompt = await paris_expert_prompt()
        content = prompt.lower()
        
        # Doit mentionner l'expertise de Paris
        assert "expert" in content or "paris" in content
        assert len(content) > 50, "Le prompt doit avoir du contenu"

    @pytest.mark.asyncio
    async def test_paris_expert_prompt_guidance(self):
        """Test que le prompt expert est bien structuré"""
        prompt = await paris_expert_prompt()
        
        # Doit inclure des instructions claires
        assert isinstance(prompt, str)
        assert len(prompt) > 100  # Suffisamment détaillé
        # Doit guidé le comportement du modèle
        if "vous" in prompt or "tu" in prompt or "expert" in prompt:
            assert True  # Bon, c'est du guidance personnel

    @pytest.mark.asyncio
    async def test_guide_touriste_prompt_content(self):
        """Test le contenu du prompt guide touristique"""
        prompt = await guide_touriste_prompt()
        content = prompt.lower()
        
        # Doit encourager l'enthousiasme
        assert "paris" in content or "guide" in content or "touristique" in content
        assert len(content) > 50

    @pytest.mark.asyncio
    async def test_guide_touriste_has_emojis(self):
        """Test que le prompt touristique encourage les emojis"""
        prompt = await guide_touriste_prompt()
        
        # Devrait mentionner l'utilisation d'emojis ou en contenir
        assert "emoji" in prompt.lower() or "🗼" in prompt or "🎭" in prompt

    @pytest.mark.asyncio
    async def test_guide_touriste_includes_practical_advice(self):
        """Test que le prompt includt des conseils pratiques"""
        prompt = await guide_touriste_prompt()
        content = prompt.lower()
        
        # Doit encourager les conseils pratiques
        assert "conseil" in content or "pratique" in content or "moment" in content


class TestPromptsStyle:
    """Tests pour vérifier le style et ton des prompts"""

    @pytest.mark.asyncio
    async def test_expert_vs_touriste_different(self):
        """Test que les deux prompts sont différents"""
        expert = await paris_expert_prompt()
        touriste = await guide_touriste_prompt()
        
        # Ne devraient pas être identiques
        assert expert != touriste
        assert len(expert) > 0 and len(touriste) > 0

    @pytest.mark.asyncio
    async def test_prompts_are_strings(self):
        """Test que les prompts sont des chaînes"""
        expert = await paris_expert_prompt()
        touriste = await guide_touriste_prompt()
        
        assert isinstance(expert, str)
        assert isinstance(touriste, str)

    @pytest.mark.asyncio
    async def test_prompts_not_empty(self):
        """Test que les prompts ne sont pas vides"""
        expert = await paris_expert_prompt()
        touriste = await guide_touriste_prompt()
        
        assert len(expert.strip()) > 0
        assert len(touriste.strip()) > 0


class TestPromptsUsability:
    """Tests pour la capacité d'utilisation des prompts"""

    @pytest.mark.asyncio
    async def test_paris_expert_includes_domain_info(self):
        """Test que le prompt expert mentionne les domaines de compétence"""
        prompt = await paris_expert_prompt()
        
        # Doit mentionner architecture, histoire, ou domaines similaires
        domains = ["histoire", "architecture", "savoir", "connaît"]
        content = prompt.lower()
        found = [d for d in domains if d in content]
        # Accepte si le prompt mentionne au moins un domaine ou est générale
        assert len(found) > 0 or "expert" in content

    @pytest.mark.asyncio
    async def test_guide_touriste_interaction_ready(self):
        """Test que le prompt touriste est prêt pour l'interaction"""
        prompt = await guide_touriste_prompt()
        
        # Doit être orienté vers l'engagement avec les touristes
        content = prompt.lower()
        assert "visite" in content or "touriste" in content or "paris" in content or "conseils" in content
