from flask import Flask, request, jsonify, render_template
import re
import math
import json

app = Flask(__name__)

class AITextDetector:
    def __init__(self):
        self.ai_indicators = {
            'formal_phrases': [
                'furthermore', 'moreover', 'consequently', 'therefore', 'nonetheless',
                'nevertheless', 'additionally', 'subsequently', 'specifically', 'particularly',
                'accordingly', 'alternatively', 'simultaneously', 'comprehensively', 'extensively',
                'systematically', 'methodically', 'strategically', 'effectively', 'efficiently'
            ],
            'technical_terms': [
                'algorithm', 'methodology', 'framework', 'paradigm', 'optimization',
                'implementation', 'configuration', 'infrastructure', 'architecture', 'protocol',
                'specification', 'initialization', 'iteration', 'evaluation', 'validation',
                'authentication', 'authorization', 'encryption', 'deployment', 'scalability'
            ],
            'academic_phrases': [
                'it is important to note', 'it should be emphasized', 'research indicates',
                'studies suggest', 'evidence shows', 'data reveals', 'analysis demonstrates',
                'findings indicate', 'results suggest', 'empirical evidence', 'statistical analysis',
                'peer-reviewed studies', 'theoretical framework', 'conceptual model'
            ],
            'structured_phrases': [
                'in conclusion', 'to summarize', 'in summary', 'overall', 'broadly speaking',
                'all things considered', 'for instance', 'for example', 'such as', 'including',
                'particularly', 'especially', 'notably', 'remarkably', 'interestingly'
            ],
            'hedge_words': [
                'potentially', 'possibly', 'presumably', 'arguably', 'conceivably',
                'theoretically', 'hypothetically', 'allegedly', 'supposedly', 'apparently',
                'seemingly', 'ostensibly', 'likely', 'probably', 'perhaps', 'might'
            ]
        }
        
        self.human_indicators = {
            'conversational': [
                'i think', 'i believe', 'in my opinion', 'personally', 'honestly',
                'frankly', 'to be honest', 'i feel like', 'i guess', 'you know',
                'like', 'um', 'uh', 'well', 'so', 'actually', 'basically',
                'literally', 'totally', 'really', 'pretty', 'quite', 'sort of'
            ],
            'personal_pronouns': [
                'i am', 'i was', 'i have', 'i had', 'i will', 'i would',
                'my', 'mine', 'myself', 'me', 'we', 'us', 'our', 'ours'
            ],
            'informal_expressions': [
                'gonna', 'wanna', 'gotta', 'kinda', 'sorta', 'dunno', 'yeah',
                'yep', 'nope', 'nah', 'ok', 'okay', 'alright', 'sure', 'fine',
                'cool', 'awesome', 'great', 'amazing', 'weird', 'strange', 'funny'
            ],
            'emotional_expressions': [
                'i love', 'i hate', 'i enjoy', 'i like', 'i dislike', 'i prefer',
                'i hope', 'i wish', 'i want', 'i need', 'i feel', 'excited',
                'happy', 'sad', 'angry', 'frustrated', 'surprised', 'confused'
            ],
            'contractions': [
                "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
                "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd",
                "won't", "can't", "don't", "doesn't", "didn't", "haven't", "hasn't"
            ]
        }

    def analyze_text(self, text):
        """Analyze text for AI vs Human indicators"""
        text_lower = text.lower()
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        ai_score = 0
        human_score = 0
        indicators_found = {'ai': [], 'human': []}

        # Check AI indicators
        for category, indicators in self.ai_indicators.items():
            for indicator in indicators:
                count = text_lower.count(indicator)
                if count > 0:
                    ai_score += count * 2
                    indicators_found['ai'].append({
                        'phrase': indicator,
                        'count': count,
                        'category': category
                    })

        # Check human indicators
        for category, indicators in self.human_indicators.items():
            for indicator in indicators:
                count = text_lower.count(indicator)
                if count > 0:
                    human_score += count * 2
                    indicators_found['human'].append({
                        'phrase': indicator,
                        'count': count,
                        'category': category
                    })

        # Advanced linguistic analysis
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # AI tends to have longer, more structured sentences
        if avg_sentence_length > 25:
            ai_score += 5
        elif avg_sentence_length < 12:
            human_score += 3

        # Check for passive voice (more common in AI)
        passive_patterns = ['was', 'were', 'been', 'being']
        passive_count = sum(text_lower.count(p) for p in passive_patterns)
        ai_score += passive_count * 0.5

        # Vocabulary complexity
        unique_words = len(set(words))
        vocab_ratio = unique_words / max(len(words), 1)
        if vocab_ratio > 0.8:
            ai_score += 2
        elif vocab_ratio < 0.6:
            human_score += 2

        # Determine final prediction
        total_score = ai_score + human_score
        if total_score == 0:
            confidence = 50
            prediction = "Inconclusive"
        elif ai_score > human_score:
            confidence = min((ai_score / total_score) * 100, 95)
            prediction = "AI Generated"
        else:
            confidence = min((human_score / total_score) * 100, 95)
            prediction = "Human Written"

        return {
            'prediction': prediction,
            'confidence': round(confidence, 1),
            'indicators': indicators_found,
            'stats': {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_sentence_length': round(avg_sentence_length, 1),
                'vocab_ratio': round(vocab_ratio, 2),
                'ai_score': round(ai_score, 1),
                'human_score': round(human_score, 1)
            }
        }

detector = AITextDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if len(text) < 20:
            return jsonify({'error': 'Text too short for analysis'}), 400
        
        result = detector.analyze_text(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)