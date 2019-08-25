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

import matplotlib.pyplot as plt
import numpy as np

class NSGA2:
    '''Main class of the algorithm.'''

    # Attributes
    POPULATION_SIZE = 10
    OFFSPRING_SIZE = 5 # A prole, descendentes.

    X_MIN_VALUE = 0
    X_MAX_VALUE = 10

    Y_MIN_VALUE = 0
    Y_MAX_VALUE = 10

    # Constructor
    def __init__(self):
        random.seed(3)

        self.population = None
        self.offspring = None

        self.x_values = list()
        self.y_values = list()

        # List with all fronts.
        self.fronts = list()

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

        self.start_new_population()
        #self.start_new_population_debug()

        self.non_dominated_sorting()

        self.crowding_distance_sorting()

        self._show_offspring()

        #self._plot_individuals()
        self._plot_individuals_fronts()

    def start_new_population(self):
        '''Initialize a new population.'''

        names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.population = list()

        for i in range(self.POPULATION_SIZE):
            x_value = random.randint(self.X_MIN_VALUE, self.X_MAX_VALUE)
            self.x_values.append(x_value)
            y_value = random.randint(self.Y_MIN_VALUE, self.Y_MAX_VALUE)
            self.y_values.append(y_value)
            individual = Individual(names[i], x_value, y_value)
            self.population.append(individual)

    def non_dominated_sorting(self):
        '''Sort the individuals according to they dominance and sort them into fronts.'''

        ''' Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual.
        Also, the first front is created.
        Then the remaining individuals are divided into fronts.
        ''' # pylint: disable=pointless-string-statement

        self.fronts.append([])

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

    def crowding_distance_sorting(self):
        '''Crowding distance sorting algorithm.'''

        self.offspring = list()
        individual_remaining = self.OFFSPRING_SIZE

        # Filling up the offspring with the first fronts.
        for front in self.fronts:
            front_size = len(front)
            # Checking if the current front fits on offspring.
            if front_size <= individual_remaining:
                # Putting one by one on offspring.
                for individual in front:
                    self.offspring.append(individual)
                    individual_remaining -= 1
            else:
                # The current front is stored.
                remaining_front = front
                break

        self.sort_individuals(remaining_front)

        # Creating a list of index that alternates with the lowest and highest values.
        index_list = []
        full_value = len(remaining_front)-1
        full_value = 5-1
        for i in range(int(full_value/2)):
            index_list.append(i)
            index_list.append(full_value)
            full_value -= 1
        index_list.append(i+1)
        if full_value % 2 == 1:
            index_list.append(full_value)

        # Adding the last but not least individuals selected.
        i = 0
        while individual_remaining > 0:
            self.offspring.append(remaining_front[index_list[i]])
            individual_remaining -= 1
            i += 1

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

        individual = Individual('F', 3, 2)
        self.population.append(individual)

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

    def _show_offspring(self):
        '''Show individuals of the offspring.'''
        print("\nOffspring:")
        for individual in self.offspring:
            sys.stdout.write(str(individual) + ", ")
        print("")

    def _show_individuals_from_list(self, individual_list):
        for individual in individual_list:
            sys.stdout.write(str(individual) + ', ')
        print()

    def _plot_individuals(self):
        plt.plot(self.x_values, self.y_values, 'ko')
        plt.axis([self.X_MIN_VALUE, self.X_MAX_VALUE, self.Y_MIN_VALUE, self.Y_MAX_VALUE])
        plt.xticks(np.arange(self.X_MIN_VALUE, self.X_MAX_VALUE+1, 1.0))
        plt.yticks(np.arange(self.Y_MIN_VALUE, self.Y_MAX_VALUE+1, 1.0))
        plt.show()

    def _plot_individuals_fronts(self):
        multiple_x_values = list()
        multiple_y_values = list()
        x_values = list()
        y_values = list()

        for front in self.fronts:
            x_values = list()
            y_values = list()
            for individual in front:
                x_values.append(individual.x_value)
                y_values.append(individual.y_value)
            multiple_x_values.append(x_values)
            multiple_y_values.append(y_values)

        #colors = ['go','ro','bo', 'mo', 'yo', 'co', 'no', 'ko']
        colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        labels = ['Front 1', 'Front 2', 'Front 3', 'Front 4', 'Front 5', 'Front 6', 'Front 7', 'Front 8']

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
