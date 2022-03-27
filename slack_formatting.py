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


def format_for_slack(results: dict) -> str:
    out = frontmatter()
    return out


def simple_text_layout(results: dict) -> str:
    out = "# Scoreboard\n\n"
    return out


def main(d={"kevin": 7, "emily": 4, "kellen": 3}):
    f = frontmatter()
    s = load_results_into_template(d)
    b = "]}"
    out = f + s[:-1] + b
    return out


if __name__ == "__main__":
    print(main())
