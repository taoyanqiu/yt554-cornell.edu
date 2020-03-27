import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_colorscales
import pandas as pd
import cufflinks as cf
import numpy as np
import re
import json
from urllib.request import urlopen
import plotly.graph_objects as go
import plotly as py

with urlopen('https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/NYS_Counties.geojson') as response:
    counties = json.load(response)

AllDate = [320, 321, 322]
df_full_data_0320 = pd.read_csv("https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/data_positive_test/data_0320_2.csv")
df_full_data_0321 = pd.read_csv("https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/data_positive_test/data_0321_2.csv")
df_full_data_0322 = pd.read_csv("https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/data_positive_test/data_0322_2.csv")
df_full_data_0320['Date'] = AllDate[0]
df_full_data_0321['Date'] = AllDate[1]
df_full_data_0322['Date'] = AllDate[2]
df_full_data_0320 = df_full_data_0320.drop(df_full_data_0320.columns[[2]], axis=1)
df_full_data_0321 = df_full_data_0321.drop(df_full_data_0321.columns[[2]], axis=1)
df_full_data_0322 = df_full_data_0322.drop(df_full_data_0322.columns[[2]], axis=1)

df_full_data = df_full_data_0320.append(df_full_data_0321)
df_full_data = df_full_data.append(df_full_data_0322)
df_full_data['infected_num'] = df_full_data['infected_num'].replace(0,np.nan)
df_full_data['infected_log'] = np.log10(df_full_data['infected_num']) + 1
df_full_data = df_full_data.fillna(0)
#df_full_data = df_full_data.append(df_full_data_0322)
print(df_full_data.head())
#print(df_full_data.shape)
#print(df_full_data.dtypes)

AllNames = ['Mar-20', 'Mar-21', 'Mar-22']

DEFAULT_OPACITY = 0.8

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''

app.layout = html.Div(children=[

	html.Div([
		html.Div([
			html.Div([
				html.H4(children='Number of COVID-19 positive cases in New York State'),
				html.P('Drag the slider to change the Date:')#,
			]),

			html.Div([
				dcc.Slider(
					id='days-slider',
					min=min(AllDate),
					max=max(AllDate),
					value=min(AllDate),
					marks={str(day): str(day) for day in AllDate}#,
				),
			], style={'width':400, 'margin':25}),

			html.Br(),

			html.P('Map transparency:',
				style={
					'display':'inline-block',
					'verticalAlign': 'top',
					'marginRight': '10px'
				}
			),

			html.Div([
				dcc.Slider(
					id='opacity-slider',
					min=0, max=1, value=DEFAULT_OPACITY, step=0.1,
					marks={tick: str(tick)[0:3] for tick in np.linspace(0,1,11)}#,
				)#,
			], style={'width':300, 'display':'inline-block', 'marginBottom':10}),

		html.P('Heatmap of COVID-19 positive cases \
			in New York State by county on {0}'.format(min(AllDate)),
			id = 'heatmap-title',
			style = {'fontWeight':600}
		),

		dcc.Graph(id = 'county-choropleth'),

		html.Div([
			html.P('†'
			)
		], style={'margin':20})

	],
	# six columns mean the width of divs
	className='six columns', style={'margin':0}),
])
])

@app.callback(
		dash.dependencies.Output('county-choropleth', 'figure'),
		[Input('days-slider', 'value'),
		Input('opacity-slider', 'value')])
def display_map(day,opacity):
	temp_zero = np.array([0])
	temp_log = np.log10(np.logspace(0,4,num=5)) + 1
	legend_vals = np.concatenate([temp_zero, temp_log])
	legend_text = np.array([0,1,10,100,'1,000','10,000'])
	#data = go.Figure()
	df = df_full_data[df_full_data.Date.eq(day)]
	trace = go.Choroplethmapbox(geojson=counties,featureidkey="properties.fips",locations=df['fips'],
                                   z=df['infected_log'],text=df['infected_num'],
                                   name=AllNames[int(day)-AllDate[0]],
                                   zmin=0,hovertext=df['name'],hoverinfo='text',
                                   hovertemplate =  '<b>%{hovertext}</b>'+\
                                                    '<br>Confirmed cases: <b>%{text}</b><br>',
                                   colorscale='Blues',marker_line_width=0.5,marker_line_color='rgb(169,164,159)',
                                   colorbar={'tickmode':'array',
                                             'tickvals':legend_vals,
                                             'ticktext':legend_text
                                             },
																	 marker = dict(opacity = opacity)
                                   #visible=False  #for the slider function
                                  )
	return {"data": [trace],"layout": dict(mapbox = dict(style = "carto-positron",center = {"lat": 43, "lon": -75.5},zoom = 5),
	                                       title={'text':'Confirmed cases of coronavirus disease (COVID-19) in New York State','xref':'paper','x':0.5},margin={"r":10,"t":50,"l":40,"b":10})
 }

@app.callback(
	Output('heatmap-title', 'children'),
	[Input('days-slider','value')]
	)
def update_map_title(day):
	return 'COVID-19 positive case \
				in New York State on {0}'.format(day)

#export FLASK_APP=yourapp
if __name__ == '__main__':
  #app.run_server(debug=True)
  #app.run('localhost', 5000)
  #export FLASK_ENV=development
  #flask run
  app.run_server(debug=True, use_reloader=False)