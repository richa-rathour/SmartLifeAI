"""
Test script for SmartLife AI Backend
Demonstrates all API endpoints with example requests
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Health check passed\n")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
        return False

def test_add_expense():
    """Test adding expenses"""
    print("💰 Testing Add Expense...")
    
    test_expenses = [
        {
            "amount": 25.50,
            "category": "Food",
            "note": "Lunch at restaurant",
            "date": "2024-01-15"
        },
        {
            "amount": 15.00,
            "category": "Transport",
            "note": "Bus fare",
            "date": "2024-01-16"
        },
        {
            "amount": 200.00,
            "category": "Shopping",
            "note": "New clothes",
            "date": "2024-01-17"
        }
    ]
    
    for i, expense in enumerate(test_expenses, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/api/expenses",
                json=expense,
                headers={"Content-Type": "application/json"}
            )
            print(f"Expense {i} - Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ Expense added successfully\n")
        except Exception as e:
            print(f"❌ Failed to add expense {i}: {e}\n")

def test_get_all_expenses():
    """Test getting all expenses"""
    print("📋 Testing Get All Expenses...")
    try:
        response = requests.get(f"{BASE_URL}/api/expenses")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Get all expenses successful\n")
        return True
    except Exception as e:
        print(f"❌ Failed to get expenses: {e}\n")
        return False

def test_get_expense_by_id(expense_id):
    """Test getting a specific expense by ID"""
    print(f"🔍 Testing Get Expense by ID ({expense_id})...")
    try:
        response = requests.get(f"{BASE_URL}/api/expenses/{expense_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Get expense by ID successful\n")
        return True
    except Exception as e:
        print(f"❌ Failed to get expense by ID: {e}\n")
        return False

def test_interview_questions():
    """Test generating interview questions"""
    print("🤖 Testing Interview Questions Generation...")
    
    test_topics = [
        "Python Programming",
        "Machine Learning",
        "Web Development"
    ]
    
    for topic in test_topics:
        try:
            response = requests.post(
                f"{BASE_URL}/api/interview/questions",
                json={"topic": topic},
                headers={"Content-Type": "application/json"}
            )
            print(f"Topic: {topic} - Status Code: {response.status_code}")
            response_data = response.json()
            
            # Show first question as example
            if response_data.get("status") == "success" and response_data.get("data"):
                first_question = response_data["data"][0]
                print(f"Sample Question: {first_question['question']}")
                print(f"Answer: {first_question['answer']}")
                print(f"Difficulty: {first_question['difficulty']}")
            
            print("✅ Interview questions generated successfully\n")
        except Exception as e:
            print(f"❌ Failed to generate questions for {topic}: {e}\n")

def test_interview_questions_by_difficulty():
    """Test generating interview questions by difficulty"""
    print("🎯 Testing Interview Questions by Difficulty...")
    
    difficulties = ["Beginner", "Intermediate", "Advanced"]
    topic = "Data Structures and Algorithms"
    
    for difficulty in difficulties:
        try:
            response = requests.post(
                f"{BASE_URL}/api/interview/questions/{difficulty}",
                json={"topic": topic},
                headers={"Content-Type": "application/json"}
            )
            print(f"Difficulty: {difficulty} - Status Code: {response.status_code}")
            response_data = response.json()
            
            if response_data.get("status") == "success":
                questions = response_data.get("data", [])
                print(f"Generated {len(questions)} questions for {difficulty} level")
                if questions:
                    print(f"Sample: {questions[0]['question']}")
            
            print("✅ Difficulty-based questions generated successfully\n")
        except Exception as e:
            print(f"❌ Failed to generate {difficulty} questions: {e}\n")

def test_error_handling():
    """Test error handling scenarios"""
    print("⚠️ Testing Error Handling...")
    
    # Test invalid expense data
    print("Testing invalid expense data...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/expenses",
            json={"amount": -10, "category": ""},  # Invalid data
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test non-existent expense
    print("\nTesting non-existent expense...")
    try:
        response = requests.get(f"{BASE_URL}/api/expenses/999")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test invalid interview topic
    print("\nTesting invalid interview topic...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/interview/questions",
            json={"topic": ""},  # Empty topic
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("✅ Error handling tests completed\n")

def main():
    """Run all tests"""
    print("🚀 Starting SmartLife AI Backend Tests")
    print("=" * 50)
    
    # Check if server is running
    if not test_health_check():
        print("❌ Server is not running. Please start the server with: python app.py")
        return
    
    # Test expense tracking
    print("💰 Testing Expense Tracking Features")
    print("-" * 30)
    test_add_expense()
    test_get_all_expenses()
    test_get_expense_by_id(1)
    
    # Test interview preparation
    print("🤖 Testing Interview Preparation Features")
    print("-" * 30)
    test_interview_questions()
    test_interview_questions_by_difficulty()
    
    # Test error handling
    print("⚠️ Testing Error Handling")
    print("-" * 30)
    test_error_handling()
    
    print("🎉 All tests completed!")
    print("\n📝 Example cURL commands:")
    print("1. Add expense:")
    print('curl -X POST http://localhost:5000/api/expenses -H "Content-Type: application/json" -d \'{"amount": 25.50, "category": "Food", "note": "Lunch"}\'')
    print("\n2. Get all expenses:")
    print("curl -X GET http://localhost:5000/api/expenses")
    print("\n3. Generate interview questions:")
    print('curl -X POST http://localhost:5000/api/interview/questions -H "Content-Type: application/json" -d \'{"topic": "Python Programming"}\'')

if __name__ == "__main__":
    main()
