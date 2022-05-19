import json


def load_results_into_template(results: dict) -> str:
    out = ""
    txt_template = {
        "type": "section",
        "fields": [
            {"type": "mrkdwn", "text": "*{name}*"},
            {"type": "mrkdwn", "text": "{value}"},
        ],
    }
    divider = ',{"type": "divider"},'
    for k, v in results.items():
        txt_template["fields"][0]["text"] = k
        txt_template["fields"][1]["text"] = str(v)
        out = out + json.dumps(txt_template) + divider
    return out


def frontmatter():
    txt = """
{
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":white_large_square::large_yellow_square::large_green_square: Scoreboard :large_green_square::large_yellow_square::white_large_square:",
				"emoji": true
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "_Average score_"
				}
			]
		},
		{
			"type": "divider"
		},
    """
    return txt


def frontmatter_with_selection():
    txt = """
{
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":white_large_square::large_yellow_square::large_green_square: Scoreboard :large_green_square::large_yellow_square::white_large_square:",
				"emoji": true
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "_Select a metric_"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": true
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Average Score",
							"emoji": true
						},
						"value": "avg_score"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Number of Games",
							"emoji": true
						},
						"value": "num_games"
					}
				],
				"action_id": "metric-dropdown"
			}
		},
		{
			"type": "divider"
		},
    """
    return txt


def main(d={"kevin": 7, "emily": 4, "kellen": 3}):
    f = frontmatter()
    s = load_results_into_template(d)
    b = "]}"
    out = f + s[:-1] + b
    return out


if __name__ == "__main__":
    print(main())
