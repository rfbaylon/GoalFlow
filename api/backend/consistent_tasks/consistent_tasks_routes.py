from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

consistent_tasks = Blueprint("consistent_tasks", __name__)

@consistent_tasks.route("/get_consistent_tasks", methods=["GET"])
def get_all_tasks():
    try:
        current_app.logger.info('Starting get_all_tasks request')
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Get query parameters for filtering
        title = request.args.get("title")
        category = request.args.get("category")
        notes = request.args.get("notes")
        
        current_app.logger.debug(f'Query parameters - title: {title}, category: {category}, notes: {notes}')

        # Prepare the Base query
        query = "SELECT * FROM consistent_tasks WHERE 1=1"
        params = []

        # Add filters if provided
        if title:
            query += " AND title = %s"
            params.append(title)
        if category:
            query += " AND category = %s"
            params.append(category)
        if notes:
            query += " AND notes = %s"
            params.append(notes)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Get column names to map to dictionaries
        columns = [col[0] for col in cursor.description]
        consistent_tasks = [dict(zip(columns, row)) for row in results]
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(consistent_tasks)} consistent tasks')
        return jsonify(consistent_tasks), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_tasks: {str(e)}')
        return jsonify({"error": str(e)}), 500

@consistent_tasks.route("/create_consistent_task", methods=["POST"])
def create_task():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["userId", "title", "slug"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO consistent_tasks (userId, title, slug, category, notes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["userId"],
                data["title"],
                data["slug"],
                data.get("category", None), 
                data.get("notes", None),
            ),
        )

        db.get_db().commit()
        new_task_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "task created successfully", "task_id": new_task_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@consistent_tasks.route("/delete_consistent_task/<int:task_id>", methods = ["DELETE"])
def delete_task(task_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM consistent_tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if not task:
            return jsonify({"error": "task not found"}), 404
        
        cursor.execute("DELETE FROM consistent_tasks WHERE id = %s", (task_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "task deleted successfully"}), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500

@consistent_tasks.route("/consistent_task/<int:task_id>", methods=["PUT"])
def rename_task(task_id):
    try:
        data = request.get_json()

        # Check if NGO exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM consistent_tasks WHERE id = %s", (task_id,))
        if not cursor.fetchone():
            return jsonify({"error": "task not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["title", "category", "notes"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(task_id)
        query = f"UPDATE consistent_tasks SET {', '.join(update_fields)} WHERE id = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "task updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@consistent_tasks.route("/consistent_task/<int:task_id>", methods=["GET"])
def get_consistent_task(task_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM consistent_tasks WHERE id = %s", (task_id,))
        task_row = cursor.fetchone()

        if not task_row:
            return jsonify({"error": "user not found"}), 404

        columns = [col[0] for col in cursor.description]
        consistent_tasks = dict(zip(columns, task_row))

        cursor.close()
        return jsonify(consistent_tasks), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500   



