from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
from datetime import datetime

habits = Blueprint("habits", __name__)

@habits.route("/create", methods=["POST"])
def add_habit():
    try:
        data = request.get_json()
        uid = data.get("uid")
        title = data.get("title")
        notes = data.get("notes")

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not uid or not title:
            return jsonify({"error": "userID and title are required"}), 400

        cursor = db.get_db().cursor()
        query = """
            INSERT INTO daily_tasks (userId, title, notes, createdAt)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (uid, title, notes))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Successfully logged!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@habits.route("/delete_habit/<int:habit_id>", methods = ["DELETE"])
def delete_habit(habit_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM daily_tasks WHERE id = %s", (habit_id,))
        habit = cursor.fetchone()
        if not habit:
            return jsonify({"error": "habit not found"}), 404
        
        cursor.execute("DELETE FROM daily_tasks WHERE id = %s", (habit_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "habit deleted successfully"}), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500
    
@habits.route("/rename_habit/<int:habit_id>", methods=["PUT"])
def rename_habit(habit_id):
    try:
        data = request.get_json()

        # Check if NGO exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM daily_tasks WHERE id = %s", (habit_id,))
        if not cursor.fetchone():
            return jsonify({"error": "habit not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["userId", "title", "status"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(habit_id)
        query = f"UPDATE daily_tasks SET {', '.join(update_fields)} WHERE id = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "habit updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

@habits.route("/subgoals", methods=["GET"])
def get_subgoal():
    try:
        current_app.logger.info('Starting get_all_goals request')
        cursor = db.get_db().cursor()
        query = "SELECT sg.goalsId, sg.title FROM subgoals sg;"
        current_app.logger.debug(f'Executing query: {query}')
        cursor.execute(query)
        goals_data = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(goals_data)} NGOs')
        return jsonify(goals_data), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@habits.route("/archive", methods=["GET"])
def get_archive():
    try:
        cursor = db.get_db().cursor()
        query = "SELECT id, title, notes, schedule, completedAt FROM goals g WHERE g.status = 'ARCHIVED';"
        cursor.execute(query)
        goals_data = cursor.fetchall()
        cursor.close()
        return jsonify(goals_data), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_active_goals: {str(e)}')
        return jsonify({"error": str(e)}), 500