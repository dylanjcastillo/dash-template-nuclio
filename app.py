import dash

from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime

pio.templates.default = "simple_white"

# Lee los datos
df = pd.read_csv("avocado.csv", index_col=0).reset_index(drop=True)
df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
df.sort_values("Date", inplace=True)
regions = df.region.unique()
avocado_types = df.type.unique()
min_date = df.Date.min()
max_date = df.Date.max()

# Selecciona el color del header
COLOR_HEADER = "rgb(14, 88, 20)"

# Lista con los títulos y los filtros de la barra de la izquierda.
MENU = [
    html.P("Avocado Type", className="title-filter"),
    dcc.RadioItems(
        id="type-selector",
        options=[{"label": t.title(), "value": t} for t in avocado_types],
        value=avocado_types[0],
    ),
    html.P("Region", className="title-filter"),
    dcc.Dropdown(
        id="region-selector",
        options=[{"label": r, "value": r} for r in regions],
        value=regions[:3],
        multi=True,
        clearable=False,
    ),
    html.P("Dates", className="title-filter"),
    dcc.DatePickerRange(
        id="date-selector",
        start_date=min_date,
        min_date_allowed=min_date,
        end_date=max_date,
        max_date_allowed=max_date,
        initial_visible_month=min_date,
    ),
]

# Lista con los gráficos
GRAFICOS = [dcc.Graph(id="line-chart"), dcc.Graph(id="donut-chart")]

# Estructura de la app (no hace falta modificarla)
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            id="header",
            children=[html.H1("Avocados Prices and Volume", id="title")],
            style={"background": COLOR_HEADER},
        ),
        html.Div(
            children=[
                html.Div(
                    id="menu",
                    children=MENU,
                ),
                html.Div(
                    id="graphs",
                    children=GRAFICOS,
                ),
            ],
            id="content",
        ),
    ],
    id="wrapper",
)


# Callback que actualiza los gráficos
@app.callback(
    [Output("line-chart", "figure"), Output("donut-chart", "figure")],
    [
        Input("type-selector", "value"),
        Input("region-selector", "value"),
        Input("date-selector", "start_date"),
        Input("date-selector", "end_date"),
    ],
)
def update_graphs(avocado_type, selected_regions, start_date, end_date):

    filter_region = df.region.isin(selected_regions)
    filter_type = df.type == avocado_type
    filter_date = df.Date.between(start_date, end_date)

    # Filter data
    df_line = df[(filter_region) & (filter_type) & (filter_date)]
    df_donut = df[(filter_region) & (filter_type) & (filter_date)][
        ["region", "Total Volume"]
    ]
    df_donut = df_donut.groupby("region").sum().reset_index()

    # Create figures
    fig_donut = px.pie(
        data_frame=df_donut,
        names="region",
        values="Total Volume",
        hole=0.5,
        title="Total Volume per Region",
    )

    fig_line = px.line(
        data_frame=df_line,
        x="Date",
        y="AveragePrice",
        color="region",
        title="Average Price of Avocados per Region",
        labels={"AveragePrice": "", "Date": ""},
    )

    fig_line.update_traces(hovertemplate="$%{y:.2f}")

    fig_line.update_yaxes(tickprefix="$")

    fig_line.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig_line.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )
    return fig_line, fig_donut


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
