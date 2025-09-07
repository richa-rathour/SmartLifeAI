"""
AI module for SmartLife AI
Handles interview preparation using LangChain and OpenAI
"""

import os
from typing import List, Dict
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class InterviewAI:
    """AI-powered interview preparation using LangChain and OpenAI"""
    
    def __init__(self):
        """Initialize the AI interview assistant"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize ChatOpenAI with GPT-3.5-turbo for cost efficiency
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=1000
        )
    
    def generate_interview_questions(self, topic: str) -> List[Dict]:
        """
        Generate 5 advanced interview questions for a given topic
        
        Args:
            topic (str): The topic to generate questions for (e.g., "Java OOP", "Machine Learning")
            
        Returns:
            List[Dict]: List of 5 interview questions with answers
        """
        try:
            # System prompt to guide the AI
            system_prompt = f"""You are an expert technical interviewer. Generate exactly 5 advanced interview questions about {topic}.
            
            For each question, provide:
            1. A clear, specific question that tests deep understanding
            2. A concise but comprehensive answer (2-3 sentences)
            3. The difficulty level (Intermediate/Advanced)
            
            Format your response as a JSON array where each object has:
            - "question": the interview question
            - "answer": the answer
            - "difficulty": the difficulty level
            
            Make sure the questions are practical and relevant to real-world scenarios in {topic}."""
            
            # Human message with the specific topic
            human_prompt = f"Generate 5 advanced interview questions about {topic} with clear, concise answers."
            
            # Create messages for the chat model
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            # Get response from the AI
            response = self.llm(messages)
            
            # Parse the response (assuming it returns valid JSON)
            import json
            try:
                questions_data = json.loads(response.content)
                
                # Ensure we have exactly 5 questions
                if len(questions_data) != 5:
                    # If not exactly 5, create a fallback response
                    return self._create_fallback_questions(topic)
                
                return questions_data
                
            except json.JSONDecodeError:
                # If JSON parsing fails, create fallback questions
                return self._create_fallback_questions(topic)
                
        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return self._create_fallback_questions(topic)
    
    def _create_fallback_questions(self, topic: str) -> List[Dict]:
        """
        Create fallback questions if AI generation fails
        
        Args:
            topic (str): The topic for questions
            
        Returns:
            List[Dict]: Fallback questions
        """
        fallback_questions = [
            {
                "question": f"What are the key concepts and principles in {topic}?",
                "answer": f"The key concepts in {topic} include fundamental principles, best practices, and core methodologies that form the foundation of this field.",
                "difficulty": "Intermediate"
            },
            {
                "question": f"How would you explain {topic} to someone with no technical background?",
                "answer": f"I would use analogies and simple language to explain {topic}, focusing on practical benefits and real-world applications.",
                "difficulty": "Intermediate"
            },
            {
                "question": f"What are the most common challenges when working with {topic}?",
                "answer": f"Common challenges include complexity management, performance optimization, and maintaining code quality while scaling applications.",
                "difficulty": "Advanced"
            },
            {
                "question": f"Can you describe a real-world project where you applied {topic}?",
                "answer": f"In a real-world project, I would apply {topic} by identifying specific use cases, implementing best practices, and measuring success through key metrics.",
                "difficulty": "Advanced"
            },
            {
                "question": f"What resources would you recommend for someone learning {topic}?",
                "answer": f"I recommend official documentation, hands-on projects, online courses, and community forums for comprehensive learning of {topic}.",
                "difficulty": "Intermediate"
            }
        ]
        
        return fallback_questions
    
    def get_question_by_difficulty(self, topic: str, difficulty: str = "All") -> List[Dict]:
        """
        Get interview questions filtered by difficulty level
        
        Args:
            topic (str): The topic for questions
            difficulty (str): Difficulty level filter ("Beginner", "Intermediate", "Advanced", "All")
            
        Returns:
            List[Dict]: Filtered questions
        """
        all_questions = self.generate_interview_questions(topic)
        
        if difficulty == "All":
            return all_questions
        
        return [q for q in all_questions if q.get("difficulty", "").lower() == difficulty.lower()]


# Global AI instance
interview_ai = InterviewAI()
