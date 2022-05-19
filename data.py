import logging
import os

import pandas as pd
from sqlalchemy import create_engine

import wordle as wd


def get_all_wordle_msgs():
    all_msgs = wd.get_messages_from_conv_history(
        wd.client, wd.WORDLE_CHANNEL_ID, limit=1000
    )
    assert len(all_msgs) > 2
    # print(f"Number of messages: {len(all_msgs)}")

    msgs = wd.extract_wordle_conversations(all_msgs)

    # print(f"Number of wordle-related messages: {len(msgs)}")
    return msgs


def make_df(msgs):
    entries = [wd.process_wordle_entry(i) for i in msgs]
    df = pd.DataFrame(entries)
    team_members = wd.get_team_members_list(wd.client)
    team_name_map = wd.id_to_name_map(team_members, "name")
    team_display_map = wd.id_to_name_map(team_members, "real_name")
    df["name"] = df.user.map(team_name_map)
    df["realname"] = df.user.map(team_display_map)
    df["datetime"] = df.ts.apply(lambda x: pd.Timestamp(float(x), unit="s"))
    df["game"] = df.game.apply(int)
    return df


def create_df():
    try:
        DATABASE_URL = os.environ["DATABASE_URL"]
        conn = create_engine(DATABASE_URL)
        df = pd.read_sql_query("select * from wordlestats", con=conn)
    except Exception as e:
        logging.error(e)

        msgs = get_all_wordle_msgs()
        df = make_df(msgs)
    return df


def pull_data_from_db(conn):
    return pd.read_sql_query('select * from "wordlestats"', con=conn)


if __name__ == "__main__":
    print("OK")
