class Student:

    def __init__(self, tg, name, surname, patronymic, group=None):
        self.tg = tg                    # Телеграмм
        self.name = name                # Имя
        self.second_name = surname      # Фамилия
        self.patronymic = patronymic    # Отчество
        self.group = group              # Группа
