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

'''File of individual class'''

class Individual():
    '''Individuals calss of the population in NSGA-II'''

    id = 1

    def __init__(self, genome):

        self.name = "i~" + str(Individual.id)
        Individual.id += 1

        # List of genotypes
        self.genome = genome

        # List of solutions
        self.solutions = list()

        # List of solutions not normalized by the evaluate method
        self.non_normalized_solutions = list()

        # Quantity of individuals which dominate this individual
        self.domination_count = 0

        # List of individuals that are dominated by this individual
        self.dominated_by = list()

        self.rank = None

        self.crowding_distance = None

    def dominates(self, individual):
        '''Function that tells if the actual individual dominates another

        A(x1, y1) dominates B(x2, y2) when:
            (x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)

        A(x1, y1, z1) dominates B(x2, y2, z2) when:
            [ (x1 <= x2) and (y1 <= y2) and (z1 <= z2) ] and [ (x1 < x2) or (y1 < y2) or (z1 < z2) ]
            [ first_half ] and [ second_half ]'''

        first_half = True
        second_half = False

        i = 0
        for solution in self.solutions:
            first_half = first_half and bool(solution <= individual.solutions[i])
            second_half = second_half or bool(solution < individual.solutions[i])
            i += 1

        return (first_half and second_half)

    def __str__(self):
        return (self.name
                + " " +  self.__str_genome__()
                + " " + self.__str_solutions__()
                + " " + str(self.rank)
                + " " + self.__str_crowding_distance__()
                #+ " " + str(self.domination_count)
                #+ " " + self.__str_dominated_by__()
                )

    def __str_genome__(self):
        if not self.genome:
            return "[]"

        result = "["

        if len(self.genome) == 1:
            result += '%.2f'%(self.genome[0]) + "]"
            return result

        for i in range(len(self.genome)-1):
            result += '%.2f'%(self.genome[i]) + " "
        result += '%.2f'%(self.genome[i+1]) + "]"

        return result

    def __str_solutions__(self):
        if not self.solutions:
            return "[]"

        result = "["

        for i in range(len(self.solutions)-1):
            result += '%.2f'%(self.solutions[i]) + ", "
        result += '%.2f'%(self.solutions[i+1]) + "]"

        return result

    def __str_crowding_distance__(self):
        if self.crowding_distance is None:
            return "-"

        return str('%.2f'%(self.crowding_distance))

    def __str_dominated_by__(self):
        if not self.dominated_by:
            return "[]"

        dominated_by_size = len(self.dominated_by)
        
        if dominated_by_size > 1:
            result = "["
            for i in range(dominated_by_size-1):
                result += str(self.dominated_by[i].name) + ", "
            result += str(self.dominated_by[i+1].name) + "]"
        else:
            result = "[" + str(self.dominated_by[0].name) + "]"

        return result
