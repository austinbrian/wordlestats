import wordle
import pytest


@pytest.fixture
def bottest_conversation_object():
    return wordle.read_bottest(wordle.client)


@pytest.fixture
def members_list():
    return wordle.get_team_members_list(wordle.client)


@pytest.fixture
def bottest_messages(bottest_conversation_object):
    messages = bottest_conversation_object.get("messages")
    assert type(messages) == list
    assert len(messages) > 10
    return messages


def test_extract_wordle_conversations(bottest_messages):
    w_convs = wordle.extract_wordle_conversations(bottest_messages)
    assert type(w_convs) == list
    assert len(w_convs) > 0
    for i in w_convs:
        assert ("Wordle ") in i.get("text")


@pytest.fixture
def wordle_bottest_messages(bottest_messages):
    messages = wordle.extract_wordle_conversations(bottest_messages)
    return messages


def test_get_game_number(wordle_bottest_messages):
    assert wordle.get_game_number("Wordle 234 5/6*") == "234"
    assert wordle.get_game_number("Wordle 444 X/6\n\n") == "444"
    assert wordle.get_game_number("Wordle 424 4/6\n") == "424"
    assert wordle.get_game_number(wordle_bottest_messages[0].get("text")) == "259"


def test_get_attempt_details(wordle_bottest_messages):
    assert wordle.get_attempt_details("Wordle 234 5/6*\n") == {
        "success": True,
        "attempts": 5,
        "hard": True,
        "game": "234",
    }
    assert wordle.get_attempt_details("Wordle 444 X/6") == {
        "success": False,
        "attempts": 6,
        "hard": False,
        "game": "444",
    }

    assert wordle.get_attempt_details("Wordle 424 X/6*") == {
        "success": False,
        "attempts": 6,
        "hard": True,
        "game": "424",
    }

    assert wordle.get_attempt_details(wordle_bottest_messages[0].get("text")) == {
        "success": True,
        "attempts": 3,
        "hard": True,
        "game": "259",
    }


def test_id_to_name_map(members_list):
    mem_map = wordle.id_to_name_map(id="USLACKBOT", mems=members_list, name="name")
    assert type(mem_map) == dict
    assert "USLACKBOT" in mem_map.keys()
    assert mem_map["USLACKBOT"] == "slackbot"

    map2 = wordle.id_to_name_map(id="USLACKBOT", mems=members_list, name="real_name")
    assert map2["USLACKBOT"] == "Slackbot"
