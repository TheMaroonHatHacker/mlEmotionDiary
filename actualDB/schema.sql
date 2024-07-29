CREATE DATABASE userdata;
USE userdata;

CREATE TABLE `credentials` (
  `username` varchar(36) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`)
);
CREATE TABLE `emotions` (
  `emotionID` int NOT NULL,
  `emotionType` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`emotionID`)
);
CREATE TABLE `entries` (
  `entryID` int NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `text` text,
  `timeanddate` datetime DEFAULT NULL,
  PRIMARY KEY (`entryID`),
  KEY `username` (`username`),
  FOREIGN KEY (`username`) REFERENCES `credentials` (`username`)
);
CREATE TABLE `emotionEntries` (
  `entryID` int NOT NULL,
  `emotionID` int NOT NULL,
  `intensity` int DEFAULT NULL,
  PRIMARY KEY (`entryID`,`emotionID`),
  KEY `emotionID` (`emotionID`),
  FOREIGN KEY (`entryID`) REFERENCES `entries` (`entryID`),
  FOREIGN KEY (`emotionID`) REFERENCES `emotions` (`emotionID`)
);

INSERT into emotions (emotionID, emotionType)
VALUES
  (0, 'anger'),
  (1, 'hate'),
  (2, 'worry'),
  (3, 'sadness'),
  (4, 'surprise'),
  (5, 'empty'),
  (6, 'happiness'),
  (7, 'boredom'),
  (8, 'relief'),
  (9, 'love'),
  (10, 'enthusiasm'),
  (11, 'fun'),
  (12, 'neutral')
;