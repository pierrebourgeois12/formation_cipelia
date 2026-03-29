# Prompts 💭

Ce dossier contient des instructions/prompts que vous pouvez donner à Claude.

## Types de prompts

### 1. Prompts de rôle
Donnez un rôle à Claude pour améliorer ses réponses.

**Exemple: expert_math.md**
```
Tu es un expert en mathématiques.

Quand l'utilisateur te pose une question sur les calculs:
1. Utilise l'outil calculate() si nécessaire
2. Explique le résultat
3. Donne du contexte mathématique

Sois pédagogique et clair.
```

### 2. Prompts d'instruction
Instructions pour utiliser spécifiquement les tools du MCP.

**Exemple: use_tools.md**
```
Tu as accès à ces tools:
- hello(name) → saluation
- calculate(operation, a, b) → calculs (+, -, *, /)
- read_resource(filename) → lire des ressources

Utilise-les quand l'utilisateur demande.
```

### 3. Prompts de contexte
Fournissez du contexte spécifique pour une tâche.

**Exemple: formation_llm.md**
```
Contexte: C'est une formation sur les MCPs.

Explique les concepts simplement.
Utilise les outils du MCP pour démontrer.
Sois pédagogique et engageant.
```

## Comment utiliser les prompts

### Dans Claude Desktop

Copier-collez le contenu du prompt au début de votre conversation:

```
[Contenu du prompt ici]

Maintenant, explique-moi comment fonctionnent les MCPs.
```

### Dans Claude API

```python
client = Anthropic()

with open("prompts/expert_math.md") as f:
    system_prompt = f.read()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Calcule 15 + 27"}
    ]
)
```

## Exemples de prompts

Vous trouverez des exemples de prompts ici. Modifiez-les selon vos besoins!
