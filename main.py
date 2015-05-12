import flask
import simulator
import student

""" main simulator class """
sm = simulator.Simulator(1)
""" main student class """
st = student.Student()
""" append student to simulator """
sm.appendObject(st, 1)
""" init flask """
app = flask.Flask(__name__, static_url_path='')

class Collector:
    data = []
    def __init__(self):
        self.append()
    def append(self):
        self.data.append({
            'tick': int(sm.counter),
            'mood': int(st.mood),
            'progress': int(st.progress),
            'satiety': int(st.satiety),
            'finances': int(st.finances)
        })
        if len(self.data) >= 20:
            self.data = self.data[1:]
    def getData(self):
        return self.data

def getParamList():
    return {
        'tick': int(sm.counter),
        'mood': int(st.mood),
        'progress': int(st.progress),
        'satiety': int(st.satiety),
        'finances': int(st.finances)
    }

""" init data collector """
collect = Collector()

@app.route('/', methods=['POST'])
def cmd():
    command = flask.request.form['cmd']
    if command == 'start':
        sm.start()
        collect.append()
    elif command == 'stop':
        sm.stop()
    return flask.render_template('index.html', param=getParamList(), 
        data=flask.json.dumps(collect.getData()))

@app.route('/json')
def json_data():
    return flask.json.dumps(collect.getData())

@app.route('/')
def index():
    collect.append()
    return flask.render_template('index.html', param=getParamList(), 
        data=flask.json.dumps(collect.getData()))

if __name__ == '__main__':
    """ run flask """
    app.run(debug=True)
