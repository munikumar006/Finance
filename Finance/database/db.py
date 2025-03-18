# SQL to create the table
CREATE_TABLE_CHITS = """
CREATE TABLE IF NOT EXISTS `chits` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `chit_name` VARCHAR(100) NOT NULL,
    `amount` DECIMAL(10, 2) NOT NULL,
    `duration_months` INT NOT NULL,
    `total_members` INT NOT NULL,
    `status` ENUM('active', 'completed') DEFAULT 'active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

CREATE_TABLE_ADMINS = """
CREATE TABLE IF NOT EXISTS `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""


import mysql.connector
from mysql.connector import Error
import os

class Database:
    def __init__(self):
        self.connection = None
        try:
            # First connect without database to create it
            temp_conn = mysql.connector.connect(
                host="localhost",
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "1611")

            )
            cursor = temp_conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS chit_fund_db")
            temp_conn.close()

            # Then connect with database
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1611",
                database="chit_fund_db"
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            # Optionally, log the error or raise an exception


    def get_connection(self):
        return self.connection
