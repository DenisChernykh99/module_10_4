import threading
from queue import Queue
import time
import random


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name_guest):
        threading.Thread.__init__(self)
        self.name_guest = name_guest

    def run(self):
        # Гость ест от 3 до 10 секунд
        sleep_time = random.randint(3, 10)
        time.sleep(sleep_time)


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                free_table = next(table for table in self.tables if table.guest is None)
                free_table.guest = guest
                print(f'{guest.name_guest} сел(-а) за стол номер {free_table.number}')
                guest.start()
            else:
                self.queue.put(guest)
                print(f'{guest.name_guest} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name_guest} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None

            if not self.queue.empty():
                for table in self.tables:
                    if table.guest is None:
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        print(f'{new_guest.name_guest} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                        new_guest.start()
                        break


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
