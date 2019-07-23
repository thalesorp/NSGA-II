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

class NSGA2:

    # Attributes
    population_size = 100
    offspring_size = 100 # A prole, descendentes.

    # Constructor
    def __init__(self):
        print('Dentro do construtor do NSGA2.')

    def run(self):
        start_new_population()

        '''
        Começa com uma população de tamanho 'population_size'.
        É criado os filhos dessa população, que terá a quantidade 'offspring_size'.
            A criação de tais filhos é feita a partir de:
                cruzamento;
                mutação.
        Ordenalos conforme o algoritmo: Non-dominated sorting.
        Pega os melhores indivíduos conforme o algoritmo: Crowding distance sorting.
        Tamanho máximo da nova população é 'population_size'.
        Volta ao início.
        '''

    def start_new_population(self):
        algo = 1
