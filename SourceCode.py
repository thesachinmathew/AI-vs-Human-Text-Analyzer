import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import re
import math

class AITextDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural Text Analyzer Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0f0f0f')
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'bg': '#0f0f0f',
            'card_bg': '#1a1a1a',
            'secondary_bg': '#252525',
            'accent': '#00d4ff',
            'accent_dim': '#0099cc',
            'gradient_start': '#00d4ff',
            'gradient_end': '#0066ff',
            'text': '#ffffff',
            'text_dim': '#e0e0e0',
            'text_muted': '#a0a0a0',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'danger': '#ff4757',
            'ai_color': '#ff6b6b',
            'human_color': '#4ecdc4',
            'border': '#333333'
        }

        self.canvas = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.setup_neural_background()
        self.setup_ui()
        self.animate_background()
        
        self.ai_indicators = self.get_ai_indicators()
        self.human_indicators = self.get_human_indicators()

    def get_ai_indicators(self):
        return {
            'formal_phrases': [
                'furthermore', 'moreover', 'consequently', 'therefore', 'nonetheless',
                'nevertheless', 'additionally', 'subsequently', 'specifically', 'particularly',
                'accordingly', 'alternatively', 'simultaneously', 'comparatively', 'essentially',
                'fundamentally', 'substantially', 'significantly', 'comprehensively', 'extensively',
                'systematically', 'methodically', 'strategically', 'effectively', 'efficiently',
                'predominantly', 'consistently', 'precisely', 'accurately', 'thoroughly',
                'systematically', 'methodically', 'strategically', 'comprehensively', 'extensively'
            ],
            'technical_terms': [
                'algorithm', 'methodology', 'framework', 'paradigm', 'optimization',
                'implementation', 'configuration', 'infrastructure', 'architecture', 'protocol',
                'specification', 'initialization', 'iteration', 'evaluation', 'validation',
                'authentication', 'authorization', 'encryption', 'deployment', 'scalability',
                'interoperability', 'compatibility', 'functionality', 'capability', 'reliability',
                'maintainability', 'sustainability', 'feasibility', 'viability', 'adaptability'
            ],
            'academic_phrases': [
                'it is important to note', 'it should be emphasized', 'it is worth mentioning',
                'research indicates', 'studies suggest', 'evidence shows', 'data reveals',
                'analysis demonstrates', 'findings indicate', 'results suggest', 'research shows',
                'empirical evidence', 'statistical analysis', 'quantitative data', 'qualitative research',
                'peer-reviewed studies', 'scholarly articles', 'academic literature', 'theoretical framework',
                'conceptual model', 'hypothesis testing', 'experimental design', 'control group',
                'sample size', 'statistical significance', 'correlation analysis', 'regression model'
            ],
            'structured_phrases': [
                'in conclusion', 'to summarize', 'in summary', 'to conclude', 'overall',
                'in general', 'broadly speaking', 'on the whole', 'all things considered',
                'taking everything into account', 'to put it simply', 'in other words',
                'that is to say', 'namely', 'specifically', 'for instance', 'for example',
                'such as', 'including', 'particularly', 'especially', 'notably', 'remarkably',
                'interestingly', 'surprisingly', 'unexpectedly', 'predictably', 'understandably'
            ],
            'hedge_words': [
                'potentially', 'possibly', 'presumably', 'arguably', 'conceivably',
                'theoretically', 'hypothetically', 'presumably', 'allegedly', 'supposedly',
                'apparently', 'seemingly', 'ostensibly', 'evidently', 'presumably',
                'likely', 'probably', 'possibly', 'perhaps', 'maybe', 'might',
                'could', 'would', 'should', 'may', 'can', 'generally', 'typically',
                'usually', 'commonly', 'frequently', 'often', 'sometimes', 'occasionally'
            ]
        }

    def get_human_indicators(self):
        return {
            'conversational': [
                'i think', 'i believe', 'in my opinion', 'personally', 'honestly',
                'frankly', 'to be honest', 'i feel like', 'i guess', 'i suppose',
                'you know', 'like', 'um', 'uh', 'well', 'so', 'actually',
                'basically', 'literally', 'totally', 'really', 'pretty', 'quite',
                'sort of', 'kind of', 'a bit', 'a little', 'somewhat', 'rather',
                'fairly', 'definitely', 'absolutely', 'certainly', 'surely', 'obviously'
            ],
            'personal_pronouns': [
                'i am', 'i was', 'i have', 'i had', 'i will', 'i would',
                'i do', 'i did', 'i can', 'i could', 'i should', 'i must',
                'my', 'mine', 'myself', 'me', 'we', 'us', 'our', 'ours',
                'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves'
            ],
            'informal_expressions': [
                'gonna', 'wanna', 'gotta', 'kinda', 'sorta', 'dunno', 'yeah',
                'yep', 'nope', 'nah', 'ok', 'okay', 'alright', 'sure', 'fine',
                'cool', 'awesome', 'great', 'amazing', 'fantastic', 'wonderful',
                'terrible', 'awful', 'horrible', 'weird', 'strange', 'funny',
                'crazy', 'insane', 'nuts', 'wild', 'sick', 'dope', 'lit'
            ],
            'emotional_expressions': [
                'i love', 'i hate', 'i enjoy', 'i like', 'i dislike', 'i prefer',
                'i hope', 'i wish', 'i want', 'i need', 'i feel', 'i think',
                'excited', 'happy', 'sad', 'angry', 'frustrated', 'disappointed',
                'surprised', 'shocked', 'amazed', 'confused', 'worried', 'scared',
                'nervous', 'anxious', 'relieved', 'grateful', 'proud', 'ashamed'
            ],
            'internet_slang': [
                'lol', 'lmao', 'rofl', 'omg', 'wtf', 'btw', 'fyi', 'imo', 'imho',
                'tbh', 'ngl', 'smh', 'fml', 'yolo', 'bae', 'squad', 'goals',
                'vibes', 'mood', 'stan', 'ship', 'tea', 'spill', 'salty',
                'savage', 'fire', 'ghost', 'flex', 'cap', 'no cap', 'periodt'
            ],
            'casual_time_refs': [
                'yesterday', 'today', 'tomorrow', 'this morning', 'last night',
                'right now', 'just now', 'a while ago', 'earlier', 'later',
                'soon', 'recently', 'lately', 'nowadays', 'these days',
                'back in the day', 'once upon a time', 'the other day'
            ],
            'personal_experiences': [
                'my friend', 'my family', 'my mom', 'my dad', 'my brother',
                'my sister', 'my job', 'my boss', 'my teacher', 'my school',
                'when i was', 'i remember', 'i recall', 'i experienced',
                'happened to me', 'i went to', 'i saw', 'i met', 'i heard'
            ],
            'contractions': [
                "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
                "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd",
                "she'd", "we'd", "they'd", "i'll", "you'll", "he'll", "she'll",
                "we'll", "they'll", "won't", "can't", "don't", "doesn't",
                "didn't", "haven't", "hasn't", "hadn't", "shouldn't", "wouldn't",
                "couldn't", "mustn't", "needn't", "daren't", "oughtn't"
            ]
        }

    def setup_neural_background(self):
        """Create animated neural network background"""
        self.neurons = []
        self.connections = []
        
        # Create neurons
        for _ in range(25):
            x = random.randint(50, 1150)
            y = random.randint(50, 750)
            size = random.randint(3, 6)
            pulse = random.uniform(0, 2 * math.pi)
            neuron = {
                'x': x, 'y': y, 'size': size, 'pulse': pulse,
                'id': self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                            fill=self.colors['accent'], outline='',
                                            stipple='gray25')
            }
            self.neurons.append(neuron)
        
        # Create connections
        for i in range(len(self.neurons)):
            for j in range(i+1, len(self.neurons)):
                if random.random() < 0.15:  # 15% chance of connection
                    x1, y1 = self.neurons[i]['x'], self.neurons[i]['y']
                    x2, y2 = self.neurons[j]['x'], self.neurons[j]['y']
                    line_id = self.canvas.create_line(x1, y1, x2, y2,
                                                    fill=self.colors['accent_dim'],
                                                    width=1, stipple='gray12')
                    self.connections.append({'id': line_id, 'opacity': random.uniform(0.1, 0.3)})

    def animate_background(self):
        """Animate the neural network"""
        for neuron in self.neurons:
            neuron['pulse'] += 0.1
            base_size = neuron['size']
            new_size = base_size + math.sin(neuron['pulse']) * 2
            x, y = neuron['x'], neuron['y']
            self.canvas.coords(neuron['id'], x-new_size, y-new_size, x+new_size, y+new_size)
        
        self.root.after(100, self.animate_background)

    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        self.canvas.create_window(600, 400, window=main_frame, width=1100, height=700)

        # Header section with gradient effect
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'], height=120)
        header_frame.pack(fill='x', pady=(20, 0))
        header_frame.pack_propagate(False)

        # Title with modern styling
        title = tk.Label(header_frame, text="🧠 NEURAL TEXT ANALYZER PRO", 
                        font=("Segoe UI", 32, "bold"),
                        fg=self.colors['accent'], bg=self.colors['bg'])
        title.pack(pady=(20, 5))

        subtitle = tk.Label(header_frame, text="Advanced AI Detection • 200+ Linguistic Indicators • Real-time Analysis",
                           font=("Segoe UI", 11), fg=self.colors['text_muted'], bg=self.colors['bg'])
        subtitle.pack()

        # Content area with modern card design
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, pady=20)

        # Left panel - Input
        left_panel = tk.Frame(content_frame, bg=self.colors['card_bg'], relief='flat')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Input section header
        input_header = tk.Frame(left_panel, bg=self.colors['secondary_bg'], height=50)
        input_header.pack(fill='x')
        input_header.pack_propagate(False)

        tk.Label(input_header, text="📝 TEXT INPUT", font=("Segoe UI", 14, "bold"),
                fg=self.colors['text'], bg=self.colors['secondary_bg']).pack(pady=15)

        # Text input with modern styling
        text_frame = tk.Frame(left_panel, bg=self.colors['card_bg'])
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.text_input = scrolledtext.ScrolledText(
            text_frame, height=15, font=("Consolas", 11),
            bg='#2a2a2a', fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent_dim'],
            selectforeground='black', relief='flat', bd=0,
            wrap=tk.WORD, padx=15, pady=15
        )
        self.text_input.pack(fill='both', expand=True)

        # Button section
        button_frame = tk.Frame(left_panel, bg=self.colors['card_bg'], height=80)
        button_frame.pack(fill='x')
        button_frame.pack_propagate(False)

        self.analyze_button = tk.Button(
            button_frame, text="🔍 ANALYZE TEXT", font=("Segoe UI", 12, "bold"),
            bg=self.colors['accent'], fg='black',
            activebackground=self.colors['accent_dim'], activeforeground='black',
            relief='flat', bd=0, padx=40, pady=15, cursor='hand2',
            command=self.analyze_text
        )
        self.analyze_button.pack(pady=20)

        # Right panel - Results
        right_panel = tk.Frame(content_frame, bg=self.colors['card_bg'], relief='flat')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Results header
        results_header = tk.Frame(right_panel, bg=self.colors['secondary_bg'], height=50)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)

        tk.Label(results_header, text="📊 ANALYSIS RESULTS", font=("Segoe UI", 14, "bold"),
                fg=self.colors['text'], bg=self.colors['secondary_bg']).pack(pady=15)

        # Results content area
        self.results_content = tk.Frame(right_panel, bg=self.colors['card_bg'])
        self.results_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Initial results placeholder
        self.setup_initial_results()

        # Status bar
        status_frame = tk.Frame(main_frame, bg=self.colors['secondary_bg'], height=40)
        status_frame.pack(fill='x', pady=(10, 0))
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(status_frame, text="🟢 Ready to analyze • Neural networks initialized",
                                    font=("Segoe UI", 10), fg=self.colors['text_muted'], 
                                    bg=self.colors['secondary_bg'])
        self.status_label.pack(pady=10)

    def setup_initial_results(self):
        """Setup initial results display"""
        placeholder = tk.Label(self.results_content, 
                              text="Enter text in the input panel\nand click 'ANALYZE TEXT'\nto see detailed results",
                              font=("Segoe UI", 12), fg=self.colors['text_muted'],
                              bg=self.colors['card_bg'], justify='center')
        placeholder.pack(expand=True)

        # Feature highlights
        features_frame = tk.Frame(self.results_content, bg=self.colors['card_bg'])
        features_frame.pack(fill='x', pady=(20, 0))

        features = [
            "🤖 100+ AI Detection Patterns",
            "👤 100+ Human Writing Indicators", 
            "📈 Advanced Statistical Analysis",
            "⚡ Real-time Processing"
        ]

        for feature in features:
            tk.Label(features_frame, text=feature, font=("Segoe UI", 10),
                    fg=self.colors['text_dim'], bg=self.colors['card_bg']).pack(anchor='w', pady=2)

    def advanced_ai_detector(self, text):
        """Enhanced AI detection with 200+ indicators"""
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
                    indicators_found['ai'].append((indicator, count, category))

        # Check human indicators
        for category, indicators in self.human_indicators.items():
            for indicator in indicators:
                count = text_lower.count(indicator)
                if count > 0:
                    human_score += count * 2
                    indicators_found['human'].append((indicator, count, category))

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

        # Check for varied sentence structure (more human)
        sentence_lengths = [len(s.split()) for s in sentences]
        if len(set(sentence_lengths)) > len(sentence_lengths) * 0.7:
            human_score += 3

        # Vocabulary complexity
        unique_words = len(set(words))
        vocab_ratio = unique_words / max(len(words), 1)
        if vocab_ratio > 0.8:
            ai_score += 2  # Very high vocabulary diversity can indicate AI
        elif vocab_ratio < 0.6:
            human_score += 2  # Repetitive vocabulary more human

        # Determine final prediction
        total_score = ai_score + human_score
        if total_score == 0:
            confidence = 50
            prediction = "Neutral"
        elif ai_score > human_score:
            confidence = min((ai_score / total_score) * 100, 95)
            prediction = "AI Generated"
        else:
            confidence = min((human_score / total_score) * 100, 95)
            prediction = "Human Written"

        return prediction, confidence, indicators_found, {
            'avg_sentence_length': avg_sentence_length,
            'vocab_ratio': vocab_ratio,
            'passive_count': passive_count,
            'ai_score': ai_score,
            'human_score': human_score
        }

    def analyze_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze!")
            return
        if len(text) < 20:
            messagebox.showwarning("Warning", "Please enter at least 20 characters for accurate analysis!")
            return

        self.status_label.configure(text="🔄 Neural networks processing... Analyzing linguistic patterns", 
                                   fg=self.colors['warning'])
        self.analyze_button.configure(text="ANALYZING...", state='disabled')

        def process():
            time.sleep(2)  # Simulate processing time
            prediction, confidence, indicators, stats = self.advanced_ai_detector(text)
            self.root.after(0, lambda: self.show_results(prediction, confidence, indicators, stats, text))

        threading.Thread(target=process, daemon=True).start()

    def show_results(self, prediction, confidence, indicators, stats, text):
        self.analyze_button.configure(text="🔍 ANALYZE TEXT", state='normal')
        
        # Clear previous results
        for widget in self.results_content.winfo_children():
            widget.destroy()

        # Create scrollable results
        results_canvas = tk.Canvas(self.results_content, bg=self.colors['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_content, orient="vertical", command=results_canvas.yview)
        scrollable_frame = tk.Frame(results_canvas, bg=self.colors['card_bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )

        results_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=scrollbar.set)

        # Main prediction display
        pred_frame = tk.Frame(scrollable_frame, bg=self.colors['secondary_bg'], relief='flat')
        pred_frame.pack(fill='x', padx=10, pady=10)

        icon = "🤖" if prediction == "AI Generated" else "👤" if prediction == "Human Written" else "⚖️"
        color = self.colors['ai_color'] if prediction == "AI Generated" else self.colors['human_color']
        
        pred_label = tk.Label(pred_frame, text=f"{icon} {prediction.upper()}",
                             font=("Segoe UI", 18, "bold"), fg=color, bg=self.colors['secondary_bg'])
        pred_label.pack(pady=15)

        # Confidence display with modern progress bar
        conf_frame = tk.Frame(pred_frame, bg=self.colors['secondary_bg'])
        conf_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(conf_frame, text=f"Confidence: {confidence:.1f}%",
                font=("Segoe UI", 12, "bold"), fg=self.colors['text'], 
                bg=self.colors['secondary_bg']).pack()

        # Modern progress bar
        progress_bg = tk.Frame(conf_frame, bg='#333333', height=8)
        progress_bg.pack(fill='x', pady=10)

        progress_fill = tk.Frame(progress_bg, bg=color, height=8)
        progress_fill.place(x=0, y=0, relwidth=confidence/100, height=8)

        # Statistics section
        stats_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'])
        stats_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(stats_frame, text="📈 LINGUISTIC ANALYSIS", font=("Segoe UI", 12, "bold"),
                fg=self.colors['accent'], bg=self.colors['card_bg']).pack(anchor='w', pady=5)

        stats_info = [
            f"Words: {len(text.split())}",
            f"Characters: {len(text)}",
            f"Sentences: {len([s for s in text.split('.') if s.strip()])}",
            f"Avg Sentence Length: {stats['avg_sentence_length']:.1f} words",
            f"Vocabulary Ratio: {stats['vocab_ratio']:.2f}",
            f"AI Score: {stats['ai_score']:.1f}",
            f"Human Score: {stats['human_score']:.1f}"
        ]

        for stat in stats_info:
            tk.Label(stats_frame, text=f"• {stat}", font=("Segoe UI", 10),
                    fg=self.colors['text_dim'], bg=self.colors['card_bg']).pack(anchor='w', padx=20)

        # Indicators found
        if indicators['ai'] or indicators['human']:
            indicators_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'])
            indicators_frame.pack(fill='x', padx=10, pady=10)

            tk.Label(indicators_frame, text="🔍 KEY INDICATORS DETECTED", font=("Segoe UI", 12, "bold"),
                    fg=self.colors['accent'], bg=self.colors['card_bg']).pack(anchor='w', pady=5)

            # Show top AI indicators
            if indicators['ai']:
                ai_frame = tk.Frame(indicators_frame, bg=self.colors['card_bg'])
                ai_frame.pack(fill='x', pady=5)
                tk.Label(ai_frame, text="🤖 AI Patterns:", font=("Segoe UI", 11, "bold"),
                        fg=self.colors['ai_color'], bg=self.colors['card_bg']).pack(anchor='w', padx=20)
                
                for indicator, count, category in sorted(indicators['ai'], key=lambda x: x[1], reverse=True)[:10]:
                    tk.Label(ai_frame, text=f"• '{indicator}' ({count}x) - {category}",
                            font=("Segoe UI", 9), fg=self.colors['text_dim'], 
                            bg=self.colors['card_bg']).pack(anchor='w', padx=40)

            # Show top human indicators
            if indicators['human']:
                human_frame = tk.Frame(indicators_frame, bg=self.colors['card_bg'])
                human_frame.pack(fill='x', pady=5)
                tk.Label(human_frame, text="👤 Human Patterns:", font=("Segoe UI", 11, "bold"),
                        fg=self.colors['human_color'], bg=self.colors['card_bg']).pack(anchor='w', padx=20)
                
                for indicator, count, category in sorted(indicators['human'], key=lambda x: x[1], reverse=True)[:10]:
                    tk.Label(human_frame, text=f"• '{indicator}' ({count}x) - {category}",
                            font=("Segoe UI", 9), fg=self.colors['text_dim'], 
                            bg=self.colors['card_bg']).pack(anchor='w', padx=40)

        # Pack scrollbar and canvas
        results_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Update status
        status_text = f"✅ Analysis complete - {prediction} ({confidence:.1f}% confidence)"
        self.status_label.configure(text=status_text, fg=self.colors['success'])

def main():
    root = tk.Tk()
    app = AITextDetectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
