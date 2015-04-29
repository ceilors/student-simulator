import simulator

class Quest:
    """
        Каждое задание имеет два возможных варианта исхода,
        которые по разному изменяют параметры студента.
        Автоматически будет выбираться тот вариант,
        который "подвинет" студента ближе к критической зоне,
        т.е. минимизируется модуль разности вектора критического
        состояния и суммы векторов задания и студента.
    """
    """
        Комментарий для нас, конкретика автоматического выбора решения:
        вычитаем из векторов критических состояний вектор студента,
        берем то к.с., при котором модуль получился минимальным:
        так мы определили "направление развития" студента.
        После этого складываем вектора impact.one и impact.two с
        вектором студента и вычитаем его из вектора выбранного к.с.
        После чего берем тот вариант исхода задания, при котором
        модуль разности получается минимальным. Т.о. мы "продвигаем"
        студента по выбранному им пути.
    """
    # влияние задание на студента
    impact_one = {
        # при первом варианте выполнения задания
        'mood':     0,
        'progress': 0,
        'satiety':  0,
        'finances': 0
    }
        # при втором варианте выполнения задания
    impact_two = {
        'mood':     0,
        'progress': 0,
        'satiety':  0,
        'finances': 0
    }
    # получаемый опыт
    xp = 0
    # название задания
    name = 'demo-quest'
    # продолжительность (в шагах)
    duration = 1

    """
        назначение: инициализация класса
        входные параметры:
            one         -- словарь влияния первого варианта решения на студента
            two         -- словарь влияния второго варианта решения на студента
            xp          -- количество получаемого опыта
            name        -- название задания
            duration    -- продолжительность задания
        выходные параметры:
            None
    """
    def __init__(self, one={'mood':0,'progress':0,'satiety':0,'finances':0},
                       two={'mood':0,'progress':0,'satiety':0,'finances':0},
                       xp=0, name='demo-quest', duration=1):
        self.impact_one = one
        self.impact_two = two
        self.xp         = xp
        self.name       = name
        self.duration   = duration

    def __str__(self):
        return '[one: {}, {}, {}, {}, two: {}, {}, {}, {}]'.format(self.impact_one['mood'], self.impact_one['progress'],
            self.impact_one['satiety'], self.impact_one['finances'], self.impact_two['mood'], self.impact_two['progress'],
            self.impact_two['satiety'], self.impact_two['finances'])

"""
    Комментарий для нас, конкретика автоматического выбора решения:
    вычитаем из векторов критических состояний вектор студента,
    берем то к.с., при котором модуль получился минимальным:
    так мы определили "направление развития" студента.
    После этого складываем вектора impact.one и impact.two с
    вектором студента и вычитаем его из вектора выбранного к.с.
    После чего берем тот вариант исхода задания, при котором
    модуль разности получается минимальным. Т.о. мы "продвигаем"
    студента по выбранному им пути.
"""
def auto_choice(student, quest):
    crit_high = [100, 100, 100, 100]
    crit_low = [-100, -100, -100, -100]
    st_high = sum(list(map(lambda i, j: (i - j) ** 2, crit_high, student)))
    st_low  = sum(list(map(lambda i, j: (i - j) ** 2, crit_low,  student)))
    st_one = list(map(lambda i, j: i + j, student, quest.impact_one.values()))
    st_two = list(map(lambda i, j: i + j, student, quest.impact_two.values()))
    if st_high > st_low:
        high_one = sum(list(map(lambda i, j: (i - j) ** 2, crit_high, st_one)))
        high_two = sum(list(map(lambda i, j: (i - j) ** 2, crit_high, st_two)))
        if high_one > high_two:
            # student choses second type
            return 0
        else:
            return 1
    else:
        low_one = sum(list(map(lambda i, j: (i - j) ** 2, crit_high, st_one)))
        low_two = sum(list(map(lambda i, j: (i - j) ** 2, crit_high, st_two)))
        if low_one > low_two:
            # student choses second type
            return 0
        else:
            return 1


job_list = [
    Quest({'mood':   6, 'progress':  10, 'satiety':  0, 'finances':   0},
          {'mood':   6, 'progress':  10, 'satiety':  0, 'finances':   0}, 10, 'Пары', 3),
    Quest({'mood':  -6, 'progress':  20, 'satiety':  0, 'finances':   0},
          {'mood':  -6, 'progress':  20, 'satiety':  0, 'finances':   0}, 20, 'Курсовая', 10),
    Quest({'mood':  10, 'progress':  -5, 'satiety':  0, 'finances':   0},
          {'mood':  10, 'progress':  -5, 'satiety':  0, 'finances':   0},  5, 'Развлечение', 3),
    Quest({'mood':  10, 'progress':   0, 'satiety': 30, 'finances': -10},
          {'mood':  10, 'progress':   0, 'satiety': 30, 'finances': -10}, 10, 'Еда', 1),
    Quest({'mood': -10, 'progress':  -5, 'satiety': -5, 'finances':  20},
          {'mood': -10, 'progress':  -5, 'satiety': -5, 'finances':  20}, 20, 'Подработка', 10)
]

def generate(student):
    # учитываем simulator.counter
    from random import choice
    from copy import deepcopy
    quest = deepcopy(choice(job_list))
    print(quest)
    return quest