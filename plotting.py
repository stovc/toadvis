import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt


def get_exp(text):
    exp_current = int(text.split('/')[0])
    exp_lim = int(text.split('/')[1])
    exp = exp_current / exp_lim
    return exp


def get_mood(text):
    mood = text.split('(')[1][:-1]
    return mood

df = pd.read_csv('messages_500K.csv', delimiter='\t')

df = df[df["text"].str.count("þþ") == 2]

cols = ['name', 'lvl', 'exp', 'status', 'bugs', 'class']

cols = ['props', 'achievements', 'fights']
df[cols] = df['text'].str.split('þþ', expand=True)

df = df.drop(columns=['text'])

# Expand props

cols = ['name', 'lvl', 'exp', 'status', 'state', 'bugs', 'class', 'mood']
df[cols] = df['props'].str.split('þ', expand=True)

df = df.drop(columns=['props'])

for col in cols:
    df[col] = df[col].str.split(': ').str[1]
print(df)
print(df['mood'])
df['mood'] = df['mood'].apply(get_mood)
print(df)
print(df['mood'])
names = list(df['name'].unique())
names.remove('Ваша Жаба')

# Expand fights

cols = ['wins', 'losses']

df_fights = df[df['fights'].str.count("þ") == 1]

df_fights[cols] = df_fights['fights'].str.split('þ', expand=True)

df_fights = df_fights.drop(columns=['fights'])

for col in cols:
    df_fights[col] = df_fights[col].str.split(': ').str[1]

with plt.xkcd():

    plt.figure(figsize=(16, 12))

    for n in names:
        dates = df[df['name'] == n]['date']
        xs = [dt.datetime.strptime(d, '%m/%d/%Y_%H:%M').date() for d in dates]

        exp_str = df[df['name'] == n]['exp']
        exp = exp_str.apply(get_exp)

        ys = df[df['name'] == n]['lvl'].astype(int)
        ys = ys + exp
        plt.plot(xs, ys, label=n)

    plt.legend()
    plt.xlabel('Дата', fontsize=24)
    plt.ylabel('Уровень жабы', fontsize=24)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.savefig('lvl.jpg')

with plt.xkcd():

    plt.figure(figsize=(12, 10))

    for n in names:

        xs = df_fights[df_fights['name'] == n]['losses'].astype(int)
        ys = df_fights[df_fights['name'] == n]['wins'].astype(int)

        plt.plot(xs, ys, label=n)

    plt.legend()
    plt.xlabel('Поражения', fontsize=24)
    plt.ylabel('Победы', fontsize=24)

    plt.savefig('fights.jpg')

with plt.xkcd():

    plt.figure(figsize=(12, 10))

    for n in names:
        dates = df[df['name'] == n]['date']
        xs = [dt.datetime.strptime(d, '%m/%d/%Y_%H:%M').date() for d in dates]

        ys = df[df['name'] == n]['bugs'].astype(int)

        plt.plot(xs, ys, label=n)

    plt.legend()
    plt.xlabel('Дата', fontsize=24)
    plt.ylabel('Букашки', fontsize=24)

    plt.savefig('bugs.jpg')



with plt.xkcd():

    plt.figure(figsize=(12, 10))

    for n in names:
        dates = df_fights[df_fights['name'] == n]['date']
        xs = [dt.datetime.strptime(d, '%m/%d/%Y_%H:%M').date() for d in dates]

        ys = df_fights[df_fights['name'] == n]['wins'].astype(int)

        plt.plot(xs, ys, label=n)

    plt.legend()
    plt.xlabel('Дата', fontsize=24)
    plt.ylabel('Победы', fontsize=24)

    plt.savefig('wins.jpg')

with plt.xkcd():

    plt.figure(figsize=(12, 10))

    for n in names:
        dates = df[df['name'] == n]['date']
        xs = [dt.datetime.strptime(d, '%m/%d/%Y_%H:%M').date() for d in dates]

        ys = df[df['name'] == n]['mood'].astype(int)

        plt.plot(xs, ys, label=n)

    plt.legend()
    plt.xlabel('Дата', fontsize=24)
    plt.ylabel('Настроение', fontsize=24)

    plt.savefig('mood.jpg')