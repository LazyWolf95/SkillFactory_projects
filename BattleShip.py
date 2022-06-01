from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете мимо поля!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Эта клетка уже поражена"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, ships_length, attitude):
        self.bow = bow
        self.length = ships_length
        self.attitude = attitude
        self.lives = ships_length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.attitude == 1:
                cur_x += i

            elif self.attitude == 0:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooter(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for s in ship.dots:
            if self.out(s) or s in self.busy:
                raise BoardWrongShipException()
        for s in ship.dots:
            self.field[s.x][s.y] = "■"
            self.busy.append(s)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        about = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for s in ship.dots:
            for sx, sy in about:
                cur = Dot(s.x + sx, s.y + sy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        result = ""
        result += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            result += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            result = result.replace("■", "O")
        return result

    def out(self, s):
        return not ((0 <= s.x < self.size) and (0 <= s.y < self.size))

    def shot(self, s):
        if self.out(s):
            raise BoardOutException()

        if s in self.busy:
            raise BoardUsedException()

        self.busy.append(s)

        for ship in self.ships:
            if s in ship.dots:
                ship.lives -= 1
                self.field[s.x][s.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.field[s.x][s.y] = "."
        print("Не попал!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        s = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {s.x+1} {s.y+1}")
        return s


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите цифры! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


def greeting_players():
    print("*******************")
    print("  Добро пожаловать ")
    print("      в игру       ")
    print("    морской бой    ")
    print("*******************")
    print(" формат ввода: x y ")
    print(" x - номер строки  ")
    print(" y - номер столбца ")


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = AI(comp, player)
        self.us = User(player, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        length = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in length:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def boards_print(self):
        print("*" * 20)
        print("Доска пользователя:")
        print(self.us.board)
        print("*" * 20)
        print("Доска компьютера:")
        print(self.ai.board)

    def loop(self):
        num = 0
        while True:
            self.boards_print()
            if num % 2 == 0:
                print("Ход пользователя!")
                repeat = self.us.move()
            else:
                print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                self.boards_print()
                print("*" * 20)
                print("Победил пользователь!")
                break

            if self.us.board.count == 7:
                self.boards_print()
                print("*" * 20)
                print("Победил компьютер!")
                break
            num += 1

    def start(self):
        greeting_players()
        self.loop()


g = Game()
g.start()
