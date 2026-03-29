"""
Paris MCP Server - Formation complète
Montre comment créer un serveur MCP avec:
1. Tools (APIs externes)
2. Resources (documents et données)
3. Prompts (instructions pour Claude)
"""

from typing import Any
import httpx
from pathlib import Path
import json
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

# ════════════════════════════════════════════════════════════════════════════
# INITIALISATION DU SERVEUR
# ════════════════════════════════════════════════════════════════════════════

mcp = FastMCP("paris")

# Constants
PARIS_OPENDATA_BASE = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets"
WEATHER_API_BASE = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "mcp-paris/1.0"

# Chemins vers les ressources
BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
PROMPTS_DIR = BASE_DIR / "prompts"


async def make_api_request(url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to API with proper error handling."""
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None


# ════════════════════════════════════════════════════════════════════════════
# 1. TOOLS (Outils que Claude peut appeler)
# ════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def get_location_weather(latitude: float, longitude: float) -> str:
    """Obtient la météo actuelle et les prévisions pour une localisation.

    Retourne la température, les conditions météo, le vent, et les prévisions
    pour les prochains jours.

    Args:
        latitude: Latitude du point d'intérêt
        longitude: Longitude du point d'intérêt
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,precipitation_probability,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Paris",
        "forecast_days": 3
    }

    data = await make_api_request(WEATHER_API_BASE, params)

    if not data:
        return "Impossible de récupérer les données météo."

    current = data.get("current", {})
    daily = data.get("daily", {})

    weather_codes = {
        0: "Ciel dégagé", 1: "Principalement dégagé", 2: "Partiellement nuageux",
        3: "Couvert", 45: "Brouillard", 48: "Brouillard givrant",
        51: "Bruine légère", 53: "Bruine modérée", 61: "Pluie légère",
        63: "Pluie modérée", 65: "Pluie forte", 71: "Neige légère",
        73: "Neige modérée", 75: "Neige forte", 95: "Orage"
    }

    current_weather_code = current.get("weather_code", 0)
    current_weather = weather_codes.get(current_weather_code, "Conditions inconnues")

    result = f"""🌤️ Météo actuelle :
{current_weather}
🌡️ Température : {current.get('temperature_2m', 'N/A')}°C (ressenti {current.get('apparent_temperature', 'N/A')}°C)
💨 Humidité : {current.get('relative_humidity_2m', 'N/A')}%
🌬️ Vent : {current.get('wind_speed_10m', 'N/A')} km/h
💧 Précipitations : {current.get('precipitation', 'N/A')} mm

📅 Prévisions sur 3 jours :
"""

    if daily and "time" in daily:
        for i in range(min(3, len(daily["time"]))):
            day_weather_code = daily["weather_code"][i] if i < len(daily.get("weather_code", [])) else 0
            day_weather = weather_codes.get(day_weather_code, "Conditions inconnues")
            result += f"""{daily['time'][i]} : {day_weather}
  Min: {daily['temperature_2m_min'][i]}°C | Max: {daily['temperature_2m_max'][i]}°C
  Précipitations: {daily['precipitation_sum'][i]} mm
"""

    return result


@mcp.tool()
async def search_trees_by_species(species: str, limit: int = 10) -> str:
    """Recherche des arbres à Paris par espèce (nom français).

    Args:
        species: Nom de l'espèce en français (ex: "Platane", "Marronnier", "Tilleul")
        limit: Nombre maximum de résultats (max 100, défaut 10)
    """
    url = f"{PARIS_OPENDATA_BASE}/les-arbres/records"
    params = {
        "where": f"libellefrancais LIKE '{species}'",
        "limit": min(limit, 100)
    }

    data = await make_api_request(url, params)

    if not data or "results" not in data:
        return f"Impossible de trouver des arbres de l'espèce '{species}'."

    if not data["results"]:
        return f"Aucun arbre trouvé pour l'espèce '{species}'."

    trees = []
    for tree in data["results"]:
        info = f"""🌳 {tree.get('libellefrancais', 'N/A')} ({tree.get('genre', 'N/A')} {tree.get('espece', 'N/A')})
📍 {tree.get('adresse', 'N/A')} - {tree.get('arrondissement', 'N/A')}
📏 H: {tree.get('hauteurenm', 'N/A')}m | 🎯 C: {tree.get('circonferenceencm', 'N/A')}cm
"""
        trees.append(info)

    return f"✅ Trouvé {len(trees)} arbre(s) :\n" + "\n---\n".join(trees)


@mcp.tool()
async def get_trees_in_arrondissement(arrondissement: str, limit: int = 10) -> str:
    """Liste les arbres dans un arrondissement de Paris.

    Args:
        arrondissement: Nom de l'arrondissement (ex: "PARIS 1ER ARRDT", "PARIS 18E ARRDT")
        limit: Nombre maximum de résultats (max 100, défaut 10)
    """
    url = f"{PARIS_OPENDATA_BASE}/les-arbres/records"
    params = {
        "where": f"arrondissement = '{arrondissement}'",
        "limit": min(limit, 100)
    }

    data = await make_api_request(url, params)

    if not data or "results" not in data:
        return f"Impossible de récupérer les arbres de {arrondissement}."

    if not data["results"]:
        return f"Aucun arbre trouvé dans {arrondissement}."

    trees = []
    for tree in data["results"]:
        info = f"{tree.get('libellefrancais', 'Inconnu')} - {tree.get('adresse', 'Adresse inconnue')} | H: {tree.get('hauteurenm', 'N/A')}m"
        trees.append(info)

    return f"🌲 {len(trees)} arbre(s) dans {arrondissement} :\n" + "\n".join(trees)


@mcp.tool()
async def get_remarkable_trees(limit: int = 20) -> str:
    """Retourne les arbres les plus remarquables de Paris.

    Les arbres remarquables sont identifiés par leur hauteur exceptionnelle.
    Les résultats sont triés par hauteur décroissante.

    Args:
        limit: Nombre maximum de résultats (max 100, défaut 20)
    """
    url = f"{PARIS_OPENDATA_BASE}/les-arbres/records"
    params = {
        "where": "hauteurenm > 10",
        "order_by": "hauteurenm desc",
        "limit": min(limit, 100)
    }

    data = await make_api_request(url, params)

    if not data or "results" not in data:
        return "Impossible de récupérer les arbres remarquables de Paris."

    if not data["results"]:
        return "Aucun arbre remarquable trouvé."

    trees = []
    for tree in data["results"][:limit]:
        height = tree.get('hauteurenm', 'N/A')
        circumference = tree.get('circonferenceencm', 'N/A')
        info = f"""🌳 {tree.get('libellefrancais', 'Inconnu')} ({tree.get('genre', 'N/A')} {tree.get('espece', 'N/A')})
📍 {tree.get('adresse', 'N/A')} - {tree.get('arrondissement', 'N/A')}
📏 Hauteur: {height}m | Circonférence: {circumference}cm
🌱 Stade: {tree.get('stadedeveloppement', 'N/A')}
"""
        trees.append(info)

    return f"🏆 {len(trees)} arbre(s) remarquable(s) (triés par hauteur) :\n" + "\n---\n".join(trees)


# ════════════════════════════════════════════════════════════════════════════
# 2. RESOURCES (Documents et données que Claude peut consulter)
# ════════════════════════════════════════════════════════════════════════════

@mcp.resource("uri://paris/guide")
async def get_paris_guide() -> Resource:
    """Guide complet sur la visite de Paris."""
    guide_path = RESOURCES_DIR / "paris_guide.txt"
    content = guide_path.read_text(encoding='utf-8')
    return Resource(
        uri="uri://paris/guide",
        name="Guide Paris",
        description="Guide complet pour visiter Paris",
        mimeType="text/plain",
        contents=content
    )


@mcp.resource("uri://paris/arrondissements")
async def get_arrondissements_data() -> Resource:
    """Données structurées sur les arrondissements de Paris."""
    data_path = RESOURCES_DIR / "arrondissements.json"
    if data_path.exists():
        content = data_path.read_text(encoding='utf-8')
    else:
        # Données par défaut
        content = json.dumps({
            "arrondissements": [
                {"numero": 1, "nom": "Île de la Cité et Palais-Royal", "attractions": ["Cathédrale Notre-Dame", "Palais-Royal"]},
                {"numero": 8, "nom": "Élysée et Champs-Élysées", "attractions": ["Élysée", "Champs-Élysées", "Arc de Triomphe"]},
                {"numero": 18, "nom": "Montmartre", "attractions": ["Basilique du Sacré-Cœur", "Moulin Rouge"]},
            ]
        }, ensure_ascii=False, indent=2)
    
    return Resource(
        uri="uri://paris/arrondissements",
        name="Arrondissements de Paris",
        description="Données sur les 20 arrondissements de Paris",
        mimeType="application/json",
        contents=content
    )


@mcp.resource("uri://paris/monuments")
async def get_monuments() -> Resource:
    """Liste des monuments principaux de Paris."""
    monuments_path = RESOURCES_DIR / "monuments.txt"
    if monuments_path.exists():
        content = monuments_path.read_text(encoding='utf-8')
    else:
        content = """MONUMENTS PRINCIPAUX DE PARIS

🗼 MONUMENTS ICONIQUES:
1. Tour Eiffel (1889) - 324m, 7M de visiteurs/an
2. Arc de Triomphe (1836) - 50m de haut
3. Cathédrale Notre-Dame (1345) - Style Gothique
4. Basilique du Sacré-Cœur (1914) - Montmartre
5. Palais du Louvre (1692) - Plus grand musée du monde

🏛️ MUSÉES:
- Louvre: 9,6M visiteurs/an
- Musée d'Orsay: Impressionnisme
- Centre Pompidou: Art moderne

🌳 PARCS:
- Jardin du Luxembourg: 23 hectares
- Bois de Boulogne: 846 hectares
- Parc des Buttes-Chaumont: 25 hectares
"""
    
    return Resource(
        uri="uri://paris/monuments",
        name="Monuments de Paris",
        description="Description des principaux monuments et attractions",
        mimeType="text/plain",
        contents=content
    )


# ════════════════════════════════════════════════════════════════════════════
# 3. PROMPTS (Contexte et instructions pour Claude)
# ════════════════════════════════════════════════════════════════════════════

@mcp.prompt("paris-expert")
async def paris_expert_prompt() -> str:
    """Tu es un expert de Paris qui connaît bien la ville."""
    prompt_path = PROMPTS_DIR / "paris_expert.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    else:
        return """Tu es un expert de Paris spécialisé dans:
- L'histoire et l'architecture
- Les arrondissements et leurs caractéristiques
- Les arbres et la nature à Paris
- Les attractions et monuments
- La météo et la géographie

Utilise les ressources disponibles pour donner des réponses précises et engageantes."""


@mcp.prompt("guide-touriste")
async def guide_touriste_prompt() -> str:
    """Tu es un guide touristique enthousiaste."""
    prompt_path = PROMPTS_DIR / "guide_touriste.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    else:
        return """Tu es un guide touristique passionné par Paris!

Quand tu décris Paris:
- Sois enthousiaste et engageant 🎭
- Partage des anecdotes historiques 📖
- Donne des conseils pratiques 💡
- Utilise des emojis appropriés 🗼
- Recommande les meilleurs moments pour visiter 🌅

Aide les touristes à planifier leur visite idéale de Paris."""


def main():
    """Lance le serveur MCP Paris."""
    print("🇫🇷 Serveur MCP Paris démarré!")
    print("📚 Tools, Resources et Prompts disponibles")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
