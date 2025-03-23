# agent.py
import random

DIRECTIONS = ["up", "down", "left", "right"]

class Agent:
    def __init__(self, chromosome_length=50):
        self.chromosome = [random.choice(DIRECTIONS) for _ in range(chromosome_length)]
        self.fitness = 0

    def move(self, maze):
        x, y = maze.start
        path = [(x, y)]
        for move in self.chromosome:
            if move == "up":
                x -= 1
            elif move == "down":
                x += 1
            elif move == "left":
                y -= 1
            elif move == "right":
                y += 1

            if maze.is_valid_move((x, y)):
                path.append((x, y))
            else:
                break  # Si choca, termina el recorrido

        return path
