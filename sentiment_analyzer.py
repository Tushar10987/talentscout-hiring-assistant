from textblob import TextBlob
from typing import Dict, List
from config import Config

class SentimentAnalyzer:
    
    def __init__(self):
        self.sentiment_history = []
    
    def analyze(self, text: str) -> Dict[str, any]:
        if not text:
            return {
                "polarity": 0.0,
                "subjectivity": 0.0,
                "label": "Neutral",
                "emoji": "😐",
                "confidence": "Low"
            }
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > Config.SENTIMENT_POSITIVE_THRESHOLD:
            label = "Positive"
            emoji = "😊"
        elif polarity < Config.SENTIMENT_NEGATIVE_THRESHOLD:
            label = "Negative"
            emoji = "😟"
        else:
            label = "Neutral"
            emoji = "😐"
        
        if subjectivity > 0.6:
            confidence = "High"
        elif subjectivity > 0.3:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        result = {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "label": label,
            "emoji": emoji,
            "confidence": confidence
        }
        
        self.sentiment_history.append(result)
        return result
    
    def get_emotional_state(self, polarity: float, subjectivity: float) -> str:
        if polarity > 0.5 and subjectivity > 0.5:
            return "Enthusiastic"
        elif polarity > 0.3:
            return "Confident"
        elif polarity < -0.3 and subjectivity > 0.5:
            return "Nervous"
        elif polarity < -0.3:
            return "Uncertain"
        elif subjectivity < 0.3:
            return "Professional"
        else:
            return "Calm"
    
    def get_aggregate_sentiment(self) -> Dict[str, any]:
        if not self.sentiment_history:
            return {
                "average_polarity": 0.0,
                "average_subjectivity": 0.0,
                "overall_label": "Neutral",
                "trend": "Stable"
            }
        
        avg_polarity = sum(s["polarity"] for s in self.sentiment_history) / len(self.sentiment_history)
        avg_subjectivity = sum(s["subjectivity"] for s in self.sentiment_history) / len(self.sentiment_history)
        
        if avg_polarity > Config.SENTIMENT_POSITIVE_THRESHOLD:
            overall_label = "Positive"
        elif avg_polarity < Config.SENTIMENT_NEGATIVE_THRESHOLD:
            overall_label = "Negative"
        else:
            overall_label = "Neutral"
        
        if len(self.sentiment_history) >= 3:
            recent = [s["polarity"] for s in self.sentiment_history[-3:]]
            if recent[-1] > recent[0]:
                trend = "Improving"
            elif recent[-1] < recent[0]:
                trend = "Declining"
            else:
                trend = "Stable"
        else:
            trend = "Stable"
        
        return {
            "average_polarity": round(avg_polarity, 3),
            "average_subjectivity": round(avg_subjectivity, 3),
            "overall_label": overall_label,
            "trend": trend,
            "emotional_state": self.get_emotional_state(avg_polarity, avg_subjectivity)
        }
    
    def get_sentiment_insights(self) -> List[str]:
        insights = []
        aggregate = self.get_aggregate_sentiment()
        
        if aggregate["overall_label"] == "Positive":
            insights.append("Candidate shows positive engagement throughout the conversation")
        elif aggregate["overall_label"] == "Negative":
            insights.append("Candidate may be experiencing stress or uncertainty")
        
        if aggregate["trend"] == "Improving":
            insights.append("Candidate's confidence is increasing")
        elif aggregate["trend"] == "Declining":
            insights.append("Candidate's engagement may be decreasing")
        
        emotional_state = aggregate["emotional_state"]
        if emotional_state == "Enthusiastic":
            insights.append("Candidate appears highly enthusiastic about the opportunity")
        elif emotional_state == "Nervous":
            insights.append("Candidate may benefit from additional support or clarification")
        elif emotional_state == "Professional":
            insights.append("Candidate maintains a professional and composed demeanor")
        
        return insights if insights else ["Neutral sentiment detected - standard engagement level"]
    
    def reset(self):
        self.sentiment_history = []
