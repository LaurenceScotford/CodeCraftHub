from flask import Flask, jsonify, request, send_from_directory
import json
from datetime import date
from pathlib import Path


app = Flask(__name__)

VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed"
}

REQUIRED_FIELDS = {
    "name",
    "description",
    "target_completion_date",
    "status",
}

DATA_FILE = Path("courses.json")


def load_courses():
    """
    Load all courses from the JSON data file.

    Returns:
        list: A list of course dictionaries. If the data file does not
        exist, an empty list is returned.

    Raises:
        json.JSONDecodeError: If the JSON file contains invalid JSON.
        OSError: If the file cannot be read.
    """
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("courses", [])


def save_courses(courses):
    """
    Save a list of courses to the JSON data file.

    Args:
        courses (list): A list of course dictionaries to save.

    Returns:
        None

    Raises:
        TypeError: If the courses data cannot be serialized as JSON.
        OSError: If the data directory or file cannot be created or written.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump({"courses": courses}, file, indent=2)


def validate_course_data(data, require_all_fields=True):
    """
    Validate course data.

    Returns:
        None if valid
        Error message string if invalid
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    if require_all_fields:
        missing_fields = REQUIRED_FIELDS - data.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            return f"Missing required fields: {missing}"

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "Name must be a non-empty string"

    if "description" in data:
        if not isinstance(data["description"], str):
            return "Description must be a string"

    if "target_completion_date" in data:
        try:
            date.fromisoformat(data["target_completion_date"])
        except (TypeError, ValueError):
            return "target_completion_date must use YYYY-MM-DD format"

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            valid_statuses = ", ".join(sorted(VALID_STATUSES))
            return f"Status must be one of: {valid_statuses}"

    return None


def find_course(courses, course_id):
    """
    Find a course by ID.

    Returns: 
        Course with given id if found
        None if not found
    """
    return next(
        (course for course in courses if course["id"] == course_id),
        None
    )


@app.get("/")
def serve_index():
    # Serves index.html from the current working directory
    return send_from_directory(".", "index.html")


@app.get("/api/health")
def health_check():
    """
    Responds with OK status to indicate server running

    Returns:
        JSON structure with HTTP status code 200
    """
    return jsonify({"status": "ok"}), 200


@app.get("/api/courses")
def get_courses():
    """
    Responds with all courses

    Returns:
        JSON structure with all courses
    """
    courses = load_courses()

    status = request.args.get("status")
    if status:
        courses = [course for course in courses if course["status"] == status]

    return jsonify(courses)


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """
    Responds with a specific course, if found
    Requires course id to be included in URL.

    Returns: 
        Course with given ID if found.
        A 404 error if not found.
    """
    courses = load_courses()

    course = next(
        (course for course in courses if course["id"] == course_id),
        None
    )

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course)


@app.post("/api/courses")
def create_course():
    data = request.get_json(silent=True)

    error = validate_course_data(data, require_all_fields=True)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()

    # Generate the next ID.
    next_id = max((course["id"] for course in courses), default=0) + 1

    new_course = {
        "id": next_id,
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_completion_date": data["target_completion_date"],
        "status": data["status"],
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201


@app.put("/api/courses/<int:course_id>")
def replace_course(course_id):
    """
    Replace an entire course.

    PUT requires all course fields:
    name, description, target_completion_date, and status.
    """
    data = request.get_json(silent=True)

    error = validate_course_data(data, require_all_fields=True)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    course.update({
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_completion_date": data["target_completion_date"],
        "status": data["status"],
    })

    save_courses(courses)

    return jsonify(course), 200


@app.patch("/api/courses/<int:course_id>")
def update_course(course_id):
    """
    Partially update a course.

    PATCH accepts one or more course fields.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    if not data:
        return jsonify({
            "error": "Request body cannot be empty"
        }), 400

    allowed_fields = REQUIRED_FIELDS
    unknown_fields = set(data.keys()) - allowed_fields

    if unknown_fields:
        unknown = ", ".join(sorted(unknown_fields))
        return jsonify({
            "error": f"Unknown field(s): {unknown}"
        }), 400

    error = validate_course_data(data, require_all_fields=False)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    if "name" in data:
        course["name"] = data["name"].strip()

    if "description" in data:
        course["description"] = data["description"].strip()

    if "target_completion_date" in data:
        course["target_completion_date"] = data[
            "target_completion_date"
        ]

    if "status" in data:
        course["status"] = data["status"]

    save_courses(courses)

    return jsonify(course), 200


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    courses.remove(course)
    save_courses(courses)
    return jsonify({"message": "Course deleted successfully"}), 200
