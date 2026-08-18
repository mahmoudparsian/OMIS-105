-- ============================================================================
--  OMIS 105 -- Sailors & Boats
--  File   : database/sql/02_data.sql
--  Purpose: Populate the database.
--
--  This file implements the POPULATION REQUIREMENTS. 
--
--  Like every other rule in this project, they are DEFINED 
--  in one place only -- the REQUIREMENTS block at the top of 
--  database/sql/01_schema.sql -- and referred to here by label:
--
--      P1  initial data from sailors_and_boats_SQL_Tutorial.pdf  -> Section A
--      P2  boats which are never reserved                        -> Section B1
--      P3  sailors who have never reserved any boat              -> Section B2
--
--  IMPORTANT: no reservations are added for the new sailors, and of the
--  tutorial's ten reserves rows only one date is changed (see P1 note below).
--  That way every worked answer in the PDF (e.g. Ex7's "22 31 64 74") still
--  reproduces exactly against this database, while the never-reserving sailors
--  and never-reserved boats give the OUTER JOIN / NOT EXISTS queries something
--  real to find.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- SECTION A -- data from the tutorial PDF                              [P1]
-- ---------------------------------------------------------------------------

-- Sailors, Figure 1. Note sid 64 and sid 74 are 
-- two *different* sailors who share the name 
-- 'Horatio' -- names are not keys.
--
INSERT INTO sailors (sid, sname, rating, age) VALUES
    (22, 'Dustin',   7, 45.0),
    (29, 'Brutus',   1, 33.0),
    (31, 'Lubber',   8, 55.5),
    (32, 'Andy',     8, 25.5),
    (58, 'Rusty',   10, 35.0),
    (64, 'Horatio',  7, 35.0),
    (71, 'Zorba',   10, 16.0),
    (74, 'Horatio',  9, 40.0),
    (85, 'Art',      3, 25.5),
    (95, 'Bob',      3, 63.5);

-- Tutorial p.7: the unrated sailor that makes 
-- COUNT(*) <> COUNT(rating).
-- Dan also never reserves a boat, so he doubles 
-- as a LEFT OUTER JOIN example.
--
INSERT INTO sailors (sid, sname, rating, age) VALUES
    (99, 'Dan',   NULL, 48.0);

-- Boats, Figure 1. 101 and 102 are both 
-- 'Interlake' -- two hulls, same model.
--
INSERT INTO boats (bid, bname, color) VALUES
    (101, 'Interlake', 'blue'),
    (102, 'Interlake', 'red'),
    (103, 'Clipper',   'green'),
    (104, 'Marine',    'red');

-- Reserves, Figure 1 -- 10 rows, dates normalized to YYYY-MM-DD.
-- Every (bid, day) pair below is distinct, so the data satisfies the
-- PRIMARY KEY (bid, day) rule as-is.
--
-- ONE DELIBERATE DEPARTURE FROM THE PDF. 
-- Figure 1 gives Dustin (22) both boat 101 AND boat 102 
-- on 1998-10-10, which R10 forbids -- so the tutorial's 
-- own sample data would not load under our schema. Boat 102 
-- is moved back to 1998-10-09 rather than dropped, which keeps 
-- all 10 rows, keeps every (sailor, boat) pairing, and keeps 
-- every sailor's reservation count -- so the PDF's worked 
-- answers still reproduce. Only queries that group by the  
-- exact day differ, and only for this one row.
--
INSERT INTO reserves (sid, bid, day) VALUES
    (22, 101, DATE '1998-10-10'),
    (22, 102, DATE '1998-10-09'),   -- PDF says 1998-10-10; moved for R10
    (22, 103, DATE '1998-10-08'),
    (22, 104, DATE '1998-10-07'),
    (31, 102, DATE '1998-11-10'),
    (31, 103, DATE '1998-11-06'),
    (31, 104, DATE '1998-11-12'),
    (64, 101, DATE '1998-09-05'),
    (64, 102, DATE '1998-09-08'),
    (74, 103, DATE '1998-09-08');


-- ---------------------------------------------------------------------------
-- SECTION B -- extra rows required by the assignment
-- ---------------------------------------------------------------------------

-- (B1) Boats that are NEVER reserved.                                  [P2]
--      These are what "find boats nobody has ever booked" 
--      queries return, and they are the rows a plain INNER JOIN 
--      against reserves silently drops.
INSERT INTO boats (bid, bname, color) VALUES
    (105, 'Sunfish',    'yellow'),
    (106, 'Catalina',   'white'),
    (107, 'Laser',      'blue'),
    (108, 'Optimist',   'green'),
    (109, 'Windseeker', 'black');

-- (B2) Sailors who have NEVER reserved a boat.                         [P3]
--      Together with Dan (99) these are the rows that only 
--      show up under LEFT OUTER JOIN / NOT EXISTS / NOT IN.
--      Their ratings (4, 5, 6) are deliberately values no tutorial sailor
--      holds, so each forms a group of one and the PDF's GROUP BY / HAVING
--      answers (EX15, EX16) still reproduce here character for character.
INSERT INTO sailors (sid, sname, rating, age) VALUES
    (96, 'Popeye',  5, 22.0),
    (97, 'Olive',   4, 31.0),
    (98, 'Wendy',   6, 29.5);

-- No reserves rows are added for 96, 97, 98 or 99 -- that is the whole point.
