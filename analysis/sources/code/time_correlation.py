import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pandas as pd

from analysis.sources.code.bias_analyse import dark_mode

df=pd.read_csv("../../output/survey_averages/30D_survey_averages.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

dark_mode = False
jump_size= 5 #in days
windowsize = 365*4 #size of the considered time_frame for the correlation

if dark_mode:
    bg_color = "black"
    ax_color = "white"
    file_ending = "dark"
else:
    bg_color = "white"
    ax_color = "black"
    file_ending = "light"

def get_corr_matrix(df, date, window):
    min_date = date - pd.Timedelta(days=window // 2)
    max_date = date + pd.Timedelta(days=window // 2)
    filtered_df = df.loc[min_date:max_date]
    return filtered_df.corr(method='pearson')

print(df)
dates=df.index.tolist()[::jump_size]

fig, ax = plt.subplots(facecolor=bg_color)
ax.set_facecolor(bg_color)
title = ax.set_title(dates[0],color=ax_color)

starting_corr=get_corr_matrix(df, dates[0], windowsize)
im = ax.imshow(
    starting_corr.values,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    interpolation="none",
)
plt.colorbar(im)

labels = starting_corr.columns
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels, rotation=45, color=ax_color)
ax.set_yticklabels(labels, color=ax_color)

plt.tight_layout()

def init():
    return [im]+[title]

def update(i):
    date=dates[i]
    corr_matrix = get_corr_matrix(df,date, 30)
    im.set_data(corr_matrix.values)
    title.set_text(date.strftime("%m-%Y"))
    return [im]+[title]

writer = FFMpegWriter(
    fps=20,
    metadata=dict(artist="you"),
    bitrate=1800,
)

print("Saving animation ...")

ani = FuncAnimation(fig, update, frames=len(df.index.tolist())//jump_size, init_func=init,
                    interval=100, blit=False, repeat=False)

ani.save(
    f"../../output/animations/time_correlation_{file_ending}.mp4",
    writer=writer)


plt.show()
