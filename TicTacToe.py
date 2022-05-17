# Игровое поле в виде списка
field = [['-'] * 3 for i in range(3)]
# Список выигрышных линий
win_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


# Функция приветствия игроков
def greeting():
    print("***************************")
    print("* Добро пожаловать в игру *")
    print('*    "Крестики-нолики"    *')
    print("***************************")


# Функция отрисовки игрового поля
def show_game_field():
    print("                      ")
    print("        | 0 | 1 | 2 | ")
    print("      --------------- ")
    for i, row in enumerate(field):
        row_field = f"      {i} | {' | '.join(row)} |"
        print(row_field)
        print("      --------------- ")


# Функция, принимающая ходы игроков
def ask_place():
    while True:
        cords = input("Введите координаты через пробел (сначала x, потом y): ").split()
        if len(cords) != 2:
            print("Введите две координаты!")
            continue

        if not (cords[0].isdigit()) or not (cords[1].isdigit()):
            print("Координаты должны быть числом!")
            continue

        x, y = map(int, cords)

        if not (0 <= x <= 2) or not(0 <= y <= 2):
            print("Координаты вне диапазона!")
            continue

        if field[x][y] != '-':
            print("Клетка занята другим игроком!")
            continue

        return x, y


# Функция определения победителя
def win_line(f, player):
    f_list = []
    for i in f:
        f_list += i
    indices = set([i for i, x in enumerate(f_list) if x == player])

    for p in win_lines:
        if len(indices.intersection(set(p))) == 3:
            return True
    return False


# Функция игры
def game():
    # Обнуляем счетчик ходов
    cnt_motion = 0
    # Вызываем приветствие
    greeting()

    while True:
        # Прибавляем количество ходов
        cnt_motion += 1
        # Отрисовываем поле
        show_game_field()
        # Определяем кто ходит крестик или нолик
        if cnt_motion % 2 != 0:
            print("Ходит крестик")
            player = 'X'
        else:
            print("Ходит нолик")
            player = 'O'
        # Получаем координаты клетки
        x, y = ask_place()
        # Пока сделано меньше 9 ходов заполняем поле
        if cnt_motion < 9:
            field[x][y] = 'X' if player == 'X' else 'O'
        # Если ходов 9 и нет победителя, то ничья и выход из цикла
        elif cnt_motion == 9:
            show_game_field()
            print("Ничья :(")
            break
        # Если сделано три и более хода проверяем нет ли победителя
        if cnt_motion >= 3:
            if win_line(field, player):
                show_game_field()
                print(f"Победил {player}, поздравляем!")
                break


game()
