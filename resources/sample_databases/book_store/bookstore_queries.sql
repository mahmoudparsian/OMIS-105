SELECT * FROM books;
SELECT * FROM customers;
SELECT * FROM orders;

-- 1) Retrieve all books in the "Fiction" genre:

SELECT *
FROM BOOKS
Where GENRE = 'FICTION'
;

-- 2) Retrieve the "average" price of all books:

SELECT AVG(PRICE)
AS AVG_PRICE
FROM BOOKS
;

-- 3) Show the top 5 most recently published books:

SELECT BOOK_ID, TITLE, AUTHOR, GENRE, PUBLISHED_YEAR
FROM BOOKS
ORDER BY PUBLISHED_YEAR ASC
LIMIT  5
;

-- 4) Count how many customers are from each country:

SELECT COUNTRY, COUNT(*) AS TOTAL_CUSTOMERS
FROM CUSTOMERS
GROUP BY COUNTRY
ORDER BY TOTAL_CUSTOMERS DESC
;

-- 5) Find books published after the year 1950:

SELECT *
FROM BOOKS
WHERE PUBLISHED_YEAR > '1950'
;

-- 6) List all customers from the Canada:

SELECT *
FROM CUSTOMERS
WHERE COUNTRY = 'CANADA'
;

-- 7) Show orders placed in November 2023:

SELECT *
FROM ORDERS
WHERE ORDER_DATE BETWEEN '2023-11-01' AND '2023-11-30'
;

-- 8) Retrieve the total stock of books available:

SELECT SUM(STOCK) AS TOTAL_STOCK
FROM BOOKS
;

-- 9) Find the details of the most expensive book:

SELECT *
FROM BOOKS
ORDER BY PRICE DESC
Limit 1
;

-- 10) Show all customers who ordered more than 1 quantity of a book:

SELECT *
FROM ORDERS
WHERE QUANTITY > 1
;

-- 11) Retrieve all orders where the total amount exceeds $20:

SELECT *
FROM ORDERS
WHERE TOTAL_AMOUNT > '20'
;

-- 12) List all genres available in the Books table:

SELECT DISTINCT GENRE
FROM BOOKS
;

-- 13) Find the book with the lowest stock:

SELECT *
FROM BOOKS
ORDER BY STOCK ASC
LIMIT 5
;

-- 14) Calculate the total revenue generated from all orders:

SELECT SUM(TOTAL_AMOUNT) 
AS TOTAL_REVENUE
FROM ORDERS
;

-- Advance Questions : 

-- 1) Retrieve the total number of books sold for each genre:

SELECT B.GENRE, SUM(O.QUANTITY) AS TOTAL_BOOKS_SOLD 
FROM ORDERS AS O
JOIN BOOKS AS B ON B.BOOK_ID = O.BOOK_ID
GROUP BY B.GENRE 
;

-- 2) Find the average price of books in the "Fantasy" genre:

SELECT AVG(PRICE) AS AVERAGE_PRICE
FROM BOOKS
WHERE GENRE ='FANTASY'
;

-- 3) List customers who have placed at least 2 orders:

SELECT O.CUSTOMER_ID , C.NAME, COUNT(O.ORDER_ID) AS ORDER_COUNT
FROM ORDERS AS O 
JOIN CUSTOMERS AS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY O.CUSTOMER_ID, C.NAME
HAVING COUNT(ORDER_ID) >= 2
 ;
 
-- 4) Find the most frequently ordered book:

SELECT BOOK_ID, COUNT(ORDER_ID) AS ORDER_COUNT
FROM ORDERS
GROUP BY BOOK_ID
ORDER BY ORDER_COUNT DESC 
LIMIT 3
;

-- 5) Show the top 3 most expensive books of 'Fantasy' Genre :

SELECT BOOK_ID, TITLE, AUTHOR, GENRE, PRICE
FROM BOOKS
WHERE GENRE = 'FANTASY'
ORDER BY PRICE DESC
LIMIT 3
;

-- 6) Retrieve the total quantity of books sold by each author:

SELECT B.AUTHOR, SUM(O.QUANTITY) AS TOTAL_BOOKS_SOLD
FROM ORDERS AS O
JOIN BOOKS AS B ON O.BOOK_ID = B.BOOK_ID
GROUP BY B.AUTHOR
;

-- 7) List the cities where customers who spent over $30 are located:

SELECT DISTINCT C.CITY, TOTAL_AMOUNT
FROM ORDERS AS O
JOIN CUSTOMERS AS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
WHERE O.TOTAL_AMOUNT > 30
;

-- 8) Find the customer who spent the most on orders:

SELECT C.CUSTOMER_ID, C.NAME, SUM(O.TOTAL_AMOUNT) AS TOTAL_SPENT
FROM ORDERS AS O
JOIN CUSTOMERS AS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.CUSTOMER_ID, C.Name
ORDER BY TOTAL_SPENT DESC
Limit 1
;







