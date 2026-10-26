# CodeCraftHub API 🚀

Welcome to **CodeCraftHub**! This project is a beginner-friendly RESTful API designed to manage and track programming courses and learning progress.

If you are learning how web servers communicate, how frontend clients talk to backend services, or how data travels across the web using JSON, this project is a practical starting point.

---

## 📖 Table of Contents

- [What is a REST API?](#what-is-a-rest-api)
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation Instructions](#installation-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints Reference](#api-endpoints-reference)
  - [1. Health Check](#1-health-check)
  - [2. Get All Courses](#2-get-all-courses)
  - [3. Get a Specific Course](#3-get-a-specific-course)
  - [4. Create a New Course](#4-create-a-new-course)
  - [5. Replace a Course (Full Update)](#5-replace-a-course-full-update)
  - [6. Update Course Fields (Partial Update)](#6-update-course-fields-partial-update)
  - [7. Delete a Course](#7-delete-a-course)
- [Testing Instructions](#testing-instructions)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## 💡 What is a REST API?

An **API** (Application Programming Interface) allows two software programs to communicate. A **REST API** uses standard web (HTTP) conventions to interact with data:

- **GET:** Retrieve information (safe to run multiple times without changing data).
- **POST:** Create a new record.
- **PUT:** Completely replace an existing record with new details.
- **PATCH:** Update only specific fields of an existing record.
- **DELETE:** Remove a record.

Data is sent and received in **JSON** (JavaScript Object Notation), a lightweight text format that both humans and computers can easily read.

---

## 🎯 Project Overview

CodeCraftHub runs on **Flask**, a lightweight Python web framework. Instead of requiring a separate database server (like PostgreSQL or MySQL), it reads and persists course records directly to a local file named `courses.json`.

Each course tracks:
- `id`: An auto-generated unique integer identifier.
- `name`: Course title (non-empty string).
- `description`: Overview of what the course covers.
- `target_completion_date`: Expected finish date (`YYYY-MM-DD`).
- `status`: Allowed values: `"Not Started"`, `"In Progress"`, or `"Completed"`.

---

## ✨ Features

- **Standard REST Routes:** Full CRUD (Create, Read, Update, Delete) capability.
- **Data Validation:** Checks for required fields, non-empty text, valid dates (`YYYY-MM-DD`), and allowed status strings.
- **Query Parameter Filtering:** Filter courses by status (e.g., `/api/courses?status=In Progress`).
- **File-Backed Persistence:** Saves updates to `courses.json` automatically.
- **Clear Error Reporting:** Returns descriptive HTTP `400 Bad Request` and `404 Not Found` JSON errors.

---

## 📂 Project Structure

```text
code-craft-hub/
│
├── app.py              # Main Flask server file containing routes and logic
├── courses.json        # Auto-generated JSON file that stores course data
├── requirements.txt    # Required Python libraries (Flask)
└── README.md           # Documentation and API reference
```

### File Breakdown:
- **`app.py`**: The application core. It loads stored data, registers endpoints, validates incoming JSON bodies, and writes back updates.
- **`courses.json`**: Acts as your local data store. If this file does not exist when the server starts, the app creates it automatically as soon as a course is added.
- **`requirements.txt`**: Declares dependencies so anyone can reproduce the environment.

---

## ⚙️ Prerequisites

Before you begin, ensure you have:
1. **Python 3.10 or newer** installed.
   - *Windows Users:* Check the box **"Add python.exe to PATH"** during installation.
2. A terminal (e.g., PowerShell on Windows, Terminal on macOS/Linux).
3. A code editor like **Visual Studio Code** (recommended).

Verify your Python installation in your terminal:

```bash
python --version
# or on some systems:
python3 --version
```

---

## 🚀 Installation Instructions

### Step 1: Open your project folder

Open your terminal or VS Code and navigate to the project directory:

```bash
cd path/to/code-craft-hub
```

### Step 2: Create a virtual environment

A virtual environment keeps your project dependencies isolated from the rest of your system.

**On Windows (PowerShell / Command Prompt):**
```powershell
python -m venv .venv
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
```

### Step 3: Activate the virtual environment

**On Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell displays an `Execution_Policies` restriction error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current terminal and retry).*

**On Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

When activated, you will see `(.venv)` at the beginning of your terminal prompt.

### Step 4: Install dependencies

Install Flask:

```bash
pip install flask
```

*(Optional)* Save this to a requirements file:
```bash
pip freeze > requirements.txt
```

---

## 🏃 Running the Application

Ensure your virtual environment is active, then start the server:

**On Windows:**
```powershell
python app.py
```

**On macOS / Linux:**
```bash
python3 app.py
```

You should see output similar to:
```text
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
Press CTRL+C to quit
```

- **`http://127.0.0.1`** is your local computer (`localhost`).
- **`5000`** is the network port Flask listens on.
- Leave this terminal window running while testing requests.

---

## 📡 API Endpoints Reference

> **Note for Windows Users:** Standard Windows PowerShell aliases `curl` to `Invoke-WebRequest`. To use standard `curl` flags on Windows, run **`curl.exe`** instead of `curl`.

---

### 1. Health Check

Verifies that the server is online and responding.

- **Method:** `GET`
- **URL:** `/api/health`

#### Example Request:
```powershell
curl.exe -i -X GET [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)
```

#### Successful Response (`200 OK`):
```json
{
  "status": "ok"
}
```

---

### 2. Get All Courses

Returns all courses currently saved. Supports optional filtering by `status`.

- **Method:** `GET`
- **URL:** `/api/courses`
- **Optional Query Parameter:** `?status=Not%20Started` (or `In%20Progress`, `Completed`)

#### Example Request (All Courses):
```powershell
curl.exe -i -X GET [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses)
```

#### Example Request (Filtered):
```powershell
curl.exe -i -X GET "[http://127.0.0.1:5000/api/courses?status=In%20Progress](http://127.0.0.1:5000/api/courses?status=In%20Progress)"
```

#### Successful Response (`200 OK`):
```json
[
  {
    "id": 1,
    "name": "Flask REST APIs",
    "description": "Learn how to build REST APIs using Flask.",
    "target_completion_date": "2026-12-15",
    "status": "Not Started"
  }
]
```

---

### 3. Get a Specific Course

Fetches details for a single course by its unique ID.

- **Method:** `GET`
- **URL:** `/api/courses/<course_id>`

#### Example Request:
```powershell
curl.exe -i -X GET [http://127.0.0.1:5000/api/courses/1](http://127.0.0.1:5000/api/courses/1)
```

#### Successful Response (`200 OK`):
```json
{
  "id": 1,
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs using Flask.",
  "target_completion_date": "2026-12-15",
  "status": "Not Started"
}
```

#### Error Response (`404 Not Found`):
```json
{
  "error": "Course not found"
}
```

---

### 4. Create a New Course

Adds a new course record. The server automatically assigns the next sequential `id`.

- **Method:** `POST`
- **URL:** `/api/courses`
- **Headers:** `Content-Type: application/json`

#### Required JSON Body:
```json
{
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs using Flask.",
  "target_completion_date": "2026-12-15",
  "status": "Not Started"
}
```

#### Example Request:
```powershell
curl.exe -i -X POST [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses) `
  -H "Content-Type: application/json" `
  -d '{"name": "Flask REST APIs", "description": "Learn how to build REST APIs using Flask.", "target_completion_date": "2026-12-15", "status": "Not Started"}'
```

#### Successful Response (`201 Created`):
```json
{
  "id": 1,
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs using Flask.",
  "target_completion_date": "2026-12-15",
  "status": "Not Started"
}
```

#### Common Error Responses (`400 Bad Request`):
- Missing keys: `{"error": "Missing required fields: description, status"}`
- Invalid date: `{"error": "target_completion_date must use YYYY-MM-DD format"}`
- Invalid status: `{"error": "Status must be one of: Completed, In Progress, Not Started"}`

---

### 5. Replace a Course (Full Update)

Overwrites **all** properties of an existing course. You must supply all fields.

- **Method:** `PUT`
- **URL:** `/api/courses/<course_id>`
- **Headers:** `Content-Type: application/json`

#### Example Request:
```powershell
curl.exe -i -X PUT [http://127.0.0.1:5000/api/courses/1](http://127.0.0.1:5000/api/courses/1) `
  -H "Content-Type: application/json" `
  -d '{"name": "Advanced Flask APIs", "description": "Deep dive into production Flask architectures.", "target_completion_date": "2026-11-30", "status": "In Progress"}'
```

#### Successful Response (`200 OK`):
```json
{
  "id": 1,
  "name": "Advanced Flask APIs",
  "description": "Deep dive into production Flask architectures.",
  "target_completion_date": "2026-11-30",
  "status": "In Progress"
}
```

---

### 6. Update Course Fields (Partial Update)

Updates only the fields you send, leaving unchanged fields intact.

- **Method:** `PATCH`
- **URL:** `/api/courses/<course_id>`
- **Headers:** `Content-Type: application/json`

#### Example Request:
```powershell
curl.exe -i -X PATCH [http://127.0.0.1:5000/api/courses/1](http://127.0.0.1:5000/api/courses/1) `
  -H "Content-Type: application/json" `
  -d '{"status": "Completed"}'
```

#### Successful Response (`200 OK`):
```json
{
  "id": 1,
  "name": "Advanced Flask APIs",
  "description": "Deep dive into production Flask architectures.",
  "target_completion_date": "2026-11-30",
  "status": "Completed"
}
```

#### Error Response for Unknown Field (`400 Bad Request`):
```powershell
curl.exe -i -X PATCH [http://127.0.0.1:5000/api/courses/1](http://127.0.0.1:5000/api/courses/1) `
  -H "Content-Type: application/json" `
  -d '{"instructor": "Alex"}'
```
```json
{
  "error": "Unknown field(s): instructor"
}
```

---

### 7. Delete a Course

Removes a course by its ID.

- **Method:** `DELETE`
- **URL:** `/api/courses/<course_id>`

#### Example Request:
```powershell
curl.exe -i -X DELETE [http://127.0.0.1:5000/api/courses/1](http://127.0.0.1:5000/api/courses/1)
```

#### Successful Response (`204 No Content`):
- Response body is empty; HTTP status code indicates completion.

#### Error Response (`404 Not Found`):
```json
{
  "error": "Course not found"
}
```

---

## 🧪 Testing Instructions

### Option A: Using the Terminal (`curl.exe`)

Open a second terminal window (leaving your server running in the first) and test in sequence:

1. **Verify server:**
   ```powershell
   curl.exe -i -X GET [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)
   ```
2. **Post course:**
   ```powershell
   curl.exe -i -X POST [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses) -H "Content-Type: application/json" -d '{"name":"Python Basics","description":"Core syntax and data structures.","target_completion_date":"2026-10-31","status":"Not Started"}'
   ```
3. **Verify it was added:**
   ```powershell
   curl.exe -i -X GET [http://127.0.0.1:5000/api/courses/1](http://127.0.0.1:5000/api/courses/1)
   ```
4. **Trigger validation failure (invalid date):**
   ```powershell
   curl.exe -i -X POST [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses) -H "Content-Type: application/json" -d '{"name":"Bad Date","description":"Test","target_completion_date":"31-10-2026","status":"Not Started"}'
   ```
   *Expected:* HTTP `400 Bad Request` explaining the date format requirement.

### Option B: VS Code REST Client Extension

If you prefer a graphical interface inside VS Code:
1. Install the **REST Client** extension by Huachao Mao.
2. Create a file named `test.http` in your workspace.
3. Paste requests like this:

```http
### Health Check
GET [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)

### Create Course
POST [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses)
Content-Type: application/json

{
  "name": "Flask REST APIs",
  "description": "Learn API development.",
  "target_completion_date": "2026-12-15",
  "status": "Not Started"
}

### Get All Courses
GET [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses)
```
4. Click the small **"Send Request"** link above each block to inspect responses directly inside VS Code.

---

## 🛠️ Troubleshooting Common Issues

### 1. `curl: (7) Failed to connect to 127.0.0.1 port 5000: Connection refused`
- **Cause:** Your Flask application isn't actively running.
- **Fix:** Open a terminal, run `python app.py`, and verify you see `Running on http://127.0.0.1:5000` before sending requests.

### 2. `The view function did not return a valid response` (HTTP 500 on DELETE)
- **Cause:** In Python/Flask, routes must explicitly return a response. If a function ends without a `return`, it returns `None`, which triggers an internal server error.
- **Fix:** Ensure the `delete_course` function in `app.py` ends with:
  ```python
  return "", 204
  ```

### 3. Single Quotes Breaking in Windows Command Prompt (`cmd.exe`)
- **Cause:** Standard Windows `cmd.exe` does not accept single-quoted strings for JSON arguments.
- **Fix:** Either use **PowerShell** with `curl.exe`, or escape double quotes inside `cmd.exe`:
  ```cmd
  curl.exe -X POST [http://127.0.0.1:5000/api/courses](http://127.0.0.1:5000/api/courses) -H "Content-Type: application/json" -d "{\"name\":\"Flask\",\"description\":\"APIs\",\"target_completion_date\":\"2026-12-15\",\"status\":\"Not Started\"}"
  ```

### 4. PowerShell Line Continuation Errors
- **Cause:** Linux/Bash uses `\` to split commands across lines; PowerShell treats `\` as a literal character.
- **Fix:** Use PowerShell's backtick character (`` ` ``) at the end of each line, or write your command on a single continuous line.

### 5. `400 Bad Request: Request body must be a JSON object`
- **Cause:** You omitted the `-H "Content-Type: application/json"` header, or the JSON body is malformed (e.g., missing double quotes around keys).
- **Fix:** Verify valid JSON formatting and ensure the `Content-Type` header is included in every `POST`, `PUT`, and `PATCH` request.