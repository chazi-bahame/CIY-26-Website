from database import SessionLocal
from models import Project

db = SessionLocal()

projects = [
    Project(
        name="AI Development",
        description="Exploring Artificial Intelligence and Machine Learning to develop useful solutions for real-world problems.",
        category="Artificial Intelligence",
        image="IMG-20260922-WA0011.jpg"
    ),

    Project(
        name="Smart Home Security",
        description="A smart security system using sensors, alarms and microcontrollers to improve home safety.",
        category="IoT & Security",
        image="IMG-20260922-WA0019.jpg"
    ),

    Project(
        name="Smart Agriculture",
        description="Using sensors, IoT and automation technologies to improve agricultural monitoring and productivity.",
        category="Smart Agriculture",
        image="IMG-20260922-WA0017.jpg"
    ),

    Project(
        name="Data Science & Signal Processing",
        description="Applying data analysis, signal processing and machine learning techniques to solve technical problems.",
        category="Data Science",
        image="IMG-20260922-WA0027.jpg"
    )
]

db.add_all(projects)
db.commit()

print("4 projects added successfully!")

db.close()