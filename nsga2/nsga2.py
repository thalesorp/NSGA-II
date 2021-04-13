#!/usr/bin/env python3
#
# A implementation of: NSGA-II
# Source: A fast and elitist multiobjective genetic algorithm: NSGA-II, 2002
# Article author: DEB, K. et al.
#
# Instituto Federal de Minas Gerais - Campus Formiga, Brazil
#
# Version 1.0
# (c) 2021 Thales Pinto <ThalesORP@gmail.com> under the GPL
#          http://www.gnu.org/copyleft/gpl.html
#

'''Main class of NSGA-II'''

from sys import maxsize
import random

from .population import Population

class NSGA2():
    '''Main class of the NSGA-II algorithm'''

    def __init__(self, generations, population_size, genome_min_value, genome_max_value, crossover_constant, crossover_rate):

        self.generations = generations

        # "N" on NSGA-II paper
        self.population_size = population_size

        self.genome_min_value = genome_min_value
        self.genome_max_value = genome_max_value

        # Distribution index. "nc" in NSGA-II paper
        self.crossover_constant = crossover_constant
        #self.crossover_constant = 5

        # Crossover probability. "pc" in NSGA-II paper
        self.crossover_rate = crossover_rate
        #self.crossover_rate = 0.9

        # Size of genome list
        # Attention! For Genetic Quantum, this value must be 1
        self.genotype_quantity = 1

        # Mutation probability. "pm" in NSGA-II paper
        self.mutation_rate = 1/self.genotype_quantity

        # Percentage of chance to disturbing one genotype of genome
        self.genotype_mutation_probability = 0.5

        # Percentage to disturb each genotype mutated
        self.disturb_percent = 0.5

        # "Rt" on NSGA-II paper
        self.population = Population(self.genotype_quantity, self.genome_min_value, self.genome_max_value)

    def run(self):
        '''Method responsible for running the main loop of NSGA-II'''

        debug = False
        plot = False

        if debug: print("# Initiating generation 0...")

        # Creating a parent population P0
        self.population.initiate(self.population_size//2)

        self.evaluate(self.population)

        fronts = self.fast_non_dominated_sort()
        #if debug: self._show_fronts(fronts)

        # "Q0" on NSGA-II paper
        offspring_population = self.usual_crossover()
        self.evaluate(offspring_population)

        best_front = None

        for i in range(self.generations):
            if debug: print("# Running generation " + str(i+1) + "...")

            # "Rt" population: union between "Pt" and "Qt", now with size of "2N"
            self.population.union(offspring_population)

            # "F" on NSGA-II paper
            fronts = self.fast_non_dominated_sort()

            best_front = fronts[0]

            self.crowding_distance_assignment(fronts)

            # "Pt+1" population
            next_population = self.new_population()

            i = 0
            while (next_population.size + fronts[i].size) <= self.population_size:
                next_population.union(fronts[i])
                i += 1

            # Sort(Fi, <n)
            self.sort_by_crowded_comparison(fronts[i])

            # "Pt+1" = "Pt+1" union fronts[i][1 : "N" - sizeof("Pt+1")]
            amount_to_insert = self.population_size - len(next_population.individuals)
            fronts[i].individuals = fronts[i].individuals[:amount_to_insert]
            next_population.union(fronts[i])

            self.population = next_population

            # Make new offspring population. "Qt+1" on NSGA-II paper
            offspring_population = self.crossover()
            self.evaluate(offspring_population)

        if debug: print(self._show_population(best_front))

        return best_front

    def evaluate(self, population):
        '''This method should be implemented by the heir class'''

        pass

    def new_population(self):
        '''Return a empty Population object'''

        return Population(self.genotype_quantity, self.genome_min_value, self.genome_max_value)

    def fast_non_dominated_sort(self):
        '''Sort the individuals according to they dominance and sort them into fronts
        Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual
        Also, the first front is created
        Then the remaining individuals are divided into fronts'''

        self.population.reset_fronts()

        # Initializing the fronts list and the first front
        fronts = list()
        fronts.append(self.new_population())

        # Each of individuals checks if dominates or is dominated with everyone else
        for i in range(self.population.size):
            for j in range(self.population.size):
                current_individual = self.population.individuals[i]
                other_individual = self.population.individuals[j]

                if i != j: # Ignoring itself
                    # Checking if dominates or are dominated by the other individuals
                    if current_individual.dominates(other_individual):
                        current_individual.dominated_by.append(other_individual)
                    elif other_individual.dominates(current_individual):
                        current_individual.domination_count += 1

            # Checking if current individual is eligible to the first front
            if current_individual.domination_count == 0:
                if current_individual not in fronts[0].individuals:
                    current_individual.rank = 1
                    fronts[0].insert(current_individual)

        # Temporary front
        #current_front = self.new_population()

        i = 0
        while len(fronts[i].individuals) > 0:
            fronts.append(self.new_population())
            for individual in fronts[i].individuals:
                for dominated_individual in individual.dominated_by:
                    dominated_individual.domination_count -= 1

                    # Now if this dominated individual aren't dominated by anyone, insert into next front
                    if dominated_individual.domination_count == 0:

                        # "+1" becasue "i" is index value, and rank starts from 1 and not 0
                        # "+1" because the rank it's for the next front
                        dominated_individual.rank = i+2
                        fronts[len(fronts)-1].insert(dominated_individual)
            i += 1

        # Deleting empty last front created in previously loops
        del fronts[len(fronts)-1]

        return fronts

    def crowding_distance_assignment(self, fronts):
        '''Calculates the crowding distance value of each individual'''

        for population in fronts:

            last_individual_index = len(population.individuals)-1

            # Reseting this value because it's a new generation
            for individual in population.individuals:
                individual.crowding_distance = 0

            genome_index = 0
            for genome_index in range(self.genotype_quantity):

                # Sorting current population (front) according to the current objective (genome)
                population.individuals.sort(key=lambda x: x.genome[genome_index])

                # The first and last individuals of current population (front) receive "infinite"
                population.individuals[0].crowding_distance = maxsize
                population.individuals[last_individual_index].crowding_distance = maxsize

                min_value, max_value = population.get_extreme_neighbours(genome_index)

                # Calculating the crowding distance of each objective (genome) of all individuals
                for i in range(1, last_individual_index):
                    right_neighbour_value = population.individuals[i+1].genome[genome_index]
                    left_neighbour_value = population.individuals[i-1].genome[genome_index]

                    # population.individuals[i].crowding_distance += ((right_neighbour_value - left_neighbour_value) / (max_value - min_value))
                    if (max_value - min_value) == 0:
                        # TODO: warning: IN CROWDING DISTANCE: division by zero!
                        #print("IN CROWDING DISTANCE: division by zero!")
                        population.individuals[i].crowding_distance += ((right_neighbour_value - left_neighbour_value) / 1)
                    else:
                        population.individuals[i].crowding_distance += ((right_neighbour_value - left_neighbour_value) / (max_value - min_value))

    def crowded_comparison(self, individual_A, individual_B):
        '''Return the best individual according to the crowded comparison operator
        in NSGA-II paper'''

        if ((individual_A.rank < individual_B.rank)
            or ((individual_A == individual_B)
            and (individual_A.crowding_distance > individual_B.crowding_distance))):
            return individual_A
        return individual_B

    def sort_by_crowded_comparison(self, population):
        '''Sort "population" with crowded comparison operator. Bubble sort'''

        for i in range(len(population.individuals)-2):

            worst = population.individuals[i]

            for j in range(1, len(population.individuals)-i):

                worst = self.crowded_comparison(worst, population.individuals[j])

            population.individuals.remove(worst)
            population.individuals.append(worst)

        worst = population.individuals[0]
        population.individuals.remove(worst)
        population.individuals.append(worst)

    def tournament_selection(self):
        '''Binary tournament selection according to crowded comparison operator'''

        first_candidate = self.population.get_random_individual()
        second_candidate = self.population.get_random_individual()

        return self.crowded_comparison(first_candidate, second_candidate)

    def usual_tournament_selection(self):
        '''Usual binary tournament selection'''

        first_candidate = self.population.get_random_individual()
        second_candidate = self.population.get_random_individual()

        first_candidate_score = 0
        second_candidate_score = 0

        for i in range(self.genotype_quantity):
            if first_candidate.genome[i] < second_candidate.genome[i]:
                first_candidate_score += 1
                continue
            if second_candidate.genome[i] < first_candidate.genome[i]:
                second_candidate_score += 1

        if first_candidate_score > second_candidate_score:
            return first_candidate

        return second_candidate

    def crossover(self):
        '''Create a offspring population using the simulated binary crossover (SBX)
        and the binary tournament selection according to the crowded comparison operator'''

        genomes_list = list()

        # Getting the quantity of individuals that are needed to create
        # TODO: This value MUST BE even
        amount_to_create = self.population_size

        # "step = 2" because each iteration generates two children
        for i in range(0, amount_to_create, 2):

            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()

            # Checking if crossover will or not be made
            if random.random() > self.crossover_rate:
                # When crossover isn't made, the children will be a clone of the parents
                child1_genome = parent1.genome
                child2_genome = parent2.genome
            else:
                child1_genome, child2_genome = self.simulated_binary_crossover(parent1, parent2)

            genomes_list.append(child1_genome)
            genomes_list.append(child2_genome)

        # Creating the offspring population
        offspring_population = self.new_population()

        # Adding the new children on that population
        for child_genome in genomes_list:
            offspring_population.new_individual(self.mutation(child_genome))

        return offspring_population

    def usual_crossover(self):
        '''Create a offspring population using the simulated binary crossover (SBX)
        and the usual binary tournament selection'''

        genomes_list = list()

        # Getting the quantity of individuals that are needed to create
        # TODO: This value MUST BE even
        amount_to_create = self.population_size

        # "step = 2" because each iteration generates two children
        for _ in range(0, amount_to_create, 2):

            parent1 = self.usual_tournament_selection()
            parent2 = self.usual_tournament_selection()

            child1_genome, child2_genome = self.simulated_binary_crossover(parent1, parent2)

            genomes_list.append(child1_genome)
            genomes_list.append(child2_genome)

        # Creating the offspring population
        offspring_population = self.new_population()

        # Adding the new children on that
        for child_genome in genomes_list:
            offspring_population.new_individual(self.mutation(child_genome))

        return offspring_population

    def simulated_binary_crossover(self, parent1, parent2):
        '''Simulated binary crossover (SBX)'''

        # Distribution index. "nc" in NSGA-II paper
        crossover_constant = self.crossover_constant

        child1_genome = list()
        child2_genome = list()

        for j in range(self.genotype_quantity):

            # Each genotype has a 50% chance of changing its value
            # TODO: This should be removed when dealing with one-dimensional solutions
            '''
            if (random.random() > 0.5) and (self.genotype_quantity != 1):
                # In this case, the children will get the value of the parents
                child1_genome.append(parent1.genome[j])
                child2_genome.append(parent2.genome[j])
                continue
            '''

            # "y1" is the lowest value between parent1 and parent2. "y2" gets the other value
            if (parent1.genome[j] < parent2.genome[j]):
                y1 = parent1.genome[j]
                y2 = parent2.genome[j]
            else:
                y1 = parent2.genome[j]
                y2 = parent1.genome[j]

            # EPS: precision error tolerance, its value is 1.0e-14 (global constant)
            eps = 0.000000000000010 #1.0e-14
            # If the value in parent1 is not the same of parent2
            if abs(parent1.genome[j] - parent2.genome[j]) > eps:
                # Lower and upper limit of genotype of an individual
                lower_bound = self.genome_min_value
                upper_bound = self.genome_max_value

                u = random.random()

                # Calculation of the first child
                beta = 1 + (2 / (y2 - y1)) * min((y1 - lower_bound), (upper_bound - y2))
                alpha = 2 - pow(beta, -(crossover_constant + 1))
                if u <= (1/alpha):
                    beta_bar = pow(alpha * u, 1/(crossover_constant + 1))
                else:
                    beta_bar = pow(1/(2 - (alpha * u)), 1/(crossover_constant + 1))
                child1_genotype = 0.5 * ((y1 + y2) - beta_bar * (y2 - y1))

                # Calculation of the second child
                beta = 1 + (2 / (y2 - y1)) * min((y1 - lower_bound), (upper_bound - y2))
                alpha = 2 - pow(beta, -(crossover_constant + 1))
                if u <= (1/alpha):
                    beta_bar = pow(alpha * u, 1/(crossover_constant + 1))
                else:
                    beta_bar = pow(1/(2 - (alpha * u)), 1/(crossover_constant + 1))
                child2_genotype = 0.5 * ((y1 + y2) + beta_bar * (y2 - y1))

                child1_genome.append(child1_genotype)
                child2_genome.append(child2_genotype)

            # The paper is not very clear about this, but i assume, in the equation of beta (not beta_bar),
            # y2 and y1, since they could not have been calculated yet, refer to the parents
            # So, if both parents are equal at the specified variable, the divisor would be zero
            # In this case, the children should have the same value as the parents. 
            else:
                child1_genome.append(parent1.genome[j])
                child2_genome.append(parent2.genome[j])

        return child1_genome, child2_genome

    def mutation(self, genome):
        '''Mutation method'''

        random.seed()

        value = random.random()
        value = random.uniform(0, 1)
        # Checking if mutation will or not occur
        if value > self.mutation_rate:
            # When mutation doesn't occur, nothing happens
            return genome

        for i in range(len(genome)):
            # Mutate that genotype
            if random.random() < self.genotype_mutation_probability:

                value = self.disturb_percent * genome[i]

                # Will it add or decrease?
                if random.random() < 0.5:
                    value = -value

                genome[i] = genome[i] + value

                # Making sure that it doesn't escape the bounds
                if genome[i] > self.genome_max_value:
                    genome[i] = self.genome_max_value
                elif genome[i] < self.genome_min_value:
                    genome[i] = self.genome_min_value

        return genome

    # Utils
    def _show_fronts(self, fronts):
        '''Show all fronts'''

        result = "FRONTS:\n"

        i = 0
        for front in fronts:
            i += 1
            result += "FRONT NUMBER " + str(i) + ":\n"

            j = 0
            for individual in front.individuals:
                j += 1
                result += (" [" + str(j) + "] " + str(individual) + "\n")

            result += "\n"

        print(result)

    def _show_population(self, population):
        '''Show all fronts'''

        result = "# [FRONT INDEX] [NAME] [GENOME LIST] [SOLUTIONS LIST] [NONDOMINATED RANK] [CROWDING DISTANCE]\n"

        j = 0
        for individual in population.individuals:
            j += 1
            result += str(j) + " " + str(individual) + "\n"

        return result
