import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pandas as pd
import seaborn as sns

window_size = 5 #in days
frame_number = 1000
dark_mode = True

PATH="../data/umfragen_wahlrecht.csv"
df = pd.read_csv(PATH, parse_dates=['date'])
df.set_index("date", inplace=True)

plot_elections=False
parties = {
    'CDU/CSU': 'black',
    'SPD': 'red',
    'GRÜNE': 'green',
    'FDP': 'yellow',
    'LINKE': 'purple',
    'AfD': 'blue',
    #'FW': 'orange',
    #'BSW': 'brown',
    #'Sonstige': 'gray',
    #'PIRATEN': '#F97F02'  # Pirate Party orange
}
bundestag_dates = [
    '2002-09-22',
    '2005-09-18',  # Early election
    '2009-09-27',
    '2013-09-22',
    '2017-09-24',
    '2021-09-26',
    '2025-02-23'   # Early election after dissolution
]
computed_dfs = []

# sets the graphic styles
if dark_mode:
    bg_color = "black"
    ax_color = "white"
    file_ending = "dark"
else:
    bg_color = "white"
    ax_color = "black"
    file_ending = "light"

for i in range(1,frame_number+1):
    averages_df = pd.DataFrame()
    for party in parties:
        temp_df = df.copy()
        temp_df[party]=pd.to_numeric(temp_df[party], errors='coerce')
        temp_df = temp_df.resample('D').agg({party: 'mean'})
        averages_df[party] = temp_df[party].rolling(f"{window_size*i}D").mean()
        print(f"{window_size*i}-day rolling average for {party} created")
    averages_df.to_csv(f"../../output/survey_averages/{window_size*i}D_survey_averages.csv",)
    computed_dfs.append(averages_df)

fig, ax = plt.subplots(facecolor=bg_color)
ax.set_facecolor(bg_color)
for spine in ax.spines.values():
    spine.set_color(ax_color)
ax.set_xlim(averages_df.index.min(), averages_df.index.max())
ax.set_ylim(0,55)
ax.tick_params(axis='x', colors=ax_color)
ax.tick_params(axis='y', colors=ax_color)
lines = [ax.plot([], [], color=color, label=party)[0] for party, color in parties.items()]
title = ax.set_title("", color=ax_color)
sns.despine(ax=ax)
ax.xaxis.label.set_color(ax_color)
ax.yaxis.label.set_color(ax_color)
if dark_mode: lines[0].set_color("white")

def init():
    for line in lines:
        line.set_data([], [])  # Or np.ma.array(x, mask=True) for lines
    return lines+[title]

def animate(i):
    for count, line in enumerate(lines):
        values = computed_dfs[i][list(parties.keys())[count]]
        line.set_data(computed_dfs[i].index, values)
    title.set_text(f"Sonntagsfrage ({i*window_size}-Tage gleitendes Fenster)")
    return lines+[title]

ax.legend()
ani = FuncAnimation(fig, animate, frames=len(computed_dfs), init_func=init,
                    interval=100, blit=True, repeat=False)

if plot_elections:
    for date in bundestag_dates:
        plt.axvline(x=date, color="lightgrey", linestyle="dashed")

writer = FFMpegWriter(
    fps=60,
    metadata=dict(artist="you"),
    bitrate=3600,
)

ani.save(
    f"../../output/animations/sonntagsfrage_rolling_window_{file_ending}.mp4",
    writer=writer
)

plt.show()
