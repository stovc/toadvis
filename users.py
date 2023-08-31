# This is a sample Python script.

from telethon.sync import TelegramClient

import csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    api_id = 26368366
    api_hash = '42ccd8df055e6f7e343071f000aeff41'
    phone = '436704082531'

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

    print('Узнаём пользователей...')
    all_participants = []
    all_participants = client.get_participants(target_group)

    print('Сохраняем данные в файл...')
    with open("members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'name', 'group'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, name, target_group.title])
    print('Парсинг участников группы успешно выполнен.')