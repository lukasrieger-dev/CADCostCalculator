def compute_part_weight(min_square, height, weight_g_cm3):
    """
    Compute the weight in gramme of the given part size and height depending
    on the grammes weight per volume.
    """
    # mm2 * mm -> mm3 -> /1000 -> cm3
    volume_cm3 = min_square * height / 1000
    weight_g = volume_cm3 * weight_g_cm3

    return weight_g
