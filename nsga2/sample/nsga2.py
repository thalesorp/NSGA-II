#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
#                                                                              #
#  NSGA-II: Non-dominated Sorting Genetic Algorithm II                         #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Contact:                                                                    #
#    Thales Otávio | @ThalesORP | ThalesORP@gmail.com                          #
#                                                                              #
################################################################################

'''Main class of NSGA-II.'''
import sys
import random
from .individual import Individual

class NSGA2:
    '''Main class of the algorithm.'''

    # Attributes
    POPULATION_SIZE = 5
    OFFSPRING_SIZE = 5 # A prole, descendentes.

    X_MIN_VALUE = 0
    X_MAX_VALUE = 5

    Y_MIN_VALUE = 0
    Y_MAX_VALUE = 5

    # Constructor
    def __init__(self):
        random.seed(1)
        self.population = None
        # List with all fronts.
        self.fronts = list()
        self.fronts.append([])

    # Methods
    def run(self):
        '''Method responsible for running the main loop of NSGA2.'''

        ''' Starts with one population of size 'POPULATION_SIZE'.
        It's created the children of this population, that will be the quantity of 'OFFSPRING_SIZE'.
        The creation of those children is made by crossover and mutation.
        Sort them with: non-dominated sorting.
        Take the best individual according with: crowding distance sorting.
        'POPULATION_SIZE' is the max size of the new population.
        Back to beginning. Repeated N generations.
        ''' # pylint: disable=pointless-string-statement

        #self.start_new_population()
        self.start_new_population_debug()

        self.non_dominated_sorting()

    def start_new_population(self):
        '''Initialize a new population.'''

        names = 'ABCDEFGHIJKL'
        self.population = list()

        for i in range(self.POPULATION_SIZE):
            x_value = random.randint(self.X_MIN_VALUE, self.X_MAX_VALUE)
            y_value = random.randint(self.Y_MIN_VALUE, self.Y_MAX_VALUE)
            individual = Individual(names[i], x_value, y_value)
            self.population.append(individual)

    def non_dominated_sorting(self):
        '''Non-dominated sorting algorithm.'''

        ''' Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual.
        Also, the first front is created.
        Then the remaining individuals are divided into fronts.
        ''' # pylint: disable=pointless-string-statement

        # Each of individuals checks if dominates or is dominated with everyone else.
        for i in range(self.POPULATION_SIZE):
            #print("\n", self.population[i])

            for j in range(self.POPULATION_SIZE):
                current_individual = self.population[i]
                other_individual = self.population[j]

                if i != j: # Ignoring itself.
                    # Checking if dominates or are dominated by the other individuals.
                    if current_individual.dominates(other_individual):
                        current_individual.dominated_by.append(other_individual)
                        #sys.stdout.write("  " + current_individual.name + " dominates " + other_individual.name + ".\n")
                    elif other_individual.dominates(current_individual):
                        current_individual.domination_count += 1
                        #sys.stdout.write("  " + current_individual.name + " is dominated by " + other_individual.name + ".\n")

            # Checking if current individual is eligible to the first front.
            if current_individual.domination_count == 0:
                if current_individual not in self.fronts[0]:
                    self.fronts[0].append(current_individual)

        print("Initially:")
        self._show_general_domination_info()

        # Temporary list with the current front.
        current_front = list()

        i = 0
        while len(self.fronts[i]) > 0: # pylint: disable=len-as-condition
            current_front = list()
            for individual in self.fronts[i]:
                for dominated_individual in individual.dominated_by:
                    dominated_individual.domination_count -= 1
                    ''' Now if this dominated individual aren't dominated by anyone,
                    insert into next front.''' # pylint: disable=pointless-string-statement
                    if dominated_individual.domination_count == 0:
                        current_front.append(dominated_individual)
            self.fronts.append(current_front)
            i += 1

        # Deleting empty last position created in previously loops.
        del self.fronts[len(self.fronts)-1]

        print("Finally:")
        self._show_general_domination_info()
        self._show_fronts()

    # Debug
    def start_new_population_debug(self):
        '''DEBUG: Initialize a new population.'''
        self.population = list()

        individual = Individual('A', 3, 3)
        self.population.append(individual)

        individual = Individual('B', 4, 2)
        self.population.append(individual)

        individual = Individual('C', 1, 2)
        self.population.append(individual)

        individual = Individual('D', 1, 1)
        self.population.append(individual)

        individual = Individual('E', 2, 1)
        self.population.append(individual)

        #individual = Individual('F', 3, 2)
        #self.population.append(individual)

    def _show_population(self):
        '''Show the x and y values of each individual of population.'''
        print("i(x,y)")
        for individual in self.population:
            print(individual)

    def _show_general_domination_info(self):
        '''Show all data of population.'''
        for individual in self.population:
            sys.stdout.write("  Individual: " + str(individual) +
                             "\tdomination count: " + str(individual.domination_count) +
                             "\tdominated by this: ")
            for dominated_individual in individual.dominated_by:
                sys.stdout.write(str(dominated_individual.name) + ", ")
            print("")
        print("")

    def _show_fronts(self):
        '''Show all fronts.'''
        i = 1
        for front in self.fronts:
            sys.stdout.write("Front " + str(i) + ": ")
            i += 1
            for individual in front:
                sys.stdout.write(str(individual) + ", ")
            print("")
