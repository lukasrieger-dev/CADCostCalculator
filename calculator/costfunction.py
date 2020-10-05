from calculator import dxfutils
from calculator.utils import *
import logging

__author__ = 'lukas'


def compute_cost(amount, file_path, height, speed, cut_speed_price_min, weight_g_cm3, material_cost_per_t, marge, offset):
    """
    Compute the cost of this position as given in this dxf file.
    A position is a part and the amount of this part.
    The cost formula is: cost = amount * margin * (material cost + time cost)
    """
    total_edge_length, min_square = dxfutils.process_dxf_file(file_path, offset)

    # material cost
    part_weight_g = compute_part_weight(min_square, height, weight_g_cm3)
    logging.debug(f'Gewicht/Teil: {round(part_weight_g/1000, 2)}kg')

    cost_per_g = material_cost_per_t / (1000 * 1000)

    # cost in Euro per g
    material_cost = part_weight_g * cost_per_g
    logging.debug(f'Materialkosten/Teil: {round(material_cost, 2)}€')

    # work time cost
    work_time_s = total_edge_length / speed
    time_cost = work_time_s * cut_speed_price_min / 60
    logging.debug(f'Zeitkosten/Teil: {round(time_cost, 2)}€')

    cost = amount * marge * (material_cost + time_cost)

    return cost
