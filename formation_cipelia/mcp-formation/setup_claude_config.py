"""Configuration automatique pour Claude Desktop"""

import json
import os
import sys
from pathlib import Path

def setup_claude_config():
    """Configure automatiquement claude_desktop_config.json"""
    
    if sys.platform == "win32":
        config_dir = os.path.join(os.getenv("APPDATA"), "Claude")
    elif sys.platform == "darwin":
        config_dir = os.path.expanduser("~/Library/Application Support/Claude")
    else:
        config_dir = os.path.expanduser("~/.config/Claude")
    
    config_file = os.path.join(config_dir, "claude_desktop_config.json")
    script_dir = str(Path(__file__).parent)
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs(config_dir, exist_ok=True)
    
    # Charger ou créer la configuration
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {"mcpServers": {}}
    
    # Ajouter notre MCP
    config["mcpServers"]["mcp-formation"] = {
        "command": "python",
        "args": ["-m", "src.main"],
        "cwd": script_dir
    }
    
    # Écrire la configuration
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration Claude Desktop réussie!")
    print(f"📄 Fichier: {config_file}")
    print(f"📍 Serveur: mcp-formation")
    print(f"📁 Chemin: {script_dir}")
    print("\n🔄 Relancez Claude Desktop complètement (fermeture + réouverture)")

if __name__ == "__main__":
    setup_claude_config()
