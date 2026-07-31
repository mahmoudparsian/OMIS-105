To create a MySQL database that can store characters from many languages (e.g., English, Arabic, Chinese, Hindi, etc.), you should use utf8mb4 encoding instead of utf8.

👉 Reason:
    •    MySQL’s utf8 only supports up to 3 bytes per character (missing some Unicode characters like emojis, some CJK symbols).
    •    utf8mb4 supports the full Unicode range (4 bytes), making it the recommended choice for multilingual applications.

⸻

✅ Steps to Create a UTF-8 (utf8mb4) MySQL Database

-- Step 1: Create database with utf8mb4 encoding and collation
CREATE DATABASE multilingual_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

-- Step 2: Create a table inside it
USE multilingual_db;

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message_text VARCHAR(500) 
        CHARACTER SET utf8mb4 
        COLLATE utf8mb4_general_ci
);

-- Step 3: Insert multilingual data
INSERT INTO messages (message_text) VALUES
('Hello World'),                  -- English
('مرحبا بالعالم'),                -- Arabic
('你好，世界'),                     -- Chinese
('नमस्ते दुनिया'),                -- Hindi
('👋🌍');                          -- Emoji


⸻

🔍 Verification

To verify encoding:

SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';

Expected key results:
    •    character_set_server = utf8mb4
    •    collation_server = utf8mb4_general_ci (or utf8mb4_unicode_ci for more accurate sorting)

⸻

⚖️ Notes on Collation
    •    utf8mb4_general_ci → Faster, general use (case-insensitive).
    •    utf8mb4_unicode_ci → More linguistically accurate comparisons (slightly slower).
    •    utf8mb4_bin → Case-sensitive, binary-safe comparisons.

⸻

👉 Recommendation: Always use utf8mb4 for new databases to ensure full multilingual and emoji support.

Would you like me to also show how to set the MySQL server defaults so that all new databases and tables use utf8mb4 automatically?
