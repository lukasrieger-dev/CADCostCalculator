import sys
import math
import ezdxf

__author__ = 'lukas'


# dxf constants
DXF_TYPE_LWPOLYLINE = 'LWPOLYLINE'
DXF_TYPE_CIRCLE = 'CIRCLE'
DXF_TYPE_TEXT = 'TEXT'


def get_arc_length(p1, p2):
    """
    Helper function to compute the arc length between two points.
    """
    x1, y1, start1, end1, bulge1 = p1
    x2, y2, start2, end2, bulge2 = p2

    # Formula: https://www.liutaiomottola.com/formulae/sag.htm
    l = (x2-x1) * 0.5
    s = l * bulge1
    r = ((s*s) + (l*l)) / (2*s)
    alpha = 2 * math.asin(l/r)
    arc_length = abs(alpha * r)

    return arc_length


def get_polyline_length(polyline):
    """
    Computes the total length of a given polyline.
    A polyline consists of points in the 2D space and a bulge value
    which indicates curves.
    """
    length = 0
    with polyline.points('xyseb') as points:
        if not (points[-1][4] == 0.0000):
            # bulge from last point to first
            length += get_arc_length(points[-1], points[0])

        for i in (range(len(points) - 1)):
            p1 = points[i]
            p2 = points[i + 1]
            x1, y1, start1, end1, bulge1 = p1
            x2, y2, start2, end2, bulge2 = p2

            if bulge1 == 0.0000:
                length += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            else:
                length += get_arc_length(p1, p2)
    return length


def get_edge_sum(msp):
    """
    Iterate over all elements in the modelspace and sum up the edge lengths.
    """
    total_length = 0
    for e in msp:
        dxftype = e.dxftype()
        if dxftype == DXF_TYPE_LWPOLYLINE:
            total_length += get_polyline_length(e)

        elif dxftype == DXF_TYPE_CIRCLE:
            circumference = 2 * e.dxf.radius * math.pi
            total_length += circumference

        else:
            print(f'Fehler: Unbekanntes CAD Element: {dxftype}')
            sys.exit(1)

    return round(total_length, 3)


def get_min_square(msp, offset=5):
    """
    Return the size of the minimal square around this drawing.
    """
    if offset < 0:
        print('Negativer Offset ist nicht erlaubt! Setze Offset = 0')
        offset = 0

    min_x = float('inf'); max_x = float('-inf')
    min_y = float('inf'); max_y = float('-inf')

    for e in msp:
        dxftype = e.dxftype()
        if dxftype == DXF_TYPE_LWPOLYLINE:
            with e.points('xyseb') as points:
                for point in points:
                    x, y, *_ = point
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        elif dxftype == DXF_TYPE_CIRCLE:
            radius = e.dxf.radius
            center = e.dxf.center

            min_x = min(min_x, center[0] - radius)
            max_x = max(max_x, center[0] + radius)
            min_y = min(min_y, center[1] - radius)
            max_y = max(max_y, center[1] + radius)

        elif dxftype == DXF_TYPE_TEXT:
            pass

        else:
            raise ValueError(f'Unknown dxftype {dxftype}!')

    a = max_x - min_x + 2*offset
    b = max_y - min_y + 2*offset

    return a, b, round(a * b, 3)


def get_dxf_model_space(path):
    document = ezdxf.readfile(path)
    return document.modelspace()


def process_dxf_file(path):
    """
    Compute total edge length and minimal square of a given drawing.
    """
    try:
        model_space = get_dxf_model_space(path)
        total_edge_length = get_edge_sum(model_space)
        print(f'Kantenlänge = {round(total_edge_length / 10, 2)}cm')

        # min_square is a tuple! (length a, length b, area)
        min_square = get_min_square(model_space)
        print(f'Kleinstes Rechteck: a = {round(min_square[0] / 10, 2)}cm, b = {round(min_square[1] / 10, 2)}cm, Fläche = {round(min_square[2] / 100, 2)}cm2')
    except FileNotFoundError:
        print(f'Die Datei {path} konnte nicht gefunden werden')
    except Exception as e:
        print(f'Fehler beim Verarbeiten von {path} -> {e}')
        sys.exit(1)

    area_mm2 = min_square[2]
    return total_edge_length, area_mm2