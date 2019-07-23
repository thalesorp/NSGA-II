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

from sample.nsga2 import NSGA2

def run():
    # Organiza aqui tudo que será passado para o NSGA-II.
    # Depois disso, chamar 'myNSGA2.run()'.
    myNSGA2 = NSGA2()
    myNSGA2.run()

if __name__ == '__main__':
    run()
