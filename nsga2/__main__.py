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

'''Class'''

from sample.nsga2 import NSGA2 # pylint: disable=import-error

def run():
    '''Method responsible for calling the NSGA-II.'''
    my_nsga2 = NSGA2()
    my_nsga2.run()

if __name__ == '__main__':
    run()
