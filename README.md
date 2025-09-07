# SmartLife AI Backend

A comprehensive Python + LangChain / Flask / AI backend application that combines expense tracking with AI-powered interview preparation using LangChain and OpenAI.

## Features

### 💰 Expense Tracking
- Add expenses with amount, category, note, and date
- Retrieve all expenses in descending order by date
- Get specific expenses by ID
- Delete expenses
- SQLite database for data persistence

### 🤖 AI-Powered Interview Preparation
- Generate 5 advanced interview questions for any topic
- Get questions filtered by difficulty level (Beginner, Intermediate, Advanced)
- Powered by OpenAI GPT-3.5-turbo via LangChain
- Clear, concise answers for each question

## Project Structure

```
SmartLifeAI/
├── app.py              # Main Flask application
├── db.py               # Database operations (SQLite)
├── ai.py               # AI interview preparation logic
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables template
├── smartlife.db        # SQLite database (created automatically)
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd SmartLifeAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `env_example.txt` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Run the application**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/` - Check if the API is running

### Expense Tracking

#### Add Expense
- **POST** `/api/expenses`
- **Body:**
  ```json
  {
    "amount": 25.50,
    "category": "Food",
    "note": "Lunch at restaurant",
    "date": "2024-01-15"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Expense added successfully",
    "data": {
      "id": 1,
      "amount": 25.50,
      "category": "Food",
      "note": "Lunch at restaurant",
      "date": "2024-01-15"
    }
  }
  ```

#### Get All Expenses
- **GET** `/api/expenses`
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Retrieved 2 expenses",
    "data": [
      {
        "id": 2,
        "amount": 15.00,
        "category": "Transport",
        "note": "Bus fare",
        "date": "2024-01-16",
        "created_at": "2024-01-16 09:30:00"
      },
      {
        "id": 1,
        "amount": 25.50,
        "category": "Food",
        "note": "Lunch at restaurant",
        "date": "2024-01-15",
        "created_at": "2024-01-15 12:30:00"
      }
    ]
  }
  ```

#### Get Expense by ID
- **GET** `/api/expenses/{id}`
- **Response:**
  ```json
  {
    "status": "success",
    "data": {
      "id": 1,
      "amount": 25.50,
      "category": "Food",
      "note": "Lunch at restaurant",
      "date": "2024-01-15",
      "created_at": "2024-01-15 12:30:00"
    }
  }
  ```

#### Delete Expense
- **DELETE** `/api/expenses/{id}`
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Expense with ID 1 deleted successfully"
  }
  ```

### Interview Preparation

#### Generate Interview Questions
- **POST** `/api/interview/questions`
- **Body:**
  ```json
  {
    "topic": "Java OOP"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Generated 5 interview questions for 'Java OOP'",
    "topic": "Java OOP",
    "data": [
      {
        "question": "What is the difference between abstraction and encapsulation?",
        "answer": "Abstraction focuses on hiding complex implementation details and showing only essential features, while encapsulation bundles data and methods together and restricts access to internal components.",
        "difficulty": "Intermediate"
      },
      {
        "question": "Explain the concept of polymorphism in Java with examples.",
        "answer": "Polymorphism allows objects of different types to be treated as objects of a common base type. In Java, this is achieved through method overriding and interfaces, enabling one interface to represent different underlying forms.",
        "difficulty": "Advanced"
      }
    ]
  }
  ```

#### Generate Questions by Difficulty
- **POST** `/api/interview/questions/{difficulty}`
- **Body:**
  ```json
  {
    "topic": "Machine Learning"
  }
  ```
- **Difficulty levels:** `Beginner`, `Intermediate`, `Advanced`, `All`

## Example API Calls

### Using cURL

#### Add an Expense
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "category": "Food",
    "note": "Lunch at restaurant",
    "date": "2024-01-15"
  }'
```

#### Get All Expenses
```bash
curl -X GET http://localhost:5000/api/expenses
```

#### Generate Interview Questions
```bash
curl -X POST http://localhost:5000/api/interview/questions \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Python Programming"
  }'
```

#### Generate Advanced Questions Only
```bash
curl -X POST http://localhost:5000/api/interview/questions/Advanced \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Data Structures and Algorithms"
  }'
```

### Using Postman

1. **Set Base URL:** `http://localhost:5000`
2. **Set Headers:** `Content-Type: application/json`
3. **Use the JSON payloads shown in the API documentation above**

## Error Handling

The API returns consistent error responses:

```json
{
  "status": "error",
  "message": "Error description"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created (for new resources)
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

## Database

The application uses SQLite for data persistence. The database file (`smartlife.db`) is created automatically when you first run the application.

### Database Schema

**expenses table:**
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing ID
- `amount` (REAL) - Expense amount
- `category` (TEXT) - Expense category
- `note` (TEXT) - Optional note
- `date` (TEXT) - Date in YYYY-MM-DD format
- `created_at` (TIMESTAMP) - Record creation timestamp

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Required for AI interview preparation features

### Flask Configuration
- Debug mode: Enabled (for development)
- Host: `0.0.0.0` (accessible from any IP)
- Port: `5000`
- CORS: Enabled for all origins

## Development

### Running in Development Mode
```bash
python app.py
```

### Running in Production
For production deployment, consider using a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Dependencies

- **Flask** (2.3.3) - Web framework
- **Flask-CORS** (4.0.0) - Cross-Origin Resource Sharing
- **LangChain** (0.0.350) - AI framework
- **OpenAI** (1.3.7) - OpenAI API client
- **python-dotenv** (1.0.0) - Environment variable management

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your `.env` file contains a valid `OPENAI_API_KEY`
   - Check that the API key has sufficient credits

2. **Database Errors**
   - Ensure the application has write permissions in the project directory
   - Delete `smartlife.db` to reset the database

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

4. **Port Already in Use**
   - Change the port in `app.py` or kill the process using port 5000

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

---

**SmartLife AI** - Making life smarter with AI-powered tools! 🚀