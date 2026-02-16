import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#only one should be true, I know there are more elegant ways...
plot_institutes = False
plot_parliaments = True

dark_mode = True

#reads the data and gets rid of irrelevant columns
df = pd.read_csv("../data/dawum-full.csv")
df.dropna(subset=['parliament_name','institute_name'], inplace=True)
df.drop(inplace=True, columns=['survey_id','survey_start','survey_end','parliament_name','institute_name','tasker_id','tasker_name','result_familie'])

print(df["survey_persons"].std())
#creates count df for elections
election_counts_df = df["parliament_id"].value_counts()
institutes = df['institute_id'].unique().tolist()

min_surveys = 0 #required survey amount by institute
sufficient_samplesize_id=[]
#checks the sample size of every institute
for id in institutes:
    survey_size =df[df['institute_id'] == id].index.size
    if survey_size > min_surveys:
        sufficient_samplesize_id.append(id)
        print(f"{id}: has {survey_size} surveys")

#only keeps surveys of institutes with sufficient sample size and resets index
filtered_df = df[df['institute_id'].isin(sufficient_samplesize_id)].reset_index(drop=True)
institute_counts_df = filtered_df['institute_id'].value_counts()

# sets the graphic styles
if dark_mode:
    bg_color = "black"
    ax_color = "white"
    file_ending = "dark"
else:
    bg_color = "white"
    ax_color = "black"
    file_ending = "light"

fig, ax = plt.subplots(facecolor=bg_color,figsize=(9,6))
ax.set_facecolor(bg_color)
plt.yticks(color=ax_color)

if plot_institutes:
    sns.barplot(ax=ax,x=institute_counts_df.index, y=institute_counts_df.values, edgecolor=bg_color,linewidth=0.5, )
    ax.set_title(f"Umfrageanzahl pro Institut (n={institute_counts_df.sum()})",color=ax_color, fontsize=28)
    plt.xticks(rotation=45,ha='right',color=ax_color)
    plt.tight_layout()
    sns.despine()
    ax.set_xlabel("Institut",color=ax_color)
    fig.savefig(f"../../output/histograms/Umfrageanzahl_pro_Institut_{file_ending}.svg")
elif plot_parliaments:
    sns.barplot(ax=ax, x=election_counts_df.index, y=election_counts_df.values, edgecolor=bg_color, linewidth=0.5, )
    ax.set_title(f"Umfrageanzahl pro Wahl (n={election_counts_df.sum()})", color=ax_color, fontsize=28)
    plt.xticks(rotation=45, ha='right',color=ax_color)
    plt.tight_layout()
    sns.despine()
    ax.set_xlabel("Wahl",color=ax_color)
    fig.savefig(f"../../output/histograms/Umfrageanzahl_pro_Wahl_{file_ending}.svg")
else:
    print("Nothing to plot")

plt.show()
