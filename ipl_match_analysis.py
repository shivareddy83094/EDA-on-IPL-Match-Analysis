#!/usr/bin/env python
# coding: utf-8

# 1. Import Libraries

# In[3]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 2. Data Exploration

# In[4]:


# Read the dataset

ipl_df=pd.read_csv("matches.csv")


# In[5]:


ipl_df.shape


# In[6]:


ipl_df.head()


# In[7]:


ipl_df.tail()


# In[8]:


ipl_df.columns


# In[9]:


ipl_df.dtypes


# 3. Data Preprocessing

# In[10]:


ipl_df.describe()


# In[11]:


ipl_df.isnull().sum()


# In[12]:


ipl_df.isnull().sum()*100/len(ipl_df)


# In[13]:


ipl_df.drop(['umpire3'], axis=1,inplace=True)


# In[14]:


ipl_df.dropna(inplace=True)


# In[15]:


ipl_df.shape


# In[16]:


ipl_df["season"].value_counts()


# 4. Data Analysis thorugh visualization

# No of matches played per season

# In[17]:


sns.countplot(ipl_df["season"])


# No of matches at each Venue

# In[18]:


plt.figure(figsize=(12,6))
sns.countplot(x='venue', data=ipl_df)
plt.xticks(rotation='vertical')
plt.show()


# No of matches Played at each city

# In[19]:


plt.figure(figsize=(12,6))
sns.countplot(x='city', data=ipl_df)
plt.xticks(rotation='vertical')
plt.show()


# No of matches played by each team

# In[20]:


ipl_temp_df = pd.melt(ipl_df, id_vars=['id','season'], value_vars=['team1', 'team2'])
plt.figure(figsize=(12,6))
sns.countplot(x='value', data=ipl_temp_df)
plt.xticks(rotation='vertical')
plt.show()


# Number of wins per team

# In[21]:


plt.figure(figsize=(12,6))
sns.countplot(x='winner', data=ipl_df)
plt.xticks(rotation='vertical')
plt.show()


# Toss Decision

# ### what is the prefererable choice in toss,is it to field or bat?
# 
# most of the teams are chosing to field when they have won the toss i.e 57.1%.The choice of batting or fielding depends on the pitch report and also on previous stats,whether the fielding first team is winning or the batting first team is winning.
# while fielding first the bowlers will get the new ball and has the upper hand using swing and turn.so,that they can restict the target and chase down the target easily.

# In[22]:


ipl_temp_series = ipl_df.toss_decision.value_counts()
labels = (np.array(ipl_temp_series.index))
sizes = (np.array((ipl_temp_series / ipl_temp_series.sum())*100))
colors = ['violet', 'red']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Toss decision percentage")
plt.show()


# Most of the decision is to field first

# In[23]:


plt.figure(figsize=(12,6))
sns.countplot(x='season', hue='toss_decision', data=ipl_df)
plt.xticks(rotation='vertical')
plt.show()


# Maximum Toss Winners

# In[24]:


plt.subplots(figsize=(8,5))
sns.barplot(x=ipl_df.toss_winner.value_counts().values,y=ipl_df.toss_winner.value_counts().index,palette="Set1")


# In[30]:


#getting the frequencies of result column
ipl_df['result'].value_counts()


# In[32]:


#finding out the number of times each team won the toss
ipl_df['toss_winner'].value_counts()


# ### win percentage of batting first

# In[34]:


# Subsetting the matches where the team won batting first
batting_first = ipl_df[ipl_df['win_by_runs'] !=0]


# In[35]:


# Checking the first 5 rows of the batting_first dataframe
batting_first.head()


# In[36]:


plt.figure(figsize=(8,8))
plt.pie(list(batting_first['winner'].value_counts()[:8]) , labels=list(batting_first['winner'].value_counts().keys()[:8]) ,autopct="%.1f%%")
plt.tight_layout()
plt.show()


# In[37]:


# Extracting the records where the team has won after batting second
batting_second = ipl_df[ipl_df['win_by_wickets'] != 0]


# In[38]:


batting_second.head()


# ### win percentage of batting second

# In[39]:


#finding out the frequecny of winning of each team batting second
batting_second['winner'].value_counts()


# In[40]:


plt.pie(list(batting_second['winner'].value_counts()[:8]),labels = list(batting_second['winner'].value_counts().keys()[:8]) , autopct='%.1f%%')
plt.tight_layout()
plt.show()


# ### How lucky are the toss winning teams?:

# In[42]:


ipl_df['toss_winner_is_winner'] = 'no'
ipl_df['toss_winner_is_winner'].loc[ipl_df.toss_winner == ipl_df.winner] = 'yes'
temp_series = ipl_df.toss_winner_is_winner.value_counts()

labels = (np.array(temp_series.index))
sizes = (np.array((temp_series / temp_series.sum())*100))
colors = ['gold', 'lightskyblue']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Toss winner is match winner")
plt.show()


# In[43]:


#If the team wins the toss, will it end up in the winning side.
plt.figure(figsize=(12,6))
sns.countplot(x='toss_winner', hue='toss_winner_is_winner', data=ipl_df)
plt.xticks(rotation='vertical')
plt.show()


# ### No. of wins by team in each city(all the seasons):

# In[44]:


x, y = 2008, 2017
while x < y:
    wins_percity = ipl_df[ipl_df['season'] == x].groupby(['winner', 'city'])['id'].count().unstack()
    plot = wins_percity.plot(kind='bar', stacked=True, title="Team wins in different cities\nSeason "+str(x), figsize=(7, 5))
    sns.set_palette("Paired", len(ipl_df['city'].unique()))
    plot.set_xlabel("Teams")
    plot.set_ylabel("No of wins")
    plot.legend(loc='best', prop={'size':8})
    x+=1


# ### No of wins by team by each venue(all the seasons):

# In[45]:


x, y = 2008, 2017
while x < y:
    wins_pervenue = ipl_df[ipl_df['season'] == x].groupby(['winner', 'venue'])['id'].count().unstack()
    plot = wins_pervenue.plot(kind='bar', stacked=True, title="Team wins in different venues\nSeason "+str(x), figsize=(10,15))
    sns.set_palette("Paired", len(ipl_df['city'].unique()))
    plot.set_xlabel("Teams")
    plot.set_ylabel("No of wins")
    plot.legend(loc='best', prop={'size':8})
    x+=1


# ### No of matches in which DL applied Seasonwise

# In[46]:


# Seasons with D/L method applied matches
dl=ipl_df.query('dl_applied==1')['season']
dl


# In[47]:


fig, ax=plt.subplots(figsize=(8,8))
#ax.set_ylim([0,5])
ax.set_title('No. of matches where D/L method was applied, season wise\n')
sns.countplot(x=dl, data=ipl_df)
plt.xlabel('\nSeason')
plt.ylabel('No. of matches\n')
plt.show()


# ### Player of the Match

# In[49]:


plt.figure(figsize=(15,7))
player_of_match=ipl_df['player_of_match'].value_counts()[:10]
sns.barplot(player_of_match.index,
            player_of_match.values,
            palette='cividis')

plt.title("Player of the Match",fontsize=15)
plt.xlabel('Player',fontsize=12)
plt.ylabel('Count',fontsize=12)


# In[ ]:





# In[ ]:




