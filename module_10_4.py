from threading import Thread
from queue import Queue
from time import sleep       #  Модуль для задержки sleep
from random import randint   # Модуль случайных чисел randmint

class Table:
    def __init__(self, number):
        self.number = number       # Номер стола
        self.guest = None          # Гость, который сидит за столом number

class Guest(Thread):
    def __init__(self, name=''):
        super().__init__()         # Инициализация для потоков
        self.name = name           # Имя посетителя (str)

    def run(self):                    # Метод для задержки
        sleep(randint(3, 10))   # Задержка на случайное количество от 3 до 10 секунд

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()             # Очередь в виде списка
        self.tables = list(tables)       # Столы в кафе (в виде списка столов)

    def guest_arrival(self, *guests):
        for guest in guests:                      # Для каждого гостя из списка гостей
            for table in self.tables:             # Для каждого стола из списка столов
                if table.guest is None:           # Если стол свободен (ищем свободный стол), то
                    table.guest = guest           # посетителю присваивается номер стола
                    guest.start()                 # Запускаем поток посетителя
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")  # Выводим сообщение
                    break                         # Если посетителю определили стол, то выходим из цикла
            else:                                 # Если свободный стол не найден, то
                self.queue.put(guest)             # добавляем посетителя в очередь
                print(f"{guest.name} в очереди")  # Выводим сообщение

    def discuss_guests(self):
        while self.queue or any(table.guest is not None for table in self.tables):
            # Пока очередь self.queue не пуста или один из столов из списка занят
            for table in self.tables:                   # Для каждого стола из списка столов
                if table.guest is not None and not table.guest.is_alive():  # Если стол занят и поток table.guest завершен
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")   # Выводим сообщение
                    table.guest = None                                      # Указываем, что стол свободен
                    print(f"Стол номер {table.number} свободен")            # Выводим сообщение
                if table.guest is None and self.queue:                      # Если стол свободен и очередь есть,то
                    if self.queue.empty() and any(table.guest is None for table in self.tables):
                                                   # Если очередь пуста и все столы свободны, то посетители обслужены и
                        return                     # выходим из функции
                    guest = self.queue.get()            # забираем из списка первого посетителя с индексом [0]
                    table.guest = guest                 # Посетителю присваивается номер стола
                    print(f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                    guest.start()                       # Запускаем поток посетителя

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel',
'Ilya', 'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
