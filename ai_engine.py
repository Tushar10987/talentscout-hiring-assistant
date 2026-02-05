from groq import Groq
from typing import Dict, List, Optional
import time
from config import Config
from utils import parse_tech_stack, calculate_experience_level
from translator import Translator

class AIEngine:
    
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.cache = {} if Config.ENABLE_CACHING else None
        self.response_times = []
    
    def _call_ai(self, prompt: str, system_prompt: str = None) -> str:
        if system_prompt is None:
            system_prompt = "You are an expert technical interviewer and hiring assistant for TalentScout recruitment agency."
        
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            elapsed_time = time.time() - start_time
            self.response_times.append(elapsed_time)
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_technical_questions(
        self,
        candidate_data: Dict,
        language: str = "en"
    ) -> str:
        cache_key = f"{candidate_data.get('tech', '')}-{candidate_data.get('experience', 0)}-{language}"
        if Config.ENABLE_CACHING and cache_key in self.cache:
            return self.cache[cache_key]
        
        technologies = parse_tech_stack(candidate_data.get('tech', ''))
        experience_level = calculate_experience_level(candidate_data.get('experience', 0))
        lang_instruction = Translator.get_language_instruction(language)
        
        prompt = f"""
Generate a comprehensive technical screening assessment for the following candidate:

**Candidate Profile:**
- Name: {candidate_data.get('name', 'N/A')}
- Position: {candidate_data.get('position', 'N/A')}
- Experience: {candidate_data.get('experience', 0)} years ({experience_level})
- Location: {candidate_data.get('location', 'N/A')}
- Tech Stack: {', '.join(technologies)}

**Instructions:**
1. Generate {Config.MIN_QUESTIONS_PER_TECH} to {Config.MAX_QUESTIONS_PER_TECH} technical questions for each technology
2. Questions should be appropriate for {experience_level} level
3. Include a mix of:
   - Theoretical knowledge questions
   - Practical problem-solving scenarios
   - Best practices and design patterns
   - Real-world application questions

4. Provide an overall assessment of the candidate's skill level
5. Suggest 2-3 focus areas for the interview
6. Include 2-3 behavioral questions related to team collaboration and problem-solving

**Format:**
Use clear markdown formatting with headers and sections for each technology.

{lang_instruction}
"""
        
        result = self._call_ai(prompt)
        
        if Config.ENABLE_CACHING:
            self.cache[cache_key] = result
        
        return result
    
    def analyze_candidate_fit(
        self,
        candidate_data: Dict,
        job_description: Optional[str] = None
    ) -> str:
        job_desc_section = f"**Job Description:**\n{job_description}\n" if job_description else ""
        
        prompt = f"""
Analyze the candidate's fit for the role based on their profile:

{job_desc_section}
**Candidate:**
- Position: {candidate_data.get('position', 'N/A')}
- Experience: {candidate_data.get('experience', 0)} years
- Tech Stack: {candidate_data.get('tech', 'N/A')}
- Location: {candidate_data.get('location', 'N/A')}

Provide a brief analysis covering strengths, potential gaps, and overall fit.
"""
        
        return self._call_ai(prompt)
    
    def generate_followup_question(
        self,
        context: str,
        previous_answer: str
    ) -> str:
        prompt = f"""
Based on the following context and answer, generate a relevant follow-up question:

**Context:** {context}
**Answer:** {previous_answer}

Generate one insightful follow-up question to dig deeper.
"""
        
        return self._call_ai(prompt)
    
    def get_average_response_time(self) -> float:
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def clear_cache(self):
        if self.cache is not None:
            self.cache = {}
