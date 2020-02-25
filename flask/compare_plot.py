from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import row, column, widgetbox
from bokeh.models import HoverTool, Slider, CustomJS
from bokeh.embed import json_item, components
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
import pandas as pd

def create_hbar(data):
	plot = figure(plot_height=300)

	x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	y = [2**v for v in x]

	plot.line(x, y, line_width=4)

	#script, div = components(plot)
	
	return plot
	
def create_hbar2(data):
	plot = figure(plot_height=300)

	x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	y = [2**v for v in x]

	plot.line(x, y, line_width=4)

	#script, div = components(plot)
	
	return plot