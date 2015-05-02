import time
import quest

class Student:
    """ 
        границы изменения параметров [-100, 100]
        критические границы [-100, -80] U [80, 100]
    """
    # параметр: настроение (0 -- нейтральное)
    mood = 0
    # параметр: успеваемость (0 -- обычная)
    progress = 0
    # параметр: сытость (0 - ...)
    satiety = 0
    # параметр: финансы (0 - ...)
    finances = 0
    # текущее задание
    quest = quest.Quest()
    # вариант решения задания
    choice = 0
    
    """
        назначение: инициализации класса
        входные параметры:
            mood        -- настроение
            progress    -- успеваемость
            satiety     -- сытость
            finances    -- финансы
            quest       -- текущее задание
            choice      -- вариант решения задания
        выходные параметры:
            None
    """
    def __init__(self, mood=0, progress=0, satiety=0, finances=0, quest=quest, choice=0):
        self.mood = mood
        self.progress = progress
        self.satiety = satiety
        self.finances = finances
        # дальнейшие настройки
        self.quest = quest
        self.choice = choice

    """
        назначение: вывод информации о текущем состоянии студента
        входные параметры:
            None
        выходные параметры:
            None
    """
    def __str__(self):
        return 'student: mood = {}, progress = {}, satiety = {}, ' \
          'finances = {}; quest: {} [{}]'.format(self.mood, self.progress, self.satiety, self.finances, self.quest.name, self.quest.duration)

    def change(self, vector):
        for i in vector:
            if i == 'mood':
                self.mood += vector[i]
            elif i == 'progress':
                self.progress += vector[i]
            elif i == 'satiety':
                self.satiety += vector[i]
            else:
                self.finances += vector[i]

    """
        назначение: изменение параметров во времени
        входные параметры:
            step        -- шаг
        выходные параметры:
            None
    """
    def step(self, step=10):
        # код отвечающий за изменение параметров 
        # в соответствии с интервалом времени
        
        # каждый шаг студенту становится скучнее и голоднее
        self.mood -= 1
        self.satiety -= 1
        # продолжение квеста или же выбор нового
        self.quest.duration -= 1
        if self.quest.duration <= 0:
            if self.choice:
                self.change(self.quest.one_impact)
            else:
                self.change(self.quest.two_impact)
            del self.quest
            # генерация задания
            st = [
                self.mood,
                self.progress,
                self.satiety,
                self.finances
            ]
            self.quest = quest.generate(st)
            self.choice = quest.auto_choice(st, self.quest)
            if self.choice:
                print('Студент выбирает первый вариант решения: {}'.format(self.quest.one_name))
            else:
                print('Студент выбирает второй вариант решения: {}'.format(self.quest.two_name))
        # вывод информации о студенте в текущий момент времени
        print(str(self))

    """
        добавить функцию внешних факторов влияющую на систему
        посредство взаимодействия с окружающими людьми/факторами/случайностями
    """
    from random import randint

    def captainCall(self):
        mood = progress = satiety = finances = 0
        info = ''
        if self.progress <= -25:
            # bad
            info = 'слишком плохой день...'
            mood = -self.inspired / 2
            progress = 5
        elif self.progress <= 50:
            # normal
            info = 'зачем?!'
            mood = -1
            progress = 1
        else:
            # good
            info = 'я умняшка...'
            mood = self.inspired / 2
            progress = 5
        return Quest({'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': finances}, \
            {}, self.xp, info, 1)

    def inspiredCall(self):
        jobSelect = randint(4)
        mood = progress = satiety = finances = 0
        info = ''
        if jobSelect == 0:
            # mood
            mood = self.inspired
            info = 'всё хорошо!'
        elif jobSelect == 1:
            # progress
            progress = self.inspired
            info = 'да я крут...'
        elif jobSelect == 2:
            # satiety
            satiety = self.inspired
            info = 'больше не могу'
        elif jobSelect == 3:
            # finances
            finances = self.inspired
            mood = self.inspired / 2
            info = '*вы находите 1000 рублей*'
        return Quest({'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': finances}, \
            {}, self.xp, info, 1)
