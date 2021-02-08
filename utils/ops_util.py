#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu" at 15:25, 06/01/2021                                                               %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Nguyen_Thieu2                                  %
#       Github:     https://github.com/thieu1995                                                        %
# ------------------------------------------------------------------------------------------------------%
## Operations util functions

from numpy.random import uniform, normal
from numpy import array
from config import *


def get_min_value(element_value_range):
    method = 'min_of_all_method'  # min_of_all_method, lower_bound_define

    if method == 'min_of_all_method':
        with open(f'{Config.RESULTS_DATA}/summary_{element_value_range[1]}.txt') as f:
            lines = f.readlines()
        min_value_information = {}
        for line in lines:
            line_data = line.rstrip('\n').split(', ')
            _value = float(line_data[3])
            if line_data[1] not in min_value_information:
                min_value_information[line_data[1]] = {line_data[0]: _value}
            else:
                if line_data[0] not in min_value_information[line_data[1]]:
                    min_value_information[line_data[1]][line_data[0]] = _value
                elif _value < min_value_information[line_data[1]][line_data[0]]:
                    min_value_information[line_data[1]][line_data[0]] = _value

        return min_value_information


def get_normal_value_of_two_matrix(matrix_1, matrix_2):
    result = []
    for i in range(len(matrix_1)):
        _result = []
        for j in range(len(matrix_1[i])):
            _result.append(normal(matrix_1[i][j], matrix_2[i][j]))
        result.append(_result)
    return array(result)


def get_trade_off_case():
    # trade_off_case = [[1/3, 1/3]]
    trade_off_case = []
    for i in range(0, 11, 1):
        i /= 10
        _case_1 = [i, round((1 - i) / 2, 2)]
        _case_2 = [round((1 - i) / 2, 2), i]
        _case_3 = [round((1 - i) / 2, 2), round((1 - i) / 2, 2)]
        trade_off_case.append(_case_1)
        trade_off_case.append(_case_2)
        trade_off_case.append(_case_3)
    return trade_off_case


print(get_trade_off_case())

