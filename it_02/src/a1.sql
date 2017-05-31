CREATE TABLE tweet (tweet_id serial primary key, handle varchar(20) NOT NULL, body varchar(200) NOT NULL, time timestamp NOT NULL, retweet_count int, favorite_count int);

CREATE TABLE hashtag(hash_id serial primary key, tweet_id int, text varchar(100) NOT NULL);
CREATE TABLE


