
# coding: utf-8

# # Recommender System
# 
# We will be developing a movie recommender system based upon Collaborative-filtering to predict the name of the movie based upon the reviews of the other critics having similar taste. The systesm uses two different methods for finding similairties between the critics known as Euclidean-Distance-Score and Pearson-Correlation-Score. The final reault for both the methods were almost similar. After finding the similarity between critics, it uses the weighted average method to assign higher weight to the peer interest critics. Finally, It normalizes the score by deviding it by the similarities of the critics who reviewed that movie.
# 
# 
# ## Finding Similar DataPoint
# 
# Two ways for calculating similarity scores

# 1. **Euclidean Distance Score** : 1/(1+sqrt of sum of squares between two points)

# In[1]:

from math import sqrt


# In[2]:

# recommendation.py
# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
           }


# In[3]:

# Function for calculating  Euclidean distance between two critics
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in si])

    return 1 / (1 + sum_of_squares)

# Calling the function
sim_distance(critics,'Lisa Rose','Gene Seymour')


# * **Pearson Correlation Score** : Correlation between sets of data is a measure of how well they are related. It shows the linear relationship between two sets of data. In simple terms, it answers the question, Can I draw a line graph to represent the data?
# 
# * Value varies between -1 to 1. 0-> Not related, -1 -> perfect negatively corelated, 1-> perfect positively corelated 
# 
# Slightly better than Euclidean because it addresses the the situation where the data isn't normalised. Like a User is giving high movie ratings in comparison to AVERAGE user.

# In[4]:

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
            # Find the number of elements
    n=len(si)
            
    # if they are no ratings in common, return 0
    if n==0: return 0
    
    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r

sim_pearson(critics,'Lisa Rose','Gene Seymour')


# Getting Top matches for a particular person based on any of the equality scores described above.

# In[5]:

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
    # Sort the list so the highest scores appear at the top
    scores.sort( )
    scores.reverse( )
    return scores[0:n]


# In[6]:

# Exapmple
topMatches(critics,'Toby',n=3)


# ### Getting Recommendation

# In[7]:

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommnedation(prefs, person, similarity=sim_pearson):
    totals= {}
    simSums= {}
    for other in prefs:
        # Dont compare to self
        if other==person: continue
        
        sim=similarity(prefs,person,other)
        
        # Ignores Score of Zero or Negatie correlation         
        if sim<=0: continue
        
        # Only score movies that person havnt seen
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity* rating
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #sum of user similarities that have rated the movie
                simSums.setdefault(item,0)
                simSums[item]+=sim
        # Creating Normalized List
        ranking=[(total/simSums[item],item) for item,total in totals.items()]
        
        # return the sorted List
        ranking.sort()
        ranking.reverse()
        return ranking


# In[8]:

# Example Recoomendation
getRecommnedation(critics,'Toby')

