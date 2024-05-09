import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
# explanations re np.where instead of df.where here https://medium.com/@kelvinsang97/python-np-where-97bdbdcf9eab
df['overweight'] = np.where(df['weight'] / ((df['height'] / 100) ** 2)>25,1,0)

# 3
df['cholesterol'] = np.where(df['cholesterol']  == 1, 0, 1)
df['gluc'] = np.where(df['gluc']  == 1, 0, 1)

#print(df)

# 4
def draw_cat_plot():
    # 5
    #melt explanation is here https://www.linkedin.com/pulse/reshaping-data-pandas-can-arslan/
    df_cat = df.melt(id_vars='cardio', value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    
    # 6
    df_cat = df.melt(id_vars='cardio', value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']).value_counts().reset_index()
    #df_cat = df_cat.value_counts().reset_index()
    
    # 7
    df_cat = df_cat.rename(columns={0: 'total'})
    
    # 8
    #check here https://www.tutorialspoint.com/seaborn/seaborn_catplot_method.htm
    #and here https://stackoverflow.com/questions/69704134/subplotting-with-catplot
    fig = sns.catplot(data=df_cat, col='cardio', x='variable', y='total', kind='bar', hue='value', order=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']).figure
    print(fig.axes[0].get_xticklabels())

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) & 
                 (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) & 
                 (df['weight'] <= df['weight'].quantile(0.975))]
    
    # 12
    
    #corr = sns.heatmap(df_heat.corr(), annot=True, fmt='.1f', square=True,)
    #corr.figure.savefig('raw_heatmap.png')
    corr = df_heat.corr()
    # 13
    # mask explanation is here https://numpy.org/doc/stable/reference/generated/numpy.triu.html
    mask = np.triu(corr)
  
    # 14
    fig= plt.subplots(figsize=(12, 12))

    # 15

    fig = sns.heatmap(corr, annot=True, fmt='.1f', square=True, mask=mask, center=0, cbar_kws={'shrink': .5}).figure

    # 16
    fig.savefig('heatmap.png')
    return fig
