# 28 SQL Queries using the movies database

~~~sql
mysql> use movies;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+--------------------+
| Tables_in_movies   |
+--------------------+
| country            |
| department         |
| gender             |
| genre              |
| keyword            |
| language           |
| language_role      |
| movie              |
| movie_cast         |
| movie_company      |
| movie_crew         |
| movie_genres       |
| movie_keywords     |
| movie_languages    |
| person             |
| production_company |
| production_country |
+--------------------+
17 rows in set (0.00 sec)
~~~


## Question 1: Find how many movies are in the database?

~~~mysql
mysql> select count(*) from movie;
+----------+
| count(*) |
+----------+
|     4803 |
+----------+
1 row in set (0.00 sec)
~~~

## Question 2: From the movie table, return the top 10 movies with a rating of 8.0 or higher

~~~mysql
select 
       movie_id, 
       title, 
       release_date, 
       ROUND(vote_average, 1) as rating
from 
       movie
where 
       vote_average > 8.0
ORDER BY
       vote_average DESC
LIMIT 
       10;
       
+----------+--------------------------+--------------+--------+
| movie_id | title                    | release_date | rating |
+----------+--------------------------+--------------+--------+
|    89861 | Stiff Upper Lips         | 1998-06-12   |   10.0 |
|    78373 | Dancer, Texas Pop. 81    | 1998-05-01   |   10.0 |
|    40963 | Little Big Top           | 2006-01-01   |   10.0 |
|   361505 | Me You and Five Bucks    | 2015-07-07   |   10.0 |
|   346081 | Sardaarji                | 2015-06-26   |    9.5 |
|    69848 | One Man's Hero           | 1999-08-02   |    9.3 |
|    88641 | There Goes My Baby       | 1994-09-02   |    8.5 |
|      278 | The Shawshank Redemption | 1994-09-23   |    8.5 |
|    43867 | The Prisoner of Zenda    | 1937-09-03   |    8.4 |
|      238 | The Godfather            | 1972-03-14   |    8.4 |
+----------+--------------------------+--------------+--------+
10 rows in set (0.00 sec)
~~~

## Question 3: From the movie table, find the top 10 highest grossing movies

~~~mysql
select 
       movie_id, 
       title, 
       release_date, 
       revenue
from 
       movie
ORDER BY
       revenue DESC
LIMIT 
       10;

+----------+----------------------------+--------------+------------+
| movie_id | title                      | release_date | revenue    |
+----------+----------------------------+--------------+------------+
|    19995 | Avatar                     | 2009-12-10   | 2787965087 |
|      597 | Titanic                    | 1997-11-18   | 1845034188 |
|    24428 | The Avengers               | 2012-04-25   | 1519557910 |
|   135397 | Jurassic World             | 2015-06-09   | 1513528810 |
|   168259 | Furious 7                  | 2015-04-01   | 1506249360 |
|    99861 | Avengers: Age of Ultron    | 2015-04-22   | 1405403694 |
|   109445 | Frozen                     | 2013-11-27   | 1274219009 |
|    68721 | Iron Man 3                 | 2013-04-18   | 1215439994 |
|   211672 | Minions                    | 2015-06-17   | 1156730962 |
|   271110 | Captain America: Civil War | 2016-04-27   | 1153304495 |
+----------+----------------------------+--------------+------------+
10 rows in set (0.01 sec)
~~~

## Question 4: Find the top 10 highest rating movies from Walt Disney Pictures.

~~~sql       
SELECT 
       m.movie_id, 
       m.title, 
       ROUND(m.vote_average, 1) as rating,
       pc.company_name
FROM 
       movie m
JOIN 
       movie_company mc ON m.movie_id = mc.movie_id
JOIN 
       production_company pc ON mc.company_id = pc.company_id
WHERE
       pc.company_name = 'Walt Disney Pictures'
ORDER BY
       m.vote_average DESC
LIMIT 
       10;      

+----------+--------------------------------------------------------+--------+----------------------+
| movie_id | title                                                  | rating | company_name         |
+----------+--------------------------------------------------------+--------+----------------------+
|   150540 | Inside Out                                             |    8.0 | Walt Disney Pictures |
|     8587 | The Lion King                                          |    8.0 | Walt Disney Pictures |
|    10681 | WALL·E                                                 |    7.8 | Walt Disney Pictures |
|   177572 | Big Hero 6                                             |    7.8 | Walt Disney Pictures |
|      404 | The Straight Story                                     |    7.7 | Walt Disney Pictures |
|    10193 | Toy Story 3                                            |    7.6 | Walt Disney Pictures |
|    10674 | Mulan                                                  |    7.6 | Walt Disney Pictures |
|       22 | Pirates of the Caribbean: The Curse of the Black Pearl |    7.5 | Walt Disney Pictures |
|     2062 | Ratatouille                                            |    7.5 | Walt Disney Pictures |
|      585 | Monsters, Inc.                                         |    7.5 | Walt Disney Pictures |
+----------+--------------------------------------------------------+--------+----------------------+
10 rows in set (0.01 sec)
~~~


## Question 5: Find the top 10 action movies with the highest ratings from the movies database.

~~~sql
SELECT 
       m.movie_id, 
       m.title, 
       ROUND(m.vote_average, 1) as rating,
       g.genre_name
FROM 
       movie m
JOIN 
       movie_genres mg ON m.movie_id = mg.movie_id
JOIN 
       genre g ON mg.genre_id = g.genre_id
WHERE
       g.genre_name = 'Action'
ORDER BY
       m.vote_average DESC
LIMIT 
       10;   

+----------+---------------------------------------------------+--------+------------+
| movie_id | title                                             | rating | genre_name |
+----------+---------------------------------------------------+--------+------------+
|    69848 | One Man's Hero                                    |    9.3 | Action     |
|      155 | The Dark Knight                                   |    8.2 | Action     |
|     1891 | The Empire Strikes Back                           |    8.2 | Action     |
|      346 | 七人の侍                                           |    8.2 | Action     |
|    27205 | Inception                                         |    8.1 | Action     |
|      122 | The Lord of the Rings: The Return of the King     |    8.1 | Action     |
|       11 | Star Wars                                         |    8.1 | Action     |
|      121 | The Lord of the Rings: The Two Towers             |    8.0 | Action     |
|      670 | 올드보이                                            |    8.0 | Action     |
|      120 | The Lord of the Rings: The Fellowship of the Ring |    8.0 | Action     |
+----------+---------------------------------------------------+--------+------------+
10 rows in set (0.01 sec)
~~~

## Question 6: Return all titles of movies with the word “dark” in it.

~~~sql
SELECT 
       movie_id, 
       title
FROM 
       movie m
WHERE
       title LIKE  '%dark%';

+----------+-------------------------------------------+
| movie_id | title                                     |
+----------+-------------------------------------------+
|       16 | Dancer in the Dark                        |
|      141 | Donnie Darko                              |
|      155 | The Dark Knight                           |
|      766 | Army of Darkness                          |
|     2666 | Dark City                                 |
|     3509 | A Scanner Darkly                          |
|     3512 | Under Siege 2: Dark Territory             |
|     4911 | Dark Blue                                 |
|     9009 | Dark Water                                |
|    10586 | The Ghost and the Darkness                |
|    10727 | Darkness Falls                            |
|    11056 | Darkness                                  |
|    12142 | Alone in the Dark                         |
|    12201 | Edge of Darkness                          |
|    13362 | Taxi to the Dark Side                     |
|    18045 | The Dark Hours                            |
|    20296 | Chocolate: Deep Dark Secrets              |
|    38031 | You Will Meet a Tall Dark Stranger        |
|    38356 | Transformers: Dark of the Moon            |
|    46261 | Don't Be Afraid of the Dark               |
|    49026 | The Dark Knight Rises                     |
|    54138 | Star Trek Into Darkness                   |
|    62213 | Dark Shadows                              |
|    71469 | The Darkest Hour                          |
|    76338 | Thor: The Dark World                      |
|    84401 | Sholem Aleichem: Laughing In The Darkness |
|    97630 | Zero Dark Thirty                          |
|   142061 | Batman: The Dark Knight Returns, Part 2   |
|   283686 | Out of the Dark                           |
|   331493 | Light from the Darkroom                   |
+----------+-------------------------------------------+
30 rows in set (0.01 sec)
~~~

## Question 7: Return all released movies produced in the UK and title contains "batman"

~~~sql
SELECT 
       m.movie_id, 
       m.title,
       m.release_date,
       m.movie_status,
       c.country_name as production_country
       
FROM 
       movie m
JOIN
       production_country pc on m.movie_id = pc.movie_id
JOIN
       country c on pc.country_id = c.country_id
WHERE
       c.country_name = 'United Kingdom' AND
       m.movie_status = 'released'       AND
       m.title LIKE '%batman%';
       
       
+----------+----------------+--------------+--------------+--------------------+
| movie_id | title          | release_date | movie_status | production_country |
+----------+----------------+--------------+--------------+--------------------+
|      268 | Batman         | 1989-06-23   | Released     | United Kingdom     |
|      272 | Batman Begins  | 2005-06-10   | Released     | United Kingdom     |
|      364 | Batman Returns | 1992-06-19   | Released     | United Kingdom     |
|      414 | Batman Forever | 1995-05-31   | Released     | United Kingdom     |
|      415 | Batman & Robin | 1997-06-20   | Released     | United Kingdom     |
+----------+----------------+--------------+--------------+--------------------+
5 rows in set (0.01 sec)
~~~

## Question 8: List top-10 movies with the highest budget and revenue 


~~~sql   
SELECT 
       movie_id, 
       title,
       budget,
       revenue    
FROM 
       movie m
ORDER BY
       budget DESC,
       revenue DESC
LIMIT
       10;
       
+----------+---------------------------------------------+-----------+------------+
| movie_id | title                                       | budget    | revenue    |
+----------+---------------------------------------------+-----------+------------+
|     1865 | Pirates of the Caribbean: On Stranger Tides | 380000000 | 1045713802 |
|      285 | Pirates of the Caribbean: At World's End    | 300000000 |  961000000 |
|    99861 | Avengers: Age of Ultron                     | 280000000 | 1405403694 |
|     1452 | Superman Returns                            | 270000000 |  391081192 |
|    38757 | Tangled                                     | 260000000 |  591794936 |
|    49529 | John Carter                                 | 260000000 |  284139100 |
|      559 | Spider-Man 3                                | 258000000 |  890871626 |
|    57201 | The Lone Ranger                             | 255000000 |   89289910 |
|   271110 | Captain America: Civil War                  | 250000000 | 1153304495 |
|    49026 | The Dark Knight Rises                       | 250000000 | 1084939099 |
+----------+---------------------------------------------+-----------+------------+
10 rows in set (0.00 sec)
~~~


## Question 9: List top 20 movies with highest rating and shortest runtime.  

~~~sql
SELECT 
       movie_id, 
       title,
       ROUND(vote_average, 1) as rating,
       runtime    
FROM 
       movie 
ORDER BY
       vote_average DESC,
       runtime ASC
LIMIT
       20;

+----------+--------------------------+--------+---------+
| movie_id | title                    | rating | runtime |
+----------+--------------------------+--------+---------+
|    40963 | Little Big Top           |   10.0 |       0 |
|   361505 | Me You and Five Bucks    |   10.0 |      90 |
|    78373 | Dancer, Texas Pop. 81    |   10.0 |      97 |
|    89861 | Stiff Upper Lips         |   10.0 |      99 |
|   346081 | Sardaarji                |    9.5 |       0 |
|    69848 | One Man's Hero           |    9.3 |     121 |
|    88641 | There Goes My Baby       |    8.5 |      99 |
|      278 | The Shawshank Redemption |    8.5 |     142 |
|    43867 | The Prisoner of Zenda    |    8.4 |     101 |
|      238 | The Godfather            |    8.4 |     175 |
|   244786 | Whiplash                 |    8.3 |     105 |
|   322745 | Counting                 |    8.3 |     111 |
|      129 | 千と千尋の神隠し         |    8.3 |     125 |
|      550 | Fight Club               |    8.3 |     139 |
|      680 | Pulp Fiction             |    8.3 |     154 |
|      424 | Schindler's List         |    8.3 |     195 |
|      240 | The Godfather: Part II   |    8.3 |     200 |
|      389 | 12 Angry Men             |    8.2 |      96 |
|      539 | Psycho                   |    8.2 |     109 |
|     4935 | ハウルの動く城           |    8.2 |     119 |
+----------+--------------------------+--------+---------+
20 rows in set (0.00 sec)
~~~


## Question 10: List all the cast and actors in the movie “Forrest Gump”

~~~sql
SELECT 
       m.movie_id, 
       m.title,
       mc.cast_order,
       mc.character_name, 
       p.person_name as cast   
FROM 
       movie m
JOIN
       movie_cast mc ON m.movie_id = mc.movie_id
JOIN 
       person p ON mc.person_id = p.person_id
WHERE
       m.title = 'Forrest Gump';    
           
+----------+--------------+------------+-----------------------------------+--------------------------+
| movie_id | title        | cast_order | character_name                    | cast                     |
+----------+--------------+------------+-----------------------------------+--------------------------+
|       13 | Forrest Gump |          0 | Forrest Gump                      | Tom Hanks                |
|       13 | Forrest Gump |          1 | Jenny Curran                      | Robin Wright             |
|       13 | Forrest Gump |          2 | Lt. Dan Taylor                    | Gary Sinise              |
|       13 | Forrest Gump |          3 | Pvt. Benjamin Buford 'Bubba' Blue | Mykelti Williamson       |
|       13 | Forrest Gump |          4 | Mrs. Gump                         | Sally Field              |
|       13 | Forrest Gump |          5 | Young Forrest Gump                | Michael Conner Humphreys |
|       13 | Forrest Gump |          6 | Young Jenny Curran                | Hanna Hall               |
|       13 | Forrest Gump |          7 | Forrest Gump Jr.                  | Haley Joel Osment        |
|       13 | Forrest Gump |          8 | School Bus Driver                 | Siobhan Fallon           |
|       13 | Forrest Gump |          9 | Drill Sergeant                    | Afemo Omilami            |
|       13 | Forrest Gump |         10 | Young Elvis Presley               | Peter Dobson             |
|       13 | Forrest Gump |         11 | College Football Coach            | Sonny Shroyer            |
|       13 | Forrest Gump |         12 | Barber                            | George Kelly             |
|       13 | Forrest Gump |         13 | Principal                         | Sam Anderson             |
|       13 | Forrest Gump |         14 | Louise                            | Margo Moorer             |
|       13 | Forrest Gump |         15 | Boy with cross                    | Christopher Jones        |
|       13 | Forrest Gump |         16 | Jenny's Father                    | Kevin Mangan             |
|       13 | Forrest Gump |         17 | High School Football Coach        | Brett Rice               |
|       13 | Forrest Gump |         18 | Recruiter                         | Daniel C. Striepeke      |
|       13 | Forrest Gump |         19 | Newscaster                        | David Brisbin            |
|       13 | Forrest Gump |         20 | Earl                              | Kirk Ward                |
|       13 | Forrest Gump |         21 | Bubba's Mother                    | Marlena Smalls           |
|       13 | Forrest Gump |         22 | Bubba's Great Grandmother         | Kitty K. Green           |
|       13 | Forrest Gump |         23 | Jenny's date                      | Mark Matheisen           |
|       13 | Forrest Gump |         24 | Local Anchor #1                   | Al Harrington            |
|       13 | Forrest Gump |         25 | President Kennedy (voice)         | Jed Gillin               |
|       13 | Forrest Gump |         26 | Army Recruiter                    | Don Fischer              |
|       13 | Forrest Gump |         27 | Barracks Recruit                  | Matt Wallace             |
|       13 | Forrest Gump |         28 | Club patron                       | Mike Jolly               |
|       13 | Forrest Gump |         29 | Club patron                       | Michael Kemmerling       |
|       13 | Forrest Gump |         30 | Club patron                       | John Voldstad            |
|       13 | Forrest Gump |         31 | Helicopter gunman                 | Daniel J. Gillooly       |
|       13 | Forrest Gump |         32 | Cleveland                         | Michael Burgess          |
|       13 | Forrest Gump |         33 | Tex                               | Steven Griffith          |
|       13 | Forrest Gump |         34 | Army Hospital Male Nurse          | Michael McFall           |
|       13 | Forrest Gump |         35 | Wounded soldier                   | Michael McFall           |
|       13 | Forrest Gump |         36 | Wounded soldier                   | Byron Minns              |
|       13 | Forrest Gump |         37 | Hospital Officer                  | Stephen Bridgewater      |
|       13 | Forrest Gump |         38 | President Johnson (voice)         | John William Galt        |
|       13 | Forrest Gump |         39 | Isabel                            | Isabel Rose              |
|       13 | Forrest Gump |         40 | Abbie Hoffman                     | Richard D'Alessandro     |
|       13 | Forrest Gump |         41 | Black Panther                     | Michael Jace             |
|       13 | Forrest Gump |         42 | Wesley                            | Geoffrey Blake           |
|       13 | Forrest Gump |         43 | Hollywood Boulevard Girlfriend    | Vanessa Roth             |
|       13 | Forrest Gump |         44 | Dick Cavett                       | Dick Cavett              |
|       13 | Forrest Gump |         45 | Carla                             | Tiffany Salerno          |
|       13 | Forrest Gump |         46 | Lenore                            | Tiffany Salerno          |
|       13 | Forrest Gump |         47 | President Nixon (voice)           | Joe Alaskey              |
|       13 | Forrest Gump |         48 | Discharge Officer                 | Lazarus Jackson          |
|       13 | Forrest Gump |         49 | Drugged Out Boyfriend             | Lazarus Jackson          |
|       13 | Forrest Gump |         50 | Elderly Southern Woman            | Nora Dunfee              |
|       13 | Forrest Gump |         51 | Waitress in cafe                  | Hallie D'Amore           |
|       13 | Forrest Gump |         52 | Taxi Driver                       | Michael Mattison         |
|       13 | Forrest Gump |         53 | Aging Hippie                      | Charles Boswell          |
|       13 | Forrest Gump |         54 | Wild eyed man                     | Timothy McNeil           |
|       13 | Forrest Gump |         55 | Crony                             | Bob Penny                |
|       13 | Forrest Gump |         56 | Football Player (uncredited)      | Greg Brown               |
|       13 | Forrest Gump |         57 | Cheerleader (uncredited)          | Troy Christian           |
|       13 | Forrest Gump |         58 | Football Coach (uncredited)       | Bryan Hanna              |
|       13 | Forrest Gump |         59 | Barracks Recruit (uncredited)     | Zach Hanner              |
|       13 | Forrest Gump |         60 | National Guardsman (uncredited)   | Aaron Michael Lacey      |
|       13 | Forrest Gump |         61 | Football Fan (uncredited)         | Jacqueline Lovell        |
|       13 | Forrest Gump |         63 | Football Player (uncredited)      | Brendan Shanahan         |
|       13 | Forrest Gump |         64 | Black Panther (uncredited)        | William Shipman          |
|       13 | Forrest Gump |         65 | Nicholas Katzenbach (uncredited)  | Robb Skyler              |
|       13 | Forrest Gump |         66 | Jenny's Babysitter (uncredited)   | Mary Ellen Trainor       |
+----------+--------------+------------+-----------------------------------+--------------------------+
66 rows in set (0.01 sec)
~~~

##  Question 11: Return all movies starred by the actor Leonardo DiCaprio with highest ratings   


~~~sql
SELECT 
       m.movie_id, 
       m.title,
       ROUND(m.vote_average, 1) as rating,
       mc.character_name, 
       p.person_name as actor   
FROM 
       movie m
JOIN
       movie_cast mc ON m.movie_id = mc.movie_id
JOIN 
       person p ON mc.person_id = p.person_id
WHERE
       p.person_name = 'Leonardo DiCaprio'
ORDER BY
       m.vote_average DESC; 
       
+----------+-----------------------------+--------+-----------------------------+-------------------+
| movie_id | title                       | rating | character_name              | actor             |
+----------+-----------------------------+--------+-----------------------------+-------------------+
|    27205 | Inception                   |    8.1 | Dom Cobb                    | Leonardo DiCaprio |
|     1422 | The Departed                |    7.9 | William Billy Costigan, Jr. | Leonardo DiCaprio |
|   106646 | The Wolf of Wall Street     |    7.9 | Jordan Belfort              | Leonardo DiCaprio |
|    11324 | Shutter Island              |    7.8 | Teddy Daniels               | Leonardo DiCaprio |
|    68718 | Django Unchained            |    7.8 | Calvin Candie               | Leonardo DiCaprio |
|      640 | Catch Me If You Can         |    7.7 | Frank Abagnale Jr.          | Leonardo DiCaprio |
|      597 | Titanic                     |    7.5 | Jack Dawson                 | Leonardo DiCaprio |
|     1587 | What's Eating Gilbert Grape |    7.5 | Arnie Grape                 | Leonardo DiCaprio |
|     1372 | Blood Diamond               |    7.3 | Danny Archer                | Leonardo DiCaprio |
|    64682 | The Great Gatsby            |    7.3 | Jay Gatsby                  | Leonardo DiCaprio |
|   281957 | The Revenant                |    7.3 | Hugh Glass                  | Leonardo DiCaprio |
|     3131 | Gangs of New York           |    7.1 | Amsterdam Vallon            | Leonardo DiCaprio |
|     2567 | The Aviator                 |    7.0 | Howard Hughes               | Leonardo DiCaprio |
|      454 | Romeo + Juliet              |    6.7 | Romeo                       | Leonardo DiCaprio |
|     4148 | Revolutionary Road          |    6.7 | Frank Wheeler               | Leonardo DiCaprio |
|     9819 | Marvin's Room               |    6.6 | Hank                        | Leonardo DiCaprio |
|    12113 | Body of Lies                |    6.5 | Roger Ferris                | Leonardo DiCaprio |
|     1907 | The Beach                   |    6.3 | Richard                     | Leonardo DiCaprio |
|     9313 | The Man in the Iron Mask    |    6.3 | King Louis XIV / Philippe   | Leonardo DiCaprio |
|    12106 | The Quick and the Dead      |    6.3 | Fee Herod The Kidu201c      | Leonardo DiCaprio |
|     9466 | Celebrity                   |    6.0 | Brandon                     | Leonardo DiCaprio |
|    88794 | J. Edgar                    |    6.0 | J. Edgar Hoover             | Leonardo DiCaprio |
+----------+-----------------------------+--------+-----------------------------+-------------------+
22 rows in set (0.14 sec)
~~~

## Question 12: Return all movies released before year 1940

~~~sql
SELECT 
       movie_id, 
       title,
       release_date
FROM 
       movie 
WHERE
       release_date < '1940-01-01'
ORDER BY
       release_date ASC;  
       
+----------+---------------------------------+--------------+
| movie_id | title                           | release_date |
+----------+---------------------------------+--------------+
|     3059 | Intolerance                     | 1916-09-04   |
|     3060 | The Big Parade                  | 1925-11-05   |
|       19 | Metropolis                      | 1927-01-10   |
|      905 | Die Büchse der Pandora          | 1929-01-30   |
|    65203 | The Broadway Melody             | 1929-02-08   |
|    22301 | Hell's Angels                   | 1930-11-15   |
|    22649 | A Farewell to Arms              | 1932-12-08   |
|     3062 | 42nd Street                     | 1933-02-02   |
|    43595 | She Done Him Wrong              | 1933-02-09   |
|     3078 | It Happened One Night           | 1934-02-22   |
|     3080 | Top Hat                         | 1935-09-06   |
|     3082 | Modern Times                    | 1936-02-05   |
|    43884 | The Charge of the Light Brigade | 1936-10-20   |
|    43867 | The Prisoner of Zenda           | 1937-09-03   |
|      408 | Snow White and the Seven Dwarfs | 1937-12-20   |
|    43839 | Alexander's Ragtime Band        | 1938-05-24   |
|    34106 | You Can't Take It With You      | 1938-08-23   |
|      630 | The Wizard of Oz                | 1939-08-15   |
|     3083 | Mr. Smith Goes to Washington    | 1939-10-19   |
|      770 | Gone with the Wind              | 1939-12-15   |
+----------+---------------------------------+--------------+
20 rows in set (0.01 sec)
~~~


## Question 13: Return all movies released between year 2000 and 2002

~~~sql
SELECT 
       movie_id, 
       title,
       release_date
FROM 
       movie 
WHERE
       release_date BETWEEN '2000-01-01' AND '2002-01-01'
ORDER BY
       release_date ASC;  
       
+----------+---------------------------------------------------+--------------+
| movie_id | title                                             | release_date |
+----------+---------------------------------------------------+--------------+
|    48217 | La veuve de Saint-Pierre                          | 2000-01-01   |
|    10471 | Next Friday                                       | 2000-01-12   |
|    10384 | Supernova                                         | 2000-01-14   |
...
|    30309 | Real Women Have Curves                            | 2002-01-01   |
|    31932 | City of Ghosts                                    | 2002-01-01   |
|    43743 | Fabled                                            | 2002-01-01   |
+----------+---------------------------------------------------+--------------+
357 rows in set (0.00 sec)
~~~


## Question 14: From the movie table, return a list of movies that do not have any rating.

~~~sql
SELECT 
       movie_id, 
       title,
       vote_average
FROM 
       movie 
WHERE
       vote_average is NULL;

Empty set (0.01 sec)
=> there is no movie where vote_average is NULL.
~~~


## Question 15: From the movie, find the year the movie “Titanic” was released.

~~~sql
SELECT 
       movie_id, 
       title,
       release_date
FROM 
       movie 
WHERE
       title = 'Titanic';

+----------+---------+--------------+
| movie_id | title   | release_date |
+----------+---------+--------------+
|      597 | Titanic | 1997-11-18   |
+----------+---------+--------------+
1 row in set (0.01 sec)
~~~


## Question 16: Find the highest rated movies released in the first quarter of year 2005.

Quarters:

	Q1: January-March
	Q2: April-June
	Q3: July-September
	Q4: October-December

~~~sql
SELECT 
       movie_id, 
       title,
       release_date,
       ROUND(vote_average, 1) as rating
FROM 
       movie 
WHERE
       release_date BETWEEN '2005-01-01' AND '2005-03-31'
ORDER BY
       vote_average DESC;  

+----------+---------------------------------------------+--------------+--------+
| movie_id | title                                       | release_date | rating |
+----------+---------------------------------------------+--------------+--------+
|   333355 | Star Wars: Clone Wars (Volume 1)            | 2005-03-21   |    8.0 |
|    67238 | Cavite                                      | 2005-03-12   |    7.5 |
|     7214 | Coach Carter                                | 2005-01-14   |    7.3 |
|     1544 | Imagine Me & You                            | 2005-02-01   |    7.0 |
|    20520 | The Motel                                   | 2005-01-01   |    7.0 |
|     1667 | La Marche de l'empereur                     | 2005-01-26   |    6.9 |
|    20981 | The Call of Cthulhu                         | 2005-01-01   |    6.9 |
|     2652 | Hard Candy                                  | 2005-01-14   |    6.8 |
|     9667 | The Jacket                                  | 2005-03-04   |    6.8 |
|     9701 | North Country                               | 2005-02-12   |    6.8 |
|    12228 | Inside Deep Throat                          | 2005-02-11   |    6.8 |
|     7453 | The Hitchhiker's Guide to the Galaxy        | 2005-01-15   |    6.6 |
|    14517 | Mirrormask                                  | 2005-01-25   |    6.6 |
|    10027 | Unleashed                                   | 2005-02-02   |    6.6 |
|    41508 | Sorstalanság                                | 2005-02-10   |    6.5 |
|    17113 | The Ballad of Jack and Rose                 | 2005-03-25   |    6.5 |
|    64973 | Peace, Propaganda & the Promised Land       | 2005-01-28   |    6.4 |
|     8488 | Hitch                                       | 2005-02-10   |    6.4 |
|    16186 | Diary of a Mad Black Woman                  | 2005-02-25   |    6.4 |
|    13682 | Pooh's Heffalump Movie                      | 2005-02-11   |    6.4 |
|    11354 | The Upside of Anger                         | 2005-01-23   |    6.4 |
|    24055 | The Puffy Chair                             | 2005-01-17   |    6.2 |
|     6961 | The Wedding Date                            | 2005-02-04   |    6.2 |
|     2026 | Hostage                                     | 2005-03-09   |    6.2 |
|    11096 | Hide and Seek                               | 2005-01-27   |    6.1 |
|     7515 | London                                      | 2005-02-10   |    6.1 |
|    40769 | Mutual Appreciation                         | 2005-03-01   |    6.1 |
|     1546 | Thumbsucker                                 | 2005-01-23   |    6.1 |
|    17880 | Because of Winn-Dixie                       | 2005-02-18   |    6.1 |
|     9928 | Robots                                      | 2005-03-10   |    6.0 |
|     8978 | Assault on Precinct 13                      | 2005-01-19   |    6.0 |
|    13374 | Ice Princess                                | 2005-03-17   |    5.9 |
|     2287 | Rize                                        | 2005-01-15   |    5.9 |
|    10022 | The Pacifier                                | 2005-03-04   |    5.8 |
|    29078 | The Game of Their Lives                     | 2005-01-01   |    5.8 |
|     1690 | Hostel                                      | 2005-01-06   |    5.7 |
|    10913 | Dear Wendy                                  | 2005-01-22   |    5.6 |
|    11804 | White Noise                                 | 2005-01-07   |    5.6 |
|    11638 | Guess Who                                   | 2005-03-25   |    5.5 |
|    18045 | The Dark Hours                              | 2005-03-11   |    5.5 |
|    10320 | The Ring Two                                | 2005-03-17   |    5.4 |
|     4551 | Be Cool                                     | 2005-03-04   |    5.4 |
|    13498 | Man of the House                            | 2005-02-25   |    5.4 |
|    10040 | Miss Congeniality 2: Armed and Fabulous     | 2005-03-11   |    5.3 |
|    14175 | Valiant                                     | 2005-03-25   |    5.2 |
|    11637 | Are We There Yet?                           | 2005-01-20   |    5.2 |
|     6439 | Racing Stripes                              | 2005-01-06   |    5.1 |
|    10012 | Cursed                                      | 2005-02-25   |    5.1 |
|    67373 | This Thing of Ours                          | 2005-01-01   |    5.0 |
|     9288 | Dungeons & Dragons: Wrath of the Dragon God | 2005-01-01   |    4.8 |
|     9947 | Elektra                                     | 2005-01-13   |    4.8 |
|    43630 | The Helix... Loaded                         | 2005-01-01   |    4.8 |
|     8968 | Boogeyman                                   | 2005-02-04   |    4.6 |
|    10214 | Son of the Mask                             | 2005-02-18   |    3.6 |
|    51820 | The Salon                                   | 2005-01-13   |    3.5 |
|    12142 | Alone in the Dark                           | 2005-01-28   |    3.1 |
|    27404 | My Big Fat Independent Movie                | 2005-03-04   |    3.0 |
+----------+---------------------------------------------+--------------+--------+
57 rows in set (0.01 sec)
~~~


## Question 17: Return the top 10 highest rated horror movies

~~~sql
SELECT 
       m.title,
       g.genre_name,
       ROUND(m.vote_average, 1) as rating
FROM 
       movie m
JOIN
       movie_genres mg ON m.movie_id = mg.movie_id
JOIN
       genre g ON mg.genre_id = g.genre_id
WHERE
       g.genre_name = 'horror'
ORDER BY
       vote_average DESC
LIMIT
       10;

+--------------------------+------------+--------+
| title                    | genre_name | rating |
+--------------------------+------------+--------+
| Psycho                   | Horror     |    8.2 |
| The Shining              | Horror     |    8.1 |
| Alien                    | Horror     |    7.9 |
| The Thing                | Horror     |    7.8 |
| Aliens                   | Horror     |    7.7 |
| Evil Dead II             | Horror     |    7.6 |
| The Exorcist             | Horror     |    7.5 |
| Night of the Living Dead | Horror     |    7.5 |
| Wind Walkers             | Horror     |    7.5 |
| Jaws                     | Horror     |    7.5 |
+--------------------------+------------+--------+
10 rows in set (0.01 sec)
~~~


## Question 18: Return all Italian movies in the database with release_date after year 2014.


~~~sql
SELECT 
       m.title,
       m.release_date,
       l.language_name
FROM 
       movie m
JOIN
       movie_languages ml ON m.movie_id = ml.movie_id
JOIN
       language l ON ml.language_id = l.language_id
WHERE
       l.language_name LIKE '%Italian%' AND
       m.release_date > '2014-01-01';

+--------------------------------------------+--------------+---------------+
| title                                      | release_date | language_name |
+--------------------------------------------+--------------+---------------+
| Big Eyes                                   | 2014-12-24   | Italiano      |
| Blackhat                                   | 2015-01-13   | Italiano      |
| The Man from U.N.C.L.E.                    | 2015-08-13   | Italiano      |
| Spectre                                    | 2015-10-26   | Italiano      |
| Unbroken                                   | 2014-12-25   | Italiano      |
| McFarland, USA                             | 2015-02-20   | Italiano      |
| Lords of London                            | 2014-01-06   | Italiano      |
| Danny Collins                              | 2015-03-19   | Italiano      |
| The Theory of Everything                   | 2014-11-26   | Italiano      |
| We Are Your Friends                        | 2015-08-26   | Italiano      |
| シン・ゴジラ                               | 2016-07-29   | Italiano      |
| Misconduct                                 | 2016-02-05   | Italiano      |
| Chiamatemi Francesco - Il Papa della gente | 2015-12-03   | Italiano      |
+--------------------------------------------+--------------+---------------+
13 rows in set (0.00 sec)
~~~

I have the following table in mysql:

~~~sql
mysql> desc movie;
+--------------+---------------+------+-----+---------+----------------+
| Field        | Type          | Null | Key | Default | Extra          |
+--------------+---------------+------+-----+---------+----------------+
| movie_id     | int           | NO   | PRI | NULL    | auto_increment |
| title        | varchar(1000) | YES  |     | NULL    |                |
| budget       | int           | YES  |     | NULL    |                |
| homepage     | varchar(1000) | YES  |     | NULL    |                |
| overview     | varchar(1000) | YES  |     | NULL    |                |
| popularity   | decimal(12,6) | YES  |     | NULL    |                |
| release_date | date          | YES  |     | NULL    |                |
| revenue      | bigint        | YES  |     | NULL    |                |
| runtime      | int           | YES  |     | NULL    |                |
| movie_status | varchar(50)   | YES  |     | NULL    |                |
| tagline      | varchar(1000) | YES  |     | NULL    |                |
| vote_average | decimal(4,2)  | YES  |     | NULL    |                |
| vote_count   | int           | YES  |     | NULL    |                |
+--------------+---------------+------+-----+---------+----------------+
13 rows in set (0.00 sec)
~~~

Can you come up with 5 simple queries and 5 intermediate queries 
with sub-queries and ranking functions.


Here are **5 simple** and **5 intermediate** SQL queries using your `movie` table structure. These include subqueries and ranking functions where appropriate.

---

## ✅ 5 Simple Queries

These are straightforward SELECT queries without subqueries or complex logic.

---

### 19. **Get the Top 10 Highest Revenue Movies**

```sql
SELECT title, revenue
FROM movie
ORDER BY revenue DESC
LIMIT 10;
```

---

### 20. **Find Movies Released After 2020**

```sql
SELECT title, release_date
FROM movie
WHERE release_date > '2020-01-01';
```

---

### 21. **Get All Movies with Vote Average Above 8**

```sql
SELECT title, vote_average
FROM movie
WHERE vote_average > 8.0;
```

---

### 22. **Find Movies with Missing Taglines**

```sql
SELECT title
FROM movie
WHERE tagline IS NULL OR tagline = '';
```

---

### 23. **Count Movies by Status**

```sql
SELECT movie_status, COUNT(*) AS count
FROM movie
GROUP BY movie_status;
```

---

## 🧠 5 Intermediate Queries (with Subqueries & Ranking)

These use subqueries, window functions, or more advanced filtering.

---

### 24. **Find the Movie with the Highest Budget**

```sql
SELECT title, budget
FROM movie
WHERE budget = (SELECT MAX(budget) FROM movie);
```

---

### 25. **Top 5 Most Voted Movies Per Year (Using Window Function)**

```sql
WITH ranked_movies AS (
    SELECT 
        title,
        YEAR(release_date) AS year,
        vote_count,
        RANK() OVER (PARTITION BY YEAR(release_date) ORDER BY vote_count DESC) 
          AS the_rank
    FROM movie
    WHERE release_date IS NOT NULL
)
SELECT *
FROM ranked_movies
WHERE the_rank <= 5;
```

---

### 26. **Find Movies with Above-Average Popularity**

```sql
SELECT title, popularity
FROM movie
WHERE popularity > (SELECT AVG(popularity) FROM movie);
```

---

### 27. **Rank Movies by Revenue Within Each Year**

```sql
WITH ranked_revenue AS (
    SELECT 
        title,
        YEAR(release_date) AS year,
        revenue,
        RANK() OVER (PARTITION BY YEAR(release_date) ORDER BY revenue DESC) AS 
          revenue_rank
    FROM movie
    WHERE release_date IS NOT NULL
)
SELECT *
FROM ranked_revenue;
```

---

### 28. **Get the Second Highest Grossing Movie**

```sql
SELECT title, revenue
FROM movie
ORDER BY revenue DESC
LIMIT 1 OFFSET 1;
```

> 🔎 Alternate using subquery:

```sql
SELECT title, revenue
FROM movie
WHERE revenue = (
    SELECT MAX(revenue)
    FROM movie
    WHERE revenue < (
        SELECT MAX(revenue)
        FROM movie
    )
);
```

---

