# SWYNEX – Authentication, Validation, and Integration

## Project overview
This project is a beginner-friendly Flask REST API demonstrating API-key authentication, request validation, consistent JSON responses, and endpoint testing.

## Features
- API-key protection using the `X-API-Key` request header.
- Input validation for task title and description.
- Consistent JSON error responses.
- Create and retrieve tasks.
- Automated tests using pytest.

## Requirements
- Python 3.9 or newer
- pip
- Postman (optional, for manual API testing)

## Setup instructions

1. Open this project folder in VS Code.
2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate it on Windows:

   ```bash
   venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Open the included `.env` file. If it is missing, copy `.env.example` and rename the copy to `.env`.
6. Replace the sample API key with a long private value. Do not commit `.env` to GitHub.

## Run the application

```bash
python app.py
```

The API runs locally at `http://127.0.0.1:5000`.

## API endpoints

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| GET | `/` | No | API welcome message |
| GET | `/health` | No | Health check |
| POST | `/api/tasks` | Yes | Create a task |
| GET | `/api/tasks` | Yes | List all tasks |
| GET | `/api/tasks/<task_id>` | Yes | Get one task |

Protected endpoints require this header:

```text
X-API-Key: your-private-api-key
```

### Example: Create a task

Send a `POST` request to:

```text
http://127.0.0.1:5000/api/tasks
```

Headers:

```text
Content-Type: application/json
X-API-Key: your-private-api-key
```

JSON body:

```json
{
  "title": "Complete SWYNEX Task 3",
  "description": "Implement authentication and validation"
}
```

Successful response: HTTP `201 Created`.

### Example: List tasks

Send a `GET` request to:

```text
http://127.0.0.1:5000/api/tasks
```

Include the `X-API-Key` header.

## Error responses

- `400 Bad Request`: invalid JSON or validation failure.
- `401 Unauthorized`: missing or incorrect API key.
- `404 Not Found`: task or route does not exist.
- `405 Method Not Allowed`: unsupported HTTP method.
- `500 Internal Server Error`: unexpected server error.

Example error response:

```json
{
  "success": false,
  "error": {
    "message": "Missing or invalid API key.",
    "status": 401
  }
}
```

## Automated testing

Run:

```bash
pytest -v
```

The tests check the public health endpoint, authentication, successful task creation, invalid input, task listing, and missing tasks.

## Important notes
- This is a learning/demo project. Tasks are stored in memory and reset when the server restarts.
- Use a unique secret API key in your local `.env` file.
- Never upload `.env` or expose your real API key in screenshots or public posts.

## Task 3 learning outcomes
This project demonstrates how authentication, input validation, consistent error handling, and endpoint integration work together in a Flask backend application.
