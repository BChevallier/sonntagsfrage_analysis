import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

plot_reg=True
dark_mode = False
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


df_dax = pd.read_csv('../data/DAX_HISTORISCHE_DATEN.csv', parse_dates=["Datum"], date_format="%d.%m.%Y")
df_dax.drop(columns=["Zuletzt","Hoch","Tief","Vol.","+/- %"], inplace=True)
df_dax.rename(columns={"Eröffn.":"DAX-Wert","Datum":"date"}, inplace=True)
df_dax.set_index("date", inplace=True)

df_dax['DAX-Wert'] = (df_dax['DAX-Wert']
               .str.replace('.', '', regex=False)  # remove thousands separator
               .str.replace(',', '.', regex=False)  # comma → decimal point
               .astype(float))

df_dax.sort_index(ascending=True, inplace=True)

df_surveys = pd.read_csv("../../output/survey_averages/30D_survey_averages.csv", parse_dates=["date"])
df_surveys.set_index("date", inplace=True)

df_comb=pd.concat([df_surveys,df_dax], axis=1)
df_comb.dropna(subset=["DAX-Wert"],inplace=True, axis=0)

df_corr = df_comb.corr(numeric_only=True)
print(df_corr.iloc[-1])

fig, ax = plt.subplots(facecolor=bg_color, figsize=(9,6))
ax.set_facecolor(bg_color)
for spine in ax.spines.values():
    spine.set_color(ax_color)
ax.set_title("Verlauf des DAX", color=ax_color)
sns.despine(ax=ax)
df_dax.plot(ax=ax, legend=False)
ax.tick_params(axis='x', colors=ax_color, rotation=45)
ax.tick_params(axis='y', colors=ax_color)
ax.set_xlabel("Zeit", color=ax_color)
ax.set_ylabel("DAX-Punkte", color=ax_color,)
plt.savefig(f"../../output/line_plots/DAX_Verlauf_{file_ending}.svg")
if plot_reg:
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
        ax.set_title(f"{party} vs DAX (r={round(df_corr.loc[party,"DAX-Wert"],2)})", color=ax_color)
        sns.despine(ax=ax)
        sns.regplot(
            data=df_comb,
            x=party,
            y="DAX-Wert",
            scatter_kws={'color': scatter_color, 'alpha': 0.7, 'label': party, "s": 10},
            line_kws={'color': "red", 'alpha': 0.6, "linewidth": 2},
            ax=ax
        )
        ax.set_xlabel("Umfragewerte", color=ax_color)
        ax.set_ylabel("DAX-Punkte", color=ax_color)
        fig.savefig(f"../../output/correlations/{party.replace("/","_")}_vs_DAX_{file_ending}.svg")
        plt.show()
