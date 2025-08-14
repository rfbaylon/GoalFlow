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