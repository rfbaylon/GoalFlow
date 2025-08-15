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
        userId = data.get("userId")
        title = data.get("title")
        notes = data.get("notes")

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not userId or not title:
            return jsonify({"error": "userID and title are required"}), 400

        cursor = db.get_db().cursor()
        query = """
            INSERT INTO daily_tasks (userId, title, notes, completed, status)
            VALUES (%s, %s, %s, 1, "ARCHIVED")
        """
        cursor.execute(query, (userId, title, notes))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Successfully logged!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500