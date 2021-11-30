from threading import Thread
import time

from timer import Timer


class Simulator:
    # шаг симуляции
    timerStep = 1
    # счётчик симуляционных тактов
    counter = 0
    hour = 0
    day = 1
    month = 9
    # список объектов симуляции
    objList = []
    log = None

    def __init__(self, log, step=1):
        """
        назначение: инициализации класса
        входные параметры:
            step        -- шаг
        выходные параметры:
            None
        """
        # инициализация симулятора
        self.timerStep = step
        self.timer = Timer(self.timerStep, self.step)
        self.log = log

    def start(self):
        """
        назначение: функция включения симуляции
        входные параметры:
            None
        выходные параметры:
            None
        """
        self.timer.start()

    def update(self, factor):
        """
        назнчение: функция обновления таймера симуляции
        входные параметры:
            factor        -- множитель шага таймера
        выходные параметры:
            None
        """
        self.timerStep *= factor
        self.timer.alter_timer(self.timerStep)

    def stop(self):
        """
        назначение: функция остановки симуляции
        входные параметры:
            None
        выходные параметры:
            None
        """
        self.timer.stop()

    def __del__(self):
        """
        назначение: деструктор класса
        входные параметры:
            None
        выходные параметры:
            None
        """
        self.objList.clear()

    def appendObject(self, obj, step):
        """
        назначение: функция добавления симулируемого объекта
        входные параметры:
            object       -- объект симуляции
            step         -- шаг обновления объекта
        выходные параметры:
            None
        """
        self.objList.append([obj, step])

    def step(self, signum=None, frame=None):
        """
        назначение: функция симуляции по таймеру
        входные параметры (в Unix-подобных системах):
            signum      -- номер сигнала
            frame       -- исполняемый фрейм*
        выходные параметры:
            None
        * смотри https://docs.python.org/2/reference/datamodel.html#frame-objects
        """
        for item in self.objList:
            thread = Thread(target=callThread, args=(item, self.counter))
            thread.start()
        # ожидаем выполнение последнего потока
        thread.join()
        system_time = time.strftime("%D %H:%M:%S", time.localtime())
        self.log.write(f"[info] simulation time {self.counter} [{system_time}]\n")
        self.log.flush()
        self.counter += 1
        self.hour = self.counter % 24
        if self.hour == 0:
            self.day += 1
            if self.month in [1, 3, 5, 7, 8, 10, 12]:
                if self.day > 31:
                    self.month += 1
                    self.day = 1
                    if self.month > 12:
                        self.month = 1
            elif self.month in [4, 6, 9, 11]:
                if self.day > 30:
                    self.month += 1
                    self.day = 1
            else:
                if self.day > 28:
                    self.month += 1
                    self.day = 1


def callThread(obj, counter):
    """
    функция обработки объектов симуляции в отдельных потоках
    входные параметры:
        obj         -- объект симуляции
        counter     -- счётчик симуляции
    выходные параметры:
        None
    """
    objName = obj[0]
    objCounter = obj[1]
    if counter % objCounter == 0:
        objName.step()
