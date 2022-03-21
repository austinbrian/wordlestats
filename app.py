from fastapi import FastAPI

import wordle as wd
from stats import get_all_wordle_msgs, make_df

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Get wordle data
    msgs = get_all_wordle_msgs()

    # Load data, prepare graph
    global df
    df = make_df(msgs)
    print(f"Loaded {len(df)} entries into analysis dataframe into memory.")


@app.get("/health")
async def healthcheck():
    return "Healthy"


@app.get("/scoreboard")
async def scoreboard():
    return df.groupby("name")["attempts"].mean().sort_values()
