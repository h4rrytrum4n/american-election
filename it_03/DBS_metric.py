import psycopg2
import pandas as pd 
import numpy as np 

# pandas nice display 
pd.options.display.max_columns
pd.set_option('display.max_columns', 200)
pd.options.display.width = 200
pd.set_option("display.max_columns",8)


#####################  DATA  TO pandas #######################################
# connection to postgres 
conn = psycopg2.connect(host="localhost",database="election", user='remi', password='remitoudic', port=5432 )
cur = conn.cursor()
cur.execute('SELECT * FROM tweet')
data= cur.fetchall()

# Extract the column names
col_names=[]
[col_names.append(elt[0]) for elt in cur.description ]
conn.close()

# export to pandas
datax= pd.DataFrame( data, columns=col_names)

###############################################################################
#                           Data Processing 
##############################################################################
#  make a big bags of words 
# idee : projection on a tweet body on a line
##############################################################################
list_big_bag= datax.body.tolist()
BAG= list_big_bag[0]
for i in range(1,10): 
    BAG= BAG+ list_big_bag[i]

BAG_words=BAG.split()
len(BAG_words)  
BAG_words=pd.Series(BAG_words)
len(BAG_words)
BAG_words=BAG_words.drop_duplicates(keep='first')
len(BAG_words)


# intersection  tweet/ bag of word 
def Tweet_bagOfWords(tweet_id):
    T=datax.loc[tweet_id,'body']
    T=T.split() 
    T=pd.Series(T)
    inter_= len(pd.Series(list(set(BAG_words).intersection(set(T)))))
    return  inter_


datax['Tweet_bagOfWords']=0 
for i in range(0,datax.shape[0]): 
    datax.loc[i,'Tweet_bagOfWords']=Tweet_bagOfWords(i)      
   
    
 # handle Categories
###############################################################################
handle_categories= datax.handle
handle_categories.drop_duplicates(keep='first', inplace=True)

datax['handle_categories']=0
     
for i in range(0,datax.shape[0]): 
    if datax.loc[i,'handle']==handle_categories[0] : 
        datax.loc[i,'handle_categories']=0 #HillaryClinton
    else:
        datax.loc[i,'handle_categories']=1 #realDonaldTrump

###############################################################################
################################  METRIC   ####################################
                 
                    # 1) jacard index function

def JakI(T1,T2): 
    # input = Body von tweet ex: t1= datax.loc[1,'body']
    # output= Jacard Index
    if (T1==1 and T2 ==1)or (T1==0 and T2 ==0) : 
        result = 1 
    elif (T1==0 and T2 ==1)or (T1==1 and T2 ==0): 
        result = 0
    else:   
    # split to have vector of words
        v1=T1.split()  
        v2=T2.split()
        
        # intersection
        inter= len(pd.Series(list(set(v1).intersection(set(v2)))))
        union= len(set(v1+v2))
        result = inter/union
    return result

'''
# test 
t1= datax.loc[1,'body']
for i in range(0,50): 
   print(JakI(t1,datax.loc[i,'body']))
'''


                    # 2)  Time Metric
         
def T_Dist(T1,T2):
    # input T1 : pandas.tslib.Timestamp
    # different ralative to period 
    
    t1= T1.timestamp() # to unix time
    t2=T2.timestamp()  
    time_dist= np.sqrt(abs(t1-t2))    # time difference
    return time_dist/1000

'''
# test 
T1=datax.loc[1,'time']  
for i in range(0,100): 
   T_Dist(datax.loc[1,'time'],datax.loc[i,'time'])
'''   
   
   
                 #  2)  Retweet Count
    
def RT_count(T1,T2): 
    diff= T1-T2
    dist_retweeet=diff
    return np.sqrt(abs(dist_retweeet))
'''
# test 
T1=datax.loc[1,'retweet_count']
for i in range(0,100): 
   RT_count(datax.loc[1,'retweet_count'],datax.loc[i,'retweet_count'])
'''

#                   2)  Distance Bag of words 
def D_BoW(T1,T2): 
    D_body=np.sqrt( abs(T1-T2))
    return D_body

'''
# test 
T1=datax.loc[1,'Tweet_bagOfWords']
T2=datax.loc[2,'Tweet_bagOfWords']
D_BoW(T1,T2)
for i in range(0,10): 
   D_BoW(datax.loc[1,'Tweet_bagOfWords'],datax.loc[i,'Tweet_bagOfWords'])
'''


############################################################################### 
               #  global function 
###############################################################################

#distance for between 2 tweets


def dbs_metric(Tweet_id1,Tweet_id2,df1,df2):
    
    # dim handle
    #d1=  JakI(datax.loc[id1,'handle'],datax.loc[id2,'handle'])
    d1=  JakI(df1.loc[Tweet_id1,'handle'],df2.loc[Tweet_id2,'handle'])
    #test  JakI(datax.loc[2,'handle'],datax.loc[5,'handle'])
    
    # dim body 
    d2=  D_BoW(df1.loc[Tweet_id1,'Tweet_bagOfWords'],df2.loc[Tweet_id2,'Tweet_bagOfWords'])
    #test D_BoW(datax.loc[7,'Tweet_bagOfWords'],datax.loc[788,'Tweet_bagOfWords'])
    
    # dim time 
    d3=T_Dist(df1.loc[Tweet_id1,'time'],df2.loc[Tweet_id2,'time'])
    # test T_Dist(datax.loc[7,'time'],datax.loc[788,'time'])
    
    # dim Retweet
    d4=RT_count(df1.loc[Tweet_id1,'retweet_count'],df2.loc[Tweet_id2,'retweet_count'])
    
    M=[d1,d2,d3,d4]
    Tweet_distance= np.sqrt( M[0]**2 + M[1]**2 + M[2]**2+ M[3]**2)

    return Tweet_distance

#dbs_metric(4,200,datax,datax)
#dbs_metric(4,1,datax,cluster_init)

'''
import DBS_metric as DBS 

#################################################################################
# Visualisierung
###############################################################################

#time vs Tweet_bagOfWords
from bokeh.plotting import figure, show, output_file

#data=datax["time"]
p = figure(title = "test",x_axis_type="datetime")
p.xaxis.axis_label = 'time'
p.yaxis.axis_label = 'Tweet_intersect_BagOfWords'

p.circle(DBS.datax["time"], DBS.datax["Tweet_bagOfWords"], line_color="gray",fill_alpha=0.2, size=2,)

output_file("times_vs_Tweet_bagOfWords.html", title='times vs Tweet_bagOfWords')

show(p)


'''
