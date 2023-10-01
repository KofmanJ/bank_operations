from src.functions import executed_operations, sorted_file, data_format, masked_card, masked_account, extract_value


def test_executed_operations():
    operations = [
        {'id': 1, 'state': 'EXECUTED', 'amount': 100},
        {'id': 2, 'state': 'CANCELLED', 'amount': 200},
        {'id': 3, 'state': 'EXECUTED', 'amount': 150},
        {'id': 4, 'amount': 50},
        {'id': 5, 'state': 'CANCELLED', 'amount': 75},
        {'id': 6, 'state': 'EXECUTED', 'amount': 300},
    ]
    executed_operation = executed_operations(operations)
    assert len(executed_operation) == 3
    assert executed_operation[0]['id'] == 1
    assert executed_operation[1]['id'] == 3
    assert executed_operation[2]['id'] == 6


def test_sorted_file():
    executed_operation = [
        {'id': 1, 'state': 'EXECUTED', "date": "2018-07-11T02:26:18.671407"},
        {'id': 2, 'state': 'CANCELLED', "date": "2019-07-12T20:41:47.882230"},
        {'id': 3, 'state': 'EXECUTED', "date": "2019-04-12T17:27:27.896421"},
        {'id': 4, 'state': 'EXECUTED', "date": "2018-12-28T23:10:35.459698"},
        {'id': 5, 'state': 'CANCELLED', "date": "2018-07-31T12:25:32.579413"},
    ]
    sorted_operation = sorted_file(executed_operation)
    assert sorted_operation == [
        {'id': 2, 'state': 'CANCELLED', "date": "2019-07-12T20:41:47.882230"},
        {'id': 3, 'state': 'EXECUTED', "date": "2019-04-12T17:27:27.896421"},
        {'id': 4, 'state': 'EXECUTED', "date": "2018-12-28T23:10:35.459698"},
        {'id': 5, 'state': 'CANCELLED', "date": "2018-07-31T12:25:32.579413"},
        {'id': 1, 'state': 'EXECUTED', "date": "2018-07-11T02:26:18.671407"},
    ]


def test_data_format():
    date = '2018-09-12T21:27:25.241689'
    assert data_format(date) == '12.09.2018'


def test_masked_card():
    card_number = '7305799447374042'
    masked_number = masked_card(card_number)
    assert len(card_number) == 16
    assert masked_number == '7305 79** **** 4042'



def test_masked_account():
    account_number = '78808375133947439319'
    masked_account_number = masked_account(account_number)
    assert len(account_number) == 20
    assert masked_account_number == '**9319'


def test_extract_value():
    operations = [
        {'id': 1, "to": "Maestro 3364923093037194"},
        {'id': 3, "from": "Счет 35116633516390079956"},
        {'id': 4}
    ]
    assert extract_value(operations, 'to') == 'Maestro 3364 92** **** 7194'
    assert extract_value(operations, 'from') == 'Счет **9956'
    assert extract_value(operations, None) == None
