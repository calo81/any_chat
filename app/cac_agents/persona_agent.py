"""
PersonaAgent - A specialized agent that acts as a specific person based on their CV data
Extends the OpenAI Agents SDK Agent class to represent different individuals.
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Tool, function_tool, Runner
import json

load_dotenv()

cv_data = {
            "name": "Sarah Johnson",
            "work_experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "TechCorp",
                    "duration": "2020-2024",
                    "description": "Led development of microservices architecture and mentored junior developers",
                    "technologies": ["Python", "Docker", "Kubernetes", "AWS", "React"]
                },
                {
                    "title": "Software Developer",
                    "company": "StartupXYZ",
                    "duration": "2018-2020",
                    "description": "Built full-stack web applications and mobile apps",
                    "technologies": ["JavaScript", "Node.js", "React Native", "MongoDB"]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "institution": "University of California",
                    "year": "2018"
                }
            ],
            "skills": [
                {"name": "Python", "category": "Programming", "level": "Expert"},
                {"name": "JavaScript", "category": "Programming", "level": "Advanced"},
                {"name": "Leadership", "category": "Soft Skills", "level": "Advanced"},
                {"name": "Problem Solving", "category": "Soft Skills", "level": "Expert"}
            ],
            "achievements": [
                {
                    "title": "Employee of the Year",
                    "type": "Award",
                    "year": "2023",
                    "description": "Recognized for outstanding leadership and technical contributions"
                },
                {
                    "title": "Open Source Contributor",
                    "type": "Recognition",
                    "year": "2022",
                    "description": "Contributed to major open source projects with 1000+ GitHub stars"
                }
            ],
            "personal_info": {
                "location": "San Francisco, CA",
                "interests": ["Machine Learning", "Open Source", "Mentoring"],
                "values": ["Innovation", "Collaboration", "Continuous Learning"]
            }
        }

person_name = "Sarah Johnson"

class PersonaAgent(Agent):
    """
    A specialized agent that acts as a specific person based on their CV data.
    Uses work experience, skills, and personal information to generate authentic responses.
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.person_name = person_name
        self.cv_data = cv_data
        self.model = model
        self.instructions = f"You are {person_name} and will respond questions based on your CV data: {cv_data}"
        
        super().__init__(name=person_name, instructions=self.instructions, model=model)

    async def run(self, input: str):
        return await Runner.run(self, input=input)

        
    async def run_stream(self, input: str):
        return await Runner.run_stream(self, input=input)
