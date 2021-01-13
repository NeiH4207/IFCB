#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu" at 15:32, 06/01/2021                                                               %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Nguyen_Thieu2                                  %
#       Github:     https://github.com/thieu1995                                                        %
# ------------------------------------------------------------------------------------------------------%

from config import Config
from optimizer.root import Root
from numpy.random import uniform, random
from utils.schedule_util import matrix_to_schedule


class BaseGA(Root):

    def __init__(self, problem=None, pop_size=10, epoch=2, func_eval=100000, time_bound=None, domain_range=None, paras=None):
        super().__init__(problem, pop_size, epoch, func_eval, time_bound, domain_range)
        if paras is None:
            paras = {"p_c": 0.9, "p_m": 0.05}
        self.p_c = paras["p_c"]
        self.p_m = paras["p_m"]

    def crossover(self, dad, mom):
        r = random()
        child = []
        if r < self.p_c:
            while True:
                for i in range(len(dad[self.ID_POS])):
                    child.append((dad[self.ID_POS][i] + mom[self.ID_POS][i]) / 2)
                schedule = matrix_to_schedule(self.problem, child[0], child[1])
                if schedule.is_valid():
                    fitness = self.Fit.fitness(schedule)
                    break
            return [child, fitness]  # [solution, fit]
        else:
            if Config.METRICS in Config.METRICS_MAX:
                return mom if dad[self.ID_FIT] < mom[self.ID_FIT] else dad
            else:
                return dad if dad[self.ID_FIT] < mom[self.ID_FIT] else mom

    def select(self, pop):
        pop_new = []
        while len(pop_new) < self.pop_size:
            fit_list = [item[self.ID_FIT] for item in pop]
            dad_index = self.get_index_roulette_wheel_selection(fit_list)
            mom_index = self.get_index_roulette_wheel_selection(fit_list)
            while dad_index == mom_index:
                mom_index = self.get_index_roulette_wheel_selection(fit_list)
            dad = pop[dad_index]
            mom = pop[mom_index]
            sol_new = self.crossover(dad, mom)
            pop_new.append(sol_new)
        return pop_new

    def mutate(self, pop):
        for i in range(self.pop_size):
            while True:
                child = []
                for j in range(len(pop[i][self.ID_POS])):
                    sol_part_temp = pop[i][self.ID_POS][j]
                    for k_row in range(sol_part_temp.shape[0]):
                        for k_col in range(sol_part_temp.shape[1]):
                            if uniform() < self.p_m:
                                sol_part_temp[k_row][k_col] = uniform(self.domain_range[0], self.domain_range[1])
                    child.append(sol_part_temp)
                schedule = matrix_to_schedule(self.problem, child[0], child[1])
                if schedule.is_valid():
                    fitness = self.Fit.fitness(schedule)
                    break
            pop[i] = [child, fitness]
        return pop

    def evolve(self, pop, fe_mode=None, epoch=None, g_best=None):
        pop = self.select(pop)
        pop = self.mutate(pop)
        if fe_mode is None:
            return pop
        else:
            counter = 2*self.pop_size   # pop_new + pop_mutation operations
            return pop, counter


