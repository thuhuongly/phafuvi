import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("ebuild-timings.csv")
df = df.pivot(index=['Package', 'Phase Function'], columns='Status', values='Timestamp').reset_index().sort_values(by=['Package', 'BEGIN'])
df.columns.name=None

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Actions of the Gentoo package manager over time", style={'text-align': 'center'}),
    html.Div(id='dummy', children=[]),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='ebuild_timing', figure={})
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output("ebuild_timing", "figure"), 
    [Input('dummy', 'id')]
)

def update_graph(option_slctd):
    container = "The executor chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    fig = go.Figure()
    names = set()
    begin = dff.loc[dff['Phase Function'] == 'pkg_setup', ['Package', 'BEGIN']].values
    end = dff.loc[dff['Phase Function'] == 'pkg_postinst', ['Package','END']].values

    timestamp = np.concatenate((begin, end), axis=1).tolist()
    executors = arrange_executor(timestamp)
    for i in range(0, len(executors)):
        traces = []
        for package in executors[i]:
            name = f"Executor {i + 1}"
            trace = go.Scatter(x=[name, name], y=[package[1], package[-1]],
                mode='lines+markers', name=package[0], legendgroup=package[0])
            fig.add_trace(trace)

    fig.update_layout(xaxis_title="Executor", yaxis_title="Timestamp")

    return fig

def arrange_executor(timestamp):
    # sort by begin time of pkg_setup
    sorted_timestamp = sorted(timestamp, key=lambda x: x[1])

    first_executor = [sorted_timestamp[0]]
    executors = [first_executor]

    for i in range(1,len(sorted_timestamp)):
        need_new = True
        for exe in executors:
            if sorted_timestamp[i] not in exe and exe[-1][-1] < sorted_timestamp[i][1]:
                exe.append(sorted_timestamp[i])
                need_new = False
                break
        if need_new == True:
            execu = []
            execu.append(sorted_timestamp[i])
            executors.append(execu)
    return executors

if __name__ == "__main__":
    import os

    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=debug)
