import dash
import dash_html_components as html
import dash_core_components as dcc
import subprocess
from dash.dependencies import Output, State, Input

import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI


# IMAGE RELATED STUFF
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import base64
from io import BytesIO


SCLK = 17
DIN = 18
DC = 27
RST = 23
CS = 22

disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
disp.begin(contrast=60)
disp.clear()
disp.display()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(style={'width':'70vw', 'margin':'auto'}, children=[
    html.H1("Message to Marco"),
    dcc.Input(
            id="Input",
            type="text",
            placeholder="message"
        ),
    html.Button('Send message', id='submit', n_clicks=0, style={'background-color':'red', 'color':'orange'}),
    html.Div(children=[], id='message'),
    html.Img(id='image', src= None, style={'border':'3px solid black', 'box-shadow': '2px 2px black', 'width':252}),
    #'border':'1px solid black', 'box-shadow': '2px 2px black'
])


@app.callback(
    Output('image', 'src'),
    [Input('Input', 'value')])
def print_on_screen(message):

    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)


    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
    #draw.rectangle((0,0,83,47), outline=0, fill=255)

    # Load default font.
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


        #disp.image(image)
        #disp.display()

        #time.sleep(5.0)
        disp.clear()
        disp.display()

    buffered = BytesIO()
    image.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue())
    return "data:image/png;base64,{}".format(img_str)

@app.callback(
    Output('message', 'children'),
    [Input('submit', 'n_clicks')],
    [State('image', 'src')])

def display_message(n_clicks, image):

    if image is None:
        return ['Insert a message']


    image = Image.open(BytesIO(base64.b64decode(image.split(",")[1])))

    disp.image(image)
    disp.display()

    time.sleep(30.0)
    disp.clear()
    disp.display()

    ''' file_path_pi = 'led_test.py'
    ip = '192.168.0.200'
    #subprocess.run("ssh -i ~/.ssh/id_rsa_pi pi@{} python {}".format(ip, file_path_pi), shell=True, check=True)
    subprocess.run("python {}".format(file_path_pi), shell=True, check=True)
    '''

    message = ['You are successfully connected!']
    return message



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8030)
