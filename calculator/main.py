from calculator import costfunction
from converter.converter import to_dxf_file
from calculator import config
import os.path
import openpyxl
from shutil import copyfile
from pathlib import Path

__author__ = 'lukas'


def check_convert_to_dxf(file_path, tmp_file_path):
    """
    Check if the file is a .GEO or a .DXF file by trying to convert it to .DXF.
    Since we have no file endings this is the only way so far.
    If the conversion is successfull, the result is saved as tmp.dxf.
    """
    path = file_path
    try:
        file_ending = file_path[-3:]
        if file_ending.upper() == 'GEO':
            to_dxf_file(file_path, tmp_file_path)
            path = tmp_file_path
    except UnicodeDecodeError:
        # file is already .dxf
        pass
    return path


def search_file(start, filename):
    """
    Looks for the given filename starting at the start_folder
    and returns the file path or None.
    """
    try:
        return next(Path(start).rglob(filename))
    except StopIteration:
        return None


def write_to_txt(file_names_not_found):
    """
    Write a list of lines (filenames) to a text file.
    """
    with open('./not_found.txt', 'w') as file:
        file.writelines(file_names_not_found)


def copy(excel_path, source_folder, target_folder, configuration):
    xlsx = openpyxl.load_workbook(excel_path)
    sheet = xlsx.active
    c, r, sep, c2, r2 = sheet.dimensions
    dimensions = c + str(configuration.Nr_erste_Reihe_Daten) + sep + c2 + r2
    values = sheet[dimensions]
    not_found = []

    for lfdNr, menge, file, *_ in values:
        filename = file.value
        source_path = search_file(source_folder, filename)
        if not source_path:
            not_found.append(filename + '\n')
            continue
        copyfile(source_path, target_folder + '/' + filename)

    write_to_txt(not_found)


def calculate_excel(configuration, drawings_path, excel_file_path, tmp_file_path):
    """
    Process the drawings referenced by the given excel file.
    """
    # hard coded material height -> speed table
    cut_speeds = {
        1.5: 6.4, 2: 5.5, 3: 4.3, 4: 3.7, 5: 3.15, 6: 2.8, 8: 2.15,
        10: 1.8, 12: 1.5, 15: 1, 16: 0.9, 20: 0.65,
    }
    drawings_path += '/'
    copy(excel_file_path, drawings_path, './Zeichnungen', configuration)

    xlsx = openpyxl.load_workbook(excel_file_path)
    sheet = xlsx.active
    min_dimension = 'A' + str(int(configuration.Nr_erste_Reihe_Daten))
    max_dimension = sheet.dimensions.split(':')[1]
    working_dimensions = min_dimension + ':' + max_dimension
    values = sheet[working_dimensions]
    row_index = int(configuration.Nr_erste_Reihe_Daten - 1)
    sum_of_all_cost = 0

    cell = configuration.Ausgabespalte + str(row_index)
    sheet[cell] = 'Kosten in €'

    # iterate over each line of the excel file
    for LfdNr, Liefermenge, ZeichnungsNr, Benennung, Dicke, Material in values:
        row_index += 1
        file_path = './Zeichnungen/' + ZeichnungsNr.value

        if not os.path.exists(file_path):
            continue

        file_path = check_convert_to_dxf(file_path, tmp_file_path)

        cost = costfunction.compute_cost(
            Liefermenge.value,
            file_path,
            Dicke.value,
            cut_speeds.get(int(Dicke.value), 0), #configuration.Schnittgeschwindigkeit_mm_s TODO: Fehlermeldung wenn unbekannte Dicke
            configuration.Kosten_Schnitt_euro_min,
            configuration.Materialgewicht_g_cm3,
            configuration.Materialkosten_euro_t,
            configuration.Gewinnmarge,
            configuration.Offset
        )

        sum_of_all_cost += cost

        # comma instead of dot for prices
        cell = configuration.Ausgabespalte + str(row_index)
        c = format(cost, '.2f')
        c = str(c)
        c = c.replace('.', ',')
        sheet[cell] = c

    xlsx.save('./output.xlsx')
    return sum_of_all_cost


def calculate_single_file(configuration, drawings_path, tmp_file_path):
    """
    Process only one single .GEO or .DXF file.
    """
    path = check_convert_to_dxf(drawings_path, tmp_file_path)

    return costfunction.compute_cost(
        1,
        path,
        configuration.Std_Dicke_mm,
        configuration.Schnittgeschwindigkeit_mm_s,
        configuration.Kosten_Schnitt_euro_min,
        configuration.Materialgewicht_g_cm3,
        configuration.Materialkosten_euro_t,
        configuration.Gewinnmarge,
        configuration.Offset
    )


def calculate(parameters, drawings_path, excel_file_path=None):
    """
    Depending on the inputs we either have to process an excel file or
    a single .GEO or .DXF file
    """
    tmp_file_path = './tmp.DXF'
    configuration = config.Configuration(**parameters)

    if excel_file_path:
        cost = calculate_excel(configuration, drawings_path, excel_file_path, tmp_file_path)
    else:
        cost = calculate_single_file(configuration, drawings_path, tmp_file_path)

    return cost
