from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import row, column, widgetbox
from bokeh.models import HoverTool, Slider, CustomJS, LabelSet, ColumnDataSource
from bokeh.embed import json_item, components
from bokeh.transform import cumsum
from bokeh.palettes import Category20c

import pandas as pd

from math import pi


def create_pie_out(data):
	reddit1 = data.loc[(data['SOURCE_SUBREDDIT'] == 'dogecoin') & (data['days'].between(0, 800))]
	reddit2 = data.loc[(data['SOURCE_SUBREDDIT'] == 'leagueoflegends') & (data['days'].between(0, 800))]
	
	x = {
		'dogecoin': len(reddit1),
		'leagueoflegends': len(reddit2)
	}
	pie_data = pd.Series(x).reset_index(name='value').rename(columns={'index':'reddit'})
	pie_data['angle'] = pie_data['value']/pie_data['value'].sum() * 2*pi
	if len(x) > 2:
		pie_data['color'] = Category20c[len(x)]
	else: pie_data['color'] = ['#3182bd', '#6baed6']
	plot = figure(plot_height=350, title="Outgoing links", toolbar_location=None, tools="hover", tooltips="@reddit: @value", x_range=(-0.5, 1.0))
	
	plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='reddit', source=pie_data)
	

	plot.axis.axis_label=None
	plot.axis.visible=False
	plot.grid.grid_line_color = None
	return plot
	
def create_pie_in(data):
	reddit1 = data.loc[(data['TARGET_SUBREDDIT'] == 'dogecoin') & (data['days'].between(0, 800))]
	reddit2 = data.loc[(data['TARGET_SUBREDDIT'] == 'leagueoflegends') & (data['days'].between(0, 800))]
	
	x = {
		'dogecoin': len(reddit1),
		'leagueoflegends': len(reddit2)
	}
	pie_data = pd.Series(x).reset_index(name='value').rename(columns={'index':'reddit'})
	pie_data['angle'] = pie_data['value']/pie_data['value'].sum() * 2*pi
	if len(x) > 2:
		pie_data['color'] = Category20c[len(x)]
	else: pie_data['color'] = ['#3182bd', '#6baed6']
	plot = figure(plot_height=350, title="Incoming links", toolbar_location=None, tools="hover", tooltips="@reddit: @value", x_range=(-0.5, 1.0))
	
	plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='reddit', source=pie_data)
	

	plot.axis.axis_label=None
	plot.axis.visible=False
	plot.grid.grid_line_color = None
	return plot