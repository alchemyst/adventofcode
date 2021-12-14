import json
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('dark_background')

YEAR = 2021
MONTH = 12
STARTTIME = 7
LABEL_SEP = 0.1

TICKS_AND_LABELS = [
    [1*60, '1 min'],
    [5*60, '5 mins'],
    [10*60, '10 mins'],
    [20*60, '20 mins'],
    [30*60, '30 mins'],
    [60*60, '1 hour'],
    [6*60*60, '6 hours'],
    [2*60*60, '2 hours'],
    [60*60*24, '1 day'],
    [10*60*60*24, '10 days'],
]

TICKS, LABELS = zip(*TICKS_AND_LABELS)

def read_local_leaderboard():
    with open('1189810.json') as f:
        leaderboard = json.load(f)

    data = []

    for member_key, member in leaderboard['members'].items():
        name = member['name']
        if name is None:
            name = member_key
        for day, stats in member['completion_day_level'].items():
            day = int(day)
            competition_start = datetime.datetime(YEAR, MONTH, day, STARTTIME, 0)
            day_data = {
                'name': name,
                'day': day,
            }
            for level in ('1', '2'):
                if level in stats:
                    ts = stats[level]['get_star_ts']
                    completed = datetime.datetime.fromtimestamp(ts)
                    duration = completed - competition_start
                    seconds = duration.total_seconds()
                else:
                    seconds = None
                day_data[f'star_{level}'] = seconds

            data.append(day_data)

    df = pd.DataFrame(data)
    df['diff'] = df['star_2'] - df['star_1']

    return df

def read_top_100():
    return pd.read_csv('scores.tsv', sep='\t')


df = read_local_leaderboard()

top100 = read_top_100().query('year == @YEAR')

print(df.sort_values(['day', 'star_2']))

fig, (ax_abs_time, ax_diff) = plt.subplots(
    2, 1,
    sharex=True,
    figsize=(6, 6),
    dpi=150,
    gridspec_kw={'height_ratios': [2, 1]},
)

last = df['day'].max()
last_time_on_last_day = df[df['day'] == last]['star_2'].max()
days = np.arange(1, last + 1)

catchup_curve = last_time_on_last_day + (last - days)*60*60*24

ax_abs_time.plot(days, catchup_curve, '--', color='pink', alpha=0.5)
ax_abs_time.text(1 + LABEL_SEP, max(catchup_curve), 'Limit for new data')

for i, (name, data) in enumerate(df.groupby('name')):
    data_by_day = data.set_index('day').sort_index()
    last_day = data_by_day.index.max()
    last_star = data_by_day.loc[last_day, 'star_2']

    color = f'C{i}'
    ax_abs_time.fill_between(
        data_by_day.index,
        data_by_day['star_1'],
        data_by_day['star_2'],
        color=color,
        alpha=0.7,
    )
    ax_abs_time.text(last_day + LABEL_SEP, last_star, name)


    doneboth = data_by_day.dropna()
    last_day = doneboth.index.max()
    last_diff = doneboth.loc[last_day, 'diff']

    ax_diff.plot(data_by_day.index, data_by_day['diff'], color=color)
    ax_diff.text(last_day + LABEL_SEP, last_diff, name)

# silver stars top 100
for i, color in enumerate(['gray', 'yellow'], 1):
    stars = top100.query('stars == @i')
    dayjitter = stars['day'] + (i - 1 + np.random.uniform(-0.4, 0.4, size=len(stars)))/3
    time = stars['seconds']
    ax_abs_time.scatter(dayjitter, time, 0.2, color=color, marker='.')

ax_abs_time.set(
    title=f'Advent of code {YEAR}',
    yscale='log',
    yticks=TICKS,
    yticklabels=LABELS,
)

ax_diff.set(
    yscale='log',
    ylabel='star_2 - star_1',
    xticks=range(1, df['day'].max()+1),
    yticks=(60,) + TICKS[:4],
    yticklabels=('1 min',) + LABELS[:4],
    xlabel='Day',
    # xlim=[1, last]
)


plt.tight_layout()
plt.show()