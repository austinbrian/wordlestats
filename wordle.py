import os
import re
from dotenv import load_dotenv
from slack_sdk import WebClient
import logging

import slack_sdk

load_dotenv()

logging.basicConfig()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOTTEST_ID = "C035T6TT4LS"

BASEURL = "https://slack.com/api"

client = WebClient(token=os.environ["BOT_TOKEN"])


def test_write_bottest(client, text):
    response = client.api_call(
        api_method="chat.postMessage",
        json={"channel": "C035T6TT4LS", "text": text},
    )
    assert response["ok"]
    assert response["message"]["text"] == text
    return


def read_bottest(client):
    return client.conversations_history(channel=BOTTEST_ID).data


def get_messages_from_conv_history(data: dict):
    # return data.get("messages")
    pass


def extract_wordle_conversations(messages: list):
    convs = []
    for i in messages:
        if re.match("Wordle \d+", i.get("text")):
            convs.append(i)
        else:
            pass
    return convs


def get_number_of_guesses(wscore_text):
    game_number, guesses = re.search("Wordle \d+", wscore_text)
    print(game_number, guesses)


def get_game_number(txt):
    num = re.search("Wordle \d+", txt)
    if num:
        return num.group(0).strip("Wordle ")
    else:
        pass


def get_attempt_details(txt: str) -> dict:
    """
    Attempt details are the the summary information available as a
    "heading" in the Wordle instance.
    """
    attempts = {"attempts": 0, "success": False, "hard": False}
    num = re.search("[\dX]/6.?", txt).group(0)
    if num:
        if "X" in num:
            attempts["attempts"] = 6
        else:
            attempts["attempts"] = int(num.strip("/6*\n"))
            attempts["success"] = True
        if "*" in num:
            attempts["hard"] = True
        attempts["game"] = get_game_number(txt)

        return attempts
    else:
        pass


def get_guess_details(txt: str):
    """
    This function extracts information about the individual guesses (the squares)
    that are included in a wordle attempt.
    """
    # TODO
    pass


def process_wordle_entry(entry: dict):
    entry = dict()
    wscore_text = re.findall("Wordle \d+ [\dX]/6*?\n", txt)
    print(wscore_text)
    if len(wscore_text) > 0:
        game_num = get_game_number(wscore_text)
        entry.update({"game": game_num})
        attempts = get_attempt_details(wscore_text)

    return entry


def get_team_members_list(client):
    return client.users_list().data.get("members")


def id_to_name_map(id: str, mems: list, name="name"):
    return {i.get("id"): i.get(name) for i in mems}


if __name__ == "__main__":
    print("OK")
