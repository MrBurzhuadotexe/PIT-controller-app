import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import base64

app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'PL', 'value': 'opt1'},
    {'label': 'EN', 'value': 'opt2'},
    {'label': 'RU', 'value': 'opt3'}
]

app.layout = html.Div([
    html.Div([
        html.Img(
            src='data:image/png;base64,{}'.format(base64.b64encode(open('cropped-Logo_PP.png', 'rb').read()).decode()),
            alt='Example Image', width='90'),
        html.H1('Regulator PID', style={'font-family': 'Arial', 'font-size': '40px'}),
        dcc.Dropdown(
            id='dropdown',
            options=dropdown_options,
            value='opt1'
        ),
        html.Div(id='output-container')
    ], style={'grid-column-gap': '0px', 'grid-row-gap': '0px',
              # 'background-color': '#f6f6f6',
              'flex-flow': 'row',
              'grid-template-rows': 'auto',
              'grid-template-columns': '.5fr 3.75fr .5fr', 'grid-auto-columns': '1fr', 'grid-auto-flow': 'row dense',
              'justify-content': 'flex-end',
              'align-items': 'center', 'justify-items': 'start',
              'display': 'grid'}),
    html.Div([
        dcc.Markdown('''
        # Opis projektu
        Celem projektu jest stworzenie symulacji silnika prądu stałego uwzględniającej jego charakterystyki fizyczne oraz zaimplementowanie regulatora PID dla kontroli prędkości obrotowej silnika w języku programowania Python. W celu osiągnięcia tego celu przeprowadziliśmy analizę i przekształcenia fizycznych równań silnika.
        
        Do realizacji symulacji użyliśmy następujących stałych dla silnika:
        >
        >$R$ = 2.0  Ohm, rezystancja uzwojenia wirnika
        >
        >$L$ = 0.1 Henry, indukcyjność uzwojenia wirnika
        >
        >$B$ = 0.5  Współczynnik tarcia
        >
        >$J$ = 0.1  Moment bezwładności wirnika
        >
        >$K_m$ = 0.1  Stała momentu obrotowego
        >
        >$K_e$ = 0.1  Stała elektromotoryczna
        >
        
        Te parametry pozwalają uwzględnić podstawowe cechy fizyczne silnika i stworzyć precyzyjną symulację jego działania. Implementacja regulatora PID zapewnia dokładną kontrolę prędkości obrotowej silnika, co stanowi kluczowy aspekt tego projektu.
        
        ''', mathjax=True, style={'font-family': 'Arial', 'font-size': '20px'}),
        html.Img(
            src='data:image/png;base64,{}'.format(base64.b64encode(open('scheme.png', 'rb').read()).decode()),alt='Example Image', width='80%'),

        ], style={'padding-left': '180px', 'padding-right': '180px', 'background-color': '#fafafa'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='speed-plot',
            ),

            dcc.Graph(
                id='pid-output-plot',
            ),

            dcc.Graph(
                id='current-plot',
            ),

            dcc.Graph(
                id='voltage-plot',
            ),
        ], style={'width': '69%', 'float': 'left', 'right': 40, 'border': '2px solid #ddd',
                  'border-radius': '5px', }),
        html.Div([
            html.Div([

                html.Div([
                    html.Div([], style={'height': '5vh'}),
                    html.Label("Kp:", style={'left': '24px', 'position': 'relative'}),
                    dcc.Slider(
                        id='slider-kp',
                        min=0,
                        max=50,
                        step=0.1,
                        value=15,
                        updatemode='drag',
                        tooltip={'always_visible': True},
                        marks=None
                    ),
                ], style={}),

                html.Div([
                    html.Label("Ki:", style={'left': '24px', 'position': 'relative'}),
                    dcc.Slider(
                        id='slider-ki',
                        min=0,
                        max=30,
                        step=0.1,
                        value=5,
                        updatemode='drag',
                        tooltip={'always_visible': True},
                        marks=None
                    ),
                ], style={}),

                html.Div([
                    html.Label("Kd:", style={'left': '24px', 'position': 'relative'}),
                    dcc.Slider(
                        id='slider-kd',
                        min=0,
                        max=0.1,
                        step=0.001,
                        value=0.04,
                        updatemode='drag',
                        tooltip={'always_visible': True},
                        marks=None
                    ),
                ], style={}),
                html.Div([
                    html.Label("Target speed:", style={'left': '24px', 'position': 'relative'}),
                    dcc.Slider(
                        id='slider-target',
                        min=0,
                        max=10,
                        step=0.01,
                        value=5.0,
                        updatemode='drag',
                        tooltip={'always_visible': True},
                        marks=None
                    ),
                ], style={}),
            ], style={
                'grid-rpw-gap': '16px',
                'grid-column-gap': '16px',
                'grid-template-rows': 'auto auto',
                'grid-template-columns': '1fr 1 fr',
                'grid-auto-columns': '1fr',
                'display': 'grid',
                'border': '2px solid #ddd',
                'border-radius': '5px',
                'width': '30%',
                'float': 'right'
            })
        ], style={'position': 'sticky',
                  'top': '50px'
                  })
    ], style={'height': '500vh'})
])


# Callback to update the plots based on user input
@app.callback(
    [Output('speed-plot', 'figure'),
     Output('pid-output-plot', 'figure'),
     Output('current-plot', 'figure'),
     Output('voltage-plot', 'figure')],
    [
        Input('slider-kp', 'value'),
        Input('slider-ki', 'value'),
        Input('slider-kd', 'value'),
        Input('slider-target', 'value')
    ]
)
def update_plots(kp, ki, kd, target):
    global Kp, Ki, Kd
    Kp = kp
    Ki = ki
    Kd = kd
    target_speed = target  # Pożądana prędkość obrotowa silnika

    # ... (previous code for simulation)
    R = 2.0  # Ohm
    L = 0.1  # Henry
    B = 0.5  # Współczynnik tarcia
    J = 0.1  # Moment bezwładności
    Km = 0.1  # Stała momentu
    Ke = 0.1  # Stała elektromagnetyczna odwrotnego pola
    Mm = 1

    I = 0.0
    E = 0.0
    speed = 0.0
    previous_error = 0.0
    integral = 0.0

    # Listy do przechowywania danych do rysowania wykresów
    speed_history = []
    target_speed_history = []
    pid_output_history = []
    current_history = []
    voltage_history = []

    # Ograniczenie sygnału wyjściowego regulatora
    pid_output_limit = 72

    # Ograniczenie maksymalnej prędkości obrotowej silnika
    max_speed_limit = 20.0  # rad/s

    # Ograniczenie początkowej prędkości kątowej
    initial_speed_limit = 0  # rad/s

    # Parametry symulacji
    Tp = 0.01
    time = np.arange(0, 2.5, Tp)

    # Symulacja silnika
    for t in time:
        # Obliczenia sterowania PID
        error = target_speed - speed
        integral += error * Tp
        derivative = (error - previous_error) / Tp
        pid_output = Kp * (error + Ki * integral + Kd * derivative)

        # Ograniczenie sygnału wyjściowego regulatora
        pid_output = np.clip(pid_output, 0, pid_output_limit)

        # Sterowanie silnikiem z uwzględnieniem wyjścia PID
        voltage = pid_output
        Ep = E
        E = ((Km * I + Mm - B * E) / J) * Tp + E

        I = ((voltage - R * I - Ke * Ep) / L) * Tp + I

        # Obliczenie napięcia na uzwojeniu
        armature_voltage = R * I + Ke * E

        # Ograniczenie maksymalnej prędkości obrotowej silnika
        speed = np.clip(E, 0, max_speed_limit)

        # Ograniczenie początkowej prędkości kątowej
        if t < Tp and abs(speed) < initial_speed_limit:
            speed = np.sign(target_speed) * initial_speed_limit

        # Zapis danych do rysowania wykresów
        speed_history.append(speed)
        target_speed_history.append(target_speed)
        pid_output_history.append(pid_output)
        current_history.append(I)
        voltage_history.append(armature_voltage)

        # Aktualizacja poprzedniego błędu
        previous_error = error

    # Update the figures for each subplot
    speed_figure = {
        'data': [
            go.Scatter(x=time, y=speed_history, name='Actual Speed'),
            go.Scatter(x=time, y=target_speed_history, mode='lines', line={'dash': 'dash'}, name='Target Speed')
        ],
        'layout': go.Layout(title='Speed Plot', xaxis={'title': 'Time (s)'}, yaxis={'title': 'Speed (rad/s)'})
    }

    pid_output_figure = {
        'data': [go.Scatter(x=time, y=pid_output_history, name='PID Output')],
        'layout': go.Layout(title='PID Output Plot', xaxis={'title': 'Time (s)'}, yaxis={'title': 'PID Output'})
    }

    current_figure = {
        'data': [go.Scatter(x=time, y=current_history, name='Armature Current')],
        'layout': go.Layout(title='Armature Current Plot', xaxis={'title': 'Time (s)'}, yaxis={'title': 'Current (A)'})
    }

    voltage_figure = {
        'data': [go.Scatter(x=time, y=voltage_history, name='Armature Voltage')],
        'layout': go.Layout(title='Armature Voltage Plot', xaxis={'title': 'Time (s)'}, yaxis={'title': 'Voltage (V)'})
    }

    return speed_figure, pid_output_figure, current_figure, voltage_figure


if __name__ == '__main__':
    app.run_server(debug=True)
