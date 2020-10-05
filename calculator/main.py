import openpyxl
from calculator import costfunction
from converter.converter import to_dxf_file
from calculator import config
from scripts.copy_files import copy
import os.path


__author__ = 'lukas'


def check_convert_to_dxf(file_path, tmp_file_path):
    """
    Check if the file is a .GEO or a .DXF file by trying to convert it to .DXF.
    Since we have no file endings this is the only way so far.
    If the conversion is successfull, the result is saved as tmp.dxf.
    """
    path = file_path
    try:
        to_dxf_file(file_path, tmp_file_path)
        path = tmp_file_path
    except UnicodeDecodeError:
        # file is already .dxf
        pass
    return path


def calculate_excel(configuration, drawings_path, excel_file_path, tmp_file_path):
    """
    Process the drawings referenced by the given excel file.
    """
    cut_speeds = {
        2: 60,
        5: 50,
        10: 25,
        15: 10,
        20: 5,
        25: 3,
    }
    drawings_path += '/'
    copy(excel_file_path, drawings_path, './Zeichnungen')

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
            cut_speeds.get(int(Dicke.value), 1), #configuration.Schnittgeschwindigkeit_mm_s
            configuration.Kosten_Schnitt_euro_min,
            configuration.Materialgewicht_g_cm3,
            configuration.Materialkosten_euro_t,
            configuration.Gewinnmarge,
            configuration.Offset
        )

        sum_of_all_cost += cost
        cell = configuration.Ausgabespalte + str(row_index)
        sheet[cell] = format(cost, '.2f')

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
