import plotly.graph_objects as go


def number_of_games_bar_graph(df):
    data = df.name.value_counts().to_dict()
    fig = go.Figure(
        data=go.Bar(x=list(data.keys()), y=list(data.values())),
        layout_title_text="Number of games played",
    )
    return fig
