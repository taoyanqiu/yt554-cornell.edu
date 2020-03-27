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