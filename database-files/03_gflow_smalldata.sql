USE `global-GoalFlow`;
SET FOREIGN_KEY_CHECKS = 0;


-- 1) USERS
INSERT INTO users (id, firstName, middleName, lastName, phoneNumber, email, role, planType, manages)
VALUES
 (1, 'Alice', 'B.',  'Cooper',   '555-0101', 'alice@example.com',  'admin',    'premium', NULL),
 (2, 'Bob',   NULL,  'Dylan',    '555-0202', 'bob@example.com',    'manager',  'standard', 1),
 (3, 'Cara',  'M.',  'Evanston', '555-0303', 'cara@example.com',   'user',     'free',     2),
 (4, 'Dan',   NULL,  'Fisher',   '555-0404', 'dan@example.com',    'user',     'free',     2),
 (5, 'Eve',   'L.',  'Garcia',   '555-0505', 'eve@example.com',    'user',     'standard', 1);


-- 2) TAGS
INSERT INTO tags (id, name, color)
VALUES
 (1, 'Urgent',    '#ff0000'),
 (2, 'Feature',   '#00ff00'),
 (3, 'Bug',       '#0000ff'),
 (4, 'Research',  '#ffff00'),
 (5, 'Personal',  '#ff00ff');


-- 3) POSTS
INSERT INTO posts (id, authorId, title, metaTitle, createdAt, updatedAt, publishedAt, slug, content, tag)
VALUES
 (1, 1, 'Welcome to GoalFlow', 'Intro to GoalFlow', '2025-07-01 09:00:00', '2025-07-01 10:00:00', '2025-07-01 10:00:00', 'welcome-to-goalflow', 'This is our first post!', 2),
 (2, 2, 'New Feature: Tags',   'Using tags',       '2025-07-05 14:30:00', NULL,                 NULL,                 'feature-tags',         'Tags help you organize.',     2),
 (3, 3, 'Bug Report Workflow',  NULL,                '2025-07-10 11:15:00', '2025-07-12 08:45:00','2025-07-12 08:45:00','bug-report-workflow',  'How to report bugs.',         3),
 (4, 4, 'Daily Tasks Tips',     NULL,                '2025-07-15 16:00:00', NULL,                 NULL,                 'daily-tasks-tips',     'Stay on track every day.',    4);


-- 4) POST_REPLY
INSERT INTO post_reply (id, userId, postId, title, createdAt, publishedAt, content, tag)
VALUES
 (1,  3, 1, 'Thanks Alice!', '2025-07-01 11:00:00', '2025-07-01 11:00:00', 'Great intro!',       5),
 (2,  4, 1, 'Excited!',      '2025-07-01 11:10:00', NULL,                 'Can’t wait to use it.', 1),
 (3,  5, 2, 'Question',      '2025-07-06 09:20:00', '2025-07-06 09:20:00', 'How do tags work?',  4),
 (4,  1, 3, 'Re: Bug Workflow','2025-07-12 09:00:00','2025-07-12 09:00:00','Nice guide.',         3),
 (5,  3, 4, 'Tip',           '2025-07-15 17:00:00', NULL,                 'I schedule mine nightly.', 4),
 (6,  2, 4, 'Thanks Cara',   '2025-07-15 17:30:00', '2025-07-15 17:30:00','Good tip!',           5);


-- 5) CONSISTENT_TASKS
INSERT INTO consistent_tasks (id, userId, title, metaTitle, slug, category, notes)
VALUES
 (1, 1, 'Daily stand-up',   'Stand-up meeting','daily-standup',   'Meetings', '15-minute team check-in.'),
 (2, 3, 'Backup database',  NULL,             'backup-database',  'Maintenance','Backup at 2 AM daily.'),
 (3, 5, 'Review roadmap',   NULL,             'review-roadmap',   'Planning', 'Monthly goals review.');


-- 6) DAILY_TASKS
INSERT INTO daily_tasks (id, userId, tagId, title, metaTitle, slug, status, completed, schedule, notes)
VALUES
 (1, 2, 1, 'Fix critical bug',      NULL, 'fix-critical-bug',      0, 0, '2025-08-06', 'Assigned by QA'),
 (2, 3, 5, 'Meditate',              NULL, 'meditate',              0, 1, '2025-08-05', '10 minutes'),
 (3, 4, 2, 'Write specs',           NULL, 'write-specs',           1, 1, '2025-08-05', 'Draft v1'),
 (4, 5, 4, 'Literature review',     NULL, 'literature-review',     0, 0, '2025-08-07', 'Collect papers'),
 (5, 1, 3, 'Verify bug fix',        NULL, 'verify-bug-fix',        0, 0, '2025-08-06', 'Test in staging');


-- 7) GOALS
INSERT INTO goals (id, userId, tagId, title, notes, onIce, status, priority, createdAt, completedAt, completed, schedule)
VALUES
 (1, 1, 2, 'Implement tagging',    'Allow custom tags',     0, 'ACTIVE', 1, '2025-06-20 12:00:00', NULL, 0, '2025-08-01'),
 (2, 2, 3, 'Stabilize releases',    'Reduce hot-fixes',      0, 'ACTIVE', 2, '2025-05-15 08:30:00', NULL, 0, '2025-09-01'),
 (3, 3, 4, 'Publish whitepaper',    NULL,                    1, 'ON ICE', 3, '2025-07-01 10:00:00', NULL, 0, NULL),
 (4, 5, 5, 'Personal blog',         'Write first post',      0, 'ACTIVE', 4, '2025-07-10 15:45:00', NULL, 0, '2025-08-10');


-- 8) SUBGOALS
INSERT INTO subgoals (id, goalsId, title, notes, status, createdAt, completedAt, completed, schedule)
VALUES
 (1, 1, 'DB schema for tags',     'Add color field', 'ACTIVE', '2025-06-21 09:00:00', NULL, 0, '2025-06-25'),
 (2, 1, 'UI for tag selector',    NULL,             'ON ICE', '2025-06-26 14:00:00', NULL, 0, NULL),
 (3, 2, 'Automate tests',         NULL,             'ACTIVE', '2025-05-16 11:00:00', '2025-07-01 17:00:00', 1, '2025-06-30'),
 (4, 4, 'Draft first post',       NULL,             'ACTIVE', '2025-07-11 10:00:00', NULL, 0, '2025-07-15');


-- 9) BUG_REPORTS
INSERT INTO bug_reports (id, userId, title, metaTitle, slug, description, dateReported, status, priority)
VALUES
 (1, 3, 'Login fails',        NULL,      'login-fails',        'Cannot login with valid creds',   '2025-07-20 13:00:00', 0, 1),
 (2, 4, 'UI glitch on mobile',NULL,      'ui-glitch-mobile',   'Buttons overlap on small screens','2025-07-22 09:15:00', 0, 2),
 (3, 5, 'Slow report gen',    NULL,      'slow-report-gen',    'Dashboard reports take >30s',      '2025-07-25 16:40:00', 0, 3);


-- 10) USER_DATA
INSERT INTO user_data (id, userId, location, totalTime, deviceType, age, registeredAt, lastLogin, isActive, postCount)
VALUES
 (1, 1, 'New York, NY',    1200, 'desktop', 29, '2025-01-05 08:00:00', '2025-08-04 18:30:00', 1, 2),
 (2, 2, 'Chicago, IL',     800,  'mobile',  35, '2025-02-10 12:15:00', '2025-08-02 20:45:00', 1, 2),
 (3, 3, 'Seattle, WA',     600,  'desktop', 27, '2025-03-15 14:20:00', '2025-08-03 09:10:00', 1, 3),
 (4, 4, 'Austin, TX',      450,  'tablet',  31, '2025-04-01 10:05:00', '2025-08-01 11:00:00', 1, 1),
 (5, 5, 'Boston, MA',      300,  'mobile',  22, '2025-05-20 16:45:00', '2025-07-30 17:25:00', 1, 1);


SET FOREIGN_KEY_CHECKS = 1;