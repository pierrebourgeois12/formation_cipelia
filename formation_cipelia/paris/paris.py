from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("paris")

# Constants
PARIS_OPENDATA_BASE = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets"
WEATHER_API_BASE = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "mcp-paris/1.0"


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

# ============================================================================
# TOOLS MÉTÉO (Open-Meteo API - Gratuite, pas de clé nécessaire)
# ============================================================================


@mcp.tool()
async def get_location_weather(latitude: float, longitude: float) -> str:
    """Obtient la météo actuelle et les prévisions pour Paris.

    Retourne la température, les conditions météo, le vent, et les prévisions
    pour les prochains jours.
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

    # Weather codes mapping (simplifié)
    weather_codes = {
        0: "Ciel dégagé",
        1: "Principalement dégagé",
        2: "Partiellement nuageux",
        3: "Couvert",
        45: "Brouillard",
        48: "Brouillard givrant",
        51: "Bruine légère",
        53: "Bruine modérée",
        61: "Pluie légère",
        63: "Pluie modérée",
        65: "Pluie forte",
        71: "Neige légère",
        73: "Neige modérée",
        75: "Neige forte",
        95: "Orage"
    }

    current_weather_code = current.get("weather_code", 0)
    current_weather = weather_codes.get(current_weather_code, " Conditions inconnues")

    result = f"""
 Météo actuelle à Paris :
{current_weather}
 Température : {current.get('temperature_2m', 'N/A')}°C (ressenti {current.get('apparent_temperature', 'N/A')}°C)
 Humidité : {current.get('relative_humidity_2m', 'N/A')}%
 Vent : {current.get('wind_speed_10m', 'N/A')} km/h
 Précipitations : {current.get('precipitation', 'N/A')} mm

 Prévisions sur 3 jours :
"""

    if daily and "time" in daily:
        for i in range(min(3, len(daily["time"]))):
            day_weather_code = daily["weather_code"][i] if i < len(daily.get("weather_code", [])) else 0
            day_weather = weather_codes.get(day_weather_code, "Conditions inconnues")
            result += f"""
{daily['time'][i]} : {day_weather}
  Min: {daily['temperature_2m_min'][i]}°C | Max: {daily['temperature_2m_max'][i]}°C
  Précipitations: {daily['precipitation_sum'][i]} mm
"""

    return result


# ============================================================================
# TOOLS ARBRES DE PARIS
# ============================================================================

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
        info = f"""
Espèce: {tree.get('libellefrancais', 'N/A')} ({tree.get('genre', 'N/A')} {tree.get('espece', 'N/A')})
Adresse: {tree.get('adresse', 'N/A')} - {tree.get('arrondissement', 'N/A')}
Stade de développement: {tree.get('stadedeveloppement', 'N/A')}
Hauteur: {tree.get('hauteurenm', 'N/A')} m | Circonférence: {tree.get('circonferenceencm', 'N/A')} cm
Coordonnées: {tree.get('geo_point_2d', {}).get('lat', 'N/A')}, {tree.get('geo_point_2d', {}).get('lon', 'N/A')}
"""
        trees.append(info)

    return f" Trouvé {len(trees)} arbre(s) :\n" + "\n---\n".join(trees)


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

    return f" {len(trees)} arbre(s) dans {arrondissement} :\n" + "\n".join(trees)


@mcp.tool()
async def find_trees_near_location(latitude: float, longitude: float, radius_m: int = 500, limit: int = 10) -> str:
    """Trouve les arbres près d'une localisation donnée.

    Args:
        latitude: Latitude du point de recherche
        longitude: Longitude du point de recherche
        radius_m: Rayon de recherche en mètres (défaut 500m)
        limit: Nombre maximum de résultats (max 50, défaut 10)
    """
    url = f"{PARIS_OPENDATA_BASE}/les-arbres/records"
    params = {
        "where": f"distance(geo_point_2d, geom'POINT({longitude} {latitude})', {radius_m}m)",
        "limit": min(limit, 50)
    }

    data = await make_api_request(url, params)

    if not data or "results" not in data:
        return f"Impossible de trouver des arbres près de ({latitude}, {longitude})."

    if not data["results"]:
        return f"Aucun arbre trouvé dans un rayon de {radius_m}m."

    trees = []
    for tree in data["results"]:
        coords = tree.get('geo_point_2d', {})
        info = f"""
{tree.get('libellefrancais', 'Inconnu')}
 {tree.get('complement_addresse', 'N/A')}
 Hauteur: {tree.get('hauteurenm', 'N/A')} m
 Coordonnées: {coords.get('lat', 'N/A')}, {coords.get('lon', 'N/A')}
"""
        trees.append(info)

    return f" {len(trees)} arbre(s) trouvé(s) dans un rayon de {radius_m}m :\n" + "\n---\n".join(trees)


@mcp.tool()
async def get_remarkable_trees(limit: int = 20) -> str:
    """Retourne les arbres les plus remarquables de Paris.

    Les arbres remarquables sont identifiés par leur hauteur exceptionnelle,
    leur circonférence importante, ou leur caractère remarquable dans le dataset.
    Les résultats sont triés par hauteur décroissante.

    Args:
        limit: Nombre maximum de résultats à retourner (max 100, défaut 20)
    """
    url = f"{PARIS_OPENDATA_BASE}/les-arbres/records"

    # Recherche des arbres remarquables en triant par hauteur décroissante
    # On filtre pour ne garder que les arbres avec une hauteur significative (> 10m)
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
    for tree in data["results"]:
        coords = tree.get('geo_point_2d', {})
        height = tree.get('hauteurenm', 'N/A')
        circumference = tree.get('circonferenceencm', 'N/A')

        info = f"""
🌳 {tree.get('libellefrancais', 'Inconnu')} ({tree.get('genre', 'N/A')} {tree.get('espece', 'N/A')})
📍 Adresse: {tree.get('adresse', 'N/A')} - {tree.get('arrondissement', 'N/A')}
📏 Hauteur: {height} m | Circonférence: {circumference} cm
🌱 Stade de développement: {tree.get('stadedeveloppement', 'N/A')}
🗺️ Coordonnées: {coords.get('lat', 'N/A')}, {coords.get('lon', 'N/A')}
"""
        trees.append(info)

    return f"🌲 {len(trees)} arbre(s) remarquable(s) de Paris (triés par hauteur) :\n" + "\n---\n".join(trees)


def main():
    """Lance le serveur MCP Paris."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
