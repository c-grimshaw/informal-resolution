import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import Base
from models.user import User
from models.grievance import Grievance, Note, GrievanceStatus

# Database setup
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Constants
UNITS = ["427SOA", "CJIRU", "CSOR", "CSOTC", "HQ", "JTF 2", "SOF MPU"]
RANKS = ["Pte", "Cpl", "MCpl", "Sgt", "WO", "MWO", "CWO", "Lt", "Capt", "Maj", "LCol", "Col"]
POSITIONS = ["Operator", "Support Staff", "Medical Staff", "Intelligence Officer", "Communications Specialist", "Logistics Coordinator"]

# Add name lists for more realistic data
FIRST_NAMES = [
    "James", "William", "John", "Michael", "David", "Robert", "Thomas", "Daniel", "Paul", "Mark",
    "Elizabeth", "Sarah", "Jennifer", "Emily", "Emma", "Olivia", "Sophia", "Isabella", "Mia", "Charlotte",
    "Christopher", "Joseph", "Andrew", "Ryan", "Alexander", "Nicholas", "Matthew", "Anthony", "Steven", "Kevin",
    "Marie", "Catherine", "Michelle", "Nicole", "Rachel", "Laura", "Amanda", "Jessica", "Melissa", "Rebecca"
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Moore", "Anderson", "Thomas", "Jackson",
    "White", "Harris", "Martin", "Thompson", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker",
    "Hall", "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson",
    "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards"
]

GRIEVANCE_TYPES = {
    "Workplace Conditions": ["Health and Safety", "Equipment", "Facilities", "Work Hours"],
    "Discrimination": ["Gender", "Race", "Age", "Religion"],
    "Harassment": ["Verbal", "Physical", "Sexual", "Psychological"],
    "Other": ["Administrative", "Pay and Benefits", "Training", "Leave"]
}
STATUSES = [GrievanceStatus.pending, GrievanceStatus.in_progress, GrievanceStatus.resolved]

def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def create_supervisor(session: Session, unit: str) -> User:
    # Replace spaces with underscores and remove any special characters for the email
    email_unit = unit.lower().replace(' ', '_').replace('/', '_')
    name = generate_name()
    email_name = name.lower().replace(' ', '.')
    
    supervisor = User(
        email=f"{email_name}@forces.gc.ca",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMxRHHJ",  # "password"
        unit=unit,
        role="supervisor",
        is_active=True,
        is_verified=True,
        is_superuser=False,
        name=name
    )
    session.add(supervisor)
    session.commit()
    return supervisor

def create_grievance(session: Session, unit: str, created_days_ago: int) -> Grievance:
    grievance_type = random.choice(list(GRIEVANCE_TYPES.keys()))
    grievance_subtype = random.choice(GRIEVANCE_TYPES[grievance_type])
    submitter_name = generate_name()
    email_name = submitter_name.lower().replace(' ', '.')
    
    grievance = Grievance(
        submitter_name=submitter_name,
        service_number=f"A{random.randint(10000, 99999)}",
        rank=random.choice(RANKS),
        email=f"{email_name}@forces.gc.ca",
        phone=f"613-555-{random.randint(1000, 9999)}",
        unit=unit,
        position=random.choice(POSITIONS),
        title=f"{grievance_type} - {grievance_subtype} Issue",
        grievance_type=grievance_type,
        grievance_subtype=grievance_subtype,
        description=f"Test grievance description for {grievance_type} - {grievance_subtype}. Submitted by {submitter_name} regarding issues with {grievance_subtype.lower()}.",
        redress_sought=f"Requesting review and appropriate action to address {grievance_subtype.lower()} concerns in accordance with unit policies.",
        status=random.choice(STATUSES),
        created_at=datetime.utcnow() - timedelta(days=created_days_ago),
        user_id=session.query(User).filter_by(unit=unit).first().id
    )
    session.add(grievance)
    session.commit()
    
    # Add random notes (30% chance per grievance)
    if random.random() < 0.3:
        supervisor = session.query(User).filter_by(unit=unit, role="supervisor").first()
        note_content = random.choice([
            f"Initial review completed. Scheduling meeting with {submitter_name} to discuss details.",
            f"Met with {submitter_name} to discuss the {grievance_subtype.lower()} concern. Follow-up actions identified.",
            f"Progress update: Working with unit leadership to address the {grievance_type.lower()} issue.",
            f"Documentation received from {submitter_name}. Under review by chain of command.",
            f"Consultation with subject matter experts regarding {grievance_subtype.lower()} concerns."
        ])
        
        note = Note(
            content=note_content,
            grievance_id=grievance.id,
            user_id=supervisor.id if supervisor else grievance.user_id
        )
        session.add(note)
        session.commit()
    
    return grievance

def main():
    with Session(engine) as session:
        # Create supervisors for each unit
        for unit in UNITS:
            create_supervisor(session, unit)
            print(f"Created supervisor for {unit}")
            
            # Create random number of grievances (3-8) for each unit
            num_grievances = random.randint(3, 8)
            for i in range(num_grievances):
                created_days_ago = random.randint(1, 365)  # Random date within the last year
                grievance = create_grievance(session, unit, created_days_ago)
                print(f"Created grievance {i+1}/{num_grievances} for {unit} from {created_days_ago} days ago")

if __name__ == "__main__":
    main()
    print("Test data population complete!") 