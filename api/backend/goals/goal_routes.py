from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

goals = Blueprint("goals", __name__)

@goals.route("/active", methods=["GET"])
def get_all_goals():
    try:
        cursor = db.get_db().cursor()
        query = "SELECT id, title, notes, schedule FROM goals g WHERE g.status = 'ACTIVE' LIMIT 3;"
        cursor.execute(query)
        goals_data = cursor.fetchall()
        cursor.close()
        return jsonify(goals_data), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
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
    



