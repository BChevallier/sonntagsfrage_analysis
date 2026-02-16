import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

dark_mode = False
reg_plot = False
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

if dark_mode:
    bg_color = "black"
    ax_color = "white"
    file_ending = "dark"
    parties["CDU/CSU"] = "white"
else:
    bg_color = "white"
    ax_color = "black"
    file_ending = "light"

df_BIP=pd.read_csv("../data/BIP.csv", sep=";", parse_dates=["time"], date_format="%Y")
df_BIP=df_BIP[df_BIP["value_variable_label"] == "Bruttoinlandsprodukt"]
df_BIP=df_BIP[["time","value"]]
df_BIP=df_BIP.sort_values(by="time", ascending=True)
df_BIP.set_index("time", inplace=True)
df_BIP["BIP"]=df_BIP["value"].str.replace(",",".").astype(float)
df_BIP.drop(columns=["value"], inplace=True)

df_surveys = pd.read_csv("../../output/survey_averages/30D_survey_averages.csv", parse_dates=["date"])
df_surveys.set_index("date", inplace=True)

df_comb=pd.concat([df_surveys,df_BIP], axis=1)
df_comb.dropna(subset=["BIP"],inplace=True, axis=0)

df_corr = df_comb.corr(numeric_only=True)
print(df_corr.iloc[-1])

fig, ax = plt.subplots(facecolor=bg_color)
for spine in ax.spines.values():
    spine.set_color(ax_color)
ax.set_facecolor(bg_color)
ax.tick_params(axis='x', colors=ax_color)
ax.tick_params(axis='y', colors=ax_color)
ax.set_title("Verlauf des BIP", color=ax_color)
ax.set_xlabel("Zeit", color=ax_color)
ax.set_ylabel("Bruttoinlandsprodukt", color=ax_color)
sns.lineplot(data=df_BIP, x="time", y="BIP",ax=ax, color="blue")
sns.despine()
plt.xticks(rotation=45)
plt.tight_layout()

sns.lineplot(data=df_BIP, x=df_BIP.index, y="BIP")
plt.savefig(f"../../output/line_plots/BIP_Verlauf_{file_ending}.svg")

if reg_plot:
    for party in parties:
        # Use a darker color for the regression line
        scatter_color = parties[party]
        try:
            rgb = mcolors.to_rgb(scatter_color)
            line_color = tuple([c * 0.6 for c in rgb])  # darken by 40%
        except ValueError:
            line_color = "orange"  # fallback
        fig, ax = plt.subplots(facecolor=bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(axis='x', colors=ax_color)
        ax.tick_params(axis='y', colors=ax_color)
        for spine in ax.spines.values():
            spine.set_color(ax_color)
        ax.set_title(f"{party} vs BIP (r={round(df_corr.loc[party, "BIP"], 2)})", color=ax_color)
        sns.despine(ax=ax)
        sns.regplot(
            data=df_comb,
            x=party,
            y="BIP",
            scatter_kws={'color': scatter_color, 'alpha': 0.7, 'label': party, "s": 10},
            line_kws={'color': "red", 'alpha': 0.6, "linewidth": 2},
            ax=ax
        )
        ax.set_xlabel("Umfragewerte", color=ax_color)
        ax.set_ylabel("Bruttoinlandsprodukt", color=ax_color)
        fig.savefig(f"../../output/correlations/{party.replace("/", "_")}_vs_BIP_{file_ending}.svg")
plt.show()



