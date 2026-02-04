import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dark_mode = True
institutes = {'FORSA': "Forsa", 'DIMAP': "Infratest dimap", 'FOWA':"Forsch'gr. Wahlen", 'ALLENS':"Allensberger", 'GMS':"GMS", 'INSA':"INSA", 'YOUGOV':"YouGov",'VERIAN':"Verian (Emnid)"}
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

df_averages = pd.read_csv('../../output/survey_averages/30D_survey_averages.csv', parse_dates=['date'])
df_averages.set_index('date', inplace=True)

df_umfragen = pd.read_csv("../data/umfragen_wahlrecht.csv", parse_dates=['date'])
df_umfragen.set_index('date', inplace=True)
df_umfragen.drop_duplicates(inplace=True)

# sets the graphic styles
if dark_mode:
    bg_color = "black"
    ax_color = "white"
    file_ending = "dark"
else:
    bg_color = "white"
    ax_color = "black"
    file_ending = "light"

for institute in institutes:
    fig, axes = plt.subplots(2, 3, figsize=(15, 11), facecolor=bg_color, sharex=True, sharey=True)
    axes = axes.ravel()
    df_deviations = pd.DataFrame()
    n=len(df_umfragen[df_umfragen["institute_id"] == institute])
    df_institute = df_umfragen[df_umfragen['institute_id'] == institute]
    for i,party in enumerate(parties):
        df_deviations[party] = pd.to_numeric(df_institute[party], errors='coerce')-pd.to_numeric(df_averages[party], errors='coerce')
        sns.histplot(df_deviations[party], bins=12, ax=axes[i], kde=True,edgecolor='white', linewidth=0.5, alpha=0.2)
        axes[i].set_facecolor(bg_color)
        axes[i].axvline(df_deviations[party].mean(), color='red',label="mean deviation")
        axes[i].axvline(0, color=ax_color, linestyle='dashed', linewidth=0.5)
        axes[i].set_xlabel("Deviation of the aggregated mean", color=ax_color)
        axes[i].tick_params(axis="x", colors=ax_color)
        axes[i].tick_params(axis="y", colors=ax_color)
        axes[i].set_title(party, color=ax_color)
        for spine in axes[i].spines.values():
            spine.set_color(ax_color)

    fig.suptitle(f"{institutes[institute]} (n={n})", fontsize=20, color='white')

    sns.despine()
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"../../output/survey_deviations/{institutes[institute]}_{file_ending}.svg")
    print(f"{df_deviations}")