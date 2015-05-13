import flask
import simulator
import student

log = open('output.log', 'w')
""" main simulator class """
sm = simulator.Simulator(log, 1)
""" main student class """
st = student.Student(log)
""" append student to simulator """
sm.appendObject(st, 1)
""" init flask """
app = flask.Flask(__name__, static_url_path='')

class Collector:
    data = []
    redraw = False
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
        if len(self.data) > 20:
            self.data = self.data[1:]
    def getData(self):
        return self.data

def getParamList():
    quest = st.quest.one_name if st.choice else st.quest.two_name
    quest += ' ' + st.quest.name
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return {
        'hour': int(sm.hour),
        'day': int(sm.day),
        'month': months[int(sm.month) - 1],
        'mood': int(st.mood),
        'progress': int(st.progress),
        'satiety': int(st.satiety),
        'finances': int(st.finances),
        'status': quest,
        'duration': st.quest.duration,
        'completed': st.duration
    }

""" init data collector """
collect = Collector()

@app.route('/', methods=['POST'])
def cmd():
    command = flask.request.form['cmd']
    if command == 'Старт':
        collect.redraw = True
        sm.start()
    elif command == 'Пауза':
        collect.redraw = False
        sm.stop()
    elif command == 'Сброс':
        st.mood = st.progress = st.satiety = st.finances = 0
    elif command == 'Стоп':
        collect.redraw = False
        st.mood = st.progress = st.satiety = st.finances = sm.counter = 0
        collect.data = []
        sm.stop()
    elif command == '>>':
        sm.update(0.5)
    elif command == '<<':
        sm.update(2.0)
    return flask.render_template('index.html')

@app.route('/json/<param>')
def json_data(param):
    if param == 'student':
        return flask.jsonify(getParamList())
    elif param == 'graph':
        if collect.redraw:
            collect.append()
        return flask.json.dumps(collect.getData())

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    """ run flask """
    app.run(debug=True)
    log.close()
