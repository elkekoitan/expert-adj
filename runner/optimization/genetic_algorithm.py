"""
Genetic Algorithm for EA Parameter Optimization
"""
import random
import logging
from typing import List, Dict, Any, Callable, Tuple
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Individual:
    """Individual in population"""
    genes: Dict[str, Any]
    fitness: float = 0.0


class GeneticAlgorithm:
    """
    Genetic Algorithm optimizer for EA parameters
    """

    def __init__(
        self,
        parameter_space: Dict[str, Dict[str, Any]],
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        elite_size: int = 2
    ):
        """
        Initialize GA optimizer

        Args:
            parameter_space: Parameter definitions
                {
                    "param_name": {
                        "type": "int|float|enum",
                        "min": min_value,
                        "max": max_value,
                        "step": step_value,
                        "values": [list for enum]
                    }
                }
            population_size: Population size
            generations: Number of generations
            mutation_rate: Mutation probability
            crossover_rate: Crossover probability
            elite_size: Number of best individuals to preserve
        """
        self.parameter_space = parameter_space
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size

        self.population: List[Individual] = []
        self.best_individual: Individual = None

    def optimize(
        self,
        fitness_function: Callable[[Dict[str, Any]], float],
        max_evaluations: int = None
    ) -> Tuple[Dict[str, Any], float]:
        """
        Run optimization

        Args:
            fitness_function: Function that evaluates parameter set
            max_evaluations: Maximum fitness evaluations

        Returns:
            (best_parameters, best_fitness)
        """
        logger.info("Starting Genetic Algorithm optimization")
        logger.info(f"Population: {self.population_size}, Generations: {self.generations}")

        evaluations = 0
        max_evals = max_evaluations or (self.population_size * self.generations)

        # Initialize population
        self.population = self._initialize_population()

        # Evaluate initial population
        for individual in self.population:
            if evaluations >= max_evals:
                break
            individual.fitness = fitness_function(individual.genes)
            evaluations += 1

        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.best_individual = self.population[0]

        logger.info(f"Initial best fitness: {self.best_individual.fitness}")

        # Evolution loop
        for generation in range(self.generations):
            if evaluations >= max_evals:
                break

            # Selection
            parents = self._selection()

            # Create offspring
            offspring = []
            while len(offspring) < self.population_size - self.elite_size:
                if evaluations >= max_evals:
                    break

                # Select two parents
                parent1, parent2 = random.sample(parents, 2)

                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                # Mutation
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                # Evaluate
                child1.fitness = fitness_function(child1.genes)
                evaluations += 1

                if evaluations < max_evals:
                    child2.fitness = fitness_function(child2.genes)
                    evaluations += 1

                offspring.extend([child1, child2])

            # Elitism: keep best individuals
            elite = self.population[:self.elite_size]

            # New population
            self.population = elite + offspring[:self.population_size - self.elite_size]
            self.population.sort(key=lambda x: x.fitness, reverse=True)

            # Update best
            if self.population[0].fitness > self.best_individual.fitness:
                self.best_individual = self.population[0]

            if generation % 10 == 0:
                logger.info(
                    f"Generation {generation}: "
                    f"Best={self.best_individual.fitness:.4f}, "
                    f"Avg={np.mean([ind.fitness for ind in self.population]):.4f}, "
                    f"Evals={evaluations}"
                )

        logger.info(f"Optimization complete. Best fitness: {self.best_individual.fitness}")
        return self.best_individual.genes, self.best_individual.fitness

    def _initialize_population(self) -> List[Individual]:
        """Generate random initial population"""
        population = []

        for _ in range(self.population_size):
            genes = {}
            for param_name, param_config in self.parameter_space.items():
                genes[param_name] = self._random_gene_value(param_config)

            population.append(Individual(genes=genes))

        return population

    def _random_gene_value(self, param_config: Dict[str, Any]) -> Any:
        """Generate random gene value based on parameter config"""
        param_type = param_config["type"]

        if param_type == "enum":
            return random.choice(param_config["values"])

        elif param_type == "int":
            min_val = param_config["min"]
            max_val = param_config["max"]
            step = param_config.get("step", 1)

            # Generate value aligned with step
            steps = (max_val - min_val) // step
            return min_val + random.randint(0, steps) * step

        elif param_type == "float":
            min_val = param_config["min"]
            max_val = param_config["max"]
            step = param_config.get("step", 0.01)

            # Generate value aligned with step
            steps = int((max_val - min_val) / step)
            return min_val + random.randint(0, steps) * step

        else:
            return param_config.get("default")

    def _selection(self) -> List[Individual]:
        """Tournament selection"""
        tournament_size = 3
        parents = []

        for _ in range(self.population_size):
            tournament = random.sample(self.population, tournament_size)
            winner = max(tournament, key=lambda x: x.fitness)
            parents.append(winner)

        return parents

    def _crossover(
        self,
        parent1: Individual,
        parent2: Individual
    ) -> Tuple[Individual, Individual]:
        """Single-point crossover"""
        genes1 = parent1.genes.copy()
        genes2 = parent2.genes.copy()

        # Random crossover point
        params = list(genes1.keys())
        if len(params) > 1:
            crossover_point = random.randint(1, len(params) - 1)

            for i, param in enumerate(params):
                if i >= crossover_point:
                    genes1[param], genes2[param] = genes2[param], genes1[param]

        return Individual(genes=genes1), Individual(genes=genes2)

    def _mutate(self, individual: Individual) -> Individual:
        """Random mutation"""
        genes = individual.genes.copy()

        for param_name, value in genes.items():
            if random.random() < self.mutation_rate:
                param_config = self.parameter_space[param_name]
                genes[param_name] = self._random_gene_value(param_config)

        return Individual(genes=genes)
