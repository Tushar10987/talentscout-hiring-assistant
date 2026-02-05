# TalentScout Hiring Assistant

Advanced AI-Powered Technical Screening Chatbot with Sentiment Analysis and Multilingual Support

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

TalentScout Hiring Assistant is an intelligent chatbot designed to streamline the initial technical screening process for recruitment agencies. It provides an efficient candidate experience while gathering comprehensive data for recruiters.

### Purpose

1. **Information Gathering**: Collects candidate details (name, contact, experience, position, location, tech stack)
2. **Technical Assessment**: Generates tailored technical questions based on candidate's tech stack
3. **Sentiment Analysis**: Analyzes candidate emotions and engagement throughout the conversation

## Features

### Core Features

- Intelligent conversation flow with step-by-step information gathering
- Dynamic question generation tailored to experience level and tech stack
- Context-aware interactions maintaining conversation context
- Input validation for email, phone, and other fields
- SQLite database for secure candidate data storage

### Advanced Features

**Sentiment Analysis**
- Real-time emotion detection using TextBlob
- Polarity and subjectivity analysis
- Emotional state classification (Enthusiastic, Confident, Nervous, etc.)
- Sentiment trend tracking throughout conversation

**Multilingual Support**
- Support for 5 languages: English, Hindi, Spanish, French, German
- Dynamic UI translation
- Language-specific question generation

**Modern UI**
- Dark theme with professional styling
- Progress tracker with visual milestones
- Responsive mobile-friendly layout
- Smooth transitions and hover effects

**Performance**
- Response caching for common queries
- Average AI response time under 3 seconds
- Efficient database queries

**Deployment Ready**
- Docker containerization
- Environment variable configuration
- Production-ready settings

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Groq API Key ([Get one here](https://console.groq.com/))

### Local Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant
   ```

2. Create virtual environment
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Download TextBlob corpora
   ```bash
   python -m textblob.download_corpora
   ```

5. Configure environment variables
   ```bash
   copy .env.example .env
   # Edit .env and add your Groq API key
   ```

6. Run the application
   ```bash
   streamlit run app.py
   ```

7. Open in browser at `http://localhost:8501`

### Docker Installation

```bash
# Create .env file with your API key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Build and start
docker-compose up -d
```

Access at `http://localhost:8501`

---

## Usage

### For Candidates

1. Click "Start Screening" button
2. Provide information step by step:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position
   - Current Location
   - Tech Stack (comma-separated)
3. Review and confirm details
4. Receive personalized technical questions
5. Download screening results (optional)

### Exit Conversation

Type: `exit`, `quit`, `bye`, `goodbye`, or `stop`

---

## Architecture

### System Architecture

```
User (Web)
    |
    v
Streamlit Frontend (app.py)
    |
    +--- AI Engine (Groq)
    +--- Translator Module
    +--- Sentiment Analyzer
    +--- Database (SQLite)
```

### File Structure

```
talentscout-hiring-assistant/
├── app.py                      # Main application
├── config.py                   # Configuration management
├── utils.py                    # Utility functions
├── translator.py               # Multilingual support
├── sentiment_analyzer.py       # Sentiment analysis
├── ai_engine.py               # AI operations
├── database.py                # Database management
├── components.py              # UI components
├── styles.css                 # Custom styling
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
└── README.md                 # Documentation
```

---

## Technologies

### Core Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Backend language |
| Streamlit | 1.28+ | Web framework |
| Groq API | Latest | LLM for question generation |
| SQLite | 3.x | Database |
| TextBlob | 0.17+ | Sentiment analysis |

### AI Model

- **Model**: Llama 3.3 70B (via Groq)
- **Provider**: Groq Cloud
- **Context Window**: 32,768 tokens
- **Average Response Time**: 2-3 seconds

---

## Deployment

### Local Deployment

```bash
streamlit run app.py
```

### Docker Deployment

```bash
docker-compose up -d
```

### AWS Deployment (EC2)

1. Launch EC2 Instance (Ubuntu 22.04 LTS, t2.medium)
2. Connect and setup:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   sudo apt update
   sudo apt install docker.io docker-compose -y
   
   git clone https://github.com/yourusername/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant
   
   nano .env  # Add your API key
   
   sudo docker-compose up -d
   ```
3. Access at `http://your-ec2-ip:8501`

---

## Configuration

Edit `config.py` to customize:

```python
ENABLE_SENTIMENT_ANALYSIS = True  # Toggle sentiment analysis
ENABLE_MULTILINGUAL = True        # Toggle language support
GROQ_MODEL = "llama-3.3-70b-versatile"  # AI model
DATA_RETENTION_DAYS = 90          # Data retention policy
```

