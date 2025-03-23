# main.py
from maze import Maze
from ga import GeneticAlgorithm

def print_path(maze, path):
    grid = [row[:] for row in maze.grid]
    for x, y in path:
        if (x, y) != maze.start and (x, y) != maze.end:
            grid[x][y] = "*"

    print("\nLaberinto con el mejor camino encontrado:")
    for row in grid:
        print("".join(str(cell) if cell != "*" else "*" for cell in row))

def main():
    maze = Maze()
    ga = GeneticAlgorithm(maze, population_size=100, chromosome_length=50, mutation_rate=0.05)

    generations = 100
    for gen in range(generations):
        ga.create_next_generation()
        best = ga.get_best_agent()
        print(f"Generación {gen + 1}: Mejor fitness = {best.fitness:.4f}")

        if best.fitness > 0.5:
            print("¡Se encontró una buena solución!")
            break

    best_agent = ga.get_best_agent()
    best_path = best_agent.move(maze)
    print_path(maze, best_path)

if __name__ == "__main__":
    main()
