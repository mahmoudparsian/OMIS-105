-- ============================================================================
--  OMIS 105 -- Sailors & Boats
--  File   : database/sql/01_schema.sql
--  Engine : DuckDB
--
--  *** THE SINGLE SOURCE OF TRUTH FOR EVERY DATABASE REQUIREMENT ***
--
--  All database requirements are defined ONCE, 
--  in the REQUIREMENTS block below, and nowhere else. 
--  The rest of this file, database/sql/02_data.sql, DESIGN.md, 
--  README.md, the Streamlit app and the Marimo notebook
--  all REFER to these labels (R1..R10, P1..P3, D1..D2) 
--  instead of restating the rules in their own words.
--
--  To change a requirement, change it HERE. 
--  Do not restate a requirement anywhere else 
--  in the project -- a second copy is a copy 
--  that will drift.
--
--  Source model (Ramakrishnan/Gehrke "Sailors" schema, 
--  see the tutorial PDF):
--
--      sailors(sid: integer, sname: string, rating: integer, age: real)
--      boats  (bid: integer, bname: string, color: string)
--      reserves(sid: integer, bid: integer, day: date)
--
--  where 
--         sid : a unique sailor ID
--         bid : a unique boat ID
--
-- ============================================================================


-- ============================================================================
--  REQUIREMENTS
-- ============================================================================
--
--  ---- THE TWO CORE RULES ------------------------------------------------
--
--  Everything about the reserves table exists to enforce these two
--  sentences. Each concerns ONE CALENDAR DAY, and each constrains a
--  DIFFERENT SIDE of the sailor-boat relationship:
--
--      (1) A SAILOR CANNOT RESERVE MORE THAN ONE BOAT IN A DAY.
--          Labelled R10 below.   
--          ENFORCED BY: UNIQUE (sid, day)     [note B]
--
--      (2) THE SAME BOAT CANNOT BE GIVEN TO MORE THAN ONE SAILOR IN A DAY.
--          Labelled R2 and R3 below (R4 and R8 are the same rule seen
--          from other angles).
--          ENFORCED BY: PRIMARY KEY (bid, day) [note A]
--
--  They are mirror images, and NEITHER IMPLIES THE OTHER: (1) says 
--  nothing about how many sailors a boat may serve, and (2) says 
--  nothing about how many boats a sailor may hold. That is why there 
--  are two constraints and not one, and why a single wider key -- the 
--  tutorial PDF's PRIMARY KEY (sid, bid, day) -- enforces NEITHER of them. 
--  Notes [A] and [B] work both rules through with real rows; DESIGN.md 
--  section 3 is the long-form argument.
--
--  Together they make any single day a ONE-TO-ONE MATCHING: each 
--  boat that is out has exactly one sailor, each sailor who is out 
--  has exactly one boat.
--
--  The labelled list below is the assignment's own wording. Where 
--  that wording is terser than the two sentences above, a READ AS 
--  note gives the reading the constraint actually implements -- 
--  it clarifies the rule, it does not add a new one.
--
--  ---- SCHEMA REQUIREMENTS (from the assignment) -------------------------
--
--  R1   Create a DuckDB database schema, and design and explain 
--       all of the tables.
--       ENFORCED BY: this file. Every table below documents 
--       its grain, its key, and why each column is typed and 
--       constrained as it is.
--
--  R2   Only 1 sailor can reserve a boat (one that is not already 
--       assigned to any sailor).
--       ENFORCED BY: reserves -- PRIMARY KEY (bid, day)          [note A]
--       READ AS: core rule (2). "Not already assigned" means not already
--       assigned FOR THAT DAY -- the rule is per-day, not forever. Boat 103
--       goes out with three different sailors on three different dates in
--       the seed data, which is legal and expected.
--
--  R3   The same boat is not reserved by 2 sailors for the same day.
--       ENFORCED BY: reserves -- PRIMARY KEY (bid, day)          [note A]
--       READ AS: core rule (2) again, stated from the boat's side. "2
--       sailors" means "more than one" -- 3 or 30 are equally forbidden,
--       because the key rejects every row after the first for a given
--       (bid, day).
--
--  R4   The same boat is not reserved multiple times for the same date.
--       ENFORCED BY: reserves -- PRIMARY KEY (bid, day)          [note A]
--       READ AS: core rule (2) with the sailor left out of it entirely --
--       one (boat, date) slot holds at most one reservation, whoever it
--       names.
--
--  R5   Dates are like 1998-10-10: YYYY-MM-DD.
--       ENFORCED BY: reserves.day typed DATE                     [note D]
--
--  R6   All sailors are unique.
--       ENFORCED BY: sailors -- PRIMARY KEY (sid)
--       Uniqueness is on sid, NOT on sname: sailors 64 and 74 are two
--       different people both called 'Horatio'. Names are not keys.
--
--  R7   All boats are unique.
--       ENFORCED BY: boats -- PRIMARY KEY (bid)
--       Again on bid, not bname: 101 and 102 are both 'Interlake'. Two
--       hulls of the same model are two distinct boats.
--
--  R8   A sailor cannot reserve the same boat multiple times for the same
--       date.
--       ENFORCED BY: reserves -- implied by PRIMARY KEY (bid, day)
--       Two such rows would share both bid and day, so the key rejects the
--       second without ever looking at sid.                      [note A]
--       READ AS: core rule (2) applied when the two sailors happen to be
--       the same person. Note this is the ONLY one of R2/R3/R4/R8/R10 that
--       the PDF's PRIMARY KEY (sid, bid, day) also catches -- it is the
--       duplicate-row case, and it is the least interesting of the five.
--
--  R9   Given a date, (sid, bid, day) must be unique -- does this make
--       sense, or is it redundant?
--       ANSWER: REDUNDANT, and therefore deliberately NOT declared. It is
--       left as a commented-out constraint on the reserves table.  [note C]
--
--  R10  A sailor cannot reserve more than one boat in a day.
--       ENFORCED BY: reserves -- UNIQUE (sid, day)                [note B]
--       READ AS: core rule (1), word for word. It is the only rule on this
--       list that constrains the SAILOR side, which is why it is the only
--       one the primary key cannot deliver.
--
--  ---- POPULATION REQUIREMENTS (from the assignment) ---------------------
--       Implemented in database/sql/02_data.sql, which is built by the same script.
--
--  P1   Initial data comes from sailors_and_boats_SQL_Tutorial.pdf.
--       One row departs from the PDF because the PDF's own Figure 1
--       violates R10 -- see the header of database/sql/02_data.sql.
--
--  P2   Add boats which are never reserved.
--
--  P3   Add sailors who have never reserved any boat.
--
--  ---- DERIVED RULES (not in the assignment; the data demands them) ------
--
--  D1   A reservation cannot name a sailor or a boat that does not exist.
--       ENFORCED BY: reserves -- FOREIGN KEY (sid), FOREIGN KEY (bid)
--
--  D2   Domain rules: 
--
--       a rating is 1..10 or NULL (unrated); 
--
--       an age is 0..120; 
--
--       names are not blank; 
--
--       a colour comes from a fixed vocabulary so that 
--       "find the red boats" cannot miss a row because
--       somebody typed 'Red' or ' red '.

--       ENFORCED BY: CHECK constraints on sailors and boats.
--       NOTE: the colour list is duplicated in src/sailors_db.py 
--       as VALID_COLORS, because the app must offer the same set 
--       the database accepts. Those two must be edited together.
--
-- ============================================================================
--  DESIGN NOTES -- why the constraints above are the ones they are
-- ============================================================================
--
--  [A] PRIMARY KEY (bid, day) -- "one boat, one day, one sailor"
--
--      WHAT IT SAYS. For each (boat, day) pair there is AT MOST ONE row, and
--      that row names the sailor holding it. Read the key as the identity of
--      a SLOT: not "a reservation event", but "boat 101 on 10 October". The
--      slot either exists (someone has it) or it does not (the boat is free).
--      `sid` is an attribute of the slot -- who holds it -- not part of what
--      makes the slot unique.
--
--      WHY NOT THE PDF'S KEY. The tutorial declares
--      PRIMARY KEY (sid, bid, day). That is wrong for R2/R3/R4:
--
--          (22, 101, '1998-10-10')   -- Dustin takes boat 101
--          (29, 101, '1998-10-10')   -- Brutus ALSO takes boat 101, same day
--
--      The two rows differ in sid, so the TRIPLE is unique and 
--      the PDF's key accepts both -- yet boat 101, one physical 
--      hull, has been handed to two sailors on the same morning. 
--      A boat cannot be in two places at once, so the database 
--      must not be able to say that it is.
--
--      WORKED EXAMPLE. The seed data has exactly one row on 1998-10-10:
--
--          sid 22 (Dustin) -- bid 101 (Interlake, blue) -- 1998-10-10
--
--      Now try to add more rows for that same day:
--
--        attempt                          outcome    why
--        ------------------------------   --------   --------------------------
--        (29, 101, '1998-10-10')          REJECTED   (101, 10-10) already taken
--          Brutus wants boat 101                     -> R2, R3
--
--        (22, 101, '1998-10-10')          REJECTED   same (bid, day) again; the
--          Dustin re-books the same boat             key never even looks at
--                                                    sid -> R4, R8
--
--        (22, 101, '1998-10-11')          accepted   different day, so a
--          Dustin keeps 101 tomorrow                 different slot
--
--      Note the second row: R4 and R8 are THE SAME two rows as far as this
--      key is concerned -- both are "a duplicate (bid, day)", and the only
--      difference between them is whether the sailor happens to match, which
--      the key never inspects. That is why one constraint answers both, and
--      why R8 needs no declaration of its own.
--
--  [B] UNIQUE (sid, day) -- "one sailor, one day, one boat"  (R10)
--
--      WHAT IT SAYS. For each (sailor, day) pair there is AT MOST ONE row,
--      and that row names the boat they took. It is note [A] with the two
--      entities swapped.
--
--      WHY THE PRIMARY KEY IS NOT ENOUGH. (bid, day) constrains the BOAT
--      side. It answers "how many sailors may hold this boat today?" -- one.
--      It is silent on "how many boats may this sailor hold today?", so on
--      its own it accepts:
--
--          (22, 101, '1998-10-10')   -- Dustin takes boat 101
--          (22, 102, '1998-10-10')   -- ...and boat 102, the same day
--
--      Those are two DIFFERENT slots -- (101, 10-10) and (102, 10-10) -- so
--      the primary key has no objection at all. This is not hypothetical:
--      it is what Figure 1 of the tutorial PDF actually contains, which is
--      why one seed row had to move (see database/sql/02_data.sql).
--
--      WORKED EXAMPLE. Same starting point, Dustin out on boat 101 on
--      1998-10-10. Boat 105 (Sunfish) is never reserved by anyone, so the
--      primary key cannot possibly object to it:
--
--        attempt                          outcome    why
--        ------------------------------   --------   --------------------------
--        (22, 105, '1998-10-10')          REJECTED   boat 105 is free, but
--          Dustin adds a second boat                 (22, 10-10) already
--                                                    exists -> R10. ONLY the
--                                                    UNIQUE catches this one.
--
--        (29, 105, '1998-10-10')          accepted   different sailor AND
--          Brutus takes the free 105                 different boat: neither
--                                                    constraint is touched
--
--      The first row is the whole reason this constraint exists. Delete
--      UNIQUE (sid, day) and it is accepted; the primary key never sees a
--      problem, because no boat was double-booked.
--
--      THE TWO TOGETHER. Each constrains one side of the relationship, and
--      neither implies the other, so both must be declared:
--
--                            forbids two rows with...
--          PRIMARY KEY (bid, day)   the same BOAT   on one day
--          UNIQUE      (sid, day)   the same SAILOR on one day
--
--      Consequently ANY SINGLE DAY is a ONE-TO-ONE MATCHING between 
--      the sailors who are out and the boats that are out. 1998-09-08 
--      in the seed data shows the shape:
--
--          sid 64 (Horatio) -- bid 102 (Interlake, red)
--          sid 74 (Horatio) -- bid 103 (Clipper, green)
--
--      Two rows, two distinct sailors, two distinct boats. Reading that 
--      day as a grid of boat x sailor, no row and no column may hold two 
--      marks.
--
--      Three practical consequences worth knowing:
--
--        * "who has boat B on day D" returns 0 or 1 rows -- and so does
--          "what did sailor S sail on day D".
--        * count(*) for one day counts the sailors out AND the boats out;
--          they are necessarily the same number.
--        * "is boat B free on D" and "is sailor S free on D" are the same
--          NOT EXISTS query with one column changed. See
--          available_boats_on() and free_sailors_on() in src/sailors_db.py.
--
--      Every outcome in both tables above is exercised by
--      `./create_database.sh --verify`, which runs these 
--      exact inserts and prints the database's own rejection.
--
--  [C] WHY R9 IS REDUNDANT
--
--      Any superset of a unique column set is automatically unique: 
--      if two rows agreed on every column of the superset, they would 
--      in  particular  agree  on  every  column  of the subset, which 
--      uniqueness has already ruled out.
--
--      (sid, bid, day) is a superset of BOTH declared constraints 
--      -- (bid, day) and (sid, day) -- so either one alone already 
--      implies it.  Declaring it would forbid nothing while costing 
--      a second index and its maintenance on every write.
--
--      The contrast is the whole lesson: (bid, day) and (sid, day) 
--      are each a subset of the triple, so each makes the triple 
--      redundant. But neither is a subset of the OTHER, which is why 
--      both are declared.   Redundancy is about the subset relation, 
--      not about how similar two constraints look.
--
--  [D] WHY DATE AND NOT THE PDF'S datetime
--
--      R5 fixes the format at YYYY-MM-DD, and DuckDB's DATE both 
--      parses and prints exactly that, so '1998-10-10' round-trips 
--      unchanged and '1998-13-45' is rejected by the type system 
--      before any constraint runs. A datetime would carry a time 
--      component, and then '1998-10-10 00:00' and '1998-10-10 09:30' 
--      would look like two different days to the primary key -- quietly 
--      reopening the double-booking hole that R2/R3/R4 exist to close.
--
--  Fuller prose versions of these notes, with worked counter-examples, 
--  are in DESIGN.md. DESIGN.md explains; this file defines.
--
--  NOTE ON DuckDB: 
--         1. Constraints must be declared inside CREATE TABLE. 
--            DuckDB does not support ALTER TABLE ... ADD CONSTRAINT, 
--            so everything is declared up-front. 
--         
--         2. Tables are dropped child-first (FK order).
-- ============================================================================

DROP TABLE IF EXISTS reserves;
DROP TABLE IF EXISTS boats;
DROP TABLE IF EXISTS sailors;

DROP SEQUENCE IF EXISTS seq_sid;
DROP SEQUENCE IF EXISTS seq_bid;


-- ----------------------------------------------------------------------------
-- 1. SAILORS -- the people who may reserve boats. One row is one person.
--
--    sid    surrogate key, and the identity R6 is about.
--    sname  the sailor's name. NOT NULL: a nameless sailor is not useful.
--    rating skill level. NULLable on purpose: the tutorial's NULL/OUTER JOIN
--           section inserts sailor 99 'Dan' unrated, which is what makes
--           COUNT(*) differ from COUNT(rating).
--    age    REAL, because the textbook ages are fractional (55.5, 25.5, 63.5).
-- ----------------------------------------------------------------------------
CREATE TABLE sailors (
    sid     INTEGER      NOT NULL,
    sname   VARCHAR(32)  NOT NULL,
    rating  INTEGER,                  -- NULL allowed: "unrated" sailor
    age     REAL,

    CONSTRAINT pk_sailors        PRIMARY KEY (sid),                                    -- R6
    CONSTRAINT ck_sailors_rating CHECK (rating IS NULL OR (rating BETWEEN 1 AND 10)),  -- D2
    CONSTRAINT ck_sailors_age    CHECK (age    IS NULL OR (age    BETWEEN 0 AND 120)), -- D2
    CONSTRAINT ck_sailors_sname  CHECK (length(trim(sname)) > 0)                       -- D2
);


-- ----------------------------------------------------------------------------
-- 2. BOATS -- the fleet that can be reserved. One row is one hull.
--
--    bid    surrogate key, and the identity R7 is about.
--    bname  model / hull name, NOT NULL.
--    color  free text in the textbook; constrained here to a small
--           vocabulary. Stored lower-case by convention.
-- ----------------------------------------------------------------------------
CREATE TABLE boats (
    bid     INTEGER      NOT NULL,
    bname   VARCHAR(32)  NOT NULL,
    color   VARCHAR(16)  NOT NULL,

    CONSTRAINT pk_boats        PRIMARY KEY (bid),                      -- R7
    CONSTRAINT ck_boats_bname  CHECK (length(trim(bname)) > 0),        -- D2
    CONSTRAINT ck_boats_color                                          -- D2
        CHECK (color IN ('red','green','blue','white','black','yellow'))
);


-- ----------------------------------------------------------------------------
-- 3. RESERVES -- the many-to-many relationship "sailor S has boat B on day D".
--    One row is one boat, on one day.
--
--    This table carries the central design decision of the assignment: the
--    choice of key, and the second constraint alongside it. Both are argued
--    in notes [A], [B] and [C] at the top of this file -- read those before
--    changing anything here.
--
--    sid    who holds the slot. NOT NULL, and not part of the primary key,
--           but constrained by UNIQUE (sid, day).
--    bid    which boat is out.
--    day    which day it is out. DATE, per R5 and note [D].
-- ----------------------------------------------------------------------------
CREATE TABLE reserves (
    sid     INTEGER  NOT NULL,
    bid     INTEGER  NOT NULL,
    day     DATE     NOT NULL,

    -- One boat, one day, one holder.
    CONSTRAINT pk_reserves         PRIMARY KEY (bid, day),   -- R2, R3, R4, R8, R9

    -- The mirror image: one sailor, one day, one boat.
    CONSTRAINT uq_reserves_sid_day UNIQUE (sid, day),        -- R10

    CONSTRAINT fk_reserves_sid FOREIGN KEY (sid) REFERENCES sailors(sid),  -- D1
    CONSTRAINT fk_reserves_bid FOREIGN KEY (bid) REFERENCES boats(bid)     -- D1
);

-- R9 is answered, not declared. See note [C] at the top of this file.
--
--     CONSTRAINT uq_reserves_sid_bid_day UNIQUE (sid, bid, day)   -- redundant


-- ----------------------------------------------------------------------------
-- 4. ID SEQUENCES for the Streamlit registration forms.
--    Seed data uses ids 22..99 (sailors) and 101..109 (boats). 
--
--    App-created rows start at 1000 so hand-entered textbook 
--    ids and app-generated ids never collide.
-- ----------------------------------------------------------------------------
CREATE SEQUENCE seq_sid START 1000;
CREATE SEQUENCE seq_bid START 1000;
