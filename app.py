import json
import logging

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi_utils.tasks import repeat_every
from sqlalchemy import create_engine

import slack_formatting
import wordle as wd
from dashboard import create_dash_app
from data import create_df, get_all_wordle_msgs, make_df

app = FastAPI()

df = create_df()


@app.on_event("startup")
@repeat_every(seconds=60 * 10)  # 10 minutes
async def startup_event():
    global df
    df = create_df()
    logging.info(f"Loaded {len(df)} entries into analysis dataframe into memory.")


@app.get("/datainfo")
async def datainfo():
    df = create_df()
    return df.describe()


@app.get("/health")
async def healthcheck():
    return "Healthy"


@app.post("/api/scoreboard")
async def api_scoreboard(request: Request):

    logging.info(request.form)
    print(request.form)
    print("*****")
    form = request.form
    # form = json.loads(request.form["payload"])
    logging.info(form)
    item = dict(**form)
    logging.info(item)

    if payload:
        if type(payload) == str:
            payload = json.loads(payload)
        action_val = (
            payload.get("state")
            .get("values")
            .get("c5C")
            .get("metric-dropdown")
            .get("selected_option")
            .get("value")
        )
        if action_val == "num_games":
            data = (
                df.groupby("name")["attempts"]
                .mean()
                .sort_values()
                .map("{:,.3f}".format)
            )
        elif action_val == "avg_score":
            data = df.groupby("name")["attempts"].count().sort_values(ascending=False)
        else:
            data = {}
        txt = slack_formatting.main(data)
        return json.loads(txt)
    else:
        data = df.groupby("name")["attempts"].mean().sort_values().map("{:,.3f}".format)
        txt = slack_formatting.main(data)
        return json.loads(txt)


@app.post("/scoreboard")
@app.get("/scoreboard")
async def scoreboard():
    data = df.groupby("name")["attempts"].mean().sort_values().map("{:,.3f}".format)
    txt = slack_formatting.main(data)
    return json.loads(txt)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
dash_app = create_dash_app(
    requests_pathname_prefix="/", external_stylesheets=external_stylesheets, df=df
)
app.mount("/", WSGIMiddleware(dash_app.server))
