import math
import ezdxf
import logging

__author__ = 'lukas'


# dxf constants
DXF_TYPE_LWPOLYLINE = 'LWPOLYLINE'
DXF_TYPE_CIRCLE = 'CIRCLE'
DXF_TYPE_TEXT = 'TEXT'
DXF_TYPE_MTEXT = 'MTEXT'
DXF_TYPE_LINE = 'LINE'
DXF_TYPE_ARC = 'ARC'
DXF_TYPE_INSERT = 'INSERT'


def distance_2d(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distance


def get_arc_length_simple(radius, angle):
    arc_length = 2*math.pi*radius * angle/360

    return arc_length


def get_arc_length(p1, p2):
    """
    Helper function to compute the arc length between two points.
    """
    x1, y1, start1, end1, bulge1 = p1
    x2, y2, start2, end2, bulge2 = p2

    reverse = False
    bulge = abs(bulge1)

    # If bulge is greater 1.0, the angle is greater 180 degrees.
    # We consider the case 360 - angle and reverse in the end.
    if bulge > 1.0:
        bulge = bulge - int(bulge) # only take digits after float point
        reverse = True

    # l is half the base side of the triangle
    l = 0.5 * distance_2d((x1, y1), (x2, y2))

    # s is the sagita: the distance between the base side of the triangle
    # and the circle. The bulge value can be negative, denoting the side
    # of the curve. Not important for its length.
    s = l * bulge

    # compute the circle's radius
    r = ((s*s) + (l*l)) / (2*s)

    # height of the triangle
    h = r - s

    if h == 0.0:
        # edge case: half circle leads to h = 0
        alpha = math.pi
    else:
        # angle in the triangle in the middle of the circle
        alpha = 2 * math.atan(l/h)

    # arc length as part of the entire circumference of the circle
    arc_length = alpha * r

    if reverse:
        arc_length = 2*r*math.pi - arc_length

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
                length += distance_2d((x1, y1), (x2, y2))
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

        elif dxftype == DXF_TYPE_ARC:
            angle = e.dxf.end_angle - e.dxf.start_angle
            total_length += get_arc_length_simple(e.dxf.radius, angle)

        elif dxftype == DXF_TYPE_LINE:
            x1, y1, _ = e.dxf.start
            x2, y2, _ = e.dxf.end
            total_length += distance_2d((x1, y1), (x2, y2))

        elif dxftype in {DXF_TYPE_TEXT, DXF_TYPE_INSERT, DXF_TYPE_MTEXT}:
            continue

        else:
            logging.error(f'Fehler -> {dxftype} is unknown.')
            raise ValueError(f'Fehler: Unbekanntes CAD Element: {dxftype}')

    return round(total_length, 3)


def get_min_square(msp, offset=5):
    """
    Return the size of the minimal square around this drawing.
    """
    if offset < 0:
        print('Negativer Offset ist nicht erlaubt! Setze Offset = 0')
        offset = 0

    all_points = []

    for e in msp:
        dxftype = e.dxftype()
        if dxftype == DXF_TYPE_LWPOLYLINE:
            with e.points('xyseb') as points:
                for point in points:
                    x, y, *_ = point
                    all_points.append((x, y))

        elif dxftype == DXF_TYPE_CIRCLE:
            radius = e.dxf.radius
            center = e.dxf.center

            all_points.append((center[0] - radius, center[1] - radius))
            all_points.append((center[0] + radius, center[1] + radius))

        elif dxftype == DXF_TYPE_LINE:
            x1, y1, _ = e.dxf.start
            x2, y2, _ = e.dxf.end

            all_points.append((x1, y1))
            all_points.append((x2, y2))

        elif dxftype == DXF_TYPE_ARC:
            x1, y1, _ = e.start_point
            x2, y2, _ = e.end_point
            radius = e.dxf.radius
            center = e.dxf.center

            all_points.append((x1, y1))
            all_points.append((x2, y2))
            all_points.append((center[0] - radius, center[1] - radius))
            all_points.append((center[0] + radius, center[1] + radius))

            #farest_point = compute_farest_point(e)
            #all_points.append(farest_point)

        elif dxftype in {DXF_TYPE_TEXT, DXF_TYPE_INSERT, DXF_TYPE_MTEXT}:
            continue

        else:
            logging.error(f'Fehler -> {dxftype} is unknown.')
            raise ValueError(f'Fehler: Unbekanntes CAD Element: {dxftype}')

    if not all_points:
        raise ValueError('Die/eine angegebene Zeichnung ist leer/fehlerhaft.')

    min_x = min(all_points, key=lambda p: p[0])[0]
    min_y = min(all_points, key=lambda p: p[1])[1]
    max_x = max(all_points, key=lambda p: p[0])[0]
    max_y = max(all_points, key=lambda p: p[1])[1]

    a = max_x - min_x + 2*offset
    b = max_y - min_y + 2*offset

    return a, b, round(a * b, 3)


def compute_farest_point(e):
    """
    OUTMOST point on arc?!
    """
    center_x, center_y, *_ = e.dxf.center
    start_angle = e.dxf.start_angle
    end_angle = e.dxf.end_angle

    #if start_angle > end_angle:
        #rotation_angle = (start_angle - end_angle)/2
        #rotation_angle += 180
    #else:
    rotation_angle = (end_angle - start_angle)/2

    radius = e.dxf.radius
    x = center_x + radius * math.cos(rotation_angle)
    y = center_y + radius * math.sin(rotation_angle)

    return x, y


def get_dxf_model_space(path):
    """
    Return the DXF file's model space.
    """
    document = ezdxf.readfile(path)
    return document.modelspace()


def process_dxf_file(path, offset):
    """
    Compute total edge length and minimal square of a given drawing.
    """
    model_space = get_dxf_model_space(path)
    total_edge_length = get_edge_sum(model_space)
    logging.debug(f'Kantenlänge = {round(total_edge_length / 10, 2)}cm')

    # min_square is a tuple! (length a, length b, area)
    min_square = get_min_square(model_space, offset)
    logging.debug(f'Kleinstes Rechteck: a = {round(min_square[0] / 10, 2)}cm, b = {round(min_square[1] / 10, 2)}cm, Fläche = {round(min_square[2] / 100, 2)}cm2')

    area_mm2 = min_square[2]
    return total_edge_length, area_mm2