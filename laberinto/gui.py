import tkinter as tk
from maze import Maze
from ga import GeneticAlgorithm
import random
import time

# Definir tamaños
MAZE_SIZE = 10  # El tamaño del laberinto en filas y columnas
CELL_SIZE = 40  # Tamaño de cada celda en píxeles

# Colores
WALL_COLOR = 'black'
PATH_COLOR = 'white'
START_COLOR = 'green'
END_COLOR = 'red'
AGENT_PATH_COLOR = 'blue'

# Inicializar la ventana de Tkinter
root = tk.Tk()
root.title("Algoritmo Genético - Resolución de Laberinto")
canvas = tk.Canvas(root, width=MAZE_SIZE * CELL_SIZE, height=MAZE_SIZE * CELL_SIZE)
canvas.pack()

# Función para dibujar el laberinto
def draw_maze(maze, path=[]):
    # Dibujar el laberinto
    for x in range(MAZE_SIZE):
        for y in range(MAZE_SIZE):
            x1, y1 = y * CELL_SIZE, x * CELL_SIZE
            x2, y2 = (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE
            if maze.grid[x][y] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, outline=WALL_COLOR)
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill=PATH_COLOR, outline=PATH_COLOR)
    
    # Dibujar el punto de inicio y fin
    start_x, start_y = maze.start
    end_x, end_y = maze.end
    canvas.create_oval(start_y * CELL_SIZE + 5, start_x * CELL_SIZE + 5,
                       (start_y + 1) * CELL_SIZE - 5, (start_x + 1) * CELL_SIZE - 5,
                       fill=START_COLOR)
    canvas.create_oval(end_y * CELL_SIZE + 5, end_x * CELL_SIZE + 5,
                       (end_y + 1) * CELL_SIZE - 5, (end_x + 1) * CELL_SIZE - 5,
                       fill=END_COLOR)
    
    # Dibujar el camino recorrido por el agente
    for (x, y) in path:
        canvas.create_rectangle(y * CELL_SIZE, x * CELL_SIZE, (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                                 fill=AGENT_PATH_COLOR, outline=AGENT_PATH_COLOR)

# Función para mostrar el laberinto con el mejor camino
def show_best_path(maze, path):
    draw_maze(maze, path)

# Función para ejecutar el algoritmo genético y visualizar el progreso
def run_genetic_algorithm():
    maze = Maze()
    ga = GeneticAlgorithm(maze, population_size=100, chromosome_length=150, mutation_rate=0.05)
    
    generations = 100
    for gen in range(generations):
        ga.create_next_generation()
        best_agent = ga.get_best_agent()
        best_path = best_agent.move(maze)

        # ✅ Aquí pones la condición para detener si llegó al final
        if best_path[-1] == maze.end:
            print("¡Se encontró un camino que llega al final!")
            break
        
        # Actualizar visualmente
        show_best_path(maze, best_path)
        generation_label.config(text=f"Generación {gen + 1}: Mejor fitness = {best_agent.fitness:.4f}")
        root.update()
        time.sleep(0.1)

    # Mostrar el mejor camino al final
    best_agent = ga.get_best_agent()
    best_path = best_agent.move(maze)
    show_best_path(maze, best_path)
    print(f"\nMejor camino encontrado después de {generations} generaciones:")
    print_path(maze, best_path)


# Función para imprimir el camino en la consola
def print_path(maze, path):
    grid = [row[:] for row in maze.grid]
    for x, y in path:
        if (x, y) != maze.start and (x, y) != maze.end:
            grid[x][y] = "*"
    
    print("\nLaberinto con el mejor camino encontrado:")
    for row in grid:
        print("".join(str(cell) if cell != "*" else "*" for cell in row))

# Etiqueta para mostrar la generación actual y el fitness
generation_label = tk.Label(root, text="Generación 0: Mejor fitness = 0.0000", font=("Arial", 14))
generation_label.pack()

# Botón para ejecutar el algoritmo
run_button = tk.Button(root, text="Iniciar Algoritmo Genético", command=run_genetic_algorithm, font=("Arial", 14))
run_button.pack()

# Dibujar el laberinto vacío al inicio
maze = Maze()
draw_maze(maze)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
