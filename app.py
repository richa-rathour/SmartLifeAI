"""
SmartLife AI - Main Flask Application
A comprehensive backend with expense tracking and AI-powered interview preparation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from db import db_manager
from ai import interview_ai

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "SmartLife AI Backend is running!",
        "version": "1.0.0",
        "endpoints": {
            "expenses": {
                "add": "POST /api/expenses",
                "get_all": "GET /api/expenses"
            },
            "interview": {
                "generate_questions": "POST /api/interview/questions"
            }
        }
    })


# ==================== EXPENSE TRACKING ENDPOINTS ====================

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    """
    Add a new expense
    
    Expected JSON payload:
    {
        "amount": 25.50,
        "category": "Food",
        "note": "Lunch at restaurant",
        "date": "2024-01-15"  // Optional, defaults to today
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        required_fields = ['amount', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Validate data types and values
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({
                    "status": "error",
                    "message": "Amount must be greater than 0"
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": "Amount must be a valid number"
            }), 400
        
        # Extract and validate optional fields
        category = str(data['category']).strip()
        note = str(data.get('note', '')).strip()
        date = data.get('date')
        
        if not category:
            return jsonify({
                "status": "error",
                "message": "Category cannot be empty"
            }), 400
        
        # Validate date format if provided
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    "status": "error",
                    "message": "Date must be in YYYY-MM-DD format"
                }), 400
        
        # Add expense to database
        expense = db_manager.add_expense(
            amount=amount,
            category=category,
            note=note,
            date=date
        )
        
        return jsonify({
            "status": "success",
            "message": "Expense added successfully",
            "data": expense
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/expenses', methods=['GET'])
def get_all_expenses():
    """
    Get all expenses ordered by date (descending)
    
    Returns:
    {
        "status": "success",
        "data": [
            {
                "id": 1,
                "amount": 25.50,
                "category": "Food",
                "note": "Lunch at restaurant",
                "date": "2024-01-15",
                "created_at": "2024-01-15 10:30:00"
            }
        ]
    }
    """
    try:
        expenses = db_manager.get_all_expenses()
        
        return jsonify({
            "status": "success",
            "message": f"Retrieved {len(expenses)} expenses",
            "data": expenses
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/expenses/<int:expense_id>', methods=['GET'])
def get_expense_by_id(expense_id):
    """
    Get a specific expense by ID
    """
    try:
        expense = db_manager.get_expense_by_id(expense_id)
        
        if not expense:
            return jsonify({
                "status": "error",
                "message": f"Expense with ID {expense_id} not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": expense
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """
    Delete an expense by ID
    """
    try:
        success = db_manager.delete_expense(expense_id)
        
        if not success:
            return jsonify({
                "status": "error",
                "message": f"Expense with ID {expense_id} not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": f"Expense with ID {expense_id} deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


# ==================== INTERVIEW PREPARATION ENDPOINTS ====================

@app.route('/api/interview/questions', methods=['POST'])
def generate_interview_questions():
    """
    Generate 5 advanced interview questions for a given topic
    
    Expected JSON payload:
    {
        "topic": "Java OOP"
    }
    
    Returns:
    {
        "status": "success",
        "data": [
            {
                "question": "What is the difference between abstraction and encapsulation?",
                "answer": "Abstraction focuses on hiding complex implementation details...",
                "difficulty": "Intermediate"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        if 'topic' not in data:
            return jsonify({
                "status": "error",
                "message": "Topic is required"
            }), 400
        
        topic = str(data['topic']).strip()
        
        if not topic:
            return jsonify({
                "status": "error",
                "message": "Topic cannot be empty"
            }), 400
        
        # Generate interview questions using AI
        questions = interview_ai.generate_interview_questions(topic)
        
        return jsonify({
            "status": "success",
            "message": f"Generated 5 interview questions for '{topic}'",
            "topic": topic,
            "data": questions
        }), 200
        
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/interview/questions/<difficulty>', methods=['POST'])
def generate_interview_questions_by_difficulty(difficulty):
    """
    Generate interview questions filtered by difficulty level
    
    Expected JSON payload:
    {
        "topic": "Machine Learning"
    }
    
    URL parameter: difficulty (Beginner, Intermediate, Advanced)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        if 'topic' not in data:
            return jsonify({
                "status": "error",
                "message": "Topic is required"
            }), 400
        
        topic = str(data['topic']).strip()
        
        if not topic:
            return jsonify({
                "status": "error",
                "message": "Topic cannot be empty"
            }), 400
        
        # Validate difficulty level
        valid_difficulties = ['Beginner', 'Intermediate', 'Advanced', 'All']
        if difficulty not in valid_difficulties:
            return jsonify({
                "status": "error",
                "message": f"Invalid difficulty level. Must be one of: {', '.join(valid_difficulties)}"
            }), 400
        
        # Generate filtered questions
        questions = interview_ai.get_question_by_difficulty(topic, difficulty)
        
        return jsonify({
            "status": "success",
            "message": f"Generated interview questions for '{topic}' (Difficulty: {difficulty})",
            "topic": topic,
            "difficulty": difficulty,
            "data": questions
        }), 200
        
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "status": "error",
        "message": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment variables.")
        print("Interview preparation features will not work without a valid API key.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
    
    # Run the Flask app
    print("Starting SmartLife AI Backend...")
    print("Available endpoints:")
    print("  GET  / - Health check")
    print("  POST /api/expenses - Add expense")
    print("  GET  /api/expenses - Get all expenses")
    print("  GET  /api/expenses/<id> - Get expense by ID")
    print("  DELETE /api/expenses/<id> - Delete expense")
    print("  POST /api/interview/questions - Generate interview questions")
    print("  POST /api/interview/questions/<difficulty> - Generate questions by difficulty")
    
    app.run(debug=True, host="127.0.0.1", port=5000)


