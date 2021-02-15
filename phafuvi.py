import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("ebuild-timings.csv")
df = df.pivot(index=['Package', 'Phase Function'], columns='Status', values='Timestamp').reset_index().sort_values(by=['BEGIN'])
df.columns.name=None

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Actions of the Gentoo package manager over time", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_executor",
                 options=[
                     {"label": "Executor 1", "value": 1},
                     {"label": "Executor 2", "value": 2},
                     {"label": "Executor 3", "value": 3},
                     {"label": "Executor 4", "value": 4}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='ebuild_timing', figure={})
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output("ebuild_timing", "figure"), 
    [Input("slct_executor", "value")]
)

def update_graph(option_slctd):
    container = "The executor chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    fig = go.Figure()
    names = set()
    for (start, end, package, function) in zip(dff["BEGIN"], dff["END"], dff["Package"], dff["Phase Function"]):
        name = f"{function}"
        if name in names:
            show_legend=False
        else:
            show_legend=True
            names.add(name)
        fig.add_trace(go.Scatter(x=[package, package], y=[start, end],
                    mode='lines+markers', name=name, legendgroup=name,
                    marker=dict(size=9, color=set_color(name)),
                    showlegend=show_legend))
    fig.update_layout(xaxis_title="Package", yaxis_title="Timestamp")
    return fig

def set_color(phase_func):
        if(phase_func == "pkg_pretend"):
            return px.colors.qualitative.G10[0]
        elif(phase_func == "pkg_setup"):
            return px.colors.qualitative.G10[1]
        elif(phase_func == "src_unpack"):
            return px.colors.qualitative.G10[2]
        elif(phase_func == "src_prepare"):
            return px.colors.qualitative.G10[3]
        elif(phase_func == "src_configure"):
            return px.colors.qualitative.G10[4]
        elif(phase_func == "src_compile"):
            return px.colors.qualitative.G10[5]
        elif(phase_func == "src_install"):
            return px.colors.qualitative.G10[6]
        elif(phase_func == "pkg_preinst"):
            return px.colors.qualitative.G10[7]
        elif(phase_func == "pkg_postinst"):
            return px.colors.qualitative.G10[8]

if __name__ == "__main__":
    app.run_server(debug=True)
