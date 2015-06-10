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
            'tick': sm.counter,
            'mood': round(st.mood),
            'progress': round(st.progress),
            'satiety': round(st.satiety),
            'finances': round(st.finances)
        })
        if len(self.data) > 20:
            self.data = self.data[1:]
    def getData(self):
        return self.data

def getParamList():
    quest = st.quest.one_name if st.choice else st.quest.two_name
    another = st.quest.two_name if st.choice else st.quest.one_name
    quest += ' ' + st.quest.name
    another += ' ' + st.quest.name
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    msg = '{:02}/{:02} {}'.format(sm.day, sm.month, quest)
    return {
        'msg': msg,
        'hour': int(sm.hour),
        'day': int(sm.day),
        'month': months[int(sm.month) - 1],
        'mood': round(st.mood),
        'progress': round(st.progress),
        'satiety': round(st.satiety),
        'finances': round(st.finances),
        'status': quest,
        'duration': st.quest.duration,
        'completed': st.duration,
        'another': another,
        'speed': sm.timerStep
    }

""" init data collector """
collect = Collector()

@app.route('/send', methods=['POST'])
def send():
    json = flask.request.get_json()
    if json['another']:
        st.choice = 1 if st.choice == 0 else 0
    elif json['start']:
        collect.redraw = True
        sm.start()
    elif json['pause']:
        collect.redraw = False
        sm.stop()
    elif json['reset']:
        st.mood = st.progress = st.satiety = st.finances = 0
    elif json['stop']:
        collect.redraw = False
        st.mood = st.progress = st.satiety = st.finances = sm.counter = 0
        collect.data = []
        sm.stop()
    elif json['fast']:
        sm.update(0.5)
    elif json['normal']:
        sm.update(1 / sm.timerStep)
    elif json['slow']:
        sm.update(2.0)
    # for normal work
    return 'Ok'

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
