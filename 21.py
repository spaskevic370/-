# Простой интерпретатор арифметических выражений
# Вариант 46:
# Функция abs() и побитовое И (&)

tokens = []
position = 0


def make_tokens(text):
    result = []
    i = 0

    while i < len(text):
        char = text[i]

        if char.isspace():
            i += 1

        elif char.isdigit() or char == '.':
            number = ''

            while i < len(text) and (
                text[i].isdigit() or text[i] == '.'
            ):
                number += text[i]
                i += 1

            try:
                if number.count('.') > 1 or number == '.':
                    raise ValueError()

                if '.' in number:
                    result.append(float(number))
                else:
                    result.append(int(number))

            except ValueError:
                raise ValueError("Неправильно записано число")

        elif text[i:i + 3] == 'abs':
            result.append('abs')
            i += 3

        elif char in '+-*/&()':
            result.append(char)
            i += 1

        else:
            raise ValueError(
                "Неизвестный символ: " + char
            )

    result.append('END')
    return result


def current():
    return tokens[position]


def next_token():
    global position

    token = current()
    position += 1
    return token


def parse_value():
    token = current()

    if token == 'abs':
        next_token()

        if current() != '(':
            raise ValueError(
                "После abs должна быть открывающая скобка"
            )

        next_token()
        value = parse_and()

        if current() != ')':
            raise ValueError("Не закрыта скобка")

        next_token()
        return abs(value)

    elif token == '(':
        next_token()
        value = parse_and()

        if current() != ')':
            raise ValueError("Не закрыта скобка")

        next_token()
        return value

    elif isinstance(token, (int, float)):
        next_token()
        return token

    else:
        raise ValueError("Проверьте выражение")


def parse_unary():
    if current() == '-':
        next_token()
        return -parse_unary()

    elif current() == '+':
        next_token()
        return parse_unary()

    return parse_value()


def parse_mul():
    value = parse_unary()

    while current() == '*' or current() == '/':
        operator = next_token()
        right = parse_unary()

        if operator == '*':
            value = value * right
        else:
            if right == 0:
                raise ValueError("На ноль делить нельзя")

            value = value / right

    return value


def parse_sum():
    value = parse_mul()

    while current() == '+' or current() == '-':
        operator = next_token()
        right = parse_mul()

        if operator == '+':
            value = value + right
        else:
            value = value - right

    return value


def parse_and():
    value = parse_sum()

    while current() == '&':
        next_token()
        right = parse_sum()

        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(
                "Для операции & нужны целые числа"
            )

        if not isinstance(right, int) or isinstance(right, bool):
            raise ValueError(
                "Для операции & нужны целые числа"
            )

        value = value & right

    return value


def calculate(text):
    global tokens, position

    tokens = make_tokens(text)
    position = 0

    result = parse_and()

    if current() != 'END':
        raise ValueError("Проверьте выражение")

    return result

while True:
    expression = input("\nВведите выражение: ")

    if expression.lower() == 'exit':
        print("Программа завершена")
        break

    try:
        result = calculate(expression)
        print("Ответ:", result)

    except ValueError as error:
        print("Ошибка:", error)

    except IndexError:
        print("Ошибка: проверьте выражение")
