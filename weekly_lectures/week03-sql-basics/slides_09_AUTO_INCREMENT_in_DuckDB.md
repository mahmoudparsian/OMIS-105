# AUTO-INCREMENT Column in DuckDB

1. DuckDB does not directly support 
   AUTO-INCREMENT in `CREATE TABLE` syntax. 
   DuckDB implements and manages 
   auto-incrementing fields/columns 
   explicitly using `SEQUENCE`s.

2. MySQL has a concept of AUTO-INCREMENT 
   feature, demonstrated below.


## 1. AUTO-INCREMENT in MySQL

In MySQL, the `AUTO_INCREMENT` attribute automatically 
generates a unique, sequential number for a column 
(typically a `PRIMARY KEY`) whenever a new row is 
added. By default, it starts at `1` and increases 
by `1` with each new record.

```sql
% mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  
Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 26.7.0 MySQL Community Server - GPL

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| db11               |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.005 sec)

mysql> use db11;
Database changed
mysql> show tables;
Empty set (0.002 sec)

mysql> CREATE TABLE users (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     username VARCHAR(50) NOT NULL,
    ->     email VARCHAR(100) NOT NULL
    -> );
Query OK, 0 rows affected (0.006 sec)

mysql> DESC users;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| username | varchar(50)  | NO   |     | NULL    |                |
| email    | varchar(100) | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
3 rows in set (0.006 sec)

mysql> INSERT INTO users (username, email) 
VALUES 
('alice_dev', 'alice@example.com'),
('bob_codes', 'bob@example.com'),
('charlie_ux', 'charlie@example.com');

mysql> SELECT * from users;
+----+------------+---------------------+
| id | username   | email               |
+----+------------+---------------------+
|  1 | alice_dev  | alice@example.com   |
|  2 | bob_codes  | bob@example.com     |
|  3 | charlie_ux | charlie@example.com |
+----+------------+---------------------+
3 rows in set (0.001 sec)
```

## 2. AUTO-INCREMENT in DuckDB

The Correct way in DuckDB v1.5.5:

You must explicitly create a `SEQUENCE` first, 
and then pass `nextval('your_sequence_name')` 
as the default value for the column.

The following examples are in DuckDB:

```sql
-- Step-1. Create a sequence
CREATE SEQUENCE user_id_seq START 1;

-- Step-2. Create the table using nextval()
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY DEFAULT nextval('user_id_seq'),
  username VARCHAR NOT NULL,
  email VARCHAR
);

INSERT INTO users(username, email)
VALUES
    ('maxp', 'maxp@yahoo.com'),
    ('janexd', 'janexd@gmail.com'), 
    ('alexp', 'alexp@yahoo.com');
 
SELECT * FROM users;
┌─────────┬──────────┬──────────────────┐
│ user_id │ username │      email       │
│  int64  │ varchar  │     varchar      │
├─────────┼──────────┼──────────────────┤
│       1 │ maxp     │ maxp@yahoo.com   │
│       2 │ janexd   │ janexd@gmail.com │
│       3 │ alexp    │ alexp@yahoo.com  │
└─────────┴──────────┴──────────────────┘
 
INSERT INTO users(user_id, username, email)
VALUES
 (1000, 'dddmaxp', 'dddmaxp@yahoo.com'),
 (1003, 'dddjanexd', 'ddjanexd@gmail.com'),
 (1007, 'dddalexp', 'dddalexp@yahoo.com');
 
 SELECT * FROM users;
┌─────────┬───────────┬────────────────────┐
│ user_id │ username  │       email        │
│  int64  │  varchar  │      varchar       │
├─────────┼───────────┼────────────────────┤
│       1 │ maxp      │ maxp@yahoo.com     │
│       2 │ janexd    │ janexd@gmail.com   │
│       3 │ alexp     │ alexp@yahoo.com    │
│    1000 │ dddmaxp   │ dddmaxp@yahoo.com  │
│    1003 │ dddjanexd │ ddjanexd@gmail.com │
│    1007 │ dddalexp  │ dddalexp@yahoo.com │
└─────────┴───────────┴────────────────────┘
 
INSERT INTO users(username, email)
VALUES
    ('maxppppp', 'maxpppp@yahoo.com'),
    ('janexdppp', 'janexdppp@gmail.com'),
    ('alexpppp', 'alexpppp@yahoo.com');
 
SELECT * FROM users;
┌─────────┬───────────┬─────────────────────┐
│ user_id │ username  │        email        │
│  int64  │  varchar  │       varchar       │
├─────────┼───────────┼─────────────────────┤
│       1 │ maxp      │ maxp@yahoo.com      │
│       2 │ janexd    │ janexd@gmail.com    │
│       3 │ alexp     │ alexp@yahoo.com     │
│    1000 │ dddmaxp   │ dddmaxp@yahoo.com   │
│    1003 │ dddjanexd │ ddjanexd@gmail.com  │
│    1007 │ dddalexp  │ dddalexp@yahoo.com  │
│       4 │ maxppppp  │ maxpppp@yahoo.com   │
│       5 │ janexdppp │ janexdppp@gmail.com │
│       6 │ alexpppp  │ alexpppp@yahoo.com  │
└─────────┴───────────┴─────────────────────┘
 

CREATE TABLE test_users (
    user_id INT PRIMARY KEY DEFAULT nextval('user_id_seq'),
    username VARCHAR NOT NULL,
    email VARCHAR
);
 
INSERT INTO test_users (username, email)
VALUES 
('alex', 'a@yahoo.com'),
('bob', 'b@yahoo.com');
 
SELECT * 
FROM  test_users;
┌─────────┬──────────┬─────────────┐
│ user_id │ username │    email    │
│  int32  │ varchar  │   varchar   │
├─────────┼──────────┼─────────────┤
│       7 │ alex     │ a@yahoo.com │
│       8 │ bob      │ b@yahoo.com │
└─────────┴──────────┴─────────────┘
```

## 3. More Examples in DuckDB

```sql
memory D CREATE SEQUENCE user_id_seq START 1;

memory D -- 2. Create the table using nextval()
memory D CREATE TABLE users (
           user_id BIGINT PRIMARY KEY 
              DEFAULT nextval('user_id_seq'),
           username VARCHAR NOT NULL,
           email VARCHAR
         );

memory D DESC users;
┌──────────────────────────────────────────────────────────┐
│                          users                           │
│                                                          │
│ user_id  bigint  not null default nextval('user_id_seq') │
│ username varchar not null                                │
│ email    varchar                                         │
└──────────────────────────────────────────────────────────┘

memory D INSERT INTO users(username, email)
         VALUES
         ('alexp', 'alexp@yahoo.com'),
         ('janet', 'janet@gmail.com'),
         ('mo', 'mo@gmail.com');

memory D SELECT * FROM users;
┌─────────┬──────────┬─────────────────┐
│ user_id │ username │      email      │
│  int64  │ varchar  │     varchar     │
├─────────┼──────────┼─────────────────┤
│       1 │ alexp    │ alexp@yahoo.com │
│       2 │ janet    │ janet@gmail.com │
│       3 │ mo       │ mo@gmail.com    │
└─────────┴──────────┴─────────────────┘
memory D
memory D INSERT INTO users(username, email)
         VALUES
         ('ted', 'ted@yahoo.com'),
         ('austin', 'austin@gmail.com'),
         ('max', 'max@gmail.com');

memory D SELECT * FROM users;
┌─────────┬──────────┬──────────────────┐
│ user_id │ username │      email       │
│  int64  │ varchar  │     varchar      │
├─────────┼──────────┼──────────────────┤
│       1 │ alexp    │ alexp@yahoo.com  │
│       2 │ janet    │ janet@gmail.com  │
│       3 │ mo       │ mo@gmail.com     │
│       4 │ ted      │ ted@yahoo.com    │
│       5 │ austin   │ austin@gmail.com │
│       6 │ max      │ max@gmail.com    │
└─────────┴──────────┴──────────────────┘
memory D INSERT INTO users(user_id, username, email)
        VALUES
         (1000, 'tedx', 'tedx@yahoo.com'),
         (2000, 'austinp', 'austinp@gmail.com');

memory D SELECT * FROM users;
┌─────────┬──────────┬───────────────────┐
│ user_id │ username │       email       │
│  int64  │ varchar  │      varchar      │
├─────────┼──────────┼───────────────────┤
│       1 │ alexp    │ alexp@yahoo.com   │
│       2 │ janet    │ janet@gmail.com   │
│       3 │ mo       │ mo@gmail.com      │
│       4 │ ted      │ ted@yahoo.com     │
│       5 │ austin   │ austin@gmail.com  │
│       6 │ max      │ max@gmail.com     │
│    1000 │ tedx     │ tedx@yahoo.com    │
│    2000 │ austinp  │ austinp@gmail.com │
└─────────┴──────────┴───────────────────┘

memory D INSERT INTO users(username, email)
         VALUES
            ('aaaatedx', 'tedx@yahoo.com'),
            ('aaaaustinp', 'austinp@gmail.com');

memory D SELECT * FROM users;
┌─────────┬────────────┬───────────────────┐
│ user_id │  username  │       email       │
│  int64  │  varchar   │      varchar      │
├─────────┼────────────┼───────────────────┤
│       1 │ alexp      │ alexp@yahoo.com   │
│       2 │ janet      │ janet@gmail.com   │
│       3 │ mo         │ mo@gmail.com      │
│       4 │ ted        │ ted@yahoo.com     │
│       5 │ austin     │ austin@gmail.com  │
│       6 │ max        │ max@gmail.com     │
│    1000 │ tedx       │ tedx@yahoo.com    │
│    2000 │ austinp    │ austinp@gmail.com │
│       7 │ aaaatedx   │ tedx@yahoo.com    │
│       8 │ aaaaustinp │ austinp@gmail.com │
└─────────┴────────────┴───────────────────┘
  10 rows                        3 columns


memory D CREATE SEQUENCE testers_id_seq START 1000;

memory D CREATE TABLE test_users (
     user_id BIGINT PRIMARY KEY DEFAULT nextval('testers_id_seq'),
     username VARCHAR NOT NULL
  );
         
memory D DESC test_users;
┌─────────────────────────────────────────────────────────────┐
│                         test_users                          │
│                                                             │
│ user_id  bigint  not null default nextval('testers_id_seq') │
│ username varchar not null                                   │
└─────────────────────────────────────────────────────────────┘

memory D INSERT INTO test_users (username)
         VALUES
         ('alex'), ('bob'), ('jane'), ('ted');

memory D SELECT * FROM test_users;
┌─────────┬──────────┐
│ user_id │ username │
│  int64  │ varchar  │
├─────────┼──────────┤
│    1000 │ alex     │
│    1001 │ bob      │
│    1002 │ jane     │
│    1003 │ ted      │
└─────────┴──────────┘

memory D select  * FRom test_users;
┌─────────┬──────────┐
│ user_id │ username │
│  int64  │ varchar  │
├─────────┼──────────┤
│    1000 │ alex     │
│    1001 │ bob      │
│    1002 │ jane     │
│    1003 │ ted      │
└─────────┴──────────┘

memory D SELECT * FROM test_users;
┌─────────┬──────────┐
│ user_id │ username │
│  int64  │ varchar  │
├─────────┼──────────┤
│    1000 │ alex     │
│    1001 │ bob      │
│    1002 │ jane     │
│    1003 │ ted      │
└─────────┴──────────┘

memory D INSERT INTO test_users (user_id, username)
         VALUES
         (2000, 'alex'), 
         (3000, 'bob'), 
         (4000, 'jane'), 
         (5000, 'ted');
         
memory D SELECT * FROM test_users;
┌─────────┬──────────┐
│ user_id │ username │
│  int64  │ varchar  │
├─────────┼──────────┤
│    1000 │ alex     │
│    1001 │ bob      │
│    1002 │ jane     │
│    1003 │ ted      │
│    2000 │ alex     │
│    3000 │ bob      │
│    4000 │ jane     │
│    5000 │ ted      │
└─────────┴──────────┘
memory D INSERT INTO test_users (username)
         VALUES
         ('alexp'), 
         ('bobp'), 
         ('janep'), 
         ('tedp');
         
memory D SELECT * FROM test_users;
┌─────────┬──────────┐
│ user_id │ username │
│  int64  │ varchar  │
├─────────┼──────────┤
│    1000 │ alex     │
│    1001 │ bob      │
│    1002 │ jane     │
│    1003 │ ted      │
│    2000 │ alex     │
│    3000 │ bob      │
│    4000 │ jane     │
│    5000 │ ted      │
│    1004 │ alexp    │
│    1005 │ bobp     │
│    1006 │ janep    │
│    1007 │ tedp     │
└─────────┴──────────┘
  12 rows  2 columns

```

## 4. References

[1. CREATE SEQUENCE Statement in DuckDB](https://duckdb.org/docs/lts/sql/statements/create_sequence)

[2. Using AUTO_INCREMENT in MySQL](https://dev.mysql.com/doc/refman/9.7/en/example-auto-increment.html)
