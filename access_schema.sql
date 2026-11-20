-- MEMBER B: page access table (run AFTER schema.sql)
USE access_demo;

CREATE TABLE IF NOT EXISTS user_pages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    page_name VARCHAR(20) NOT NULL,
    UNIQUE KEY uniq_user_page (user_id, page_name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);