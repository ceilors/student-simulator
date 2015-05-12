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
    quest = st.quest.one_name if st.choice == 0 else st.quest.two_name
    quest += ' ' + st.quest.name
    return {
        'tick': int(sm.counter),
        'mood': int(st.mood),
        'progress': int(st.progress),
        'satiety': int(st.satiety),
        'finances': int(st.finances),
        'status': quest,
        'duration': st.quest.duration
    }

""" init data collector """
collect = Collector()

@app.route('/', methods=['POST'])
def cmd():
    command = flask.request.form['cmd']
    if command == 'start':
        sm.start()
    elif command == 'stop':
        sm.stop()
    elif command == 'reset':
        st.mood = st.progress = st.satiety = st.finances = 0
    return flask.render_template('index.html')

@app.route('/json/<param>')
def json_data(param):
    if param == 'student':
        return flask.jsonify(getParamList())
    elif param == 'graph':
        collect.append()
        return flask.json.dumps(collect.getData())

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    """ run flask """
    app.run(debug=True)
