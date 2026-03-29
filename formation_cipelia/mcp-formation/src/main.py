"""
MCP Formation - Serveur MCP simple pour la formation LLM

Montre comment:
1. Créer des tools MCP
2. Servir des resources
3. Utiliser des prompts
4. Tester en local et sur Claude
"""

from mcp.server.fastmcp import FastMCP
from mcp.types import Resource
import json
from pathlib import Path

# ════════════════════════════════════════════════════════════════════════════
# 1. INITIALISER LE SERVEUR
# ════════════════════════════════════════════════════════════════════════════

mcp = FastMCP("mcp-formation")


# ════════════════════════════════════════════════════════════════════════════
# 2. DÉFINIR LES TOOLS (ce que Claude peut appeler)
# ════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def hello(name: str) -> str:
    """Salue quelqu'un.
    
    Args:
        name: Le nom de la personne
    
    Returns:
        Une salutation personnalisée
    """
    return f"Bonjour {name}! 👋"


@mcp.tool()
async def calculate(operation: str, a: float, b: float) -> str:
    """Effectue une opération mathématique simple.
    
    Args:
        operation: "add", "subtract", "multiply", "divide"
        a: Premier nombre
        b: Deuxième nombre
    
    Returns:
        Le résultat de l'opération
    """
    try:
        if operation == "add":
            return f"{a} + {b} = {a + b}"
        elif operation == "subtract":
            return f"{a} - {b} = {a - b}"
        elif operation == "multiply":
            return f"{a} × {b} = {a * b}"
        elif operation == "divide":
            if b == 0:
                return "Erreur: Division par zéro!"
            return f"{a} ÷ {b} = {a / b}"
        else:
            return f"Opération inconnue: {operation}"
    except Exception as e:
        return f"Erreur: {e}"


@mcp.tool()
async def list_resources() -> str:
    """Liste toutes les ressources disponibles.
    
    Returns:
        Liste des ressources (documents, données, etc.)
    """
    resources_dir = Path(__file__).parent.parent / "resources"
    if not resources_dir.exists():
        return "Aucune ressource disponible"
    
    files = list(resources_dir.glob("*"))
    if not files:
        return "Aucune ressource disponible"
    
    result = "Ressources disponibles:\n"
    for file in files:
        result += f"  • {file.name}\n"
    return result


@mcp.tool()
async def read_resource(filename: str) -> str:
    """Lit le contenu d'une ressource.
    
    Args:
        filename: Nom du fichier dans le dossier resources/
    
    Returns:
        Le contenu du fichier
    """
    resources_dir = Path(__file__).parent.parent / "resources"
    file_path = resources_dir / filename
    
    if not file_path.exists():
        return f"Ressource '{filename}' non trouvée"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erreur lecture: {e}"


# ════════════════════════════════════════════════════════════════════════════
# 3. AJOUTER DES RESOURCES (pour Claude)
# ════════════════════════════════════════════════════════════════════════════

@mcp.resource("guide://formation")
async def get_formation_guide() -> str:
    """Guide de la formation"""
    return """
# GUIDE FORMATION MCP

## Qu'est-ce qu'un MCP?
Un Model Context Protocol server permet à Claude d':
1. Appeler des outils (tools)
2. Accéder à des ressources (documents, données)
3. Recevoir des instructions personnalisées (prompts)

## Structure du projet
- src/main.py       → Serveur MCP
- src/tools/        → Outils supplémentaires
- resources/        → Données et documents
- prompts/          → Instructions Claude

## Appels disponibles
- hello(name) → Salutation
- calculate(operation, a, b) → Calculs
- list_resources() → Liste ressources
- read_resource(filename) → Lire ressource
"""


@mcp.resource("guide://tools")
async def get_tools_guide() -> str:
    """Comment créer des tools"""
    return """
# CRÉER DES TOOLS

## Syntaxe de base
```python
@mcp.tool()
async def mon_outil(param: str) -> str:
    \"\"\"Description de l'outil\"\"\"
    return f"Résultat"
```

## Exemple complet
```python
@mcp.tool()
async def fetch_data(url: str) -> str:
    \"\"\"Récupère des données d'une URL\"\"\"
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

## Points importants
- Toujours utiliser async/await
- Ajouter des docstrings
- Spécifier les types (param: type -> return type)
- Gérer les erreurs
"""


# ════════════════════════════════════════════════════════════════════════════
# 4. FONCTION PRINCIPALE
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Lance le serveur MCP"""
    # Note: pas de print() ici - les messages interfèrent avec le protocole MCP (stdio)
    # qui communique uniquement via JSON sur stdout/stderr
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
