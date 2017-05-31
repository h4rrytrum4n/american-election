import psycopg2
import csv
import re

def importTweets():
    tweetsImported = 0;
    
    #Open and prepare the csv data for read
    tweetCSV = open('../data/tweet.csv', 'rt')
    tweetReader = csv.reader(tweetCSV, delimiter = ';')

    #Open connection to the PostgreSQL DB.
    try:
        conn = psycopg2.connect("dbname='election' user='postgres' host='localhost' password='postgres'")
        print "Connection sucessful"
    except:
        print "Connection failed"
        return

    #Create a cursor which will be used for DB programming
    cur = conn.cursor()
    #Prepare the insertion query   
    queryTweet = """INSERT INTO tweet (handle, body, time, retweet_count, favorite_count)
        VALUES (%s, %s, %s, %s, %s);"""
    #Iterate through each row in the given data
    #Prepare the values that are going to be inserted
    for entry in tweetReader:
        vals = (entry[0], repr(entry[1]), entry[2], entry[3], entry[4], )
        try:
            #Execute query and commit changes
            cur.execute(queryTweet, vals)
            conn.commit()
            tweetsImported = tweetsImported + 1
        except:
            print "Query failed!"        
    #Close the cursor and the connection
    cur.close();
    conn.close();
    print '%s %d' % ("Imported tweets: ", tweetsImported)


def importHashtags():
    hashImported = 0;
    
    #Open and prepare the data for reading
    hashCSV = open('../data/hashtag.csv', 'rt')
    hashReader = csv.reader(hashCSV, delimiter = ';')
    
    #Open connection to the PostgreSQL DB.
    try:
        conn = psycopg2.connect("dbname='election' user='postgres' host='localhost' password='postgres'")
        print "Connection sucessful"
    except:
        print "Connection failed"
        return

    #Create a cursor which will be used for DB programming
    cur = conn.cursor()
    #Prepare the insertion query   
    queryHash = """INSERT INTO hashtag (tweet_id, text) VALUES (%s, %s);"""

    #Iterate through each row of the given data
    #Prepare values that are going to be inserted
    for entry in hashReader:
        vals = (entry[0], entry[1], )
        try:
            #Execute the query and commit changes
            cur.execute(queryHash, vals)
            conn.commit()
            hashImported = hashImported + 1
        except:
            print "Query failed!"
    #Close the cursor and the connection 
    cur.close()
    conn.close()
    print '%s %d' % ("Imported hashtags: ", hashImported)


