import simulator

class Quest:
    """
        Каждое задание имеет два возможных варианта исхода,
        которые по разному изменяют параметры студента.
        Автоматически будет выбираться тот вариант,
        который "подвинет" студента ближе к нормальному состоянию,
        т.е. минимизируется модуль суммы векторов задания и студента.
    """
    # название задания
    name = 'demo-quest'
    # первый вариант выполнения задания
    #   влияние задания на студента
    impact_one = {
        'mood':     0,
        'progress': 0,
        'satiety':  0,
        'finances': 0
    }
    #   название решения
    one_name = 'first'
    # первый вариант выполнения задания
    #   влияние задания на студента
    impact_two = {
        'mood':     0,
        'progress': 0,
        'satiety':  0,
        'finances': 0
    }
    #   название решения
    two_name = 'second'
    # получаемый опыт
    xp = 0
    # продолжительность (в шагах)
    duration = 1
    # текст выводимый при получении задания
    info = ''

    """
        назначение: инициализация класса
        входные параметры:
            name        -- название задания
            one         -- словарь влияния первого варианта решения на студента
            one_name    -- название первого варианта решения
            two         -- словарь влияния второго варианта решения на студента
            two_name    -- название второго варианта решения
            xp          -- количество получаемого опыта
            name        -- название задания
            duration    -- продолжительность задания
            info        -- текст выводимый при получении задания
        выходные параметры:
            None
    """
    def __init__(self, name='кнопку "Старт" для начала симуляции',
                       one_name='Нажмите',
                       one={'mood':0,'progress':0,'satiety':0,'finances':0},
                       two_name='Жмякни',
                       two={'mood':0,'progress':0,'satiety':0,'finances':0},
                       xp=0, duration=1, info=''):
        self.name       = name
        self.one_name   = one_name
        self.one_impact = one
        self.two_name   = two_name
        self.two_impact = two
        self.xp         = xp
        self.duration   = duration
        self.info       = info

    def __str__(self):
        return '{}, {}, {}; {}: {}, {}: {}'.format(self.name, self.xp, self.duration,
            self.one_name, self.one_impact, self.two_name, self.two_impact)

def auto_choice(student, quest):
    one = [
        quest.one_impact['mood'],
        quest.one_impact['progress'],
        quest.one_impact['satiety'],
        quest.one_impact['finances']
    ]
    two = [
        quest.two_impact['mood'],
        quest.two_impact['progress'],
        quest.two_impact['satiety'],
        quest.two_impact['finances']
    ]
    st_one = abs(sum(list(map(lambda i, j: (i + j) ** 2, student, one))))
    st_two = abs(sum(list(map(lambda i, j: (i + j) ** 2, student, two))))
    if st_one > st_two:
        # student choses second type
        return 0
    else:
        # student choses first type
        return 1


job_list = [
    # шаблон задания:
    # Quest(name,
    #       one_name, {'mood': mood1, 'progress': progress1, 'satiety': satiety1, 'finances': finances1},
    #       two_name, {'mood': mood2, 'progress': progress2, 'satiety': satiety2, 'finances': finances2},
    #       xp, duration)
    # Значения mood1,2, progress1,2 и др. являются коэффициентами (!),
    # реальное значение изменений зависит от текущего состояния студента
    Quest('пары',
          'Посетить',      {'mood':  0, 'progress':  1, 'satiety':  0, 'finances':  0},
          'Пропустить',    {'mood':  1, 'progress': -1, 'satiety':  0, 'finances':  0},
           30, 3, 'Пора и поучиться'),
    Quest('курсовую',
          'Сделать',       {'mood': -1, 'progress':  3, 'satiety': -1, 'finances':  0},
          'Купить',        {'mood':  1, 'progress':  3, 'satiety':  0, 'finances': -2},
           50, 5, 'Hate this'),
    Quest('',
          'Играться',      {'mood':  2, 'progress':  0, 'satiety': -1, 'finances':  0},
          'Прогуляться',   {'mood':  3, 'progress':  0, 'satiety': -1, 'finances': -1},
           30, 3, 'I love it!'),
    Quest('еду',
          'Приготовить',   {'mood':  1, 'progress':  0, 'satiety':  2, 'finances':  0},
          'Заказать',      {'mood':  3, 'progress':  0, 'satiety':  2, 'finances': -1},
           10, 1, 'omnomnom'),
    Quest('денег',
          'Работать ради', {'mood':  1, 'progress': -1, 'satiety': -1, 'finances':  3},
          'Одолжить',      {'mood': -1, 'progress':  0, 'satiety':  0, 'finances':  3},
           50, 5, 'no money - no honey')
]

def generate(student):
    from random import choice
    from copy import deepcopy
    mood, progress, satiety, finances = student
    # учитываем состояние студента,
    # учитываем simulator.counter
    quest = deepcopy(choice(job_list))
    return quest