from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

support = Blueprint("support", __name__)

@support.route("/bugs", methods=["GET"])
def get_appstats():
    try:
        cursor = db.get_db().cursor()
        query = "SELECT title, description, id, priority, completed FROM bug_reports WHERE completed = 0;"
        cursor.execute(query)
        stats = cursor.fetchall()
        cursor.close()
        return jsonify(stats), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@support.route("/bugs/<int:bug_id>/complete", methods=["PUT"])
def mark_bug_complete(bug_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM bug_reports WHERE id = %s", (bug_id,))
        bug = cursor.fetchone()
        if not bug:
            return jsonify({"error": "Bug not found"}), 404
        # Update bug status to completed (1)
        cursor.execute("UPDATE bug_reports SET completed = 1 WHERE id = %s", (bug_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Bug marked as completed successfully"}), 200
    except Error as e: 
        return jsonify({"error": str(e)}), 500


support.route("/bug_reports", methods=["GET"])
def get_bug_reports():
    try:
        current_app.logger.info('Starting get_bug_reports request')
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        userId = request.args.get("userId")
        title = request.args.get("title")
        description = request.args.get("description")
        status = request.args.get("status")
        priority = request.args.get("priority")
        
        current_app.logger.debug(f'Query parameters - userId: {userId}, title: {title}, description: {description}, status: {status}, priority: {priority}')

        # Prepare the Base query
        query = "SELECT * FROM bug_reports WHERE 1=1"
        params = []

        # Add filters if provided
        if userId:
            query += " AND userId = %s"
            params.append(userId)
        if title:
            query += " AND title = %s"
            params.append(title)
        if description:
            query += " AND description = %s"
            params.append(description)
        if status:
            query += " AND status = %s"
            params.append(status)
        if priority:
            query += " AND priority = %s"
            params.append(priority)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Get column names to map to dictionaries
        columns = [col[0] for col in cursor.description]
        bug_reports = [dict(zip(columns, row)) for row in results]
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(bug_reports)} bug reports')
        return jsonify(bug_reports), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_bug_reports: {str(e)}')
        return jsonify({"error": str(e)}), 500

@support.route("/bug_reports/<int:bug_reports_id>", methods=["PUT"])
def archive_bug_report(bug_report_id):
    try:
        data = request.get_json()

        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM bug_reports WHERE id = %s", (bug_report_id,))
        if not cursor.fetchone():
            return jsonify({"error": "bug report not found"}), 404
        
        query = 'UPDATE bug_reports SET status = 1 WHERE id = %s'
        cursor.execute(query, (bug_report_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "bug report updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    
@support.route("/appstats", methods=["GET"])
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