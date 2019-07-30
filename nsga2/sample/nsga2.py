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
        random.seed(3)
        self.population = list()

    # Methods
    def run(self):
        '''Method responsible for running the main loop of NSGA2.'''
        self.start_new_population()

        self._show_population()

        self.non_dominated_sorting()

        # pylint: disable=pointless-string-statement
        '''
        Starts with one population of size 'POPULATION_SIZE'.
        It's created the children of this population, that will be the quantity of 'OFFSPRING_SIZE'.
        The creation of those children is made by:
            crossover;
            mutation.
        Sort them with: Non-dominated sorting.
        Take the best individual according with: Crowding distance sorting.
        Max size of the new population is: 'POPULATION_SIZE'.
        Go back to beginning.
        '''

    def non_dominated_sorting(self):
        '''Non-dominated sorting algorithm.'''

        # pylint: disable=pointless-string-statement
        '''
        Step 1: Everyone check with everyone who dominates who.
                Then, fill up the GDI list (which by the way, each position
                correlate with each individual) with:
                    - Domination count = quantity of individuals dominates this individual;
                    - Dominated by = list of individuals that are dominated by.
                The result is:
                general_domination_info = [ [domination_count, [dominated_by_list] ], ...]
        '''

        general_domination_info = list()
        # Each of individuals checks if dominates or is dominated by everyone else.
        for i in range(self.POPULATION_SIZE):
            # Quantity of individuals dominates this individual.
            domination_count = 0
            # List of individuals that are dominated by this individual.
            dominated_by = list()

            for j in range(self.POPULATION_SIZE):
                if i != j: # Ignoring itself.
                    if self.population[i].dominates(self.population[j]):
                        dominated_by.append(j)
                    else:
                        domination_count += 1

            general_domination_info.append([domination_count, dominated_by])

        #self._show_GDI(general_domination_info)

        # pylint: disable=pointless-string-statement
        '''
        Step 2: Now is the time to divide them into fronts.
                While there's individuals with "domination_count = 0" do:
                    Add all with 'domination_count = 0' to current front.
                    Iterates over them and then over all dominated_by lists:
                        decrement they domination_count by one.
            The result is:
            fronts = [ [individuals of front 0], [individuals of front 1], ... ]
        '''

        # List with all fronts.
        fronts = list()
        # Temporary list with the current front.
        current_front = list()

        while NSGA2._check_domination_count(general_domination_info):

            self._show_GDI(general_domination_info)

            sys.stdout.write("Fronts:")
            print(fronts)

            for individual in range(self.POPULATION_SIZE):
                domination_count = general_domination_info[individual][0]
                # If there's no domination over this individual, add him to the current front.
                if domination_count == 0:
                    general_domination_info[individual][0] -= 1
                    current_front.append(individual)
            # When the current front is over, add it to the fronts list.
            fronts.append(current_front)
            current_front = list()

            # Iterating over the last added front.
            last_front_position = fronts[len(fronts)-1]
            for i in range(len(last_front_position)):

                individual = fronts[len(fronts)-1][i]

                dominated_by_list = general_domination_info[individual][1]

                # Iterating over the list of individuals of this especific individual.
                for j, individual_that_dominates in enumerate(dominated_by_list):
                    # Decrementing domination_count of each individual that dominates.
                    general_domination_info[individual_that_dominates][0] -= 1

            input()

        print("Finally:")
        self._show_GDI(general_domination_info)

    def start_new_population(self):
        '''Initialize a new population.'''
        for _ in range(self.POPULATION_SIZE):
            x_value = random.randint(self.X_MIN_VALUE, self.X_MAX_VALUE)
            y_value = random.randint(self.Y_MIN_VALUE, self.Y_MAX_VALUE)
            individual = Individual(x_value, y_value)
            self.population.append(individual)

    def _show_population(self):
        '''Show the x and y values of each individual of population.'''
        print("i(x,y)")
        for i in range(self.POPULATION_SIZE):
            sys.stdout.write(str(i) + "(" + str(self.population[i].x_value)
                             + "," + str(self.population[i].y_value) + ")\n")
        print("")

    def _show_GDI(self, general_domination_info):
        for i in range(self.POPULATION_SIZE):
            domination_count = general_domination_info[i][0]
            dominated_by = general_domination_info[i][1]
            print("Individual:", i, "\tdomination_count:", domination_count,
                  "\tdominated by:", dominated_by)
        print("")

    @staticmethod
    def _check_domination_count(general_domination_info):
        '''Check if there's at least one individual with "domination_count = 0".
            If there is, True is returned. Otherwise, False.'''
        for info in general_domination_info:
            if info[0] <= 1:
                return True
        return False

    @staticmethod
    def _show_fronts(fronts):
        '''Show all fronts.'''
        for front in fronts:
            print(front)
