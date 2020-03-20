from bokeh.layouts import row, column, widgetbox
from bokeh.embed import json_item

from flask import Flask, jsonify, render_template, request, Response
from flask_cors import cross_origin
from flask_socketio import SocketIO

from random import randint

import json
import os
import pandas as pd
import random
import time

# App config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhlfsddkjhlsdakjhl'
socketio = SocketIO(app)

pd.options.mode.chained_assignment = None  # default='warn'

# Load in the data and do some pre-processing

data = pd.read_csv('../data/reddit_total_400.csv')
data['LINK_SENTIMENT'][data['LINK_SENTIMENT'] < -0] = 0
data_days = data.groupby('days').size().to_frame()
print('Dataset Loaded')

with open('../data/sentiment_pairs.json', 'r') as file:
    sen_pairs = json.load(file)
	
try:
	dict_amount_df = pd.read_csv('../data/dict_amount.csv', index_col=0)
	print('Amounts loaded')
except FileNotFoundError:
	print('File not found, creating amounts CSV') 
	with open('../data/dict_amount.json', 'r') as file:
		dict_amount = json.load(file)
	dict_amount_df = pd.DataFrame(dict_amount)
	dict_amount_df.to_csv('../data/dict_amount.csv')
	print('Amounts loaded and file saved')


try:
	dict_sentiment_df = pd.read_csv('../data/dict_sentiment.csv', index_col=0)
	print('Sentiment loaded')
except FileNotFoundError:
	print('File not found, creating Sentiment CSV') 
	with open('../data/dict_sentiment.json', 'r') as file:
		dict_sentiment = json.load(file)
	dict_sentiment_df = pd.DataFrame(dict_sentiment)
	dict_sentiment_df.to_csv('../data/dict_sentiment.csv')
	print('Sentiment loaded and file saved')

# Structure of the default response
main_menu_response = {
    "nodes": [
        {
            "subredditName": "soccer",
            "subscriberCount": 600
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
top: return only the top given number of subreddits
example: http://localhost:5000/main?fromDate=20&endDate=800, http://localhost:5000/main?fromDate=20&endDate=800&top=50
"""
@app.route("/main", methods=['GET', 'POST'])
@cross_origin()
def main_screen():
	# set the default parameters if not given
	if 'fromDate' in request.args:
		fromDate = int(request.args['fromDate'])
	else:
		fromDate = 0
	if 'endDate' in request.args:
		endDate = int(request.args['endDate'])
	else:
		endDate = 1217
	if 'top' in request.args:
		top = request.args['top']
		v = data.SOURCE_SUBREDDIT.value_counts()
		treshold = v[int(top)]
		start = time.process_time()
		data2 = data[data.SOURCE_SUBREDDIT.isin(v.index[v.gt(treshold)])]
	else:
		data2 = data
	# Code for every day with a pre-processed dataset
	if (fromDate == 0 and endDate == 1217):
		response = data2.loc[data2['days'].between(fromDate, endDate)]
		uniques = response.SOURCE_SUBREDDIT.unique()
		link_pairs_temp = response.groupby(['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT']).size().reset_index()
		link_pairs_temp = link_pairs_temp.loc[link_pairs_temp[0].ge(5)]
		link_pairs = link_pairs_temp.values.tolist()
		nodes = [{"subredditName":reddit, "subscriberCount":randint(0,100000)} for reddit in uniques]
		links = [{	"fromSubredditName": link[0],
					"toSubredditName": link[1],
					"sentiment": sen_pairs.get(link[0]+link[1], 0.5),
					"volume": link[2]} 
				for link in link_pairs]
		main_menu_response_filtered = {"nodes":nodes,"links":links}
		return app.response_class(
			response=json.dumps(main_menu_response_filtered),
			status=200,
			mimetype="application/json"
		)
	# Code for given a time range
	else:
		response = data2.loc[data2['days'].between(fromDate, endDate)]
		sent_dt = dict_sentiment_df.iloc[:, fromDate:endDate].sum(axis=1)
		amount_dt = dict_amount_df.iloc[:, fromDate:endDate].sum(axis=1)
		uniques = response.SOURCE_SUBREDDIT.unique()
		link_pairs_temp = response.groupby(['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT']).size().reset_index()
		link_pairs_temp = link_pairs_temp.loc[link_pairs_temp[0].ge(5)]
		link_pairs = link_pairs_temp.values.tolist()
		nodes = [{"subredditName":reddit, "subscriberCount":randint(0,100000)} for reddit in uniques]
		links = [{	"fromSubredditName": link[0],
					"toSubredditName": link[1],
					"sentiment": sent_dt.get(link[0]+link[1])/amount_dt.get(link[0]+link[1]),
					"volume": link[2]} 
				for link in link_pairs]
		main_menu_response_filtered = {"nodes":nodes,"links":links}
		return app.response_class(
			response=json.dumps(main_menu_response_filtered),
			status=200,
			mimetype="application/json"
		)

"""
Returns a list of data for volume per day.

Optional arguments:
fromDate: inclusive start date for the filtering
endDate: exclusive end date for the filtering
example: http://localhost:5000/maintotal?fromDate=20&endDate=800
"""
@app.route("/maintotal", methods=['GET', 'POST'])
@cross_origin()
def main_screen_total():
	if 'fromDate' in request.args:
		fromDate = int(request.args['fromDate'])
	else:
		fromDate = 0
	if 'endDate' in request.args:
		endDate = int(request.args['endDate'])
	else:
		endDate = 1217
	if (fromDate != None and endDate != None):
		response = data_days[fromDate:endDate]
		main_menu_response_filtered = response.to_dict()[0]
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
	else:
		name = 'soccer'
	response = data.query('SOURCE_SUBREDDIT == @name')
	link_pairs = response.groupby(['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT']).size().reset_index().values.tolist()
	nodes = []
	links = []
	for link in link_pairs:
		nodes.append({
			"subredditName": link[1],
			"subscriberCount":randint(0,100000)
		})
		sent = response.query('SOURCE_SUBREDDIT == @link[0] and TARGET_SUBREDDIT == @link[1]')['LINK_SENTIMENT']
		links.append({
			"fromSubredditName": link[0],
			"toSubredditName": link[1],
			"sentiment": sent.sum()/len(sent),
			"volume": link[2]
		})
	filtered_main_menu_response_searched = {"nodes":nodes,"links":links}
	return app.response_class(
		response=json.dumps(filtered_main_menu_response_searched),
		status=200,
		mimetype="application/json"
	)

# Function to convert the GET string to a list
def Convert(string): 
    li = list(string.split(",")) 
    return li 
"""
Returns data for the radar plot for a given 1 or multiple subreddits splitted by a comma
Mandatory parameters:
name(s): exact name of the subreddit for which to retrieve statistics
example: http://localhost:5000/radar?name=soccer,2007scape,politics
"""
@app.route("/radar", methods=['GET', 'POST'])
@cross_origin()
def radar_screen():
	rader_columns=['SOURCE_SUBREDDIT', 'LINK_SENTIMENT', 'Automated readability index']
	if 'name' in request.args:
		list = request.args['name']
	else:
		list = 'soccer'
	list = Convert(list)
	nodes = []
	for name in list:
		name = name.lower()
		response1 = data.loc[data['SOURCE_SUBREDDIT'] == name][rader_columns]
		response2 = data.loc[data['TARGET_SUBREDDIT'] == name]['TARGET_SUBREDDIT']
		response1['ARI_normalized']=(response1['Automated readability index']-response1['Automated readability index'].min())/(response1['Automated readability index'].max()-response1['Automated readability index'].min())
		incoming_volume = len(response2)/(len(response1)+len(response2))
		radar_view_response_searched = {
			"group": name,
			"axes": [
				{
					"axis": "Automated readability index",
					"value": float(response1['ARI_normalized'].mean()),
					"valueMin": float(response1['Automated readability index'].min()),
					"valueMax": float(response1['Automated readability index'].max()),
					"description": 'Automated readability index' 
				},
				{
					"axis": "Sentiment",
					"value": response1['LINK_SENTIMENT'].sum()/len(response1['LINK_SENTIMENT']),
					"valueMin": 0,
					"valueMax": 1,
					"description": 'Sentiment of given subreddit' 
				},
				{
					"axis": "Volume Incoming Ratio",
					"value": float(incoming_volume),
					"valueMin": 0,
					"valueMax": 1,
					"description": 'Incoming value compared to outgoing volume' 
				},
				{
					"axis": "Volume Outgoing Ratio",
					"value": float(1-incoming_volume),
					"valueMin": 0,
					"valueMax": 1,
					"description": 'Outgoing value compared to incoming volume' 
				},
				{
					"axis": "Average awards",
					"value": round(random.uniform(0,0.1), 5),
					"valueMin": 0,
					"valueMax": 0.1,
					"description": 'Average awards per link' 
				}
			]
		}
		nodes.append(radar_view_response_searched)
	
	return app.response_class(
		response=json.dumps(nodes),
		status=200,
		mimetype="application/json"
	)

	
###################
# TESTING ENDPOINTS
###################
@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/vis4')
def vis4():
    return render_template('vis4.html', name='leagueoflegends,soccer')

if __name__ == '__main__':
	socketio.run(app, debug=False)