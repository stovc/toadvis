# This is a sample Python script.

from telethon.sync import TelegramClient

import csv
import constants
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

if __name__ == '__main__':
    api_id = constants.api_id
    api_hash = constants.api_hash
    phone = constants.phone

    client = TelegramClient(phone, api_id, api_hash)

    client.start()

    chats = []
    last_date = None
    size_chats = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=size_chats,
        hash=0
    ))
    chats.extend(result.chats)

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=size_chats,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    for g in groups:
        if g.title == 'Жабки':
            target_group = g

    all_messages = []
    offset_id = 0
    limit = 100
    total_messages = 0
    total_count_limit = 500000

    NL = 'þ'

    while True:
        history = client(GetHistoryRequest(
            peer=target_group,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            msg = message.to_dict()
            if 'message' in msg:
                txt = msg['message'].replace('\n', NL)
                if '🐸Имя жабы:' in txt:
                    msg = {'date': msg['date'].strftime("%m/%d/%Y_%H:%M"), 'text': txt}
                    print(total_messages, msg['date'])
                    all_messages.append(msg)
        offset_id = messages[len(messages) - 1].id
        total_messages += limit
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    print("Saving...")

    with open("messages_500K.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["date", "text"])
        for message in all_messages:
            date = message['date']
            text = message['text']
            writer.writerow([date, text])
    print("Done.")
