from src.functions import read_file, executed_operations, sorted_file, show_operations


def main():
    # Чтение данных из файла
    operations = read_file('operations.json')

    # Фильтрация операций по статусу "Выполнено"
    executed_operation = executed_operations(operations)

    # Сортировка операций по дате
    sorted_operations = sorted_file(executed_operation)

    # Вывод отсортированных операций в заданном формате
    show_operations(sorted_operations)

if __name__ == '__main__':
    main()
