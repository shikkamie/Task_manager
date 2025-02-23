"""
Тестовое задание 1:
Напиши программу, которая:

    Запрашивает у пользователя список чисел (например, через input).
    Создаёт класс NumberAnalyzer с методом, который находит среднее арифметическое этих чисел.
    Выводит результат.
    Отправь мне код, я проверю и дам обратную связь.
"""

class NumberAnalyzer:
    def __init__(self, numbers):
        self.numbers = numbers

    def average(self):
        if not self.numbers:
            return 0
        return sum(self.numbers) / len(self.numbers)


def get_input_user():
    print('Вводите числа по одному. Для завершения введите <q>')
    user_input = []

    while True:
        try:

            a = input('Ввод: ')
            if a.lower() == 'q':
                break
            user_input.append(int(a))
        except ValueError:
            print("И чё ты ввёл?\nВводи заново")





    return user_input



et = get_input_user()

test = NumberAnalyzer(et)
print(test.average())
