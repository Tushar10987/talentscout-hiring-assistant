# Quick Start Guide

## Running the Application

The application is currently running at: **http://localhost:8501**

### Access the Application

1. Open your web browser
2. Navigate to: `http://localhost:8501`
3. You should see the TalentScout Hiring Assistant welcome screen

---

## Quick Test Flow

### Complete Screening Test

1. **Welcome Screen**
   - Click "Start Screening" button
   
2. **Enter Information**
   - Name: John Doe
   - Email: john.doe@example.com
   - Phone: +1 234 567 8900
   - Experience: 5 years
   - Position: Full Stack Developer
   - Location: San Francisco, CA
   - Tech Stack: Python, React, PostgreSQL, Docker, AWS

3. **Observe Features**
   - Progress tracker updates
   - Language selector (try switching languages)
   - Sentiment analysis badge appears
   - Input validation works

4. **Confirm and Generate**
   - Review your details
   - Click "Confirm & Continue"
   - Wait for AI to generate questions (2-3 seconds)

5. **View Results**
   - Technical questions generated
   - Sentiment insights displayed
   - Performance metrics shown
   - Export to JSON available

---

## Test Multilingual Support

1. Find the language selector at the top-right
2. Switch between: English, Hindi, Spanish, French, German
3. Notice how the UI updates instantly

---

## Test Sentiment Analysis

When entering your tech stack, try different tones:
- **Positive**: "I'm really excited about Python, React, and AWS!"
- **Neutral**: "Python, React, PostgreSQL"
- **Negative**: "I'm not very confident with these technologies"

Watch the sentiment badge update with score.

---

## Exit Functionality

At any point, type one of these keywords:
- `exit`
- `quit`
- `bye`
- `goodbye`
- `stop`

---

## Performance Metrics

After completing a screening:
- **AI Response Time**: Should be under 3 seconds
- **Total Time**: Complete screening in 4-5 minutes
- **Sentiment Analysis**: Real-time emotional state tracking

---

## Troubleshooting

### Application Not Loading

1. Check if Streamlit is running in terminal
2. Verify the port number (should be 8501)
3. Try refreshing the browser
4. Clear browser cache if needed

### Database Errors

1. Database is auto-created on first run
2. Check if write permissions exist
3. Delete `talentscout.db` and restart app

### API Errors

1. Verify Groq API key is set in `.env`
2. Check internet connection
3. Verify API quota hasn't been exceeded

---

## Project Files

### Core Files
- `app.py` - Main application
- `config.py` - Configuration
- `ai_engine.py` - AI operations
- `database.py` - Data persistence
- `sentiment_analyzer.py` - Sentiment analysis
- `translator.py` - Multilingual support
- `components.py` - UI components
- `utils.py` - Helper functions
- `styles.css` - Custom styling

### Deployment
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose
- `.env.example` - Environment template
- `requirements.txt` - Dependencies

---

## Key Features

### Sentiment Analysis
- Real-time emotion detection
- Visual sentiment badges
- Recruiter insights

### Multilingual Support
- 5 languages supported
- Dynamic UI translation
- Language-specific questions

### Modern UI
- Dark theme with teal accents
- Smooth transitions
- Responsive layout

### Performance
- Under 3s AI response time
- Response caching
- Efficient database queries

### Cloud Ready
- Docker containerization
- Environment configuration
- Production-ready settings

---

## Next Steps

1. Test the application with the complete flow
2. Try different languages
3. Review the code architecture
4. Check README.md for detailed documentation
5. Use Docker for deployment

---

Made by TalentScout Team
