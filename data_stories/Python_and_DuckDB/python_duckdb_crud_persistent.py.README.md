we want to show integration of python 
and duckdb by a simple .py program: 
python program will do the following: 
1. create a table 
sales(sale_id, customer, product, price, sale_date), 

2. add 4 records one by one, 

3. add 4 records in bulk kind, 

4. update a column of a record , 

5. update another column of another record, 

6. delete a record by sale_id, 

7. delete another record by a sale_id,  : 

show before and after queries. and make duckdb persistent.

View python_duckdb_crud_demo.py
Run it with python python_duckdb_crud_demo.py. Here's what it does across 7 steps:
Step 1 — Creates a persistent DuckDB database (sales_demo.duckdb on disk) and a sales(sale_id, customer, product, price, sale_date) table.
Step 2 — Inserts 4 records one-by-one using parameterized queries (Alice/Laptop, Bob/Mouse, Carol/Keyboard, David/Monitor). Shows the table after.
Step 3 — Inserts 4 records in bulk using executemany() (Eva/Headphones, Frank/Webcam, Grace/USB Hub, Henry/SSD Drive). Shows before and after.
Step 4 — Updates Bob's Mouse price from $29.99 to $24.99. Shows before and after.
Step 5 — Updates Grace's product from "USB Hub" to "Docking Station". Shows before and after.
Step 6 — Deletes sale_id=4 (David's Monitor). Shows before and after.
Step 7 — Deletes sale_id=6 (Frank's Webcam). Shows before and after.

The database file persists on disk — after the script ends, 
you can reconnect and the data is still there. 
The script also drops/recreates the table at the start, 
so it's safe to run multiple times.

