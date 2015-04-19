import simulator
import student
import time

if __name__ == '__main__':
    sm = simulator.Simulator(1)
    st = student.Student()
    sm.appendObject(st, 2)
    print('Start timer!')
    sm.start()
    i = 0
    while i < 5:
        time.sleep(1)
        i += 1
    print('Stop timer!')
    sm.stop()
    time.sleep(3)
