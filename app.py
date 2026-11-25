import os
import secrets
from functools import wraps

from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["API_KEY"] = os.getenv("API_KEY", "dev-only-change-me")

    if test_config:
        app.config.update(test_config)

    # In-memory storage for this learning project.
    app.tasks = []
    app.next_task_id = 1

    def error_response(message, status_code, details=None):
        response = {
            "success": False,
            "error": {
                "message": message,
                "status": status_code
            }
        }
        if details:
            response["error"]["details"] = details
        return jsonify(response), status_code

    def require_api_key(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            provided_key = request.headers.get("X-API-Key", "")
            expected_key = app.config.get("API_KEY", "")

            if not expected_key or not secrets.compare_digest(
                provided_key, expected_key
            ):
                return error_response(
                    "Missing or invalid API key.",
                    401
                )
            return view_function(*args, **kwargs)
        return decorated_function

    @app.get("/")
    def home():
        return jsonify({
            "success": True,
            "message": "SWYNEX Task 3 Secure Task Management API",
            "documentation": "See README.md for API usage and testing."
        }), 200

    @app.get("/health")
    def health():
        return jsonify({
            "success": True,
            "message": "API is running."
        }), 200

    @app.post("/api/tasks")
    @require_api_key
    def create_task():
        if not request.is_json:
            return error_response(
                "Request body must be valid JSON.",
                400
            )

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return error_response(
                "Request body must be a JSON object.",
                400
            )

        title = data.get("title")
        description = data.get("description", "")

        errors = {}

        if not isinstance(title, str) or not title.strip():
            errors["title"] = "Title is required and must be a non-empty string."
        elif len(title.strip()) > 100:
            errors["title"] = "Title must not exceed 100 characters."

        if not isinstance(description, str):
            errors["description"] = "Description must be a string."
        elif len(description) > 500:
            errors["description"] = "Description must not exceed 500 characters."

        if errors:
            return error_response(
                "Input validation failed.",
                400,
                errors
            )

        task = {
            "id": app.next_task_id,
            "title": title.strip(),
            "description": description.strip()
        }
        app.tasks.append(task)
        app.next_task_id += 1

        return jsonify({
            "success": True,
            "message": "Task created successfully.",
            "data": task
        }), 201

    @app.get("/api/tasks")
    @require_api_key
    def get_tasks():
        return jsonify({
            "success": True,
            "count": len(app.tasks),
            "data": app.tasks
        }), 200

    @app.get("/api/tasks/<int:task_id>")
    @require_api_key
    def get_task(task_id):
        task = next(
            (item for item in app.tasks if item["id"] == task_id),
            None
        )

        if task is None:
            return error_response("Task not found.", 404)

        return jsonify({
            "success": True,
            "data": task
        }), 200

    @app.errorhandler(404)
    def not_found(_error):
        return error_response("The requested resource was not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return error_response("HTTP method not allowed for this endpoint.", 405)

    @app.errorhandler(500)
    def internal_server_error(_error):
        return error_response("An internal server error occurred.", 500)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
