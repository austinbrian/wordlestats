from enum import Enum
from typing import List

import pandas as pd


def create_metric(df: pd.DataFrame, key):
    if key == "num-games":
        return df.name.value_counts().to_dict()
    if key == "avg-guesses":
        return (
            df.groupby("name")["attempts"]
            .mean()
            .sort_values(ascending=True)
            .map("{:,.3f}".format)
            .to_dict()
        )
    if key == "wins":
        return (
            df[df.success]
            .groupby("name")
            .index.count()
            .sort_values(ascending=False)
            .to_dict()
        )
    if key == "losses":
        return df[df.success == False].name.value_counts().to_dict()
    gdf = df.groupby("name").agg({"success": sum, "game": "count", "attempts": sum})
    if key == "pwin":
        return (gdf.success / gdf.game).sort_values().to_dict()

    if key == "apw":
        return (gdf.attempts / gdf.success).sort_values().to_dict()
