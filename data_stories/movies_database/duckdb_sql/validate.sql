-- ============================================================
-- validate.sql  --  sanity checks run against movies_db.duckdb
-- Invoked automatically by create_db.sh after the load.
-- ============================================================

.mode box
.print '--- tables ---'
SHOW TABLES;

.print '--- row counts per table ---'
SELECT 'country'             AS table_name, COUNT(*) AS rows FROM country
UNION ALL SELECT 'department',        COUNT(*) FROM department
UNION ALL SELECT 'gender',            COUNT(*) FROM gender
UNION ALL SELECT 'genre',             COUNT(*) FROM genre
UNION ALL SELECT 'keyword',           COUNT(*) FROM keyword
UNION ALL SELECT 'language',          COUNT(*) FROM language
UNION ALL SELECT 'language_role',     COUNT(*) FROM language_role
UNION ALL SELECT 'movie',             COUNT(*) FROM movie
UNION ALL SELECT 'movie_cast',        COUNT(*) FROM movie_cast
UNION ALL SELECT 'movie_company',     COUNT(*) FROM movie_company
UNION ALL SELECT 'movie_crew',        COUNT(*) FROM movie_crew
UNION ALL SELECT 'movie_genres',      COUNT(*) FROM movie_genres
UNION ALL SELECT 'movie_keywords',    COUNT(*) FROM movie_keywords
UNION ALL SELECT 'movie_languages',   COUNT(*) FROM movie_languages
UNION ALL SELECT 'person',            COUNT(*) FROM person
UNION ALL SELECT 'production_company',COUNT(*) FROM production_company
UNION ALL SELECT 'production_country',COUNT(*) FROM production_country
ORDER BY table_name;

.print '--- smoke test: a 3-table join (top 5 highest-grossing, with director) ---'
SELECT
    m.title,
    m.revenue,
    p.person_name AS director
FROM movie m
JOIN movie_crew mc ON mc.movie_id = m.movie_id AND mc.job = 'Director'
JOIN person p      ON p.person_id  = mc.person_id
ORDER BY m.revenue DESC
LIMIT 5;

.print '--- expected: movie = 4803 rows, 17 tables, joins return data ---'
