-- Create the table
CREATE TABLE sales (
    id INTEGER,
    item VARCHAR,
    category VARCHAR,
    price DECIMAL(5,2),
    quantity INTEGER
);

-- Insert exactly 10 rows of data
INSERT INTO sales VALUES 
(1, 'Latte', 'Beverage', 4.50, 2),
(2, 'Croissant', 'Bakery', 3.00, 1),
(3, 'Cappuccino', 'Beverage', 4.00, 3),
(4, 'Muffin', 'Bakery', 2.50, 4),
(5, 'Espresso', 'Beverage', 2.50, 1),
(6, 'Croissant', 'Bakery', 3.00, 2),
(7, 'Latte', 'Beverage', 4.50, 1),
(8, 'Bagel', 'Bakery', 3.50, 3),
(9, 'Tea', 'Beverage', 3.00, 2),
(10, 'Muffin', 'Bakery', 2.50, 1);
