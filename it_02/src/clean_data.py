import csv
import re

def cleanData():
    tweetID, hashCount, ahshWritten = 0, 0, 0;
    hashtags = []

    #Open files for read/write
    rawData=open('../data/tweets_raw.csv', 'rt')
    hashtagCSV=open('../data/hashtag.csv', 'wt')
    tweetCSV=open('../data/tweet.csv', 'wt')

    try:
        #Prepare csv read/write iterators
        reader = csv.reader(rawData, delimiter=';')
        writerHashtag = csv.writer(hashtagCSV, delimiter=';')
        writerTweet = csv.writer(tweetCSV, delimiter=';')
        #Omit the first row in the given data
        next(reader)
        #Iterate through each row of the given data
        for row in reader:
            #Extract all the relevant tweet informations
            #handle, text, time, retweet_count, favorite_count
            writerTweet.writerow((row[0], row[1], row[4], row[7], row[8]))
            #See if there're any #'s at all in the tweet
            #Count every occurence if true
            match = len(re.findall('#', row[1]))
	    if(match):
                hashCount = hashCount + match
                #Substitute whitespaces after #
	        row[1] = re.sub('# ', '#', row[1])
                #Extract every # into an temporary array
                hashtags = re.findall(r'#\w+', row[1])
                #Save the extracted #'s and their corresponding TweedID
                #Count each # that is written
                for ahsh in hashtags:
                    writerHashtag.writerow((tweetID, ahsh))
                    ahshWritten = ahshWritten +1
	    tweetID = tweetID+1
    finally:
            #Close all filedescriptors
	    rawData.close()
	    hashtagCSV.close()
	    tweetCSV.close()

    print '%s %d' % ('Occurences of #\'s in the given data: ', hashCount) 
    print '%s %s' % ('Extracted #\'s count: ', ahshWritten)
