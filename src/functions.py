import json

def read_file(filename):
    """
    Функция открывает файл формата json.
    :param filename: название файла.
    :return: данные, содержащиеся в файле.
    """
    # Построить путь к файлу operations.json относительно папки src
    operate_file = os.path.join(os.path.dirname(__file__), '..', filename)

    # Открыть файл operations.json и загрузить его содержимое
    with open(operate_file, 'r', encoding="utf8") as file:
        file_operations = json.load(file)

    return file_operations


def executed_operations(path):
    """
    Возвращает только выполненные файлы.
    :param path: название файла.
    :return: список выполенных операций.
    """
    executed_title = []
    for operation in path:
        if 'state' in operation and operation['state'] == 'EXECUTED':
            executed_title.append(operation)
    return executed_title


def sorted_file(path):
    """
    Функция сортирует по дате файл из функции executed_operations()
    :param path: название файла
    :return: отсортированный по дате файл
    """
    sorted_operation = []
    for operation in sorted(path, key=lambda operation: operation["date"], reverse=True):
        sorted_operation.append(operation)
        if len(sorted_operation) == 5:
            break
    return sorted_operation
