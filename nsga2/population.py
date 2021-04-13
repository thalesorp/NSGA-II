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

'''File of population class'''

import sys
import random

from .individual import Individual

class Population():
    '''Class of population of indiviuals, used by NSGA-II'''

    # "I" for integers and "R" for real values
    RANDOM_TYPE = "R"

    def __init__(self, genotype_quantity, genome_min_value, genome_max_value):
        random.seed()

        # Size of genome list
        self.genotype_quantity = genotype_quantity

        self.genome_min_value = genome_min_value
        self.genome_max_value = genome_max_value

        self.size = 0

        self.individuals = list()

    def initiate(self, n_individuals):
        '''Initialize a new population'''

        for _ in range(n_individuals):
            genome = list()

            for _ in range(self.genotype_quantity):
                if self.RANDOM_TYPE == "R":
                    genotype = random.uniform(self.genome_min_value, self.genome_max_value)
                if self.RANDOM_TYPE == "I":
                    genotype = random.randrange(self.genome_min_value, self.genome_max_value + 1)
                genome.append(genotype)

            self.new_individual(genome)

    def new_individual(self, genome):
        '''Create a new individual with "genome" and insert into population'''

        self.insert(Individual(genome))

    def insert(self, individual):
        '''Insert a new individual into population'''

        self.individuals.append(individual)
        self.size += 1

    def delete_individual(self, individual):
        '''Delete "individual" from population'''

        self.individuals.remove(individual)
        self.size -= 1

    def union(self, population):
        '''Union operation over "population" and current population'''

        for individual in population.individuals:
            self.insert(individual)

    # Front utils
    def reset_fronts(self):
        '''Delete all fronts and prepare the population to be sorted in fronts'''

        for individual in self.individuals:
            individual.domination_count = 0
            individual.dominated_by = list()

        self.fronts = list()

    def new_front(self):
        '''Start a new front'''

        self.fronts.append([])

    def get_random_individual(self):
        '''Return a random individual of this population'''

        index = random.randint(0, self.size-1)

        return self.individuals[index]

    def add_to_front(self, index, individual):
        '''Add the individual into "index" front'''

        self.fronts[index].append(individual)

    def get_last_front_index(self):
        '''Retun the index of last front'''

        return len(self.fronts)-1

    def add_to_last_front(self, individual):
        '''Add individual to last front'''

        self.fronts[self.get_last_front_index()].append(individual)

    def get_last_front(self):
        '''Return the last front'''

        return self.fronts[len(self.fronts)-1]

    def delete_individual_from_last_front(self, individual):
        '''Deletes the individual from front AND from individuals list'''

        # Deleting from last front the individual with index = "index"
        last_front = self.get_last_front()
        index = last_front.index(individual)
        del last_front[index]

        self.delete_individual(individual)

    def delete_last_front(self):
        '''Deleting the last front and the individuals inside'''

        last_front = self.get_last_front()

        for individual in last_front:
            self.delete_individual(individual)

        self.fronts.remove(last_front)

    # Crowding Distance utils
    def get_neighbour(self, individual_genome, front_index, genome_index):
        '''Return the left and right neighbour values of "individual_genome"'''

        genome_list = list()

        for individual in self.fronts[front_index]:
            genome_list.append(individual.genome[genome_index])

        genome_list.sort()

        individual_genome_index = genome_list.index(individual_genome)

        # Usually, the value is as described bellow
        left_neighbour_index = individual_genome_index - 1
        right_neighbour_index = individual_genome_index + 1

        # But when isn't, then it's checked the cases when there's no neighbour on one side
        if individual_genome_index == 0:
            # When it happens, the closest neighbour it's himself
            left_neighbour_index = 0
        if individual_genome_index == (len(genome_list)-1):
            right_neighbour_index = (len(genome_list)-1)


        return genome_list[left_neighbour_index], genome_list[right_neighbour_index]

    def get_extreme_neighbours(self, genome_index):
        '''Return the highest and lowest neighbour values of "individual_genome"'''

        genome_list = list()

        for individual in self.individuals:
            genome_list.append(individual.genome[genome_index])

        return min(genome_list), max(genome_list)

    # Utils
    def _show_individuals(self):
        '''Show the values of each individual of population'''

        result = "INDIVIDUALS:\n"
        i = 1
        for individual in self.individuals:
            result += (" [" + str(i) + "] " + str(individual) + "\n")
            i += 1

        print(result)

    def _show_front(self, front_index):
        '''Show only front with "front_index"'''

        result = "FRONT:\n"
        j = 0
        for individual in self.fronts[front_index]:
            j += 1
            result += (" [" + str(j) + "] " + str(individual) + "\n")

        result += "\n"

        print(result)

    def _show_fronts_simple(self):
        '''Show all fronts'''

        result = "FRONTS:\n"

        i = 0
        for front in self.fronts:
            i += 1
            result += "FRONT NUMBER " + str(i) + ":\n"

            j = 0
            for individual in front:
                j += 1
                result += (" [" + str(j) + "] " + individual.__str_genome__() + "\n")

            result += "\n"

        print(result)

    def _show_general_domination_info(self):
        '''Show all data of population'''

        for individual in self.individuals:
            sys.stdout.write("  Individual: " + str(individual)
                             + "\tdomination count: " + str(individual.domination_count)
                             + "\tdominated by this: ")
            for dominated_individual in individual.dominated_by:
                sys.stdout.write(str(dominated_individual.name) + ", ")
            print("")
        print("")

    def _show_fronts_with_crowding_distance(self):
        '''Show all fronts'''

        i = 1
        for front in self.fronts:
            sys.stdout.write("Front " + str(i) + ": ")
            i += 1
            for individual in front:
                sys.stdout.write(str(individual)+ ".CD: "
                                 + str(individual.crowding_distance) + ", ")
            print("")
