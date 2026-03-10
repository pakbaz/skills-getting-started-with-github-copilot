"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports
    "Soccer Team": {
        "description": "Competitive soccer training and interschool matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Basketball drills, scrimmages, and league games",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    # Artistic
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media art techniques",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Rehearse and perform plays, improve acting and stagecraft skills",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    # Intellectual
    "Math Olympiad": {
        "description": "Prepare for math competitions with challenging problems and proofs",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Club": {
        "description": "Practice public speaking, argumentation, and competitive debate",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "evelyn@mergington.edu"]
    },
    # Sports
    "Swimming Team": {
        "description": "Swim training, stroke technique, and competitive swim meets",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["logan@mergington.edu", "ella@mergington.edu"]
    },
    "Track and Field": {
        "description": "Sprinting, distance running, jumping, and throwing events",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["mason@mergington.edu", "aria@mergington.edu"]
    },
    # Artistic
    "Music Band": {
        "description": "Learn instruments, rehearse ensemble pieces, and perform at school events",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["elijah@mergington.edu", "scarlett@mergington.edu"]
    },
    "Photography Club": {
        "description": "Explore digital and film photography, composition, and editing",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["aiden@mergington.edu", "grace@mergington.edu"]
    },
    # Intellectual
    "Science Bowl": {
        "description": "Study and compete in science trivia across physics, chemistry, and biology",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["benjamin@mergington.edu", "chloe@mergington.edu"]
    },
    "Model United Nations": {
        "description": "Simulate UN committees, draft resolutions, and debate global issues",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["alexander@mergington.edu", "lily@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student not found in activity")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
