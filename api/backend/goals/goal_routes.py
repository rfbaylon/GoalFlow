from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

goals = Blueprint("goals", __name__)

@goals.route("/active", methods=["GET"])
def get_active_goals():
    try:
        cursor = db.get_db().cursor()
        query = "SELECT id, title, notes, schedule FROM goals g WHERE g.status = 'ACTIVE';"
        cursor.execute(query)
        goals_data = cursor.fetchall()
        cursor.close()
        return jsonify(goals_data), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_active_goals: {str(e)}')
        return jsonify({"error": str(e)}), 500
    

@goals.route("/all", methods=["GET"])
def get_all_goals():
    try:
        cursor = db.get_db().cursor()
        query = "SELECT id, title, notes, schedule, status FROM goals g;"
        cursor.execute(query)
        goals_data = cursor.fetchall()
        cursor.close()
        return jsonify(goals_data), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_goals: {str(e)}')
        return jsonify({"error": str(e)}), 500

@goals.route("/subgoals", methods=["GET"])
def get_subgoal():
    try:
        current_app.logger.info('Starting get_all_goals request')
        cursor = db.get_db().cursor()
        query = "SELECT g.id, sg.title FROM subgoals sg JOIN goals g ON g.id = sg.goalsid;"

        current_app.logger.debug(f'Executing query: {query}')
        cursor.execute(query)
        goals_data = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(goals_data)} NGOs')
        return jsonify(goals_data), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
        return jsonify({"error": str(e)}), 500
    

@goals.route("/<int:goal_id>/complete", methods=["PUT"])
def mark_goal_complete(goal_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM goals WHERE id = %s", (goal_id,))
        goal = cursor.fetchone()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        # Update goal status to completed (1)
        cursor.execute("UPDATE goals SET completed = 1, status = 'ARCHIVED' WHERE id = %s", (goal_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Goal marked as completed successfully"}), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500
    

@goals.route("/<int:goal_id>/delete", methods=["DELETE"])
def delete_goal(goal_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM goals WHERE id = %s", (goal_id,))
        goal = cursor.fetchone()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        # Update goal status to completed (1)
        cursor.execute("DELETE FROM goals WHERE id = %s", (goal_id,))
        db.get_db().commit()
        cursor.close() 

        return jsonify({"message": "Goal deleted"}), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500    

@goals.route("/creategoals", methods=["POST"])
def add_goal():
    try:
        data = request.get_json()
        user_id = data.get("userID")
        title = data.get("title")
        notes = data.get("notes")
        status = data.get("status", "ACTIVE")
        priority = data.get("priority", "low")
        schedule = data.get("schedule")  # YYYY-MM-DD

        cursor = db.get_db().cursor()
        query = """
            INSERT INTO goals (userId, title, notes, status, priority, schedule)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, title, notes, status, priority, schedule))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Goal added successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

