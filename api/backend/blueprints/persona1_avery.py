from flask import Blueprint, request, current_app, jsonify
from backend.db_connection import db
from mysql.connector import Error
from datetime import datetime
import re

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)

# Blueprint for Persona 1 (Avery)
persona1_bp = Blueprint("persona1", __name__, url_prefix="/persona1")

# Avery's profile
@persona1_bp.route("/me", methods=["GET"])
def me():
    
    try:
        user_id = int(request.args.get("userId", 1))
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            cur.close()
            return jsonify({"error": "user not found"}), 404

        cur.execute("SELECT * FROM user_data WHERE userId = %s ORDER BY (lastLogin IS NULL) ASC, lastLogin DESC, id DESC LIMIT 1", (user_id,))
        latest_data = cur.fetchone()

        cur.close()
        return jsonify({"user": user, "latest_user_data": latest_data}), 200

    except Error as e:
        current_app.logger.exception("DB error")
        return jsonify({"error": str(e)}), 500

# Posts
@persona1_bp.route("/posts", methods=["GET"])
def list_posts():
    try:
        user_id = int(request.args.get("userId", 1))
        limit = int(request.args.get("limit", 10))
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT p.*, t.name AS tagName, t.color AS tagColor FROM posts p LEFT JOIN tags t ON p.tag = t.id WHERE p.authorId = %s ORDER BY p.createdAt DESC, p.id DESC LIMIT %s", (user_id, limit))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows), 200

    except Error as e:
        current_app.logger.exception("DB error")
        return jsonify({"error": str(e)}), 500

# Post create
@persona1_bp.route("/posts", methods=["POST"])
def create_post():
    try:
        data = request.get_json(force=True) or {}
        user_id = int(data.get("userId", 1))
        title = (data.get("title") or "").strip()
        content = data.get("content")
        tag_id = data.get("tagId")
        meta_title = data.get("metaTitle")

        if not title or not tag_id:
            return jsonify({"error": "title and tagId are required"}), 400

        base_slug = slugify(title)
        slug = base_slug
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        conn = db.get_db()
        cur = conn.cursor()

        n = 1
        while True:
            cur.execute("SELECT 1 FROM posts WHERE slug = %s", (slug,))
            exists = cur.fetchone()
            if not exists:
                break
            n += 1
            slug = f"{base_slug}-{n}"

        cur.execute("""
            INSERT INTO posts (authorId, title, metaTitle, createdAt, publishedAt, slug, content, tag)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, title, meta_title, now, now, slug, content, int(tag_id)))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return jsonify({"message": "created", "post_id": new_id, "slug": slug}), 201

    except Error as e:
        current_app.logger.exception("DB error")
        return jsonify({"error": str(e)}), 500

# Daily tasks 
@persona1_bp.route("/daily-tasks", methods=["GET"])
def list_daily_tasks():
    try:
        user_id = int(request.args.get("userId", 1))
        date_str = request.args.get("date")  
        status = request.args.get("status")

        conn = db.get_db()
        cur = conn.cursor(dictionary=True)

        q = """SELECT dt.*, CONCAT_WS(' ', u.firstName, u.lastName) AS userName
        FROM daily_tasks dt
        JOIN users u ON dt.userId = u.id
        WHERE dt.userId = %s
        """
        params = [user_id]

        if date_str:
            q += " AND dt.schedule = %s"
            params.append(date_str)

        if status is not None:
            q += " AND dt.status = %s"
            params.append(int(status))

        q += " ORDER BY dt.schedule DESC, dt.id DESC"

        cur.execute(q, tuple(params))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows), 200

    except Error as e:
        current_app.logger.exception("DB error")
        return jsonify({"error": str(e)}), 500

# Daily task delete
@persona1_bp.route("/daily-tasks/<int:task_id>", methods=["DELETE"])
def delete_daily_task(task_id: int):
    try:
        user_id = int(request.args.get("userId", 1))
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT id FROM daily_tasks WHERE id = %s AND userId = %s", (task_id, user_id))
        row = cur.fetchone()
        if not row:
            cur.close()
            return jsonify({"error": "task not found"}), 404

        cur = conn.cursor()
        cur.execute("DELETE FROM daily_tasks WHERE id = %s", (task_id,))
        conn.commit()
        cur.close()
        return jsonify({"message": "deleted"}), 200

    except Error as e:
        current_app.logger.exception("DB error")
        return jsonify({"error": str(e)}), 500

# Goal update
@persona1_bp.route("/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id: int):
    try:
        user_id = int(request.args.get("userId", 1))
        data = request.get_json(force=True) or {}

        allowed = ["title", "notes", "onIce", "status", "priority", "completed", "schedule"]
        sets, params = [], []

        for k in allowed:
            if k in data and data[k] is not None:
                sets.append(f"{k} = %s")
                params.append(data[k])

        if not sets:
            return jsonify({"error": "no valid fields to update"}), 400

        conn = db.get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT id FROM goals WHERE id = %s AND userId = %s", (goal_id, user_id))
        row = cur.fetchone()
        if not row:
            cur.close()
            return jsonify({"error": "goal not found"}), 404

        q = f"UPDATE goals SET {', '.join(sets)} WHERE id = %s"
        params.append(goal_id)

        cur = conn.cursor()
        cur.execute(q, tuple(params))
        conn.commit()
        cur.close()
        return jsonify({"message": "updated"}), 200

    except Error as e:
        current_app.logger.exception("DB error")
        return jsonify({"error": str(e)}), 500
