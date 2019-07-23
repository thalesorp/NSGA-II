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
        self.population = list()

    def run(self):
        '''Method responsible for running the main loop of NSGA2.'''
        self.start_new_population()

        self.show_population()

        self.non_dominated_sorting()
        # pylint: disable=pointless-string-statement
        '''
        Começa com uma população de tamanho 'POPULATION_SIZE'.
        É criado os filhos dessa população, que terá a quantidade 'offspring_size'.
            A criação de tais filhos é feita a partir de:
                cruzamento;
                mutação.
        Ordenalos conforme o algoritmo: Non-dominated sorting.
        Pega os melhores indivíduos conforme o algoritmo: Crowding distance sorting.
        Tamanho máximo da nova população é 'POPULATION_SIZE'.
        Volta ao início.
        '''

    def non_dominated_sorting(self):
        '''???'''
        general_domination_info = list()

        # Each of individuals checks if dominates or is dominated by everyone else.
        for i in range(self.POPULATION_SIZE):
            # Quantity of individuals that this individual dominates.
            domination_count = 0
            # List of individuals that dominates this individual.
            dominated_by = list()

            for j in range(self.POPULATION_SIZE):
                if i != j: # Ignoring itself.
                    if self.population[i].dominates(self.population[j]):
                        domination_count += 1
                    else:
                        dominated_by.append(j)

            general_domination_info.append([domination_count, dominated_by])

            print( general_domination_info[len(general_domination_info) - 1] )

        print(general_domination_info)

        for i in range(self.POPULATION_SIZE):
            domination_count = general_domination_info[i][0]
            dominated_by = general_domination_info[i][1]
            print("Indivíduo:", i, "\tdomination_count:", domination_count,
                  "\tdominated by:", dominated_by)

    def start_new_population(self):
        '''Initialize a new population.'''
        for _ in range(self.POPULATION_SIZE):
            x_value = random.randint(self.X_MIN_VALUE, self.X_MAX_VALUE)
            y_value = random.randint(self.Y_MIN_VALUE, self.Y_MAX_VALUE)
            individual = Individual(x_value, y_value)
            self.population.append(individual)

    def show_population(self):
        '''Show the x and y values of each individual of population.'''
        print("I\tX\tY")
        for i in range(self.POPULATION_SIZE):
            print(i, "\t", self.population[i])
