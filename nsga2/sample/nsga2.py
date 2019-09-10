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

from .population import Population

import matplotlib.pyplot as plt
import numpy as np

class NSGA2:
    '''Main class of the NSGA-II algorithm.'''

    # Attributes
    POPULATION_SIZE = 10
    OFFSPRING_SIZE = 5

    X_MIN_VALUE = 0
    X_MAX_VALUE = 10

    Y_MIN_VALUE = 0
    Y_MAX_VALUE = 10

    GENERATIONS = 10

    # Constructor
    def __init__(self):
        random.seed(3)

        self.population = Population(
            self.POPULATION_SIZE, self.OFFSPRING_SIZE,
            self.X_MIN_VALUE, self.X_MAX_VALUE,
            self.Y_MIN_VALUE, self.Y_MAX_VALUE)

    # Methods
    def run(self):
        '''Method responsible for running the main loop of NSGA2.'''

        ''' Starts with one population of size 'POPULATION_SIZE'.
        It's created the children of this population, that will be the quantity of 'OFFSPRING_SIZE'.
        The creation of those children is made by crossover and mutation.
        Sort them with: non-dominated sorting.
        Take the best individual according with: crowding distance sorting.
        'POPULATION_SIZE' is the max size of the new population.
        Back to beginning. Repeated N generations.'''

        self.population.start_new_population()
        #self.start_new_population()
        #self.start_new_population_debug()

        print("Initially:")
        self.population._show_general_domination_info()

        self.non_dominated_sorting()

        print("And them:")
        #self.population._show_general_domination_info()
        self.population._show_fronts()
        #self.population._show_fronts_with_crowding_distance()

        self.crowding_distance_sorting()

        print("Finally:")
        #self.population._show_general_domination_info()
        self.population._show_fronts()
        #self.population._show_fronts_with_crowding_distance()

        #self.population._show_offspring()

        self._plot_individuals_fronts()

    def non_dominated_sorting(self):
        '''Sort the individuals according to they dominance and sort them into fronts.'''

        ''' Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual.
        Also, the first front is created.
        Then the remaining individuals are divided into fronts.'''

        self.population.fronts.append([])

        # Each of individuals checks if dominates or is dominated with everyone else.
        for i in range(self.POPULATION_SIZE):
            for j in range(self.POPULATION_SIZE):
                current_individual = self.population.individuals[i]
                other_individual = self.population.individuals[j]

                if i != j: # Ignoring itself.
                    # Checking if dominates or are dominated by the other individuals.
                    if current_individual.dominates(other_individual):
                        current_individual.dominated_by.append(other_individual)
                    elif other_individual.dominates(current_individual):
                        current_individual.domination_count += 1

            # Checking if current individual is eligible to the first front.
            if current_individual.domination_count == 0:
                if current_individual not in self.population.fronts[0]:
                    self.population.fronts[0].append(current_individual)

        # Temporary list with the current front.
        current_front = list()

        i = 0
        while len(self.population.fronts[i]) > 0: # pylint: disable=len-as-condition
            current_front = list()
            for individual in self.population.fronts[i]:
                for dominated_individual in individual.dominated_by:
                    dominated_individual.domination_count -= 1
                    ''' Now if this dominated individual aren't dominated by anyone,
                    insert into next front.'''
                    if dominated_individual.domination_count == 0:
                        current_front.append(dominated_individual)
            self.population.fronts.append(current_front)
            i += 1

        # Deleting empty last position created in previously loops.
        del self.population.fronts[len(self.population.fronts)-1]

    def crowding_distance_sorting(self):
        '''Crowding distance sorting algorithm.'''

        ''' Reject the fronts that doesn't fit in the population of next generation.
        Find the crowding distance value for each individual.
        Sort them in they front with this value.
        Discard the individuals that doesn't fit on new population.'''

        ''' Rejecting the fronts that doesn't fit in the population for next generation.'''

        individual_quantity = 0
        exceeded_front_index = 0
        i = 0
        while exceeded_front_index == 0:
            # Checking if the quantity of individuals exceeded the limit, wich is OFFSPRING_SIZE.
            if individual_quantity >= self.OFFSPRING_SIZE:
                exceeded_front_index = i
            else:
                individual_quantity += len(self.population.fronts[i])
            i += 1

        # Actually deleting the fronts that exceed.
        del self.population.fronts[exceeded_front_index : len(self.population.fronts)]


        ''' Calculating the crowding distance value for each individual.'''

        for front in self.population.fronts:

            # Temporary lists that holds the x and y values of current front.
            x_values = list()
            y_values = list()

            for individual in front:
                x_values.append(individual.x_value)
                y_values.append(individual.y_value)
            x_values.sort()
            y_values.sort()

            min_x_value = min(x_values)
            max_x_value = max(x_values)
            min_y_value = min(y_values)
            max_y_value = max(y_values)

            # Getting the data and making the calculation of crowding distance for each individual.
            for individual in front:
                # Getting the index of current individual on the x and y values lists.
                x_index = x_values.index(individual.x_value)
                y_index = y_values.index(individual.y_value)

                # X:
                # Usually, the value is as described bellow.
                x_left_neighbour_index = x_index - 1
                x_right_neighbour_index = x_index + 1
                # But when isn't, then it's checked the cases when there's no neighbour on one side.
                if x_index == 0:
                    # When it happens, the closest neighbour it's himself.
                    x_left_neighbour_index = 0
                elif x_index == (len(x_values)-1):
                    x_right_neighbour_index = (len(x_values)-1)
                # Getting the value of neighbous, which is what matters.
                x_value_left_neighbour = x_values[x_left_neighbour_index]
                x_value_right_neighbour = x_values[x_right_neighbour_index]

                # Y:
                y_top_neighbour_index = y_index + 1
                y_bottom_neighbour_index = y_index - 1

                if y_index == 0:
                    y_bottom_neighbour_index = 0
                elif y_index == (len(y_values)-1):
                    y_top_neighbour_index = (len(y_values)-1)

                y_value_top_neighbour = y_values[y_top_neighbour_index]
                y_value_bottom_neighbour = y_values[y_bottom_neighbour_index]

                individual.crowding_distance += ((x_value_right_neighbour - x_value_left_neighbour)
                                                / (max_x_value - min_x_value))

                individual.crowding_distance += ((y_value_top_neighbour - y_value_bottom_neighbour)
                                                / (max_y_value - min_y_value))


        ''' Sorting the individuals with crowding distance value.'''

        self.population.sort_fronts_by_crowding_distance()

        # Getting the front that will have individuals removed.
        last_front = self.population.fronts[len(self.population.fronts)-1]


        ''' Getting the amount of individuals that are gonna be removed and removing them.'''

        amount_to_remove = 0

        # Getting the amount of individuals from all fronts but the last.
        individual_counter = 0
        for i in range(0, len(self.population.fronts)-1):
            individual_counter += len(self.population.fronts[i])

        # Quantity of individuals of last front that will continue to next generation.
        remaining_individuals = self.population.offspring_size - individual_counter

        amount_to_remove = len(last_front) - remaining_individuals

        # Deleting the last "amount_to_remove" individuals.
        del last_front[ len(last_front) - amount_to_remove :]

    def mutation(self):
        ''' '''
        pass

    def crossover(self):
        ''' '''
        pass

    # Utils
    def sort_individuals(self, individual_list):
        '''Sort an list of individuals.'''

        sum_list = list()
        xy_sum = 0
        for individual in individual_list:
            xy_sum = individual.x_value + individual.y_value
            sum_list.append(xy_sum)

        lowest = None
        for i in range(len(individual_list)):
            # Finding the lowest value.
            lowest_index = 0
            lowest = sum_list[0]
            for j in range(1, len(sum_list)):
                if sum_list[j] < lowest:
                    lowest_index = j
                    lowest = sum_list[j]

            # Remove an element from list by index.
            sum_list.pop(lowest_index)
            lowest = individual_list.pop(lowest_index)
            # Insert the lowest to the first available position.
            sum_list.insert(0, sys.maxsize)
            individual_list.insert(i, lowest)

    def _show_individuals_from_list(self, individual_list):
        for individual in individual_list:
            sys.stdout.write(str(individual) + ', ')
        print()

    # Plotting
    def _plot_individuals_fronts(self):
        multiple_x_values = list()
        multiple_y_values = list()
        x_values = list()
        y_values = list()

        for front in self.population.fronts:
            x_values = list()
            y_values = list()
            for individual in front:
                x_values.append(individual.x_value)
                y_values.append(individual.y_value)
            multiple_x_values.append(x_values)
            multiple_y_values.append(y_values)

        #colors = ['go','ro','bo', 'mo', 'yo', 'co', 'no', 'ko']
        colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo', 'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo', 'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo', 'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo', 'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo', 'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo', 'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        labels = ['Front 1', 'Front 2', 'Front 3', 'Front 4', 'Front 5', 'Front 6', 'Front 7', 'Front 8', 'Front 9', 'Front 10', 'Front 11', 'Front 12', 'Front 13', 'Front 14', 'Front 15', 'Front 16', 'Front 17', 'Front 18', 'Front 19', 'Front 20', 'Front 21', 'Front 22', 'Front 23', 'Front 24', 'Front 25', 'Front 26', 'Front 27', 'Front 28', 'Front 29', 'Front 30']

        ax = plt.subplot(111)

        i = 0
        for i in range(len(multiple_x_values)):
            plt.plot(multiple_x_values[i], multiple_y_values[i], colors[i], label=labels[i])

        #plt.plot(self.x_values, self.y_values, 'ro')
        #plt.plot(self.x_values, self.y_values, 'ro')

        plt.axis([self.X_MIN_VALUE, self.X_MAX_VALUE, self.Y_MIN_VALUE, self.Y_MAX_VALUE])
        plt.xticks(np.arange(self.X_MIN_VALUE, self.X_MAX_VALUE+1, 1.0))
        plt.yticks(np.arange(self.Y_MIN_VALUE, self.Y_MAX_VALUE+1, 1.0))

        plt.title('Individual fronts')
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

        #plt.legend(loc='upper left')
        plt.show()
