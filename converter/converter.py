import ezdxf
from calculator.dxfutils import distance_2d
import math


__author__ = 'lukas'


def read_section(geo_file_path, section_id):
    """
    Reads the section indicated by the id from the .geo file and returns
    all lines from the section in a list of strings.
    """
    read = False
    section = []

    with open(geo_file_path) as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(section_id):
                read = True

            if line.startswith('##~~'):
                # Don't stop, section can be split
                read = False

            if read:
                section.append(line)

    return section


def get_points(geo_file_path):
    """
    Extracts all points (coordinates) from the .geo file and stores them
    in a dictionary: key = point id, value = x, y
    """
    points = dict()
    point_idx = 1
    section_points = read_section(geo_file_path, '#~31')

    for line in section_points:
        split = line.split(' ')
        if len(split) == 3:
            x, y, _ = split
            points[str(point_idx)] = float(x), float(y)
            point_idx += 1

    return points


def get_elements(geo_file_path):
    """
    Extracts the CAD elements from the elements section and returns them
    as a list of tuples. The first entry of each tuple is the element type name.
    """
    section_elements = read_section(geo_file_path, '#~331')
    elements = []

    for i in range(len(section_elements)):
        line = section_elements[i]

        if line.startswith('LIN'):
            points = section_elements[i+2].split(' ')
            elements.append(('LIN', points[0], points[1].strip('\n')))

        if line.startswith('ARC'):
            points = section_elements[i+2].split(' ')
            elements.append(('ARC', points[0], points[1], points[2].strip('\n')))

        if line.startswith('CIR'):
            center_id = section_elements[i+2].strip('\n')
            radius = float(section_elements[i+3].strip('\n'))
            elements.append(('CIR', center_id, radius))

    return elements


def to_dxf_file(geo_file_path, output_file_path):
    """
    Converts a .geo file to a .dxf file.
    """
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    points = get_points(geo_file_path)
    elements = get_elements(geo_file_path)

    for element in elements:
        element_type = element[0]
        print(element_type)

        if element_type.startswith('LIN'):
            type_, p_id_1, p_id_2 = element
            p1 = points[p_id_1]
            p2 = points[p_id_2]

            msp.add_line(p1, p2)

        if element_type.startswith('ARC'):
            type_, center_id, start_id, end_id = element
            center = points[center_id]
            start = points[start_id]
            end = points[end_id]

            radius = distance_2d(center, start)
            angle_start = math.degrees(math.atan2(start[1]-center[1], start[0]-center[0]))
            angle_end = math.degrees(math.atan2(end[1]-center[1], end[0]-center[0]))

            msp.add_arc(center, radius, angle_start, angle_end)

        if element_type == 'CIR':
            type_, center_id, radius = element
            center = points[center_id]

            msp.add_circle(center, radius)

    doc.saveas(output_file_path)


if __name__ == '__main__':
    print('#     GEO to DXF Converter    #')
    input_file = input('Enter input file path:')
    output_file_name = input('Enter output name')
    to_dxf_file(input_file, output_file_name)
