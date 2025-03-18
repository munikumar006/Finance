from flask import Flask
import os

from fastapi import FastAPI
from routes.flask_routes import flask_bp
from routes.fastapi_routes import fastapi_router
from database.db import Database

# Initialize Flask
flask_app = Flask(__name__)
flask_app.register_blueprint(flask_bp)

# Initialize FastAPI
fastapi_app = FastAPI()

# Mount FastAPI on Flask
from asgi_tools.middleware import BaseMiddeware

flask_app.wsgi_app = ResponseMiddleware(fastapi_app, flask_app.wsgi_app)

fastapi_app.include_router(fastapi_router)

if __name__ == '__main__':
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

    db = Database()
    connection = db.get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(CREATE_TABLE_CHITS)
            cursor.execute(CREATE_TABLE_USERS)
            cursor.execute(CREATE_TABLE_ADMINS)
            connection.commit()
            print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
        
        import uvicorn
        uvicorn.run(flask_app, host="0.0.0.0", port=8000)
    else:
        print("Failed to establish database connection")
