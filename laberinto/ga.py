# ga.py
import random
from agent import Agent
from math import dist

class GeneticAlgorithm:
    def __init__(self, maze, population_size=100, chromosome_length=50, mutation_rate=0.05):
        self.maze = maze
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_rate = mutation_rate
        self.population = [Agent(chromosome_length) for _ in range(population_size)]

    def evaluate_fitness(self):
        for agent in self.population:
            path = agent.move(self.maze)
            last_pos = path[-1]
            # Usamos distancia euclidiana a la meta como medida de fitness (cuanto menor, mejor)
            agent.fitness = 1 / (dist(last_pos, self.maze.end) + 1)

    def select_parents(self):
        # Selección por torneo
        tournament_size = 5
        selected = random.sample(self.population, tournament_size)
        selected.sort(key=lambda a: a.fitness, reverse=True)
        return selected[0], selected[1]

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.chromosome_length - 2)
        child_chromosome = (
            parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        )
        return Agent(self.chromosome_length), child_chromosome

    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] = random.choice(["up", "down", "left", "right"])
        return chromosome

    def create_next_generation(self):
        new_population = []

        self.evaluate_fitness()
        self.population.sort(key=lambda a: a.fitness, reverse=True)

        # Elitismo: mantener los mejores
        elite_count = int(0.1 * self.population_size)
        new_population.extend(self.population[:elite_count])

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child, child_chromosome = self.crossover(parent1, parent2)
            child.chromosome = self.mutate(child_chromosome)
            new_population.append(child)

        self.population = new_population

    def get_best_agent(self):
        return max(self.population, key=lambda a: a.fitness)
