# TD3 - Game Search - Correction sur le code original

Cette version conserve `game.py`, les fichiers `static/` et `templates/`, ainsi que la structure et les traces de `algorithms.py` du professeur.

Les TODO de `algorithms.py` sont remplis : Minimax, Alpha-Beta, UCT et rétropropagation MCTS. `app.py` utilise maintenant `import algorithms`, car son import original `algorithms_sol` faisait référence à un fichier absent de l'archive.

## Installation

```powershell
python -m pip install -r requirements.txt
python app.py
```

Ouvrir http://localhost:5000

## Exercice 4

```powershell
python benchmark.py
```

Le script écrit un CSV et deux graphiques PNG dans `results/`.
