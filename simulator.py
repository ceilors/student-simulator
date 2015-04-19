import signal
import time
import os

class Simulator:
    # шаг симуляции
    timerStep = 1
    # счётчик симуляционных тактов
    counter = 0
    # список объектов симуляции
    objList = []

    """
        назначение: инициализации класса
        входные параметры:
            step        -- шаг
        выходные параметры:
            None
    """
    def __init__(self, step=1):
        # инициализация симулятора
        self.timerStep = step
        signal.signal(signal.SIGALRM, self.step)
        signal.setitimer(signal.ITIMER_REAL, step, step)

    """
        назнчение: функция включения симуляции
        входные параметры:
            None
        выходные параметры:
            None
    """
    def start(self):
        signal.setitimer(signal.ITIMER_REAL, self.timerStep, self.timerStep)

    """
        назнчение: функция остановки симуляции
        входные параметры:
            None
        выходные параметры:
            None
    """
    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0)

    """
        назначение: деструктор класса
        входные параметры:
            None
        выходные параметры:
            None
    """
    def __del__(self):
        self.objList.clear()

    """
        назначение: функция добавление симулируемого объекта 
        входные параметры:
            object       -- объект симуляции
            step         -- шаг обновления объекта
        выходные параметры:
            None
    """
    def appendObject(self, obj, step):
        self.objList.append([obj, step])

    """
        назначение: функция симуляции по таймеру
        входные параметры:
            signum      -- номер сигнала
            frame       -- исполняемый фрейм*
        выходные параметры:
            None
        * смотри https://docs.python.org/2/reference/datamodel.html#frame-objects
    """  
    def step(self, signum, frame):
        for item in self.objList:
            objName = item[0]
            objCounter = item[1]
            if self.counter % objCounter == 0:
                objName.step()
        print('signal {}'.format(time.ctime()))
        self.counter += 1
