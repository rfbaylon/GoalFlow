from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

tags = Blueprint("tags", __name__)

@tags.route("/get_tag", methods=["GET"])
def get_all_tags():
    try:
        current_app.logger.info('Starting get_all_tags request')
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        name = request.args.get("name")
        color = request.args.get("color")
        
        current_app.logger.debug(f'Query parameters - name: {name}, color: {color}')

        # Prepare the Base query
        query = "SELECT * FROM tags WHERE 1=1"
        params = []

        # Add filters if provided
        if name:
            query += " AND name = %s"
            params.append(name)
        if color:
            query += " AND color = %s"
            params.append(color)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Get column names to map to dictionaries
        columns = [col[0] for col in cursor.description]
        tags_list = [dict(zip(columns, row)) for row in results]
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(tags_list)} tags')
        return jsonify(tags_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_tags: {str(e)}')
        return jsonify({"error": str(e)}), 500

@tags.route("/create_tag", methods=["POST"])
def create_tag():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["color"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO tags (name, color)
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (
                data.get("name"),
                data.get("color"),  # <-- FIXED
            ),
        )

        db.get_db().commit()
        new_tag_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "tag created successfully", "tag_id": new_tag_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@tags.route("/delete_tag/<int:tag_id>", methods = ["DELETE"])
def delete_tags(tag_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM tags WHERE id = %s", (tag_id,))
        tag = cursor.fetchone()
        if not tag:
            return jsonify({"error": "tag not found"}), 404
        
        cursor.execute("DELETE FROM tags WHERE id = %s", (tag_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "tag deleted successfully"}), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500

@tags.route("/rename_tag/<int:tag_id>", methods=["PUT"])
def rename_tag(tag_id):
    try:
        data = request.get_json()

        # Check if NGO exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM tags WHERE id = %s", (tag_id,))
        if not cursor.fetchone():
            return jsonify({"error": "tag not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["name", "color"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(tag_id)
        query = f"UPDATE tags SET {', '.join(update_fields)} WHERE id = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "tag updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

@tags.route("/goals/<int:goal_id>/tags", methods=["GET"])
def get_goal_tags(goal_id):
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT t.id, t.name, t.color
        FROM tags t
        JOIN goals_tags gt ON gt.tag_id = t.id
        WHERE gt.goal_id = %s
    """, (goal_id,))
    return jsonify(cursor.fetchall())
