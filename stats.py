import pandas as pd
from argon2 import extract_parameters

import wordle as wd

WORDLE_CHANNEL_ID = "C02TCE39Y81"


def main():
    all_msgs = wd.get_messages_from_conv_history(
        wd.client, WORDLE_CHANNEL_ID, limit=1000
    )
    assert len(all_msgs) > 2
    print(f"Number of messages: {len(all_msgs)}")

    msgs = wd.extract_wordle_conversations(all_msgs)

    print(f"Number of wordle-related messages: {len(msgs)}")


def make_df(msgs):
    entries = [wd.process_wordle_entry(i) for i in msgs]
    df = pd.DataFrame(entries)
    team_members = wd.get_team_members_list(wd.client)
    team_name_map = wd.id_to_name_map(team_members, "name")
    team_display_map = wd.id_to_name_map(team_members, "real_name")
    df["name"] = df.user.map(team_name_map)
    df["realname"] = df.user.map(team_display_map)
    return df


if __name__ == "__main__":
    main()
