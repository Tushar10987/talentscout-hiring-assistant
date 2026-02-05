import re
import hashlib
import secrets
from datetime import datetime

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    cleaned = re.sub(r'[^\d+]', '', phone)
    return len(cleaned) >= 10

def sanitize_input(text: str) -> str:
    return text.strip()[:500]

def parse_tech_stack(tech_stack: str) -> list:
    if not tech_stack:
        return []
    technologies = [tech.strip() for tech in tech_stack.split(',')]
    return [tech for tech in technologies if tech]

def calculate_experience_level(years: int) -> str:
    if years == 0:
        return "Entry Level"
    elif years <= 2:
        return "Junior"
    elif years <= 5:
        return "Mid-Level"
    elif years <= 10:
        return "Senior"
    else:
        return "Expert"

def get_greeting_by_time() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Hello"

def generate_session_id() -> str:
    return secrets.token_hex(16)

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text: str, max_length: int = 100) -> str:
    return text[:max_length] + "..." if len(text) > max_length else text

def estimate_completion_time(current_step: int, total_steps: int) -> int:
    avg_time_per_step = 30
    remaining_steps = total_steps - current_step
    return remaining_steps * avg_time_per_step
