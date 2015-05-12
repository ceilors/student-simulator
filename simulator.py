from threading import Thread
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
    log = None

    """
        назначение: инициализации класса
        входные параметры:
            step        -- шаг
        выходные параметры:
            None
    """
    def __init__(self, log, step=1):
        # инициализация симулятора
        self.timerStep = step
        self.log = log
        signal.signal(signal.SIGALRM, self.step)

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
        назначение: функция добавления симулируемого объекта
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
            thread = Thread(target=callThread, args=(item, self.counter))
            thread.start()
        # ожидаем выполнение последнего потока
        thread.join()
        system_time = time.strftime('%D %H:%M:%S', time.localtime())
        self.log.write('[info] simulation time {} [{}]\n'.format(self.counter, system_time))
        self.log.flush()
        self.counter += 1

"""
    функция обработки объектов симуляции в отдельных потоках
    входные параметры:
        obj         -- объект симуляции
        counter     -- счётчик симуляции
    выходные параметры:
        None
"""
def callThread(obj, counter):
    objName = obj[0]
    objCounter = obj[1]
    if counter % objCounter == 0:
        objName.step()
