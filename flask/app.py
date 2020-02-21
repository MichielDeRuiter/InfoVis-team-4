import os
from flask import Flask, render_template
from flask_socketio import SocketIO
import pandas as pd
import compare_plot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhlfsddkjhlsdakjhl'
socketio = SocketIO(app)

data_title = pd.read_csv('../reddit_raw_data/reddit_title_props_seperated.csv')
data_body = pd.read_csv('../reddit_raw_data/reddit_body_props_seperated.csv')
data = pd.read_csv('../data/reddit_total.csv')
data_50 = pd.read_csv('../data/reddit_total_50.csv')
data_400 = pd.read_csv('../data/reddit_total_400.csv')


@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/vis1')
def vis1():
    return render_template('vis1.html', dataframe=data_400[0:100])	

@app.route('/vis2')
def vis2():
    return render_template('vis2.html', data=data_50)
	
@app.route('/vis3')
def vis3():
	plot = compare_plot.create_hbar()
	return render_template('vis3.html', plot=plot)


if __name__ == '__main__':
    socketio.run(app, debug=True)