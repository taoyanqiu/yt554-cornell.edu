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

