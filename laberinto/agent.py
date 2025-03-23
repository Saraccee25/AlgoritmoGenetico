import random

DIRECTIONS = ["up", "down", "left", "right"]

class Agent:
    def __init__(self, chromosome_length=50):
        self.chromosome = [random.choice(DIRECTIONS) for _ in range(chromosome_length)]
        self.fitness = 0

    def move(self, maze):
        x, y = maze.start
        path = [(x, y)]
        visited = set(path)  # Usamos un conjunto para evitar repeticiones

        for move in self.chromosome:
            new_x, new_y = x, y
            if move == "up":
                new_x -= 1
            elif move == "down":
                new_x += 1
            elif move == "left":
                new_y -= 1
            elif move == "right":
                new_y += 1

            if maze.is_valid_move((new_x, new_y)) and (new_x, new_y) not in visited:
                x, y = new_x, new_y
                path.append((x, y))
                visited.add((x, y))  # Marcar como visitado

            if (x, y) == maze.end:
                break  # Ya llegó, no necesita seguir

        return path
