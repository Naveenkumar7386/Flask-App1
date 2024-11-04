# from flask import Flask, render_template, request, redirect
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # MySQL configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'  # Your MySQL username
# app.config['MYSQL_PASSWORD'] = 'G_naveen@2024'  # Your MySQL password
# app.config['MYSQL_DB'] = 'DEMO'

# mysql = MySQL(app)


# @app.route('/')
# def index():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT ID, NAME, AGE, GENDER FROM DEMO_TABLE")
#     users = cursor.fetchall()
#     cursor.close()
#     return render_template('index.html', users=users)


# @app.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         age = request.form['age']
#         gender = request.form['gender']

#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO DEMO_TABLE (NAME, AGE, GENDER) VALUES (%s, %s, %s)", (name, age, gender))
#         mysql.connection.commit()
#         cursor.close()
#         return redirect('/')
#     return render_template('add_user.html')


# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# import mysql.connector

# app = Flask(__name__)
# CORS(app)  # Enable CORS for the entire app

# # Database connection configuration
# db_config = {
#     'host': 'localhost',  # Update with your database host
#     'user': 'root',       # Update with your database user
#     'password': 'G_naveen@2024',  # Update with your database password
#     'database': 'DEMO'
# }

# # Establish connection
# def get_db_connection():
#     connection = mysql.connector.connect(**db_config)
#     return connection

# # Endpoint to get all records (GET request)
# @app.route('/api/records', methods=['GET'])
# def get_records():
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT Id, name, age, gender FROM DEMO_TABLE")
#         records = cursor.fetchall()
#         return jsonify(records)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         connection.close()

# # Endpoint to add a new record (POST request)
# @app.route('/api/add-record', methods=['POST'])
# def add_record():
#     try:
#         data = request.get_json()
#         name = data.get('name')
#         age = data.get('age')
#         gender = data.get('gender')

#         if not all([name, age, gender]):
#             return jsonify({'error': 'Missing data'}), 400

#         connection = get_db_connection()
#         cursor = connection.cursor()
#         query = "INSERT INTO DEMO_TABLE (name, age, gender) VALUES (%s, %s, %s)"
#         cursor.execute(query, (name, age, gender))
#         connection.commit()

#         return jsonify({'message': 'Record added successfully'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         connection.close()

# if __name__ == '__main__':
#     app.run(debug=True)



# Endpoint to delete a record (DELETE request)
# @app.route('/api/delete-record/<int:Id>', methods=['DELETE'])  # Changed to <int:Id>
# def delete_record(Id):
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("DELETE FROM DEMO_TABLE WHERE Id = %s", (Id,))  # Id remains unchanged
#         connection.commit()
#         return jsonify({'message': 'Record deleted successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         connection.close()


from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Database connection configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'G_naveen@2024'),
    'database': os.getenv('DB_NAME', 'DEMO')
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Endpoint to get all records (GET request)
@app.route('/api/records', methods=['GET'])
def get_records():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT Id, name, age, gender FROM DEMO_TABLE")
        records = cursor.fetchall()
        return jsonify(records)
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint to add a new record (POST request)
@app.route('/api/add-record', methods=['POST'])
def add_record():
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        if not all([name, age, gender]):
            return jsonify({'error': 'Missing data'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO DEMO_TABLE (name, age, gender) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, gender))
        connection.commit()

        return jsonify({'message': 'Record added successfully'}), 201
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint to update a record (PATCH request)
@app.route('/api/update-record/<int:Id>', methods=['PATCH'])
def update_record(Id):
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        if not all([name, age, gender]):
            return jsonify({'error': 'Missing data'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE DEMO_TABLE SET name = %s, age = %s, gender = %s WHERE Id = %s"
        cursor.execute(query, (name, age, gender, Id))
        connection.commit()

        return jsonify({'message': 'Record updated successfully'}), 200
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint to delete a record (DELETE request)
@app.route('/api/delete-record/<int:id>', methods=['DELETE'])
def delete_record(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if the record exists
        cursor.execute("SELECT * FROM DEMO_TABLE WHERE Id = %s", (id,))
        record = cursor.fetchone()
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        # Proceed to delete the record
        cursor.execute("DELETE FROM DEMO_TABLE WHERE Id = %s", (id,))
        connection.commit()
        return jsonify({'message': 'Record deleted successfully'}), 200
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

