DROP DATABASE IF EXISTS `ALS`;
CREATE DATABASE IF NOT EXISTS `ALS` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ALS`;


CREATE TABLE user
(
    id int NOT NULL AUTO_INCREMENT,
    username varchar(40) NOT NULL,
    password varchar(102) NOT NULL,
    picture varchar(200), 
    PRIMARY KEY (id)
    
);

CREATE TABLE tweet
(
    tweet_id int NOT NULL AUTO_INCREMENT,
    tweet_text varchar(150) NOT NULL,
    author_id int NOT NULL,
    replies_to int ,
    publish_date DATE,
    PRIMARY KEY (tweet_id),
    FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (replies_to) REFERENCES tweet (tweet_id) ON DELETE CASCADE
);

CREATE TABLE likes
(
    user_id int NOT NULL,
    tweet_id int NOT NULL,
    PRIMARY KEY (user_id,tweet_id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (tweet_id) REFERENCES tweet(tweet_id) ON DELETE CASCADE
);

