import pygal
from pygal.style import DarkStyle


histo_config = pygal.Config()
histo_config.show_minor_x_labels = False
histo_config.truncate_label=20
histo_config.y_title='Share Price ($)'
histo_config.style = DarkStyle


def render_graph_histo(x_val, y_val, rng, stock_name):
	try:
		graph = pygal.Line(histo_config, show_legend=False)

		if rng == '1d':
			graph.title = '{} Share Price over the last day'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		elif rng == '5d':
			graph.title = '{} Share Price over last 5 Days'.format(stock_name)
			N = 1
			S = 0

		elif rng == '1m':
			graph.title = '{} Share Price over last Month'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		elif rng == '3m':
			graph.title = '{} Share Price over last 3 Months'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		elif rng == '6m':
			graph.title = '{} Share Price over last 6 Months'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		elif rng == '1y':
			graph.title = '{} Share Price over last year'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		elif rng == '5y':
			graph.title = '{} Share Price over last 5 years'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		elif rng == 'max':
			graph.title = '{} Max Share Price'.format(stock_name)
			N = round(len(x_val)/6)
			S = N

		graph.x_labels = x_val
		graph.x_labels_major = x_val[S::N]
		graph.add('Share Price', y_val)


		graph_data = graph.render_data_uri()

		return graph_data

	except Exception:
		return("static/graph_error.png")


def render_graph_comp(graph_data1, graph_data2, graph_data3, name1, name2, name3, rng):
	try:
		graph = pygal.Line(histo_config)

		if rng == '1d':
			graph.title = 'Comparison over the last day'
			N = round(len(graph_data1[0])/6)
			S = N

		elif rng == '5d':
			graph.title = 'Comparison over last 5 Days'
			N = 1
			S = 0

		elif rng == '1m':
			graph.title = 'Comparison over last Month'
			N = round(len(graph_data1[0])/6)
			S = N

		elif rng == '3m':
			graph.title = 'Comparison over last 3 Months'
			N = round(len(graph_data1[0])/6)
			S = N

		elif rng == '6m':
			graph.title = 'Comparison over last 6 Months'
			N = round(len(graph_data1[0])/6)
			S = N

		elif rng == '1y':
			graph.title = 'Comparison over last year'
			N = round(len(graph_data1[0])/6)
			S = N

		elif rng == '5y':
			graph.title = 'Comparison over last 5 years'
			N = round(len(graph_data1[0])/6)
			S = N

		elif rng == 'max':
			graph.title = 'Comparison Price'
			N = round(len(graph_data1[0])/6)
			S = N

		graph.x_labels = graph_data1[0]
		graph.x_labels_major = graph_data1[0][S::N]

		graph.add(name1, graph_data1[1])
		graph.add(name2, graph_data2[1])

		if name3:
			graph.add(name3, graph_data3[1])

		graph_data = graph.render_data_uri()

		return graph_data

	except Exception:
		return("static/graph_error.png")
