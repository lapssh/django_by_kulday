while True:
    num1 = int(input('Введите первое число: '))
    if num1 == 0:
        break
    num2 = int(input('Введите второе число: '))
    print(f'{num1} делится нацело на {num2} = {num1//num2}')
    print(f'{num1} остаток от деления на {num2} = {num1%num2}')
