import json

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

import slack_formatting
import wordle as wd
from stats import get_all_wordle_msgs, make_df

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=60 * 10)  # 10 minutes
async def startup_event():
    msgs = get_all_wordle_msgs()

    global df
    df = make_df(msgs)
    print(f"Loaded {len(df)} entries into analysis dataframe into memory.")


@app.get("/health")
async def healthcheck():
    return "Healthy"


@app.post("/scoreboard")
@app.get("/scoreboard")
async def scoreboard():
    data = df.groupby("name")["attempts"].mean().sort_values().map("{:,.3f}".format)
    txt = slack_formatting.main(data)
    return json.loads(txt)


@app.get("/formatting")
async def formatting():
    txt = slack_formatting.main()
    j = json.loads(txt)
    return j
