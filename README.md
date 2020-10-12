
<h1> pi-message-webapp </h1> 

<h2>Create a simple Dash web app to interact with Adafruit Nokia LCD screen through Raspberry Pi</h2>

<h3>Final result looks like:</h3> 

<div float="left">
  <img src="/img/photoexample1.jpeg" width="50%" />
  <img src="/img/screenshot1.jpeg" width="40%" /> 
</div>

<h4>Get started </h4>

<p>Import necessary packages and dependencies</p>

``` 
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, State, Input

import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import base64
from io import BytesIO 
```

<p>Set up screen properties</p>

```
SCLK = 17
DIN = 18
DC = 27
RST = 23
CS = 22

disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
disp.begin(contrast=60)
disp.clear()
disp.display()
```

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

<h4>Add actions</h4>

<p>Display message on the Pi screen. </p>

```
@app.callback(
    Output('image', 'src'),
    [Input('Input', 'value')])
    
```

```
def print_on_screen(message):

    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)


    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
    font = ImageFont.load_default()

    row = 20

    draw.rectangle((32,2,54,16), outline=0, fill=255)
    draw.line((32,2,43,10), fill=0)
    draw.line((43,10,54,2), fill=0)


    if message is not None:

        while len(message) > 0:
            draw.text((2, row), message[0:min(13, len(message))], font=font)
            message = message[min(13, len(message)):]
            row = row + 9


        image = image.convert('1')
        disp.clear()
        disp.display()

    buffered = BytesIO()
    image.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue())
    return "data:image/png;base64,{}".format(img_str)
```    
  
    
<p>Print success message on the webapp </p>

```
@app.callback(
    Output('message', 'children'),
    [Input('submit', 'n_clicks')],
    [State('image', 'src')])
  ```
  
   ```

  def display_message(n_clicks, image):

    if image is None:
        return ['Insert a message']


    image = Image.open(BytesIO(base64.b64decode(image.split(",")[1])))

    disp.image(image)
    disp.display()

    time.sleep(5.0)
    disp.clear()
    disp.display()

    message = ['Your message was sent!']
    return message

  ```
