import requests
from pandas import DataFrame as df
import plotly.graph_objects as go

#Le pego a la api
r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')

#Pido la columna de location
r = df(r.json()['locations'])

lon = []
lat = []

for x in r['coordinates']:
    lon.append(x['longitude'])
    lat.append(x['latitude'])

r['lat'] = df(lat)
r['lon'] = df(lon)

confirmed = []
confirmed_size = []
deaths = []
deaths_size = []
recovered =[]
recovered_size = []

for x in  r['latest']:
    confirmed.append(x['confirmed'])
    confirmed_size.append(int(x['confirmed'])/700) 
    deaths.append(x['deaths'])
    deaths_size.append(int(x['deaths'])/500)
    recovered.append(x['recovered'])
    recovered_size.append(int(x['recovered']))

r['confirmed'] = df(confirmed)
r['confirmed_size'] = df(confirmed_size)
r['deaths'] = df(deaths)
r['deaths_size'] = df(deaths_size)
r['recovered'] = df(recovered)
r['recovered_size'] =  df(recovered_size)

print(r['recovered_size'][r['recovered_size']!=0])

map_confirmados = go.Scattermapbox(
    customdata= r.loc[:,['confirmed','deaths','recovered']],
    name = 'Casos Confirmados',
    lon = r['lon'],
    lat = r['lat'],
    mode = 'markers',
    text = r['country'],
    hovertemplate= "<b>%{text}</b><br><br>"+
                    "Confirmados: %{customdata[0]}<br>"+ 
                    "<extra></extra>",

    
                    
    marker = go.scattermapbox.Marker(
        size = r['confirmed_size'],
        color = 'red',
        opacity = 0.7
    )
    
)

map_muertos = go.Scattermapbox(
    customdata= r.loc[:,['confirmed','deaths','recovered']],
    name = 'Muertes',
    lon = r['lon'],
    lat = r['lat'],
    mode = 'markers',
    text = r['country'],
    hovertemplate= "<b>%{text}</b><br><br>"+
                    "Muertos: %{customdata[1]}<br>"+ 
                    "<extra></extra>",

    
                    
    marker = go.scattermapbox.Marker(
        size = r['deaths_size'],
        color = 'black',
        opacity = 0.7
    )
)

map_recuperados = go.Scattermapbox(
    customdata= r.loc[:,['confirmed','deaths','recovered']],
    name = 'Recuperados',
    lon = r['lon'],
    lat = r['lat'],
    mode = 'markers',
    text = r['country'],
    hovertemplate= "<b>%{text}</b><br><br>"+
                    "Recuperados: %{customdata[2]}<br>"+ 
                    "<extra></extra>",

    
                    
    marker = go.scattermapbox.Marker(
        size = r['recovered_size'],
        color = 'green',
        opacity = 0.7
    )
)

layout = go.Layout(
    mapbox_style = 'white-bg',
    autosize = True,
    mapbox_layers = [
        {
            'below' : 'traces',
            'sourcetype' : 'raster',
            'source': [
                'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}'
            ]
        }
    ]
)



data = [ map_confirmados, map_muertos, map_recuperados ]
fig = go.Figure(data=data, layout = layout)

fig.show()