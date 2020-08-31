import openpyxl
from shutil import copyfile
from pathlib import Path


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


if __name__ == '__main__':
    excel_path = input('Pfad + Name der Excel-Datei: ')
    source_folder = input('Pfad zum Start-Ordner: ')
    target_folder = input('Pfad zum Ziel-Ordner: ')

    # Die Excel-Datei enthält eine Spalte mit Dateinamen, ohne Überschrift!
    xlsx = openpyxl.load_workbook(excel_path)
    sheet = xlsx.active
    dimensions = sheet.dimensions
    values = sheet[dimensions]
    not_found = []

    for file in values:
        filename = file.value
        source_path = search_file(source_folder, filename)
        if not source_path:
            print(f'Datei nicht gefunden: {filename}')
            not_found.append(filename + '\n')
            continue
        copyfile(source_path, target_folder + '/' + filename)

    write_to_txt(not_found)