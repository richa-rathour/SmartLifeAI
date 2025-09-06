"""
Database module for SmartLife AI
Handles SQLite database operations for expense tracking
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    """Manages SQLite database operations for the SmartLife AI application"""
    
    def __init__(self, db_path: str = "smartlife.db"):
        """
        Initialize database manager
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create expenses table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        note TEXT,
                        date TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                print("Database initialized successfully")
                
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise
    
    def add_expense(self, amount: float, category: str, note: str = "", date: str = None) -> Dict:
        """
        Add a new expense to the database
        
        Args:
            amount (float): Expense amount
            category (str): Expense category
            note (str): Optional note about the expense
            date (str): Date in YYYY-MM-DD format, defaults to today
            
        Returns:
            Dict: Created expense data with ID
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO expenses (amount, category, note, date)
                    VALUES (?, ?, ?, ?)
                """, (amount, category, note, date))
                
                expense_id = cursor.lastrowid
                conn.commit()
                
                return {
                    "id": expense_id,
                    "amount": amount,
                    "category": category,
                    "note": note,
                    "date": date
                }
                
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")
            raise
    
    def get_all_expenses(self) -> List[Dict]:
        """
        Get all expenses ordered by date (descending)
        
        Returns:
            List[Dict]: List of all expenses
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, amount, category, note, date, created_at
                    FROM expenses
                    ORDER BY date DESC, created_at DESC
                """)
                
                expenses = []
                for row in cursor.fetchall():
                    expenses.append({
                        "id": row[0],
                        "amount": row[1],
                        "category": row[2],
                        "note": row[3],
                        "date": row[4],
                        "created_at": row[5]
                    })
                
                return expenses
                
        except sqlite3.Error as e:
            print(f"Error fetching expenses: {e}")
            raise
    
    def get_expense_by_id(self, expense_id: int) -> Optional[Dict]:
        """
        Get a specific expense by ID
        
        Args:
            expense_id (int): ID of the expense
            
        Returns:
            Optional[Dict]: Expense data if found, None otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, amount, category, note, date, created_at
                    FROM expenses
                    WHERE id = ?
                """, (expense_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "amount": row[1],
                        "category": row[2],
                        "note": row[3],
                        "date": row[4],
                        "created_at": row[5]
                    }
                return None
                
        except sqlite3.Error as e:
            print(f"Error fetching expense: {e}")
            raise
    
    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by ID
        
        Args:
            expense_id (int): ID of the expense to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                conn.commit()
                
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error deleting expense: {e}")
            raise


# Global database instance
db_manager = DatabaseManager()
