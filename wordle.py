import logging
import os
import re

from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

logging.basicConfig()

BOT_TOKEN = os.getenv("BOT_TOKEN")
client = WebClient(token=os.environ["BOT_TOKEN"])


def get_messages_from_conv_history(client, channel_id):
    return client.conversations_history(channel=channel_id).data.get("messages", [])


def extract_wordle_conversations(messages: list):
    convs = []
    for i in messages:
        if re.match("Wordle \d+", i.get("text")):
            convs.append(i)
        else:
            pass
    return convs


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
    attempts = get_attempt_details(entry.get("text"))
    entry.update(attempts)
    return entry


def get_team_members_list(client):
    return client.users_list().data.get("members")


def id_to_name_map(id: str, mems: list, name="name"):
    return {i.get("id"): i.get(name) for i in mems}


if __name__ == "__main__":
    print("OK")
