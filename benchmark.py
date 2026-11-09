"""TD3 - Exercice 4: benchmark des algorithmes du Puissance 4.

Lancement : python benchmark.py
Génère un CSV et deux figures PNG dans le dossier results/.
"""
import csv
from pathlib import Path

from game import create_board
from algorithms import minimax, alphabeta, mcts


def benchmark(board, algorithm, **kwargs):
    """Exécute un algorithme et retourne ses métriques de performance."""
    name = algorithm if isinstance(algorithm, str) else algorithm.__name__
    functions = {'minimax': minimax, 'alphabeta': alphabeta, 'mcts': mcts}
    fn = functions[name.lower().replace('-', '').replace('_', '')] if isinstance(algorithm, str) else algorithm
    result = fn(board, **kwargs)
    return {
        'algorithm': name,
        'configuration': (f"Depth {kwargs['depth']}" if 'depth' in kwargs
                          else f"{kwargs['num_simulations']} simulations"),
        'move': result['move'],
        'score': result['score'],
        'nodes_explored': result['nodes_explored'],
        'time': result['time'],
    }


def main():
    board = create_board()
    results = []
    for depth in (1, 2, 3, 4, 5):
        mm = benchmark(board, 'minimax', depth=depth)
        ab = benchmark(board, 'alphabeta', depth=depth)
        assert mm['score'] == ab['score'], f"Valeurs différentes à profondeur {depth}"
        assert ab['nodes_explored'] <= mm['nodes_explored'], f"Alpha-Beta explore plus de noeuds à profondeur {depth}"
        results.extend((mm, ab))

    for simulations in (100, 500, 1000, 2000):
        results.append(benchmark(board, 'mcts', num_simulations=simulations, seed=42))

    headers = ('algorithm', 'configuration', 'move', 'score', 'nodes_explored', 'time')
    print(f"{'Algorithm':<13} {'Configuration':<19} {'Move':>5} {'Score':>12} {'Nodes':>10} {'Time (s)':>10}")
    print('-' * 76)
    for item in results:
        print(f"{item['algorithm']:<13} {item['configuration']:<19} {item['move'] + 1:>5} "
              f"{item['score']:>12} {item['nodes_explored']:>10} {item['time']:>10.6f}")

    output = Path(__file__).resolve().parent / 'results'
    output.mkdir(exist_ok=True)
    with (output / 'benchmark_results.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('Matplotlib absent : installez-le avec python -m pip install matplotlib pour les graphiques.')
        return

    for name, label in (('minimax', 'Minimax'), ('alphabeta', 'Alpha-Beta')):
        subset = [r for r in results if r['algorithm'] == name]
        plt.plot(range(1, 6), [r['nodes_explored'] for r in subset], marker='o', label=label)
    plt.xlabel('Profondeur de recherche')
    plt.ylabel('Nombre de noeuds explorés')
    plt.title('Minimax et Alpha-Beta : noeuds explorés')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output / 'minimax_alphabeta_nodes.png', dpi=160)
    plt.close()

    budgets = (100, 500, 1000, 2000)
    times = [r['time'] for r in results if r['algorithm'] == 'mcts']
    plt.plot(budgets, times, marker='o', label='MCTS')
    plt.xlabel('Nombre de simulations')
    plt.ylabel('Temps d’exécution (s)')
    plt.title('MCTS : temps en fonction des simulations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output / 'mcts_time.png', dpi=160)
    plt.close()
    print(f'\nRésultats enregistrés dans : {output}')


if __name__ == '__main__':
    main()
