# MCP Formation 📚

Un serveur MCP minimaliste pour apprendre comment fonctionnent les MCPs et comment les tester.

## Structure

```
mcp-formation/
├── src/
│   ├── main.py              # 🔌 Serveur MCP principal
│   └── tools/               # 📦 Tools supplémentaires (optionnel)
├── resources/               # 📄 Données et documents
├── prompts/                 # 💭 Instructions pour Claude
├── tests/                   # 🧪 Tests
└── README.md
```

## Installation rapide

### 1. Créer l'environnement virtuel

```bash
python -m venv venv
source venv/bin/activate          # Mac/Linux
# OU
venv\Scripts\activate             # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer l'environnement

```bash
cp .env.example .env
```

## Tester en local

Lancer le serveur MCP:

```bash
python -m src.main
```

Vous devriez voir: `🚀 Serveur MCP Formation démarré`

Pour arrêter: **Ctrl+C**

## Tester sur Claude Desktop

### Option 1: Configuration automatique (Windows)

```bash
python setup_claude_config.py
```

Puis relancez Claude Desktop complètement (fermeture + réouverture).

### Option 2: Configuration manuelle

1. Ouvrez le fichier de configuration Claude:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Ajoutez (ou remplacez le contenu):

```json
{
  "mcpServers": {
    "mcp-formation": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/chemin/complet/vers/mcp-formation"
    }
  }
}
```

⚠️ **Remplacez `/chemin/complet/vers/mcp-formation`** par le chemin réel sur votre machine.

3. Relancez Claude Desktop complètement.

4. Testez! Dites à Claude:
   ```
   Appelle l'outil hello avec name="Formation"
   ```

## Les outils disponibles

### `hello(name: str) -> str`
Salue quelqu'un.

**Exemple**: `hello(name="Pierre")` → `"Bonjour Pierre! 👋"`

### `calculate(operation: str, a: float, b: float) -> str`
Effectue une opération mathématique: "add", "subtract", "multiply", "divide"

**Exemple**: `calculate(operation="add", a=10, b=5)` → `"10 + 5 = 15"`

### `list_resources() -> str`
Liste les ressources disponibles dans le dossier `resources/`.

### `read_resource(filename: str) -> str`
Lit le contenu d'une ressource.

## Comment ajouter un nouveau tool

1. Ouvrez `src/main.py`
2. Ajoutez une fonction avec `@mcp.tool()`:

```python
@mcp.tool()
async def mon_nouveau_outil(param: str) -> str:
    """Description de ce que fait cet outil"""
    return f"Résultat: {param}"
```

3. Testez: `python -m src.main`
4. Utilisez dans Claude: `Appelle mon_nouveau_outil avec param="test"`

## Comment ajouter une ressource

1. Créez un fichier dans le dossier `resources/` (ex: `data.txt`)
2. Lancez le serveur: `python -m src.main`
3. Utilisez dans Claude:
   ```
   Lis la ressource data.txt
   # Claude appellera: read_resource(filename="data.txt")
   ```

## Tests unitaires

Lancer les tests:

```bash
pytest tests/ -v
```

Créez vos tests dans `tests/test_*.py`:

```python
import pytest
from src.main import hello

@pytest.mark.asyncio
async def test_hello():
    result = await hello("Pierre")
    assert "Bonjour Pierre" in result
```

## Structure d'un MCP

```
Tool (outil)
  ↓
MCP Server (serveur)
  ↓
Claude
  ↓
Résultat
```

Claude peut:
1. 🔍 **Voir** tous les tools disponibles
2. 🎯 **Décider** quels tools appeler
3. 📞 **Appeler** les tools
4. 💬 **Répondre** à l'utilisateur avec les résultats

## Fichiers importants

| Fichier | Rôle |
|---------|------|
| `src/main.py` | Définit les tools et resources |
| `resources/` | Données accessibles par Claude |
| `prompts/` | Instructions personnalisées pour Claude |
| `tests/` | Tests unitaires |
| `claude_desktop_config.json` | Configuration Claude Desktop |

## Dépannage

### Le serveur ne démarre pas
```bash
python --version  # Doit être >= 3.10
pip install -r requirements.txt
```

### Claude ne voit pas le MCP
- Vérifiez le chemin dans le `.json` (doit être complet)
- Relancez Claude **complètement** (fermeture + réouverture)
- Testez d'abord en local: `python -m src.main`

## Exemples de prompts

Dans le dossier `prompts/`, vous pouvez créer des instructions pour guider Claude:

**prompts/expert.md**
```
Tu es un expert en mathématiques.
Quand l'utilisateur demande un calcul, utilise l'outil calculate.
Explique le résultat de façon pédagogique.
```

## Ressources

- [Docs MCP](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlopp/fastmcp)
- [Claude API](https://docllaude.ai)
