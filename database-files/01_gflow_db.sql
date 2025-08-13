-- Drops the old, and recreates the database. Then use it.
DROP DATABASE IF EXISTS `global-GoalFlow`;
CREATE DATABASE `global-GoalFlow`;
USE `global-GoalFlow`;





-- USERS TABLE
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
firstName       VARCHAR(50)                                 NOT NULL,
middleName      VARCHAR(50),
lastName        VARCHAR(50)                                 NOT NULL,
phoneNumber     VARCHAR(15),
email           VARCHAR(75)                                 NOT NULL,
role            ENUM('user', 'manager', 'admin')            NOT NULL,
planType        ENUM('free', 'standard', 'enterprise')      NOT NULL DEFAULT 'free',
manages         INT,
id              INT                                         AUTO_INCREMENT NOT NULL,   -- DIF. NAME

PRIMARY KEY (id),

UNIQUE INDEX uq_idx_phoneNumber (phoneNumber),
UNIQUE INDEX uq_idx_email (email),
INDEX idx_manages (manages),
INDEX idx_role (role),

FOREIGN KEY (manages) REFERENCES users(id)
 ON DELETE SET NULL
 ON UPDATE CASCADE
);





-- TAGS TABLE
DROP TABLE IF EXISTS tags;
CREATE TABLE IF NOT EXISTS tags (
name            VARCHAR(50),
color           VARCHAR(7)          NOT NULL DEFAULT '#ffffff',
id              INT                 AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_name (name)
);





-- POSTS TABLE
DROP TABLE IF EXISTS posts;
CREATE TABLE IF NOT EXISTS posts (
authorId        INT                 NOT NULL,   -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(75)         NOT NULL,
metaTitle       VARCHAR(100),                   -- EXTRA ATTRIBUTE
createdAt       DATETIME            NOT NULL,
updatedAt       DATETIME,                       -- EXTRA ATTRIBUTE
publishedAt     DATETIME,                       -- EXTRA ATTRIBUTE
content         TEXT,
id              INT                 AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_authorId (authorId),

FOREIGN KEY (authorId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);





-- POSTS_TAGS   -  (BRIDGE TABLE) 
DROP TABLE IF EXISTS posts_tags;
CREATE TABLE posts_tags (
post_id       INT         NOT NULL,
tag_id        INT         NOT NULL,

PRIMARY KEY (post_id, tag_id),

INDEX idx_posts_tags_post (post_id),
INDEX idx_posts_tags_tag  (tag_id),

FOREIGN KEY (post_id) REFERENCES posts(id) 
 ON DELETE CASCADE 
 ON UPDATE CASCADE,

FOREIGN KEY (tag_id)  REFERENCES tags(id)  
 ON DELETE CASCADE 
 ON UPDATE CASCADE
);





-- POST_REPLY TABLE
DROP TABLE IF EXISTS post_reply;
CREATE TABLE IF NOT EXISTS post_reply (
userId          INT                 NOT NULL,   -- NEEDED EXTRA ATTRIBUTE
postId          INT                 NOT NULL,   -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(100)        NOT NULL,
createdAt       DATETIME            NOT NULL,
publishedAt     DATETIME,                       -- EXTRA ATTRIBUTE
content         TEXT,
id              INT                 AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX index_userId (userId),
INDEX index_postId (postId),

FOREIGN KEY (userId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE,

FOREIGN KEY (postId) REFERENCES posts(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);




-- POST_REPLY_TAGS   -  (BRIDGE TABLE) 
DROP TABLE IF EXISTS post_reply_tags;
CREATE TABLE post_reply_tags (
post_reply_id   INT     NOT NULL,
tag_id          INT     NOT NULL,

PRIMARY KEY (post_reply_id, tag_id),

INDEX idx_post_reply_tags_pr (post_reply_id),
INDEX idx_post_reply_tags_tag (tag_id),

FOREIGN KEY (post_reply_id) REFERENCES post_reply(id) 
 ON DELETE CASCADE 
 ON UPDATE CASCADE,

FOREIGN KEY (tag_id) REFERENCES tags(id)
 ON DELETE CASCADE 
 ON UPDATE CASCADE
);





-- USER_DATA TABLE
DROP TABLE IF EXISTS user_data;
CREATE TABLE IF NOT EXISTS user_data (
userId          INT                                     NOT NULL,                     -- NEEDED EXTRA ATTRIBUTE
location        VARCHAR(100),                                                         -- city name, state.?
deviceType      ENUM('mobile', 'tablet', 'desktop')     NOT NULL,
age             TINYINT                                 UNSIGNED,
registeredAt    VARCHAR(100)                            NOT NULL,
lastLogin       DATETIME,                                                             -- EXTRA ATTRIBUTE
isActive        TINYINT(1)                              NOT NULL DEFAULT 1,           -- EXTRA ATTRIBUTE
id              INT                                     AUTO_INCREMENT NOT NULL,      -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_userId (userId),
INDEX idx_deviceType (deviceType),
INDEX idx_lastLogin (lastLogin),

FOREIGN KEY (userId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);





-- BUG_REPORTS TABLE
DROP TABLE IF EXISTS bug_reports;
CREATE TABLE IF NOT EXISTS bug_reports (
userId          INT                                             NOT NULL,   -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(75)                                     NOT NULL,
metaTitle       VARCHAR(100),                                               -- EXTRA ATTRIBUTE
description     TEXT,
dateReported    DATETIME                                        NOT NULL DEFAULT CURRENT_TIMESTAMP,
completed       TINYINT(1)                                      NOT NULL DEFAULT 0,         -- 0 = Not Completed, 1 = Completed
priority        ENUM('critical', 'high', 'medium', 'low')       NOT NULL DEFAULT 'low',     -- where 1 = critical, 2 = high, 3 = medium, 4 = low
id              INT                                             AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_copmleted (completed),
INDEX idx_priority (priority),
INDEX idx_dateReported (dateReported),

FOREIGN KEY (userId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);





-- CONSISTENT_TASKS TABLE
DROP TABLE IF EXISTS consistent_tasks;
CREATE TABLE IF NOT EXISTS consistent_tasks (
userId          INT                 NOT NULL,   -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(75)         NOT NULL,
metaTitle       VARCHAR(100),                   -- EXTRA ATTRIBUTE
category        VARCHAR(100),
createdAt       DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP,
notes           TEXT,
id              INT                 AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_category (category),
INDEX idx_createdAt (createdAt),

FOREIGN KEY (userId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);





-- DAILY_TASKS TABLE
DROP TABLE IF EXISTS daily_tasks;
CREATE TABLE IF NOT EXISTS daily_tasks (
userId          INT                                         NOT NULL,   -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(75)                                 NOT NULL,
metaTitle       VARCHAR(100),                                           -- EXTRA ATTRIBUTE
status          ENUM('ON ICE', 'PLANNED', 'ACTIVE', 'ARCHIVED')       NOT NULL DEFAULT 'PLANNED', -- ON ICE, PLANNED, ACTIVE, ARCHIVED
completed       TINYINT(1)                                  NOT NULL DEFAULT 0,
schedule        DATE,
notes           TEXT,
id              INT                                         AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_userId (userId),
INDEX idx_schedule (schedule),
INDEX idx_status (status),

FOREIGN KEY (userId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);





-- DAILY_TASKS_TAGS   -  (BRIDGE TABLE) 
DROP TABLE IF EXISTS daily_tasks_tags;
CREATE TABLE daily_tasks_tags (
daily_task_id       INT         NOT NULL,
tag_id              INT         NOT NULL,

PRIMARY KEY (daily_task_id, tag_id),

INDEX idx_daily_tasks_tags_dt (daily_task_id),
INDEX idx_daily_tasks_tags_tag (tag_id),

FOREIGN KEY (daily_task_id) REFERENCES daily_tasks(id) 
 ON DELETE CASCADE 
 ON UPDATE CASCADE,

FOREIGN KEY (tag_id) REFERENCES tags(id)
 ON DELETE CASCADE 
 ON UPDATE CASCADE
);





-- GOALS TABLE
DROP TABLE IF EXISTS goals;
CREATE TABLE IF NOT EXISTS goals (
userId          INT                                         NOT NULL,                   -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(75)                                 NOT NULL,
notes           TEXT,
onIce           TINYINT(1)                                  NOT NULL DEFAULT 0,
status          ENUM('ON ICE', 'PLANNED', 'ACTIVE', 'ARCHIVED')       NOT NULL DEFAULT 'PLANNED', -- ON ICE, PLANNED, ACTIVE, ARCHIVED
priority        ENUM('critical', 'high', 'medium', 'low')   NOT NULL DEFAULT 'low',     -- where 1 = critical, 2 = high, 3 = medium, 4 = low
createdAt       DATETIME                                    NOT NULL DEFAULT CURRENT_TIMESTAMP,
completedAt     DATETIME,
completed       TINYINT(1)                                  NOT NULL DEFAULT 0,         -- EXTRA ATTRIBUTE, NOT SURE
schedule        DATE,                                           -- ADDED ?
id              INT                                         AUTO_INCREMENT NOT NULL,    -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_userId (userId),
INDEX idx_status (status),
INDEX idx_priority (priority),
INDEX idx_createdAt (createdAt),
INDEX idx_completedAt (completedAt),

FOREIGN KEY (userId) REFERENCES users(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);





-- GOALS_TAGS   -  (BRIDGE TABLE)
DROP TABLE IF EXISTS goals_tags;
CREATE TABLE goals_tags (
goal_id     INT     NOT NULL,
tag_id      INT     NOT NULL,

PRIMARY KEY (goal_id, tag_id),

INDEX idx_goals_tags_goal (goal_id),
INDEX idx_goals_tags_tag  (tag_id),

FOREIGN KEY (goal_id) REFERENCES goals(id) 
 ON DELETE CASCADE 
 ON UPDATE CASCADE,

FOREIGN KEY (tag_id)  REFERENCES tags(id)  
 ON DELETE CASCADE 
 ON UPDATE CASCADE
);





-- SUBGOALS TABLE
DROP TABLE IF EXISTS subgoals;
CREATE TABLE IF NOT EXISTS subgoals (
goalsId         INT                 NOT NULL,                           -- NEEDED EXTRA ATTRIBUTE
title           VARCHAR(75)         NOT NULL,
notes           TEXT,
status          ENUM('ON ICE', 'PLANNED', 'ACTIVE', 'ARCHIVED')       NOT NULL DEFAULT 'PLANNED', -- ON ICE, PLANNED, ACTIVE, ARCHIVED
createdAt       DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP, -- EXTRA ATTRIBUTE
completedAt     DATETIME,                                               -- EXTRA ATTRIBUTE
completed       TINYINT(1)          NOT NULL DEFAULT 0,
schedule        DATE,                                                   -- ADDED ?
id              INT                 AUTO_INCREMENT NOT NULL,            -- DIF. NAME

PRIMARY KEY (id),

INDEX idx_goalsId (goalsId),
INDEX idx_status (status),
INDEX idx_createdAt (createdAt),
INDEX idx_completedAt (completedAt),

FOREIGN KEY (goalsId) REFERENCES goals(id)
 ON UPDATE RESTRICT
 ON DELETE CASCADE
);