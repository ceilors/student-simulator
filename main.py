from flask import Flask, render_template
import simulator
import student

""" main simulator class """
sm = simulator.Simulator(1)
""" main student class """
st = student.Student()
""" append student to simulator """
sm.appendObject(st, 1)
""" init flask """
app = Flask(__name__)

def getParamList():
    return {
        'mood': int(st.mood),
        'progress': int(st.progress),
        'satiety': int(st.satiety),
        'finances': int(st.finances)
    }

@app.route('/cmd/<command>')
def cmd(command):
    if command == 'start':
        sm.start()
    elif command == 'stop':
        sm.stop()
    return render_template('index.html', param=getParamList())

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', param=getParamList())

if __name__ == '__main__':
    """ run flask """
    app.run(debug=True)
