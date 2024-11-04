from flask import Flask, jsonify, request
import mysql.connector
import os
import logging

app = Flask(__name__)

# Configure logging for better debugging
logging.basicConfig(level=logging.ERROR)

@app.route('/api/records', methods=['GET'])
def get_records():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "G_naveen@2024"),
            database=os.getenv("DB_NAME", "DEMO")
        )

        # Check if the connection was successful
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM demo_table")
            records = cursor.fetchall()
            return jsonify(records)
        else:
            app.logger.error("Failed to connect to the database.")
            return jsonify({"error": "Database connection failed"}), 500

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        # Safely close the cursor and connection if they were created
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            connection.close()

if __name__ == "__main__":
    # Run the app on the Render-provided port or default to 5000
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
