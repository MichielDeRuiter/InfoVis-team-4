import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import cross_origin
from flask_socketio import SocketIO
import pandas as pd
import compare_plot
from flask import jsonify
from flask import Response

from bokeh.layouts import row, column, widgetbox
from bokeh.embed import json_item

import json

from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhlfsddkjhlsdakjhl'
socketio = SocketIO(app)

# data_title = pd.read_csv('../reddit_raw_data/reddit_title_props_seperated.csv')
# data_body = pd.read_csv('../reddit_raw_data/reddit_body_props_seperated.csv')
# data = pd.read_csv('../data/reddit_total.csv')
# data_50 = pd.read_csv('../../data/reddit_total_50.csv')
data = pd.read_csv('../data/reddit_total_400.csv')

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
    "timeseries":
        {
            "minValue": 100,
            "maxValue": 700,
            "attributeName": "Total Volume",
            "values": [
                {
                    "fromDate": 1,
                    "toDate": 10,
                    "value": 300
                },
                {
                    "fromDate": 11,
                    "toDate": 20,
                    "value": 450
                },
                {
                    "fromDate": 21,
                    "toDate": 30,
                    "value": 700
                },
                {
                    "fromDate": 31,
                    "toDate": 40,
                    "value": 550
                }
            ]
        }
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

radar_view_response = {
    "subredditName": "soccer",
    "attributes": [
        {
            "name": "Sentiment",
            "value": 0.7,
            "valueNormalized": 0.7,
            "valueMin": -1,
            "valueMax": 1
        },
        {
            "name": "Readability Score",
            "value": 12,
            "valueNormalized": 0.9,
            "valueMin": 0,
            "valueMax": 14
        },
        {
            "name": "Volume Incoming Ratio",
            "value": 0.45,
            "valueNormalized": 0.45,
            "valueMin": 0,
            "valueMax": 1
        },
        {
            "name": "Volume Outgoing Ratio",
            "value": 0.25000000001,
            "valueNormalized": 0.25000000001,  # this is on purpose to test UI rounding
            "valueMin": 0,
            "valueMax": 1
        },
        {
            "name": "Total Volume to top 50 subreddits",
            "value": 12345678,
            "valueNormalized": 0.43333333,
            "valueMin": 0,
            "valueMax": 1
        },
    ]
}

#######################
# PRODUCTION ENDPOINTS
#######################

"""
Returns a list of data for the network and bar graph visualization.

Optional arguments:
fromDate: inclusive start date for the filtering
endDate: exclusive end date for the filtering
example: http://localhost:5000/main?fromDate=20&endDate=800
"""


@app.route("/main", methods=['GET', 'POST'])
@cross_origin()
def main_screen():
    import time
    fromDate, endDate = None, None
    if 'fromDate' in request.args:
        fromDate = request.args['fromDate']
    else:
        fromDate = 0
    if 'endDate' in request.args:
        endDate = request.args['endDate']
    else:
        endDate = 1216
    if 'top' in request.args:
        top = request.args['top']
        v = data.SOURCE_SUBREDDIT.value_counts()
        treshold = v[int(top)]
        start = time.process_time()
        data2 = data[data.SOURCE_SUBREDDIT.isin(v.index[v.gt(treshold)])]
    else:
        data2 = data
    if (fromDate != None and endDate != None):
        response = data2.loc[data2['days'].between(int(fromDate), int(endDate))]
        total_value = len(response)
        uniques = response.SOURCE_SUBREDDIT.unique()
        link_pairs_temp = response.groupby(['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT']).size().reset_index()
        # link_pairs_temp.to_csv('temp.csv')
        link_pairs_temp = link_pairs_temp.loc[link_pairs_temp[0].ge(5)]
        link_pairs = link_pairs_temp.values.tolist()
        nodes = []
        links = []
        for reddit in uniques:
            nodes.append({"subredditName": reddit, "subscriberCount": randint(0, 100000)})
        for link in link_pairs:
            links.append({
                "fromSubredditName": link[0],
                "toSubredditName": link[1],
                "sentiment": 0.3,
                "volume": link[2]
            })
        main_menu_response_filtered = {"nodes": nodes, "links": links}
        return app.response_class(
            response=json.dumps(main_menu_response_filtered),
            status=200,
            mimetype="application/json"
        )


"""
Searches for a subreddit with given name (future also fulltext search on attributes and description)
Mandatory parameters:
name: name of the subreddit to search for
example: http://localhost:5000/search?name=soccer
"""


@app.route("/search", methods=['GET', 'POST'])
@cross_origin()
def main_screen_date_range():
    if 'name' in request.args:
        name = request.args['name']
        response = data.loc[data['SOURCE_SUBREDDIT'] == name]
        link_pairs = response.groupby(['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT']).size().reset_index().values.tolist()
        print(link_pairs)
        nodes = []
        links = []
        for link in link_pairs:
            nodes.append({
                "subredditName": link[1],
                "subscriberCount": randint(0, 100000)
            })
            links.append({
                "fromSubredditName": link[0],
                "toSubredditName": link[1],
                "sentiment": 0.3,
                "volume": link[2]
            })
        print(nodes)
        filtered_main_menu_response_searched = {"nodes": nodes, "links": links}
        return app.response_class(
            response=json.dumps(filtered_main_menu_response_searched),
            status=200,
            mimetype="application/json"
        )
    else:
        return app.response_class(
            response=json.dumps(filtered_main_menu_response),
            status=200,
            mimetype="application/json"
        )


def Convert(string):
    li = list(string.split(","))
    return li


"""
Returns data for the radar plot for a given 1 subreddit
Mandatory parameters:
name: exact name of the subreddit for which to retrieve statistics
example: http://localhost:5000/radar?name=soccer
"""


@app.route("/radar", methods=['GET', 'POST'])
@cross_origin()
def radar_screen():
    rader_columns = ['SOURCE_SUBREDDIT', 'LINK_SENTIMENT', 'Automated readability index']
    if 'name' in request.args:
        list = request.args['name']
        list = Convert(list)
        # name = name[0]
        # name = name.lower()
        nodes = []
        for name in list:
            name = name.lower()
            print(name)
            response1 = data.loc[data['SOURCE_SUBREDDIT'] == name][rader_columns]
            response2 = data.loc[data['TARGET_SUBREDDIT'] == name]['TARGET_SUBREDDIT']
            response1['Link_normalized'] = (response1['LINK_SENTIMENT'] - response1['LINK_SENTIMENT'].min()) / (
                    response1['LINK_SENTIMENT'].max() - response1['LINK_SENTIMENT'].min())
            response1['ARI_normalized'] = (response1['Automated readability index'] - response1['Automated readability index'].min()) / (
                    response1['Automated readability index'].max() - response1['Automated readability index'].min())
            incoming_volume = len(response2) / (len(response1) + len(response2))
            radar_view_response_searched = {
                "group": name,
                "axes": [
                    {
                        "axis": "Automated readability index",
                        "valueOLD": float(response1['Automated readability index'].mean()),
                        "value": float(response1['ARI_normalized'].mean()),
                        "valueMin": float(response1['Automated readability index'].min()),
                        "valueMax": float(response1['Automated readability index'].max()),
                        "description": 'TEST'
                    },
                    {
                        "axis": "Sentiment",
                        "value": float(response1['LINK_SENTIMENT'].mean()),
                        "valueNormalized": float(response1['Link_normalized'].mean()),
                        "valueMin": float(response1['LINK_SENTIMENT'].min()),
                        "valueMax": float(response1['LINK_SENTIMENT'].max())
                    },
                    {
                        "axis": "Volume Incoming Ratio",
                        "value": float(incoming_volume),
                        "valueNormalized": 0.45,
                        "valueMin": 0,
                        "valueMax": 1
                    },
                    {
                        "axis": "Volume Outgoing Ratio",
                        "value": float(1 - incoming_volume),
                        "valueNormalized": 0.25000000001,  # this is on purpose to test UI rounding
                        "valueMin": 0,
                        "valueMax": 1
                    }

                ]
            }
            nodes.append(radar_view_response_searched)

        return app.response_class(
            response=json.dumps(nodes),
            status=200,
            mimetype="application/json"
        )
    else:
        return app.response_class(
            response=json.dumps(radar_view_response),
            status=200,
            mimetype="application/json"
        )


@app.route("/example", methods=['GET', 'POST'])
def example():
    if 'query' in request.args:
        query = request.args['query']
        print(query)
        return jsonify(filtered_main_menu_response)
    else:
        return jsonify(main_menu_response)


###################
# TESTING ENDPOINTS
###################
@app.route('/')
def index():
    return render_template('index.html', data=data)


@app.route('/vis1')
def vis1():
    return render_template('vis1.html', dataframe=data[0:100])


@app.route('/vis2')
def vis2():
    return render_template('vis2.html', data=data)


@app.route('/vis3')
def vis3():
    return render_template('vis3.html')


@app.route('/vis4')
def vis4():
    return render_template('vis4.html', name='leagueoflegends,soccer')


# @app.route('/data_the_avengers.csv')
# def favicon():
#     return redirect(url_for('static', filename='csv/data_the_avengers.csv'))


@app.route('/plot')
def plot():
    plot1 = compare_plot.create_pie_out(data)
    plot3 = compare_plot.create_pie_in(data)
    layout = row(plot1, plot3)
    plots = json_item(layout, "myplot")
    return json.dumps(plots)


if __name__ == '__main__':
    socketio.run(app, debug=True)
