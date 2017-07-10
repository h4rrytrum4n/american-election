import random
import pandas as pd 
import DBS_metric as DBS 
# Reference
# K-Means  Lloyd  ALgo 
# https://de.wikipedia.org/wiki/K-Means-Algorithmus

##############################################################################
# HELP Functions  Algo start line 130 



##############################################################################
# ########################## initialisierung ################################


# input1=   dataframe 'datax'  which all information 
# input2 =  number of clusters ( centers  . it could be done also random 
# output =  dataframe  which the ' random centers '  to stat KMeams 

def intinialiserung(df, number_of_cluster):

    number_of_cluster= 3
    num_of_tweet= DBS.datax.shape[0] 

    cluster_list=[]

    for dim in range(0,number_of_cluster):
        r_d1=DBS.datax.loc[random.randint(0,num_of_tweet),'handle']
        r_d2=DBS.datax.loc[random.randint(0,num_of_tweet),'Tweet_bagOfWords']
        r_d3=DBS.datax.loc[random.randint(0,num_of_tweet),'retweet_count']
        r_d4=DBS.datax.loc[random.randint(0,num_of_tweet),'time']
        r_d5=DBS.datax.loc[random.randint(0,num_of_tweet),'handle_categories']
        dimensions=[r_d1,r_d2,r_d3,r_d4,r_d5]
        dimensions= pd.DataFrame(dimensions)
        dimensions=dimensions.transpose()
        cluster_list.append(dimensions)
    
    cluster_init=pd.concat(cluster_list)
    names={0:'handle', 1: 'Tweet_bagOfWords',2: 'retweet_count', 3: 'time',4: 'favorite_count'}
    cluster_init = cluster_init.rename(columns=names)
    cluster_init.reset_index(drop=True, inplace=True)
    return cluster_init


############################# Zuordung  #######################################   

# 1) distance zu cluster jeder cluster 1 

# find nearest center of a tweet
# input1= Tweet_id or DF_index ( int )
# input2= cordinates of the centers - in a dataframe  with same column names 
#         as in functin initialisierung.  ex: cluster_init       
#output = dataframe with all the dimensions     
def find_cluster(Tweet_id,centers):

    number_of_cluster= centers.shape[0]
    distance_to_cluster=list()
    
    for cluster in range(0,number_of_cluster ):
        to_cluster = DBS.dbs_metric(Tweet_id,cluster,DBS.datax,centers) 
        distance_to_cluster.append(float(to_cluster))
    cluster_name=distance_to_cluster.index(min(distance_to_cluster))
    return cluster_name  # test find_cluster(3,cluster_init)

#  very uneficient .... to improve ! 
def write_label(df,centers):
    for i in range(0,df.shape[0]):
            df.loc[i,'label_cluster']= find_cluster(i,centers)
    return  df  
     
########################### Aktualisierung  ###################################

def compute_centers(data_with_label,number_of_cluster):
    # 1) GROUPBY cluster
    by_label=data_with_label.groupby( 'label_cluster' )
    group_list=list()
    for i in range(0,number_of_cluster):
        group_list.append(by_label.get_group(i))
    by_label=DBS.datax.groupby( 'label_cluster')
    
    # 2) Group in List 
    group_list=list()
    for i in range(0,number_of_cluster):
        group_list.append(by_label.get_group(i))
        
    # HANDLE MEANS  - FOR EACH GROUP 
    #sum the ones / the lenght of the vector
    handle_means=[group_list[i]['handle_categories'].sum(axis=0)/by_label.size()[i] for i in range(0,number_of_cluster)]
    # get a vector of 3 means 
    #assign a value to the sums , if more  than 0,5 => 1
    handle_means_cat=list()
    for i in range(0,number_of_cluster):
        if handle_means[i]>0.5: 
            handle_means_cat.append(0) 
        else: 
             handle_means_cat.append(1)   
             
             
    # BoW FOR EACH GROUP 
    BoW_meam=[group_list[i]['Tweet_bagOfWords'].sum(axis=0)/by_label.size()[i] for i in range(0,number_of_cluster)] 
    BoW__meam= [BoW_meam[i] for i in range (0,number_of_cluster) ]       
    '''        
    # DATUM MEAN FOR EACH GROUP     
    TIME=group_list[i]['time']
    TIME.reset_index(drop=True, inplace=True)
    time_list=[]
    for i in range (0,TIME.shape[0]):
        time_list.append(TIME[i].timestamp())
    
    Datum_meam=[sum(time_list)/len for i in range(0,number_of_cluster)]              
    ''' 
    # retwwet  
    retwwet_meam=[group_list[i]['retweet_count'].sum(axis=0)/by_label.size()[i] for i in range(0,number_of_cluster)] 
    retwwet_meam= [round(retwwet_meam[i]) for i in range (0,number_of_cluster) ]      
       
     # all toghther in a df 
    updated_center= pd.DataFrame([BoW__meam,retwwet_meam,handle_means_cat]).transpose()
    names={0:'Tweet_bagOfWords', 1: 'retweet_count',2: 'handle'}
    updated_center = updated_center.rename(columns=names)
    
    #  cleaning dirty stuffs  
    for i in range(0, number_of_cluster):
        if updated_center.handle[i]==0: updated_center.handle[i]='realDonaldTrump'
        else: updated_center.handle[i]='HillaryClinton'
    
    return updated_center

#%%
###############################################################################
#                                   K_MEANS  ALGO 
#
###############################################################################
number_of_cluster=3
cluster_init= intinialiserung(DBS.datax,3)

#DBS.datax.drop('body',inplace=True, axis=1) 
listOfCenters=list()    
for i in range(0,20): 
    # first round
    if i== 0:
        labelled_data=write_label(DBS.datax,cluster_init)
        new_centers= compute_centers(labelled_data,number_of_cluster) 
        new_centers=  pd.concat([new_centers, cluster_init.time], axis=1)
        listOfCenters.append(new_centers)
     # round n>1    
    else:
        labelled_data= write_label(DBS.datax,new_centers)  
        new_centers=   compute_centers(labelled_data,number_of_cluster)
        new_centers=  pd.concat([new_centers, cluster_init.time], axis=1)
        listOfCenters.append(new_centers)
        
    

listOfCenters=listOfCenters
results=pd.DataFrame(listOfCenters)
results.to_json('results5.js')
results.to_csv('results5.csv')
#results.to_excel('results')
print('done ') 
