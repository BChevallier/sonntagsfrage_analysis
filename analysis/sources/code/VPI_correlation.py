import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

reg_plot = True
dark_mode = True
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

df_VPI = pd.read_csv('../data/VPI.csv', sep=",", parse_dates=["date"], date_format="%Y-%m")
df_VPI.sort_values("date", inplace=True)
df_VPI=df_VPI[df_VPI["value_unit"]!="%"].reset_index(drop=True)
df_VPI.set_index("date", inplace=True)
df_VPI.drop(columns=["value_unit"], inplace=True)
df_VPI["value"]=df_VPI["value"].astype(float)
df_VPI.rename(columns={"value":"VPI"}, inplace=True)

df_survey = pd.read_csv("../../output/survey_averages/30D_survey_averages.csv", sep=",", parse_dates=["date"])

df_comb=df_survey.merge(df_VPI, how="inner", on="date")
df_comb.set_index("date", inplace=True)
df_corr=df_comb.corr(numeric_only=True)
df_corr_col=df_corr["VPI"].drop("VPI")
sns.heatmap(df_corr_col.to_frame(), cmap="coolwarm", square=True,)
print(df_corr_col)

fig, ax = plt.subplots(facecolor=bg_color)
for spine in ax.spines.values():
    spine.set_color(ax_color)
ax.set_facecolor(bg_color)
ax.tick_params(axis='x', colors=ax_color)
ax.tick_params(axis='y', colors=ax_color)
ax.set_title("Verlauf des VPI", color=ax_color)
ax.set_xlabel("Zeit", color=ax_color)
ax.set_ylabel("Verbraucherpreisindex", color=ax_color)
sns.lineplot(data=df_VPI, x="date", y="VPI",ax=ax)
sns.despine()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(f"../../output/line_plots/VPI_Verlauf_{file_ending}.svg")

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
        ax.set_title(f"{party} vs VPI (r={round(df_corr.loc[party, "VPI"], 2)})", color=ax_color)
        sns.despine(ax=ax)
        sns.regplot(
            data=df_comb,
            x=party,
            y="VPI",
            scatter_kws={'color': scatter_color, 'alpha': 0.7, 'label': party, "s": 10},
            line_kws={'color': "red", 'alpha': 0.6, "linewidth": 2},
            ax=ax
        )
        ax.set_xlabel("Umfragewerte", color=ax_color)
        ax.set_ylabel("Verbraucherpreisindex", color=ax_color)
        fig.savefig(f"../../output/correlations/{party.replace("/", "_")}_vs_VPI_{file_ending}.svg")
plt.show()

