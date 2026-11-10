# First Normal Form (1NF) Examples
First Normal Form (1NF) means 

* every table cell holds only one single (atomic) value, and 
* there are no repeating lists or groups packed into a single column



# The Problem: Not in 1NF

Imagine a simple student table where one column lists multiple courses separated by commas: 

|`student_id`  | `student_name`   | `courses_enrolled` |
|------------|----------------|------------------|
|101         |John Smith      | Math, Physics    |
|102         | Sarah Lee      | History          |
|103         | Max Smith      | SQL, Java, AI    |


• Why it breaks 1NF: The Courses Enrolled (`courses_enrolled`)
cell contains multiple values packed together (Math, Physics), 
which makes searching or sorting difficult.

# The Fix: In 1NF

To make this table follow 1NF, you break the multi-valued 
cell so each row represents just one single fact/item: 

|`student_id`  | `student_name`   | `course` |
|------------|----------------|------------------|
|101         | John Smith      | Math |
|101         | John Smith     | Physics |
|102         | Sarah Lee      | History |
|103         | Max Smith      | SQL |
|103         | Max Smith      | Java    |
|103         | Max Smith      |  AI    |


## The Core Rules of 1NF

1. **Single Value per Cell**: No lists, arrays, or comma-separated values in a single box.
2. **Same Data Type**: Every value in a specific column must be the same kind of data (e.g., all dates or all text).
3. **Unique Rows**: Each row needs a unique identifier (like a Primary Key) so you can tell them apart.
4. **Unique Column Names**: No two columns can share the same name.

# The Fix: In 1NF : Deeper

Break `student_name` into `first_name` and `last_name`:

|`student_id`  | `first_name` | `last_name`  | `course` |
|------------|----------------|------------------|-------|
|101         | John | Smith      | Math |
|101         | John | Smith     | Physics |
|102         | Sarah | Lee      | History |
|103         | Max | Smith      | SQL |
|103         | Max | Smith      | Java    |
|103         | Max | Smith      |  AI    |


# Example: Repeating Columns

First Normal Form (1NF) requires that every cell in a table holds a single, indivisible value (an atomic value) and that you eliminate repeating groups or columns. 

## Before 1NF: A Table with Repeating Columns

Imagine a Student table that tracks up to three phone numbers using repeated columns (Phone1, Phone2, Phone3): 

|`student_id` |	`student_name`	| `phone1` | `phone2` | `phone3` |
|-------------|----------------|----------|----------|----------|
|101          |	Alice          | 555-1111  | 555-2222 | NULL  |
|102	         |Bob	          | 555-3333  | NULL | NULL |
|103	         |Charlie	        |555-4444  | 555-5555 |555-6666|


## Why this violates 1NF:

* It uses repeating columns (phone1, phone2, phone3) for the exact same type of data. 
* It leaves empty/null spaces for students who don't have three phone numbers. 
* It breaks if a student gets a 4th phone number (you’d have to redesign the table structure).

## After 1NF: Fixing It Two Ways

You can fix this violation in two standard ways to achieve 1NF:

### Approach 1: Flattening the Table (Single-Table 1NF)

You remove the repeating columns and give each phone number its own row. Alice now takes up two rows, and Bob takes up one: 

|`student_id`	 |`student_name` |`phone_number` |
|-------------|----------------|----------|
|101	|Alice	|555-1111|
|101	|Alice	|555-2222
|102	|Bob	|555-3333
|103	|Charlie	|555-4444
|103	|Charlie	|555-5555
|103	|Charlie	|555-6666

* Why it is 1NF: Every cell contains just one atomic value, and there are no duplicate phone columns. 

* The downside: Student names (Alice, Charlie) are repeated, which causes data redundancy. 

### Approach 2: Moving the Repeating Data to a Child Table (Relational 1NF)

Instead of cramming everything into one flat table, you split the data into a main table and a separate `student_phone` table linked by the `student_id`: 

**Table 1: `students`**

|`student_id`	| `student_name`|
|----|----|
|101	|Alice|
|102	|Bob|
|103	|Charlie|

**Table 2: `student_phone` (Child Table)**

|`phone_id`|	`student_id`| `phone_number`|
|----|----|----|
|1	|101	|555-1111|
|2	|101	|555-2222|
|3	|102	|555-3333|
|4	|103	|555-4444|
|5	|103	|555-5555|
|6	|103	|555-6666|

* **Why this is best:** <br>
* It satisfies 1NF completely while keeping your data clean, flexible, and free of wasted blank space. 

----

## Example

### Before 1NF: An Order Table with Repeating Columns
Imagine an `Order` table that tries to track up to 
three items purchased in a single transaction using 
`Item1`, `Item2`, and `Item3`:

| `order_id` | `customer_name` | `Item1` | `Item2` | `Item3` |
| :--- | :--- | :--- | :--- | :--- |
| 5001 | David | Laptop | Mouse | *null* |
| 5002 | Emma | Keyboard | *null* | *null* |
| 5003 | Frank | Monitor | Desk | Chair |

#### Why this violates 1NF:
* **Repeating data groups:** `Item1`, `Item2`, and `Item3` are identical types of data stamped across the columns.
* **Wasted storage:** Emma only bought one thing, leaving two columns empty (`null`).
* **Hard ceiling limit:** If Frank decides to buy a 4th item (like a lamp), the system breaks because there is no `Item4` column. 

---

### After 1NF: Fixing the Design

To make this table compliant with 1NF and ensure it 
can handle an unlimited number of items per order, 
we split it into a parent table and a child table.

**Table 1: `Orders` (Parent Table)**
This table only holds information that applies to the 
entire order as a single event.

| `order_id` | `customer_name` |
| :--- | :--- |
| 5001 | David |
| 5002 | Emma |
| 5003 | Frank |

**Table 2: `order_items` (Child Table / Repeating Group Extracted)**
Every single item purchased gets its own clean row, linked back to the main order via the `OrderID`.

| `order_item_id` | `order_id` | `item_name` |
| :--- | :--- | :--- |
| 1 | 5001 | Laptop |
| 2 | 5001 | Mouse |
| 3 | 5002 | Keyboard |
| 4 | 5003 | Monitor |
| 5 | 5003 | Desk |
| 6 | 5003 | Chair |


