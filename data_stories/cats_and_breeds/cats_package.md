# Cats, Breeds, Tricks Database Package

## Schema
```sql

CREATE DATABASE IF NOT EXISTS catshow;
USE catshow;

CREATE TABLE breeds (
    breed VARCHAR(20) PRIMARY KEY,
    description VARCHAR(128)
);

CREATE TABLE cats (
    cat_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    color VARCHAR(20),
    country VARCHAR(20),
    gender ENUM('MALE','FEMALE') NOT NULL,
    breed VARCHAR(20),
    price INT,
    FOREIGN KEY (breed) REFERENCES breeds(breed)
);

CREATE TABLE tricks (
    trick_id INT PRIMARY KEY,
    trick VARCHAR(40) UNIQUE NOT NULL
);

CREATE TABLE cat_tricks (
    cat_id INT,
    trick_id INT,
    PRIMARY KEY (cat_id, trick_id),
    FOREIGN KEY (cat_id) REFERENCES cats(cat_id),
    FOREIGN KEY (trick_id) REFERENCES tricks(trick_id)
);

```

## Sample Data
```sql
INSERT INTO breeds(breed, description) VALUES
('Persian','Long-haired, calm'),
('Siamese','Vocal, slender'),
('MaineCoon','Large, fluffy'),
('Bengal','Spotted, active'),
('Sphynx','Hairless, affectionate'),
('Ragdoll','Blue eyes, docile'),
('BritishShorthair','Round face, dense coat'),
('ScottishFold','Folded ears, sweet'),
('Abyssinian','Short hair, playful'),
('RussianBlue','Silver-blue, intelligent');
```
```sql
INSERT INTO tricks(trick_id, trick) VALUES
(1,'ring a bell'),
(2,'fetch'),
(3,'lie down'),
(4,'jumping'),
(5,'roll over'),
(6,'spin'),
(7,'high five'),
(8,'hoop jumping'),
(9,'sit'),
(10,'stand');
```
```sql
INSERT INTO cats(cat_id,name,date_of_birth,color,country,gender,breed,price) VALUES
(1,'Luna','2021-08-02','cream','GERMANY','MALE','Siamese',1928),
(2,'Milo','2018-10-13','silver','MEXICO','MALE','Siamese',4937),
(3,'Oliver','2020-05-14','cream','USA','MALE','Persian',2005),
(4,'Leo','2020-10-31','cream','MEXICO','MALE','RussianBlue',4564),
(5,'Loki','2020-05-09','brown','MEXICO','FEMALE','Bengal',153),
(6,'Bella','2022-04-04','silver','ITALY','FEMALE','MaineCoon',2376),
(7,'Chloe','2018-11-15','smoke','GERMANY','MALE','Bengal',859),
(8,'Simba','2020-02-18','white','GERMANY','FEMALE','Siamese',455),
(9,'Nala','2022-02-03','tabby','USA','FEMALE','ScottishFold',745),
(10,'Cleo','2021-02-04','smoke','MEXICO','FEMALE','Sphynx',4829),
(11,'Zoe','2019-01-29','cream','CANADA','FEMALE','Siamese',753),
(12,'Oscar','2022-10-18','smoke','USA','FEMALE','Bengal',2377),
(13,'Misty','2020-07-17','black','GERMANY','FEMALE','Ragdoll',1816),
(14,'Muffin','2021-10-04','silver','USA','MALE','Sphynx',4475),
(15,'Rocky','2022-02-02','black','ITALY','FEMALE','Bengal',2311),
(16,'Sasha','2023-03-11','black','GERMANY','MALE','Abyssinian',1976),
(17,'Pumpkin','2022-08-11','smoke','GERMANY','FEMALE','Persian',2293),
(18,'Ginger','2018-05-16','tabby','GERMANY','MALE','Bengal',4189),
(19,'Snowy','2020-03-21','black','GERMANY','MALE','ScottishFold',2120),
(20,'Salem','2022-03-06','tabby','GERMANY','FEMALE','Abyssinian',4880),
(21,'Coco','2020-03-28','black','CANADA','FEMALE','Ragdoll',844),
(22,'Mittens','2022-03-28','smoke','USA','MALE','Persian',1410),
(23,'Whiskers','2022-06-11','tabby','USA','FEMALE','BritishShorthair',3226),
(24,'Toby','2021-05-05','tabby','GERMANY','MALE','ScottishFold',1038),
(25,'Daisy','2021-10-28','smoke','GERMANY','FEMALE','Abyssinian',1013),
(26,'Mocha','2019-08-25','black','ITALY','MALE','BritishShorthair',2257),
(27,'Felix','2023-06-14','smoke','CANADA','MALE','Abyssinian',2544),
(28,'Smokey','2022-09-20','tabby','CANADA','MALE','Abyssinian',3163),
(29,'Lily','2022-04-11','tabby','MEXICO','MALE','MaineCoon',2755),
(30,'Shadow','2020-09-27','cream','GERMANY','FEMALE','Persian',2061),
(31,'Ruby','2018-04-29','tabby','USA','MALE','Bengal',4081),
(32,'Pearl','2022-07-30','smoke','MEXICO','MALE','Siamese',1151),
(33,'Sunny','2021-09-13','tabby','CANADA','FEMALE','ScottishFold',4422),
(34,'Jasper','2022-11-22','brown','CANADA','MALE','RussianBlue',2653),
(35,'Poppy','2020-03-28','brown','MEXICO','FEMALE','Ragdoll',1091),
(36,'Charlie','2019-05-23','cream','GERMANY','MALE','Bengal',4919),
(37,'Pepper','2021-02-08','tabby','CANADA','MALE','Bengal',681),
(38,'Mango','2021-12-20','black','USA','MALE','Persian',2806),
(39,'Marble','2018-05-26','black','GERMANY','FEMALE','Abyssinian',1855),
(40,'Ash','2021-01-09','silver','MEXICO','FEMALE','MaineCoon',2090),
(41,'Echo','2022-05-26','smoke','ITALY','MALE','ScottishFold',872),
(42,'Storm','2018-07-18','white','ITALY','FEMALE','BritishShorthair',3925),
(43,'Ivy','2022-11-05','silver','USA','MALE','Persian',3398),
(44,'Onyx','2022-01-31','smoke','USA','MALE','Ragdoll',1669),
(45,'Angel','2019-01-25','brown','CANADA','FEMALE','Abyssinian',1603),
(46,'Tiger','2019-07-25','black','USA','FEMALE','ScottishFold',4608),
(47,'Panda','2018-07-20','silver','MEXICO','MALE','Persian',864),
(48,'Hazel','2023-03-13','black','ITALY','FEMALE','Bengal',4043),
(49,'Cupcake','2019-03-14','cream','CANADA','FEMALE','BritishShorthair',117),
(50,'Midnight','2020-03-10','smoke','ITALY','FEMALE','Sphynx',3565),
(51,'Pearl2','2021-11-27','silver','ITALY','MALE','Abyssinian',1655),
(52,'Zelda','2019-08-31','cream','MEXICO','MALE','Bengal',2669),
(53,'Simone','2018-04-28','tabby','ITALY','MALE','Persian',565),
(54,'Cinder','2023-05-22','cream','CANADA','MALE','Abyssinian',4974),
(55,'Dusty','2018-05-20','brown','USA','MALE','Bengal',4842),
(56,'Fluffy','2021-05-02','tabby','USA','FEMALE','Persian',4881),
(57,'Momo','2021-03-03','white','GERMANY','MALE','Abyssinian',2673),
(58,'Zeus','2019-05-04','brown','CANADA','FEMALE','Sphynx',3845),
(59,'Thor','2019-10-10','cream','ITALY','MALE','Siamese',700),
(60,'Athena','2021-01-06','tabby','GERMANY','MALE','Bengal',2959);
```
```sql
INSERT INTO cat_tricks(cat_id,trick_id) VALUES
(55,2),
(58,1),
(45,1),
(36,7),
(50,6),
(47,7),
(28,3),
(5,1),
(5,10),
(19,9),
(30,9),
(51,7),
(9,8),
(11,5),
(2,2),
(57,2),
(48,8),
(35,8),
(24,8),
(29,4),
(7,1),
(7,10),
(18,10),
(55,4),
(54,6),
(56,3),
(59,2),
(45,3),
(47,9),
(27,6),
(36,9),
(28,5),
(8,2),
(5,3),
(9,1),
(30,2),
(52,8),
(41,8),
(57,4),
(46,4),
(35,1),
(32,5),
(13,10),
(38,9),
(40,6),
(6,4),
(18,3),
(15,7),
(21,2),
(49,9),
(29,6),
(39,10),
(53,9),
(54,8),
(22,3),
(45,5),
(37,1),
(27,8),
(37,10),
(5,5),
(17,7),
(60,5),
(51,2),
(8,4),
(19,4),
(41,1),
(3,8),
(52,10),
(43,7),
(32,7),
(41,10),
(24,3),
(26,9),
(15,9),
(16,8),
(7,5),
(21,4),
(18,5),
(6,6),
(54,1),
(55,8),
(31,8),
(22,5),
(36,4),
(27,1),
(3,1),
(45,7),
(28,9),
(5,7),
(30,6),
(9,5),
(52,3),
(43,9),
(32,9),
(33,8),
(24,5),
(13,5),
(49,4),
(15,2),
(18,7),
(7,7),
(39,5),
(53,4),
(31,1),
(20,1),
(31,10),
(22,7),
(47,6),
(20,10),
(37,5),
(17,2),
(28,2),
(56,9),
(5,9),
(60,9),
(50,8),
(41,5),
(43,2),
(52,5),
(11,4),
(24,7),
(15,4),
(13,7),
(16,3),
(25,6),
(26,4),
(18,9),
(55,3),
(54,5),
(56,2),
(12,8),
(14,5),
(37,7),
(17,4),
(4,4),
(50,1),
(43,4),
(32,4),
(44,3),
(10,1),
(42,6),
(33,3),
(35,9),
(26,6),
(25,8),
(16,5),
(18,2),
(1,7),
(53,8),
(40,8),
(20,5),
(22,2),
(45,4),
(12,1),
(34,4),
(31,5),
(29,8),
(12,10),
(3,7),
(14,7),
(4,6),
(60,4),
(51,1),
(50,3),
(5,4),
(51,10),
(52,9),
(32,6),
(42,8),
(33,5),
(44,5),
(10,3),
(25,1),
(1,9),
(25,10),
(7,4),
(39,2),
(53,1),
(29,1),
(40,10),
(54,9),
(20,7),
(29,10),
(6,8),
(34,6),
(5,6),
(58,9),
(55,10),
(51,3),
(50,5),
(52,2),
(59,8),
(42,1),
(30,8),
(10,5),
(13,4),
(35,4),
(25,3),
(57,10),
(40,3),
(29,3),
(54,2),
(31,9),
(22,6),
(21,8),
(23,5),
(37,4),
(20,9),
(58,2),
(4,10),
(50,7),
(52,4),
(32,1),
(30,1),
(43,1),
(41,4),
(42,3),
(8,1),
(19,10),
(10,7),
(2,3),
(16,2),
(57,3),
(46,3),
(48,9),
(39,6),
(29,5),
(20,2),
(6,3),
(31,2),
(23,7),
(14,4),
(3,4),
(58,4),
(36,1),
(59,3),
(36,10),
(50,9),
(28,6),
(30,3),
(33,2),
(42,5),
(17,6),
(1,6),
(11,8),
(16,4),
(46,5),
(48,2),
(49,1),
(38,1),
(38,10),
(6,5),
(26,8),
(22,1),
(31,4),
(23,9),
(14,6),
(55,7),
(58,6),
(53,10),
(36,3),
(47,3),
(12,9),
(59,5),
(17,8),
(8,5),
(44,4),
(30,5),
(19,5),
(28,8),
(11,10),
(2,7),
(57,7),
(39,1),
(15,1),
(49,3),
(15,10),
(40,9),
(6,7),
(20,6),
(18,6),
(53,3),
(45,8),
(47,5),
(36,5),
(27,2),
(17,1),
(28,10),
(30,7),
(10,4),
(19,7),
(8,7),
(43,10),
(46,9),
(48,6),
(15,3),
(29,2),
(49,5),
(18,8),
(21,7);
```

---

# Query Library
## 20 Basic Queries

**1. List all cats**
```sql
SELECT * FROM cats;
```

**2. List all breeds**
```sql
SELECT * FROM breeds;
```

**3. List all tricks**
```sql
SELECT * FROM tricks;
```

**4. Show cats from USA**
```sql
SELECT * FROM cats WHERE country='USA';
```

**5. Cats with black color**
```sql
SELECT * FROM cats WHERE color='black';
```

**6. Female cats only**
```sql
SELECT * FROM cats WHERE gender='FEMALE';
```

**7. Cats priced over 1000**
```sql
SELECT * FROM cats WHERE price>1000;
```

**8. Count all cats**
```sql
SELECT COUNT(*) FROM cats;
```

**9. Average price of cats**
```sql
SELECT AVG(price) FROM cats;
```

**10. Oldest cat**
```sql
SELECT * FROM cats ORDER BY date_of_birth LIMIT 1;
```

**11. Latest 5 cats**
```sql
SELECT * FROM cats ORDER BY date_of_birth DESC LIMIT 5;
```

**12. Breeds starting with 'S'**
```sql
SELECT * FROM breeds WHERE breed LIKE 'S%';
```

**13. Distinct colors**
```sql
SELECT DISTINCT color FROM cats;
```

**14. Distinct countries**
```sql
SELECT DISTINCT country FROM cats;
```

**15. Top 10 cats by price**
```sql
SELECT * FROM cats ORDER BY price DESC LIMIT 10;
```

**16. Names of all male cats**
```sql
SELECT name FROM cats WHERE gender='MALE';
```

**17. Cats born in 2020**
```sql
SELECT * FROM cats WHERE YEAR(date_of_birth)=2020;
```

**18. All Persian cats**
```sql
SELECT * FROM cats WHERE breed='Persian';
```

**19. All tricks containing 'jump'**
```sql
SELECT * FROM tricks WHERE trick LIKE '%jump%';
```

**20. Count tricks**
```sql
SELECT COUNT(*) FROM tricks;
```

## 20 Basic-to-Intermediate Queries

**1. Join cats with breeds**
```sql
SELECT c.name,b.description FROM cats c JOIN breeds b ON c.breed=b.breed;
```

**2. Join cats with their tricks**
```sql
SELECT c.name,t.trick FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id JOIN tricks t ON t.trick_id=ct.trick_id;
```

**3. Number of tricks per cat**
```sql
SELECT c.name,COUNT(ct.trick_id) FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id GROUP BY c.name;
```

**4. Cats with more than 3 tricks**
```sql
SELECT c.name FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id GROUP BY c.name HAVING COUNT(ct.trick_id)>3;
```

**5. Average price per breed**
```sql
SELECT breed,AVG(price) FROM cats GROUP BY breed;
```

**6. Count cats per country**
```sql
SELECT country,COUNT(*) FROM cats GROUP BY country;
```

**7. Breeds with average price >2000**
```sql
SELECT breed FROM cats GROUP BY breed HAVING AVG(price)>2000;
```

**8. Cats with no tricks**
```sql
SELECT c.* FROM cats c LEFT JOIN cat_tricks ct ON c.cat_id=ct.cat_id WHERE ct.trick_id IS NULL;
```

**9. Tricks with no cats**
```sql
SELECT t.* FROM tricks t LEFT JOIN cat_tricks ct ON t.trick_id=ct.trick_id WHERE ct.cat_id IS NULL;
```

**10. Most expensive cat per country**
```sql
SELECT country,MAX(price) FROM cats GROUP BY country;
```

**11. Cats and their age**
```sql
SELECT name,TIMESTAMPDIFF(YEAR,date_of_birth,CURDATE()) as age FROM cats;
```

**12. Trick count by breed**
```sql
SELECT b.breed,COUNT(ct.trick_id) FROM cats c JOIN breeds b ON c.breed=b.breed JOIN cat_tricks ct ON c.cat_id=ct.cat_id GROUP BY b.breed;
```

**13. Breeds with male/female counts**
```sql
SELECT breed,gender,COUNT(*) FROM cats GROUP BY breed,gender;
```

**14. Cats born before 2019**
```sql
SELECT * FROM cats WHERE date_of_birth<'2019-01-01';
```

**15. Average price per country**
```sql
SELECT country,AVG(price) FROM cats GROUP BY country;
```

**16. Top 5 cats with most tricks**
```sql
SELECT c.name,COUNT(ct.trick_id) cnt FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id GROUP BY c.cat_id ORDER BY cnt DESC LIMIT 5;
```

**17. Number of cats per breed**
```sql
SELECT breed,COUNT(*) FROM cats GROUP BY breed;
```

**18. Number of cats per color**
```sql
SELECT color,COUNT(*) FROM cats GROUP BY color;
```

**19. List cats with trick 'fetch'**
```sql
SELECT c.name FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id JOIN tricks t ON ct.trick_id=t.trick_id WHERE t.trick='fetch';
```

**20. List tricks learned by Persian cats**
```sql
SELECT DISTINCT t.trick FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id JOIN tricks t ON ct.trick_id=t.trick_id WHERE c.breed='Persian';
```

## 20 Intermediate Queries

**1. CTE: most expensive cat per breed**
```sql
WITH mx AS (
 SELECT breed,MAX(price) as maxp FROM cats GROUP BY breed
) SELECT c.name,c.breed,c.price FROM cats c JOIN mx ON c.breed=mx.breed AND c.price=mx.maxp;
```

**2. CTE: cats with above avg price in their breed**
```sql
WITH avgp AS (
 SELECT breed,AVG(price) av FROM cats GROUP BY breed
) SELECT c.name,c.breed,c.price FROM cats c JOIN avgp a ON c.breed=a.breed WHERE c.price>a.av;
```

**3. Rank cats by price per breed**
```sql
SELECT name,breed,price,RANK() OVER(PARTITION BY breed ORDER BY price DESC) rnk FROM cats;
```

**4. CTE: oldest cat per country**
```sql
WITH oldest AS (
 SELECT country,MIN(date_of_birth) d FROM cats GROUP BY country
) SELECT c.name,c.country,c.date_of_birth FROM cats c JOIN oldest o ON c.country=o.country AND c.date_of_birth=o.d;
```

**5. CTE: cats with at least 5 tricks**
```sql
WITH trick_counts AS (
 SELECT cat_id,COUNT(*) c FROM cat_tricks GROUP BY cat_id
) SELECT c.name FROM cats c JOIN trick_counts tc ON c.cat_id=tc.cat_id WHERE tc.c>=5;
```

**6. Cats with trick diversity (≥3)**
```sql
SELECT c.name,COUNT(DISTINCT t.trick) FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id JOIN tricks t ON t.trick_id=ct.trick_id GROUP BY c.name HAVING COUNT(DISTINCT t.trick)>=3;
```

**7. Breed with max avg price**
```sql
SELECT breed,AVG(price) av FROM cats GROUP BY breed ORDER BY av DESC LIMIT 1;
```

**8. Countries with >10 cats**
```sql
SELECT country,COUNT(*) FROM cats GROUP BY country HAVING COUNT(*)>10;
```

**9. CTE: trick popularity**
```sql
WITH pop AS (
 SELECT t.trick,COUNT(*) c FROM cat_tricks ct JOIN tricks t ON ct.trick_id=t.trick_id GROUP BY t.trick
) SELECT * FROM pop ORDER BY c DESC;
```

**10. CTE: gender ratio per breed**
```sql
WITH g AS (
 SELECT breed,gender,COUNT(*) c FROM cats GROUP BY breed,gender
) SELECT * FROM g;
```

**11. Window: order cats by dob**
```sql
SELECT name,date_of_birth,ROW_NUMBER() OVER(ORDER BY date_of_birth) rn FROM cats;
```

**12. Cats not in breed list**
```sql
SELECT * FROM cats WHERE breed NOT IN (SELECT breed FROM breeds);
```

**13. Average tricks per cat**
```sql
SELECT AVG(cnt) FROM (SELECT COUNT(*) cnt FROM cat_tricks GROUP BY cat_id) x;
```

**14. Cats with no breed info**
```sql
SELECT * FROM cats WHERE breed IS NULL;
```

**15. Top 3 most expensive cats**
```sql
SELECT * FROM cats ORDER BY price DESC LIMIT 3;
```

**16. Cats born in same year as 'Luna'**
```sql
SELECT * FROM cats WHERE YEAR(date_of_birth)=(SELECT YEAR(date_of_birth) FROM cats WHERE name='Luna');
```

**17. Tricks per country**
```sql
SELECT country,COUNT(ct.trick_id) FROM cats c JOIN cat_tricks ct ON c.cat_id=ct.cat_id GROUP BY country;
```

**18. Breeds with cats over 4000**
```sql
SELECT DISTINCT breed FROM cats WHERE price>4000;
```

**19. Cats with unique trick only**
```sql
SELECT c.name FROM cats c WHERE 1=(SELECT COUNT(*) FROM cat_tricks WHERE cat_id=c.cat_id);
```

**20. CTE: youngest cat per breed**
```sql
WITH y AS (SELECT breed,MAX(date_of_birth) d FROM cats GROUP BY breed)
 SELECT c.name,c.breed,c.date_of_birth FROM cats c JOIN y ON c.breed=y.breed AND c.date_of_birth=y.d;
```
