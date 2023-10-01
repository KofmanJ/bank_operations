import json
import os
from datetime import datetime

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
    Функция возвращает только выполненные файлы.
    :param path: название файла.
    :return: список выполненных операций.
    """
    executed_title = []
    for operation in path:
        if 'state' in operation and operation['state'] == 'EXECUTED':
            executed_title.append(operation)
    return executed_title


def sorted_file(path):
    """
    Функция сортирует по дате файл из функции executed_operations().
    :param path: название файла.
    :return: отсортированный по дате файл.
    """
    sorted_operation = []
    for operation in sorted(path, key=lambda operation: operation["date"], reverse=True):
        sorted_operation.append(operation)
        if len(sorted_operation) == 5:
            break
    return sorted_operation


def data_format(date_str):
    """
    Функция возвращает дату в понятном для клиента формате "ДД.ММ.ГГГГ".
    :param date_str: строка с датой.
    :return: строка с датой в формате "ДД.ММ.ГГГГ".
    """
    date_formatted = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
    return date_formatted.strftime('%d.%m.%Y')


def masked_card(card_number):
    """
    Функция принимает на вход номер кредитной карты и возвращает его маскированную версию.
    Первые 6 и последние 4 цифры остаются видимыми, остальные маскируются символами *.
    :param card_number: номер карты.
    :return: замаскированный номер.
    """
    masked_number = card_number[:4] + ' ' + card_number[4:6] + '** **** ' + card_number[-4:]
    return masked_number


def masked_account(account_number):
    """
    Функция принимает на вход номер банковского счета и возвращает его маскированную версию.
    :param account_number: номер банковского счета.
    :return: маскированная версия номера.
    """
    masked_number = '**' + account_number[-4:]
    return masked_number


def extract_value(json_list, key):
    """
    Функция извлекает значение заданного ключа из списка словарей и возвращает замаскированный номер счета или карты.
    :param json_list: cписок словарей.
    :param key: ключ, из которого необходимо извлечь значение.
    :return: замаскированный номер счета или карты. Значение None, если ключа нет в словаре.
    """
    # Список платежных систем, для которых необходимо маскировать номера карт.
    payment_list = ["MasterCard", "Maestro", "Visa Gold", "Visa Platinum", "Visa Classic", "МИР"]

    for item in json_list:    # Выполняемые иттерации по каждому словарю из списка.
        if key in item:    # Если ключ найден в словаре, значение будет извлечено.
            value = item[key]
            if value.startswith("Счет"):    # Если значение начинается со "Счет", извлекается номер счета.
                account_number = value.split()[-1]    # Разделяем строку на список подстрок и извлекаем номер счета.
                masked_number = masked_account(account_number)    # Маскируем номер счета с помощью функции.
                return f"Счет {masked_number}"
            else:
                card_number = None
                for card_type in payment_list:    # Выполняем итерацию по списку платежных систем.
                    value_list = value.split()
                    if card_type in value:    # Проверяем наличие платежной системы в словаре.
                        card_number = value.split()[-1]    # Извлекаем номер карты.
                        masked_number = masked_card(card_number)    # Маскируем номер карты с помощью функции.
                        if len(value.split()) == 3:
                            return f"{' '.join(value_list[0:2])} {masked_number}"
                        elif len(value.split()) == 2:
                            return f"{' '.join(value_list[0:1])} {masked_number}"
                if card_number is None:
                    return None
    return None


def show_operations(operations):
    """
    Функция выводит информацию о каждой операции в удобном для пользователя формате на экран.
    :param operations: список операций, каждая из которых представлена в виде словаря.
    :return: None.
    """
    # Проходим по каждой операции в списке операций
    for operation in operations:
        date = data_format(operation["date"])    # Получаем дату операции
        description = operation["description"]    # Получаем описание операции
        from_value = extract_value([operation], "from")
        to_value = extract_value([operation], "to")
        amount = operation["operationAmount"]["amount"]
        currency = operation["operationAmount"]["currency"]["name"]
        if from_value == None:
            print(f"{date} {description}\n{to_value}\n{amount} {currency}\n")
        else:
            print(f"{date} {description}\n{from_value} -> {to_value}\n{amount} {currency}\n")