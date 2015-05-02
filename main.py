import simulator
import student

if __name__ == '__main__':
    """ main simulator class """
    sm = simulator.Simulator(1)
    """ main student class """
    st = student.Student()
    """ append student to simulator """
    sm.appendObject(st, 1)

    """ start simulator """
    sm.start()
    test = input('---- Press enter to quit! ----\n')
    """ stop simulator """
    sm.stop()
