import os
from flask import Flask, render_template
from flask_socketio import SocketIO
import pandas as pd
import compare_plot
from flask import jsonify

from bokeh.layouts import row, column, widgetbox
from bokeh.embed import json_item

import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhlfsddkjhlsdakjhl'
socketio = SocketIO(app)

#data_title = pd.read_csv('../reddit_raw_data/reddit_title_props_seperated.csv')
#data_body = pd.read_csv('../reddit_raw_data/reddit_body_props_seperated.csv')
data = pd.read_csv('../../data/reddit_total.csv')
data_50 = pd.read_csv('../../data/reddit_total_50.csv')
#data_400 = pd.read_csv('../../data/reddit_total_400.csv')


main_menu_response = {
    "nodes": [
        {
            "subredditName": "soccer",
            "subscriberCount": 500
        },
        {
            "subredditName": "barcelona",
            "subscriberCount": 125
        },
        {
            "subredditName": "chelsea",
            "subscriberCount": 450
        }
    ],
    "links": [
        {
            "fromSubredditName": "soccer",
            "toSubredditName": "barcelona",
            "overallSentiment": 0.3,
            "incomingSentiment": -0.5,
            "outgoingSentiment": 0.8,
            "totalVolume": 400,
            "incomingVolume": 300,
            "outgoingVolume": 100
        },
        {
            "fromSubredditName": "soccer",
            "toSubredditName": "chelsea",
            "overallSentiment": 0.4,
            "incomingSentiment": 0.5,
            "outgoingSentiment": -0.1,
            "totalVolume": 750,
            "incomingVolume": 300,
            "outgoingVolume": 450
        }
    ],
    "timeseries": [
        {
            "fromDate": 1,
            "toDate": 10,
            "totalVolume": 300
        },
        {
            "fromDate": 11,
            "toDate": 20,
            "totalVolume": 450
        },
        {
            "fromDate": 21,
            "toDate": 30,
            "totalVolume": 700
        },
        {
            "fromDate": 31,
            "toDate": 40,
            "totalVolume": 550
        }
    ]
}


filtered_main_menu_response = {
    "centeredSubredditName": "soccer",
    "nodes": [
        {
            "subredditName": "soccer",
            "subscriberCount": 500
        },
        {
            "subredditName": "barcelona",
            "subscriberCount": 125
        },
        {
            "subredditName": "chelsea",
            "subscriberCount": 450
        }
    ],
    "links": [
        {
            "fromSubredditName": "soccer",
            "toSubredditName": "barcelona",
            "overallSentiment": 0.3,
            "incomingSentiment": -0.5,
            "outgoingSentiment": 0.8,
            "totalVolume": 400,
            "incomingVolume": 300,
            "outgoingVolume": 100
        },
        {
            "fromSubredditName": "soccer",
            "toSubredditName": "chelsea",
            "overallSentiment": 0.4,
            "incomingSentiment": 0.5,
            "outgoingSentiment": -0.1,
            "totalVolume": 750,
            "incomingVolume": 300,
            "outgoingVolume": 450
        }
    ]
}




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
    return render_template('vis3.html')

@app.route('/plot')
def plot():
    plot1 = compare_plot.create_pie_out(data_400)
    plot3 = compare_plot.create_pie_in(data_400)
    layout = row(plot1, plot3)
    plots = json_item(layout, "myplot")
    return json.dumps(plots)


@app.route("/main")
def main_screen():
    return jsonify(main_menu_response)


@app.route("/search")
def main_screen_date_range():
    return Flask.make_response(jsonify(filtered_main_menu_response), 200)



if __name__ == '__main__':
    socketio.run(app, debug=True)