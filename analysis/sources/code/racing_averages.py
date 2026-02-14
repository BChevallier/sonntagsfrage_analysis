import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation, FFMpegWriter


window_size = 30 #in days
jump_size = 45 #amount of days from one frame to the next
plot_points = False
dark_mode = False
plot_elections=False

PATH="../data/umfragen_wahlrecht.csv"
df_umfragen = pd.read_csv(PATH, parse_dates=['date'])
df_umfragen.set_index("date", inplace=True)

print(df_umfragen["institute_id"].unique())

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

df_average=pd.DataFrame()
for party in parties:
    df_temp=df_umfragen.copy()
    df_temp[party]=pd.to_numeric(df_temp[party], errors='coerce')
    df_temp = df_temp.resample('D').agg({party: 'mean'})
    df_average[party]=df_temp[party].rolling(f"{window_size}D", center=True).mean()

# sets the graphic styles
if dark_mode:
    bg_color = "black"
    ax_color = "white"
    file_ending = "dark"
else:
    bg_color = "white"
    ax_color = "black"
    file_ending = "light"


fig, ax = plt.subplots(facecolor=bg_color)
ax.set_facecolor(bg_color)
ax.tick_params(axis='x', colors=ax_color)
ax.tick_params(axis='y', colors=ax_color)
for spine in ax.spines.values():
    spine.set_color(ax_color)
sns.despine(ax=ax)
ax.set_xlim(df_average.index.min(), df_average.index.max())
ax.set_ylim(0,55)
title = ax.set_title("",color=ax_color)


lines = [ax.plot([], [], color=color, label=party)[0] for party, color in parties.items()]
points= [ax.scatter([],[], color=color, s=20) for party, color in parties.items()]

if dark_mode: lines[0].set_color("white")

def init():
    return lines+points+ [title]

def animate(i):
    for count, party in enumerate(parties):
        values=df_average[party].iloc[:i*jump_size]
        lines[count].set_data(df_average.iloc[:i*jump_size].index, values)
        if i * jump_size > 0 and plot_points:
            x = df_average.index[i * jump_size - 1]
            y = df_average[party].iloc[i * jump_size - 1]
            points[count].set_offsets([[x, y]])
        else:
            points[count].set_offsets([np.empty(2)])
    #title.set_text(df_average.index[i*jump_size].year)
    print(f"Frame {i}/{len(df_average)//jump_size-1} generated!")
    return lines+points+ [title]

ax.legend(loc="upper right", frameon=True)
ani = FuncAnimation(fig, animate, frames=len(df_average)//jump_size, init_func=init,
                    interval=100, blit=False, repeat=False)

writer = FFMpegWriter(
    fps=60,
    metadata=dict(artist="you"),
    bitrate=3600,
)

print("Saving animation ...")
ani.save(
    f"../../output/animations/racing_average_{file_ending}.gif",
    writer=writer)

plt.show()