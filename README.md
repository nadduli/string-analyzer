# String Analyzer REST API

A simple yet powerful Node.js + Express REST API that analyzes strings, computes their properties, and stores them persistently in a local JSON file (storage.json).
It supports filtering, natural language queries, and CRUD operations on string data.

## Features

- POST /strings → Analyze and store a new string
- GET /strings/:string_value → Retrieve analysis for a specific string
- GET /strings → List all analyzed strings with optional filters
- GET /strings/filter-by-natural-language → Use natural language to query (e.g., “palindromic strings containing the letter a”)
- DELETE /strings/:string_value → Remove a stored string

### Each analyzed string includes

✅ Length
✅ Palindrome check
✅ Word count
✅ Unique character count
✅ Character frequency map
✅ SHA-256 hash
✅ Timestamp of creation

## Tech Stack

- Node.js — JavaScript runtime
- Express.js — Backend framework
- Crypto — For hashing strings (SHA-256)
- CORS — Cross-Origin Resource Sharing
- fs — For lightweight local persistence

## 📁 Project Structure

```pgsql
string-analyzer-api/
├── routes/
│   └── strings.js        # Router handling string endpoints
├── storage.json           # Auto-generated persistent storage
├── server.js              # Express app entry point
├── package.json
└── README.md
```

## ⚙️ Installation & Setup

- Clone the repo

```bash
git clone <your-repo-url>
cd string-analyzer-api
```

- Install dependencies

```bash
npm install
```

- Create a .env file (optional)

```bash
PORT=3000
```

- Run the server

```bash
npm start
```

## API Endpoints

- ➕ POST /strings

Analyze and store a string.

Request Body:

```bash
{
  "value": "madam"
}
```

Response:

```json
{
  "id": "b1a4d5f3e...",
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "sha256_hash": "b1a4d5f3e...",
    "character_frequency_map": {
      "m": 2,
      "a": 2,
      "d": 1
    }
  },
  "created_at": "2025-10-21T19:00:00.000Z"
}
```

- 🔍 GET /strings

Retrieve all analyzed strings with optional filters.

Example Query:

```bash
/strings?is_palindrome=true&min_length=3&contains_character=a
```

## GET /strings/filter-by-natural-language

Query strings using natural English.

Example:

```bash
/strings/filter-by-natural-language?query=palindromic strings longer than 3 characters containing the letter a
```

```json
Response:
{
"data": [...],
"count": 2,
"interpreted_query": {
"original": "palindromic strings longer than 3 characters containing the letter a",
"parsed_filters": {
"is_palindrome": true,
"min_length": 4,
"contains_character": "a"
}
}
}
```

## 🧾 GET /strings/:string_value

Retrieve analysis for a specific string.

Example:

```bash
/strings/hello
```

## ❌ DELETE /strings/:string_value

Delete a string from storage.

Example:

```bash
DELETE /strings/hello
```

Response:
_204 No Content_

## 🧪 Testing with Postman / curl

Example 1: Add a string

```bash
curl -X POST http://localhost:3000/strings \
-H "Content-Type: application/json" \
-d '{"value":"madam"}'
```

Example 2: Get palindromic strings

```bash
curl "http://localhost:3000/strings?is_palindrome=true"
```

Example 3: Use natural language filtering

```bash
curl "http://localhost:3000/strings/filter-by-natural-language?query=single word palindromic strings"
```

## 💾 Persistent Storage

All analyzed strings are stored in a local file:

```pgsql
storage.json
```
