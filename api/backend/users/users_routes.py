from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

users = Blueprint("users", __name__)

@users.route("/appstats", methods=["GET"])
def get_appstats():
    try:
        cursor = db.get_db().cursor()
        query = "SELECT userId, registeredAt FROM user_data;"
        cursor.execute(query)
        stats = cursor.fetchall()
        cursor.close()
        return jsonify(stats), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# @users.route("/users", methods=["GET"])
# def get_all_users():
#     try:
#         current_app.logger.info('Starting get_all_users request')
#         cursor = db.get_db().cursor()

#         # Get query parameters for filtering
#         firstname = request.args.get("firstName")
#         lastname = request.args.get("lastName")
#         phonenumber = request.args.get("phoneNumber")
#         email = request.args.get("email")
#         role = request.args.get("role")
        


#         current_app.logger.debug(f'Query parameters - firstName: {firstname}, lastName: {lastname}, phoneNumber: {phonenumber}, email: {email}, role: {role}')

#         # Prepare the Base query
#         query = "SELECT * FROM users WHERE 1=1"
#         params = []

#         # Add filters if provided
#         if firstname:
#             query += " AND firstName = %s"
#             params.append(firstname)
#         if lastname:
#             query += " AND lastName = %s"
#             params.append(lastname)
#         if phonenumber:
#             query += " AND phoneNumber = %s"
#             params.append(phonenumber)
#         if email:
#             query += " AND email = %s"
#             params.append(email)
#         if role:
#             query += " AND role = %s"
#             params.append(role)

#         current_app.logger.debug(f'Executing query: {query} with params: {params}')
#         cursor.execute(query, params)
#         results = cursor.fetchall()

#         # Get column names to map to dictionaries
#         columns = [col[0] for col in cursor.description]
#         users = [dict(zip(columns, row)) for row in results]
#         cursor.close()

#         current_app.logger.info(f'Successfully retrieved {len(users)} users')
#         return jsonify(users), 200
#     except Error as e:
#         current_app.logger.error(f'Database error in get_all_users: {str(e)}')
#         return jsonify({"error": str(e)}), 500

# @users.route("/get_user/<int:user_id>", methods=["GET"])
# def get_user(user_id):
#     try:
#         cursor = db.get_db().cursor()

#         cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#         user_row = cursor.fetchone()

#         if not user_row:
#             return jsonify({"error": "user not found"}), 404

#         columns = [col[0] for col in cursor.description]
#         user = dict(zip(columns, user_row))

#         cursor.close()
#         return jsonify(user), 200
    
#     except Error as e:
#         return jsonify({"error": str(e)}), 500

# @users.route("/create_users", methods=["POST"])
# def create_user():
#     try:
#         data = request.get_json()

#         # Validate required fields
#         required_fields = ["firstName", "lastName", "email", "role"]
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({"error": f"Missing required field: {field}"}), 400

#         cursor = db.get_db().cursor()

#         query = """
#         INSERT INTO users (firstName, middleName, lastName, phoneNumber, email, role, planType, manages)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(
#             query,
#             (
#                 data["firstName"],
#                 data.get["middleName"],
#                 data["lastName"],
#                 data["phoneNumber"],
#                 data["email"],
#                 data["role"],
#                 data.get("planType", "plan_name"),
#                 data.get("manages")
#             ),
#         )

#         db.get_db().commit()
#         new_user_id = cursor.lastrowid
#         cursor.close()

#         return (
#             jsonify({"message": "user created successfully", "user_id": new_user_id}),
#             201,
#         )
#     except Error as e:
#         return jsonify({"error": str(e)}), 500
    
# @users.route("/delete_users/<int:user_id>", methods = ["DELETE"])
# def delete_user(user_id):
#     try:
#         cursor = db.get_db().cursor()
        
#         cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#         user = cursor.fetchone()
#         if not user:
#             return jsonify({"error": "user not found"}), 404
        
#         cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#         db.get_db().commit()
#         cursor.close()

#         return jsonify({"message": "user deleted successfully"}), 200
#     except Error as e: 
#         return jsonify({"error": str(e)}), 500

# @users.route("/user_data/<int:user_data_id>", methods=["GET"])
# def get_user_data(user_data_id):
#     try:
#         cursor = db.get_db().cursor()
        
#         cursor.execute("SELECT * FROM user_data WHERE id = %s", (user_data_id,))
#         user_row = cursor.fetchone()

#         if not user_row:
#             return jsonify({"error": "user not found"}), 404

#         columns = [col[0] for col in cursor.description]
#         user_data = dict(zip(columns, user_row))

#         cursor.close()
#         return jsonify(user_data), 200
    
#     except Error as e:
#         return jsonify({"error": str(e)}), 500

