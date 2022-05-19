import os
import random

import dash
import flask
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

import figures as figs
from metrics import create_metric


def create_dash_app(
    requests_pathname_prefix: str = None, df: pd.DataFrame = None, **kwargs
) -> dash.Dash:
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get("secret_key", "secret")

    if df is None:
        df = pd.read_csv(
            "https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv"
        )

    app = dash.Dash(
        __name__,
        server=server,
        requests_pathname_prefix=requests_pathname_prefix,
        **kwargs
    )

    app.scripts.config.serve_locally = False
    dcc._js_dist[0]["external_url"] = "https://cdn.plot.ly/plotly-basic-latest.min.js"

    app.layout = html.Div(
        [
            html.H2(
                id="topblocks",
                children="\U0001F7E9 \U0001F7E8 \U0001F7E9 \U0001F7E8 \U00002B1C",
            ),
            html.H1("WordleStats Dashboard"),
            dcc.Dropdown(
                id="dropdown",
                options=[
                    {"label": "Average number of attempts", "value": "avg-guesses"},
                    {"label": "Number of games played", "value": "num-games"},
                    {"label": "Number of wins", "value": "wins"},
                    {"label": "Number of losses", "value": "losses"},
                    {"label": "Percentage win", "value": "pwin"},
                    {"label": "Attempts per win", "value": "apw"},
                ],
                value="num-games",
            ),
            dcc.Graph(id="bar-graph", figure=figs.number_of_games_bar_graph(df)),
            html.H2(
                id="bottomblocks",
                children="\U0001F7E9 \U0001F7E8 \U0001F7E9 \U0001F7E8 \U00002B1C",
            ),
        ],
        className="container",
    )

    @app.callback(
        Output("bar-graph", "figure"),
        [Input("dropdown", "value"), Input("dropdown", "label")],
    )
    def update_graph(selected_dropdown_value, selected_dropdown_label):
        data = create_metric(df, selected_dropdown_value)
        fig = figs.bar_graph_of_names(data, selected_dropdown_label)

        return fig

    @app.callback(Output("topblocks", "children"), [Input("dropdown", "value")])
    def update_top_bar(value):
        """
        Update the wordle boxes at the top every time we change the dropdown val
        """
        boxes = ["\U0001F7E9", "\U0001F7E8", "\U00002B1C"]
        return " ".join(random.choices(boxes, k=5))

    @app.callback(Output("bottomblocks", "children"), [Input("dropdown", "value")])
    def update_bottom_bar(value):
        """
        Update the wordle boxes at the bottom every time we change the dropdown val
        """
        boxes = ["\U0001F7E9", "\U0001F7E8", "\U00002B1C"]
        return " ".join(random.choices(boxes, k=5))

    return app
