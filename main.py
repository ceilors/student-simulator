import simulator
import student
import time

if __name__ == '__main__':
    """ main simulator class """
    sm = simulator.Simulator(1)
    st = student.Student()
    sm.appendObject(st, 1)

    # start simulator
    sm.start()
    test = input('---- Press enter to quit! ----\n')
    sm.stop()
