-- authors
CREATE TABLE authors (
   author_id INT PRIMARY KEY,
   name VARCHAR NOT NULL,
   email VARCHAR NOT NULL UNIQUE,
   age INT,
   country VARCHAR NOT NULL
);

-- books
CREATE TABLE books (
   book_id VARCHAR PRIMARY KEY,
   author_id INT,
   title VARCHAR NOT NULL,
   category VARCHAR NOT NULL,
   publication_year INT NOT NULL,
   -- every books.author_id must exist in authors
   FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- orders
CREATE TABLE orders (
   order_id INT PRIMARY KEY,
   book_id VARCHAR NOT NULL,
   sale_price INT NOT NULL,
   order_date DATE NOT NULL,
   -- every orders.book_id must exist in books
   FOREIGN KEY (book_id) REFERENCES books(book_id)
);
