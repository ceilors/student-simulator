from random import randint, random
from math import atan, pi
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
    duration = 0
    # константы
    xp = 50
    inspired = 20
    slowness = 3
    
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

    """
        назначение: изменение параметров студента
        входные параметры:
            vector      -- словарь изменений параметров
        выходные параметры:
            None
    """
    def change(self, vector):
        for i in vector:
            if i == 'mood':
                self.mood += vector[i]
                if self.mood > 100:
                    self.mood = 100
                elif self.mood < -100:
                    self.mood = -100
            elif i == 'progress':
                self.progress += vector[i]
                if self.progress > 100:
                    self.progress = 100
                elif self.progress < -100:
                    self.progress = -100
            elif i == 'satiety':
                self.satiety += vector[i]
                if self.satiety > 100:
                    self.satiety = 100
                elif self.satiety < -100:
                    self.satiety = -100
            else:
                self.finances += vector[i]
                if self.finances > 100:
                    self.finances = 100
                elif self.finances < -100:
                    self.finances = -100

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
        
        # с вероятностью 25% студенту станет скучнее
        if randint(0, 3) == 1:
            self.mood -= 1
        elif not randint(0, 2):
            # если не стало, то с вероятностью 33% ему станет веселее
            self.mood += 1
        # с вероятностью 33% студенту станет голоднее
        if randint(0, 2) == 1:
            self.satiety -= 1
        # продолжение квеста или же выбор нового
        self.duration += 1
        if self.quest.duration < self.duration:
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
            elif chance <= 0.1 * atan(-self.progress / 25) / pi + 0.05:
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
            self.duration = 0
            self.quest.duration *= self.slowness
        # вывод информации о студенте в текущий момент времени
        self.log.write(str(self)+'\n')

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
            {'mood':  mood, 'progress':  progress, 'satiety': 0, 'finances': 0},
            'Игнорировать',
            {'mood': -mood, 'progress': -progress, 'satiety': 0, 'finances': 0},
            self.xp, 1, info)

    def inspiredCall(self):
        jobSelect = randint(0, 4)
        mood = progress = satiety = finances = 0
        name = ''
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
        return quest.Quest(name, 'Вдохновение',
            {'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': finances},
            '',
            {'mood': mood, 'progress': progress, 'satiety': satiety, 'finances': finances},
            self.xp, 1 / self.slowness, info)
