from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

# Flask app initialization
app = Flask(__name__)
CORS(app)

# MySQL database connection
connection = pymysql.connect(
    host='your-rds-endpoint',
    user='admin',
    password='your-password',
    database='flask_crud'
)

# ===========================
#        CRUD ROUTES
# ===========================

# ➡️ **Get All Users**
@app.route('/users', methods=['GET'])
def get_users():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return jsonify(users), 200

# ➡️ **Add a New User**
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (data['name'], data['email'], data['phone'], data['address'])
        )
        connection.commit()
    return jsonify({"message": "User added successfully"}), 201

# ➡️ **Update a User**
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE users SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s",
            (data['name'], data['email'], data['phone'], data['address'], id)
        )
        connection.commit()
    return jsonify({"message": "User updated successfully"}), 200

# ➡️ **Delete a User**
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        connection.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# ➡️ **Health Check Route**
@app.route('/', methods=['GET'])
def health_check():
    return "Flask CRUD Application is running!", 200

# ===========================
#        Run the App
# ===========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
