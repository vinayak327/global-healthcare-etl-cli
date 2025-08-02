CREATE TABLE IF NOT EXISTS daily_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_date DATE NOT NULL,
    country_name VARCHAR(255) NOT NULL,
    total_cases BIGINT,
    new_cases INT,
    total_deaths BIGINT,
    new_deaths INT,
    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (report_date, country_name)
);
