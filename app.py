import os
import glob
import json

from flask import Flask
from flask import request, render_template, redirect, url_for


app = Flask(__name__)
boards = [os.path.basename(fn)[:-5] for fn in glob.glob('data/*.json')]


def load_json(board_name):
    with open('data/%s.json' % board_name, encoding='utf-8') as f:
        data = json.load(f)
    return data


def dump_json(board_name):
    with open('data/%s.json' % board_name, 'w', encoding='utf-8') as f:
        json.dump(datafile, f)


@app.route('/')
def home():
    return render_template('index.html', boards=boards)


@app.route('/posts/<string:board_name>')
def board(board_name):
    global datafile, current_loaded
    if current_loaded != board_name:
        datafile = load_json(board_name)
    current_loaded = board_name

    def parse_int(x):
        return int(x) if x else 0

    titles = [data['title'] for data in datafile]
    scored = [parse_int(data.get('our_score', '')) > 0 for data in datafile]
    return render_template('board.html', board_name=board_name, titles=zip(titles, scored))


@app.route('/posts/<string:board_name>/<int:data_id>')
def post(board_name, data_id):
    global datafile
    data = datafile[data_id]
    return render_template(
        'show.html', board_name=board_name, data_id=data_id, data=data)


@app.route('/evaluate/<string:board_name>/<int:data_id>', methods=['POST'])
def evaluate(board_name, data_id):
    global datafile
    real_data = datafile[data_id]
    data = request.form
    data = {k: v for k, v in request.form.items()}
    post_score = data.pop('post')

    real_data['our_score'] = post_score
    for cmt_k, cmt_v in data.items():
        cmt_id = int(cmt_k.split('_')[1])
        real_data['comments'][cmt_id]['our_score'] = cmt_v

    dump_json(board_name)
    return redirect(url_for('board', board_name=board_name) + '#post_%d' % (data_id + 1))


if __name__ == "__main__":
    global current_loaded
    current_loaded = None
    app.run()
