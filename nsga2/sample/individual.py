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

'''File of individual class.'''

class Individual: # pylint: disable=too-few-public-methods
    '''Class of individuals of the population of NSGA-II.'''

    # Constructor
    def __init__(self, x_value, y_value):
        self.x_value = x_value
        self.y_value = y_value

    def __str__(self):
        return str(self.x_value) + "\t" + str(self.y_value)

    # Methods
    def dominates(self, individual):
        '''Function that tells if the actual individual dominates another.
            A(x1, y1) dominates B(x2, y2) when:
                (x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)'''

        a = bool(self.x_value <= individual.x_value) # pylint: disable=invalid-name
        b = bool(self.y_value <= individual.y_value) # pylint: disable=invalid-name
        c = bool(self.x_value < individual.x_value) # pylint: disable=invalid-name
        d = bool(self.y_value < individual.y_value) # pylint: disable=invalid-name

        return (a and b) and (c or d)
