from random import randint, random
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
    log = None
    # константы
    xp = 50
    inspired = 20
    
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
    def __init__(self, log, mood=0, progress=0, satiety=0, finances=0, quest=quest, choice=0):
        self.log = log
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
        fmt_str = 'student: mood = {}, progress = {}, satiety = {}, finances = {} [{}]'
        return fmt_str.format(self.mood, self.progress, self.satiety, self.finances,
            self.quest.duration)

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
            chance = random()
            # подобрать вероятность для случайных событий
            if chance <= 0.05:
                self.quest = self.inspiredCall()
            elif chance <= 0.2:
                self.quest = self.captainCall()
            else:
                self.quest = quest.generate(st)
            self.choice = quest.auto_choice(st, self.quest)
            fmt_str = '{} {}'
            if self.choice:
                fmt_str = fmt_str.format(self.quest.one_name, self.quest.name)
            else:
                fmt_str = fmt_str.format(self.quest.two_name, self.quest.name)
            self.log.write('{}\n* {} *\n'.format(fmt_str, self.quest.info))
        # вывод информации о студенте в текущий момент времени
        self.log.write(str(self)+'\n')

    """
        добавить функцию внешних факторов влияющую на систему
        посредство взаимодействия с окружающими людьми/факторами/случайностями
    """

    def captainCall(self):
        mood = progress = satiety = 0
        name = 'звонок старосты '
        if self.progress <= -25:
            # bad
            info = 'вы плохо учились'
            mood = -self.inspired / 2
            progress = 5
        elif self.progress <= 50:
            # normal
            info = 'ошиблась номером'
            mood = -1
            progress = 1
        else:
            # good
            info = 'пришла стипендия'
            mood = self.inspired / 2
            progress = 5
        # пока оставляю без изменения второе событие
        return quest.Quest(name, 'Ответить на',
            {'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': 0},
            'Игнорировать',
            {'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': 0},
            self.xp, 1, info)

    def inspiredCall(self):
        jobSelect = randint(0, 4)
        mood = progress = satiety = finances = 0
        name = 'Вдохновение'
        if jobSelect == 0:
            # mood
            mood = self.inspired
            info = 'вас пропёрло на хорошое настроение'
        elif jobSelect == 1:
            # progress
            progress = self.inspired
            info = 'вас посетило вдохновение'
        elif jobSelect == 2:
            # satiety
            satiety = self.inspired
            info = 'вы очень хорошо покушали'
        else:
            # finances
            finances = self.inspired
            mood = self.inspired / 2
            info = 'вы нашли N рублей'
        # пока оставляю без изменения второе событие
        return quest.Quest(name, '',
            {'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': finances},
            '',
            {'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': finances},
            self.xp, 1, info)
