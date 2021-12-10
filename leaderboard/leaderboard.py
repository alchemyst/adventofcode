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
    [5*60, '5 mins'],
    [10*60, '10 mins'],
    [15*60, '15 mins'],
    [30*60, '30 mins'],
    [60*60, '1 hour'],
    [12*60*60, '12 hours'],
    [2*60*60, '2 hours'],
    [60*60*24, '1 day'],
]

TICKS, LABELS = zip(*TICKS_AND_LABELS)

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

print(df.sort_values(['day', 'star_2']))

fig, ax = plt.subplots(dpi=150)

last = df['day'].max()
last_time_on_last_day = df[df['day'] == last]['star_2'].max()
days = np.arange(1, last + 1)

catchup_curve = last_time_on_last_day + (last - days)*60*60*24

ax.plot(days, catchup_curve, '--', color='pink', alpha=0.5)
ax.text(1 + LABEL_SEP, max(catchup_curve), 'Limit for new data')

for i, (name, data) in enumerate(df.groupby('name')):
    data_by_day = data.set_index('day').sort_index()
    last_day = data_by_day.index.max()
    last_star = data_by_day.loc[last_day, 'star_2']

    color = f'C{i}'
    ax.fill_between(
        data_by_day.index,
        data_by_day['star_1'],
        data_by_day['star_2'],
        color=color,
        alpha=0.7,
    )
    ax.text(last_day + LABEL_SEP, last_star, name)

ax.set(
    title=f'Advent of code {YEAR}',
    yscale='log',
    yticks=TICKS,
    yticklabels=LABELS,
    xticks=range(1, df['day'].max()+1),
    xlabel='Day',
    xlim=[1, last]
)

plt.show()