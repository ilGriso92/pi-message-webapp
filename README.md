
<h1> pi-message-webapp </h1> 

<h2>Create a simple Dash web app to interact with Adafruit Nokia LCD screen through Raspberry Pi</h2>

<h3>Final result looks like:</h3> 

<div float="left">
  <img src="/img/photoexample1.jpeg" width="50%" />
  <img src="/img/screenshot1.jpeg" width="40%" /> 
</div>


<h4>Web App's Interface </h4>

<p>Link to external CSS stylesheet</p>

``` 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

```
<p>Arrange Web App layout through HTML</p>

```
app.layout = html.Div(style={'width':'70vw', 'margin':'auto'}, children=[
    html.H1("Message to Pi"),
    dcc.Input(
            id="Input",
            type="text",
            placeholder="message"
        ),
    html.Button('Send message', id='submit', n_clicks=0, style={'background-color':'red', 'color':'orange'}),
    html.Br(),
    html.Div(children=[], id='message'),
    html.Br(),
    html.Img(id='image', src= None, style={'border':'3px solid black', 'box-shadow': '2px 2px black', 'width':252}),
])
```
