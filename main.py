import re
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics
from datetime import datetime
import random

@dataclass
class Character:
    """Represents a character with their dialogue traits."""
    name: str
    voice_patterns: Dict[str, float]  # linguistic patterns and frequencies
    emotional_range: List[str]
    speech_quirks: List[str]
    dialogue_count: int = 0
    avg_sentence_length: float = 0.0
    vocabulary_complexity: float = 0.0

@dataclass
class DialogueLine:
    """Represents a single line of dialogue."""
    speaker: str
    text: str
    context: str
    emotional_tone: str
    timestamp: str
    scene_position: int

@dataclass
class SceneContext:
    """Context information for the current scene."""
    setting: str
    mood: str
    tension_level: int  # 1-10 scale
    characters_present: List[str]
    plot_points: List[str]

@dataclass
class DialogueAlternative:
    """Represents an alternative phrasing for dialogue."""
    original_phrase: str
    alternatives: List[str]
    character_voice_adjusted: List[str]  # alternatives adapted to character voice
    tone_context: str

class DialogueComposer:
    """AI-driven story writing coach for dialogue composition."""
    
    def __init__(self):
        self.characters: Dict[str, Character] = {}
        self.dialogue_history: List[DialogueLine] = []
        self.scene_context: Optional[SceneContext] = None
        self.cliche_patterns = self._load_cliche_patterns()
        self.cliche_alternatives = self._load_cliche_alternatives()
        self.trope_database = self._load_trope_database()
        self.tone_keywords = self._load_tone_keywords()
        self.voice_modifiers = self._load_voice_modifiers()
        
    def _load_cliche_patterns(self) -> List[str]:
        """Load common cliché patterns to detect in dialogue."""
        return [
            r"think outside the box",
            r"loose cannon",
            r"perfect storm",
            r"can of worms",
            r"what goes around comes around",
            r"dead as a doornail",
            r"plenty of fish in the sea",
            r"ignorance is bliss",
            r"like a kid in a candy store",
            r"you can't judge a book by its cover",
            r"take the tiger by the tail",
            r"every rose has its thorn",
            r"good things come to those who wait",
            r"in the nick of time",
            r"if only walls could talk",
            r"the apple doesn't fall far from the tree",
            r"the pot calling the kettle black",
            r"the grass is always greener on the other side",
            r"beating a dead horse"
        ]
    
    def _load_cliche_alternatives(self) -> Dict[str, List[str]]:
        """Load fresh alternatives for common clichés."""
        return {
            "think outside the box": [
                "find a new angle",
                "break the pattern",
                "try something unexpected",
                "look at it differently",
                "challenge the assumptions"
            ],
            "loose cannon": [
                "unpredictable force",
                "wild card",
                "walking disaster",
                "chaos magnet",
                "human hurricane"
            ],
            "perfect storm": [
                "worst-case scenario",
                "everything going wrong at once",
                "complete disaster",
                "catastrophic alignment",
                "nightmare convergence"
            ],
            "can of worms": [
                "messy situation",
                "complicated problem",
                "tangled mess",
                "rabbit hole",
                "minefield"
            ],
            "what goes around comes around": [
                "karma catches up",
                "actions have consequences",
                "the universe balances things out",
                "payback time",
                "justice finds a way"
            ],
            "dead as a doornail": [
                "completely lifeless",
                "stone cold",
                "gone for good",
                "finished",
                "beyond saving"
            ],
            "plenty of fish in the sea": [
                "other opportunities out there",
                "not the only option",
                "more chances ahead",
                "different paths to explore",
                "other doors will open"
            ],
            "ignorance is bliss": [
                "sometimes not knowing is better",
                "knowledge can be a burden",
                "the truth hurts",
                "some things are better left unknown",
                "reality can be harsh"
            ],
            "like a kid in a candy store": [
                "absolutely thrilled",
                "overwhelmed with excitement",
                "eyes wide with wonder",
                "spoiled for choice",
                "drunk on possibilities"
            ],
            "you can't judge a book by its cover": [
                "appearances can be deceiving",
                "there's more than meets the eye",
                "looks don't tell the whole story",
                "first impressions can be wrong",
                "scratch the surface"
            ],
            "in the nick of time": [
                "just barely made it",
                "cutting it close",
                "with seconds to spare",
                "at the last possible moment",
                "pulled it off somehow"
            ],
            "beating a dead horse": [
                "pointless argument",
                "wasted effort",
                "going in circles",
                "talking to a wall",
                "spitting in the wind"
            ]
        }
    
    def _load_voice_modifiers(self) -> Dict[str, Dict[str, List[str]]]:
        """Load voice modification patterns for different character types."""
        return {
            "formal": {
                "prefixes": ["Perhaps", "It appears that", "One might consider", "I believe"],
                "sentence_structures": ["complex", "conditional"],
                "word_choices": ["sophisticated", "precise"]
            },
            "casual": {
                "prefixes": ["Look", "Okay", "Yeah", "Well"],
                "contractions": ["can't", "won't", "doesn't", "haven't"],
                "informal_markers": ["like", "you know", "kinda", "sorta"]
            },
            "dramatic": {
                "intensifiers": ["absolutely", "completely", "utterly", "devastatingly"],
                "emotional_markers": ["!", "...", "—"],
                "repetition": True
            },
            "terse": {
                "characteristics": ["short_sentences", "minimal_words", "direct"],
                "avoid": ["unnecessary_words", "elaboration"]
            }
        }
    
    def _load_trope_database(self) -> Dict[str, List[str]]:
        """Load common dialogue tropes by category."""
        return {
            "villain_monologue": [
                "you see, my plan was",
                "before you die",
                "you cannot stop me",
                "i have already won"
            ],
            "exposition_dump": [
                "as you know",
                "remember when we",
                "let me tell you about"
            ],
            "romantic_tension": [
                "you drive me crazy",
                "i hate that i love you",
                "we can't keep doing this"
            ],
            "conflict_escalation": [
                "you always do this",
                "here we go again",
                "typical"
            ]
        }
    
    def _load_tone_keywords(self) -> Dict[str, List[str]]:
        """Load keywords associated with different emotional tones."""
        return {
            "angry": ["furious", "rage", "damn", "hell", "angry", "mad", "pissed", "livid", "hate"],
            "sad": ["tears", "crying", "hurt", "broken", "lost", "empty", "alone", "depressed", "sob"],
            "happy": ["amazing", "wonderful", "fantastic", "love", "joy", "excited", "thrilled", "delighted"],
            "fearful": ["scared", "terrified", "afraid", "nightmare", "panic", "dangerous", "worried", "anxious"],
            "sarcastic": ["oh great", "fantastic", "wonderful", "sure", "right", "obviously", "brilliant", "perfect"],
            "romantic": ["love", "heart", "beautiful", "forever", "soul", "kiss", "darling", "honey", "sweetheart"],
            "mysterious": ["secret", "hidden", "shadow", "whisper", "unknown", "strange", "curious", "enigma"],
            "aggressive": ["fight", "kill", "destroy", "attack", "war", "battle", "crush", "defeat"],
            "defensive": ["told you", "already", "didn't do", "wasn't me", "innocent", "prove it"]
        }

    def add_character(self, name: str, voice_description: Dict = None) -> None:
        """Add a new character to track."""
        voice_patterns = voice_description or {
            "formality": 0.5,  # 0 = very casual, 1 = very formal
            "verbosity": 0.5,  # 0 = terse, 1 = verbose
            "emotion_intensity": 0.5,  # 0 = flat, 1 = dramatic
            "interruption_tendency": 0.3,  # likelihood to interrupt
            "question_frequency": 0.2,  # frequency of asking questions
        }
        
        self.characters[name] = Character(
            name=name,
            voice_patterns=voice_patterns,
            emotional_range=[],
            speech_quirks=[]
        )
    
    def set_scene_context(self, setting: str, mood: str, tension: int, 
                         characters: List[str], plot_points: List[str] = None) -> None:
        """Set the current scene context."""
        self.scene_context = SceneContext(
            setting=setting,
            mood=mood,
            tension_level=tension,
            characters_present=characters,
            plot_points=plot_points or []
        )
    
    def generate_dialogue_alternatives(self, speaker: str, text: str, 
                                     num_alternatives: int = 5) -> List[DialogueAlternative]:
        """Generate fresh alternatives for clichéd dialogue while maintaining character voice."""
        alternatives = []
        
        # Find clichés in the text
        text_lower = text.lower()
        detected_cliches = []
        
        for pattern in self.cliche_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # Find the actual phrase in original case
                start, end = match.span()
                original_phrase = text[start:end]
                detected_cliches.append((original_phrase, pattern))
        
        # Generate alternatives for each detected cliché
        for original_phrase, pattern in detected_cliches:
            base_alternatives = self.cliche_alternatives.get(pattern, [])
            
            if base_alternatives:
                # Select diverse alternatives
                selected_alternatives = random.sample(
                    base_alternatives, 
                    min(num_alternatives, len(base_alternatives))
                )
                
                # Adapt alternatives to character voice
                character_adapted = self._adapt_to_character_voice(
                    speaker, selected_alternatives, text
                )
                
                alternative = DialogueAlternative(
                    original_phrase=original_phrase,
                    alternatives=selected_alternatives,
                    character_voice_adjusted=character_adapted,
                    tone_context=self._analyze_tone(text)
                )
                
                alternatives.append(alternative)
        
        return alternatives
    
    def _adapt_to_character_voice(self, speaker: str, alternatives: List[str], 
                                 original_text: str) -> List[str]:
        """Adapt alternative phrases to match character's established voice patterns."""
        if speaker not in self.characters:
            return alternatives
        
        character = self.characters[speaker]
        voice_patterns = character.voice_patterns
        adapted_alternatives = []
        
        for alt in alternatives:
            adapted = alt
            
            # Adjust formality level
            formality = voice_patterns.get("formality", 0.5)
            if formality > 0.7:  # Formal character
                adapted = self._make_more_formal(adapted)
            elif formality < 0.3:  # Casual character
                adapted = self._make_more_casual(adapted)
            
            # Adjust verbosity
            verbosity = voice_patterns.get("verbosity", 0.5)
            if verbosity > 0.7:  # Verbose character
                adapted = self._make_more_verbose(adapted)
            elif verbosity < 0.3:  # Terse character
                adapted = self._make_more_terse(adapted)
            
            # Adjust emotional intensity
            emotion_intensity = voice_patterns.get("emotion_intensity", 0.5)
            if emotion_intensity > 0.7:  # Dramatic character
                adapted = self._add_emotional_intensity(adapted)
            elif emotion_intensity < 0.3:  # Flat character
                adapted = self._reduce_emotional_intensity(adapted)
            
            adapted_alternatives.append(adapted)
        
        return adapted_alternatives
    
    def _make_more_formal(self, text: str) -> str:
        """Make text more formal for character voice."""
        formal_replacements = {
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "isn't": "is not",
            "aren't": "are not",
            "yeah": "yes",
            "okay": "very well",
            "sure": "certainly"
        }
        
        result = text
        for informal, formal in formal_replacements.items():
            result = re.sub(r'\b' + informal + r'\b', formal, result, flags=re.IGNORECASE)
        
        # Add formal prefixes only if text doesn't already start formally
        if not re.match(r'^(Perhaps|It seems|One might|I believe)', result):
            formal_prefixes = ["Perhaps", "It appears that", "One might say"]
            if random.random() < 0.2:  # Reduced frequency
                prefix = random.choice(formal_prefixes)
                result = f"{prefix} {result.lower()}"
        
        return result
    
    def _make_more_casual(self, text: str) -> str:
        """Make text more casual for character voice."""
        casual_replacements = {
            "cannot": "can't",
            "will not": "won't",
            "do not": "don't",
            "is not": "isn't",
            "are not": "aren't",
            "very well": "okay",
            "certainly": "sure",
            "perhaps": "maybe"
        }
        
        result = text
        for formal, casual in casual_replacements.items():
            result = re.sub(r'\b' + formal + r'\b', casual, result, flags=re.IGNORECASE)
        
        # Add casual markers occasionally, but not if already present
        if not re.match(r'^(Look|Hey|Well|You know)', result, re.IGNORECASE):
            casual_markers = ["Look,", "Hey,", "Well,"]
            if random.random() < 0.2:  # Reduced frequency
                marker = random.choice(casual_markers)
                result = f"{marker} {result.lower()}"
        
        return result
    
    def _make_more_verbose(self, text: str) -> str:
        """Make text more verbose for character voice."""
        verbose_expansions = {
            "bad": "absolutely terrible",
            "good": "quite excellent",
            "big": "enormously large",
            "small": "rather diminutive",
            "fast": "incredibly swift",
            "slow": "painfully sluggish",
            "hard": "extraordinarily difficult",
            "easy": "remarkably simple"
        }
        
        result = text
        for simple, verbose in verbose_expansions.items():
            result = re.sub(r'\b' + simple + r'\b', verbose, result, flags=re.IGNORECASE)
        
        # Add explanatory phrases
        explanatory_additions = [
            ", if you understand what I mean",
            ", as I'm sure you can appreciate",
            ", which is quite significant",
            ", in my considered opinion"
        ]
        
        if random.random() < 0.4:
            addition = random.choice(explanatory_additions)
            result = result.rstrip('.!?') + addition + "."
        
        return result
    
    def _make_more_terse(self, text: str) -> str:
        """Make text more terse for character voice."""
        # Remove unnecessary words
        terse_removals = [
            r'\b(quite|rather|very|really|absolutely|completely)\s+',
            r'\b(I think|I believe|it seems|perhaps|maybe)\s+',
            r'\b(you know|like|sort of|kind of)\s+',
            r',\s*(which is|that is|as you know)',
        ]
        
        result = text
        for pattern in terse_removals:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        # Simplify sentence structure
        result = re.sub(r'\s+', ' ', result).strip()
        
        # Remove trailing qualifiers
        result = re.sub(r',?\s+(I guess|I suppose|or something)\.?$', '.', result)
        
        return result
    
    def _add_emotional_intensity(self, text: str) -> str:
        """Add emotional intensity for dramatic characters."""
        intensifiers = ["absolutely", "completely", "utterly", "totally", "damn"]
        
        # Add intensifier
        if random.random() < 0.5:
            intensifier = random.choice(intensifiers)
            # Insert before adjectives or important words
            result = re.sub(r'\b(bad|good|wrong|right|important|serious)\b', 
                          f'{intensifier} \\1', text, flags=re.IGNORECASE)
        else:
            result = text
        
        # Add emotional punctuation
        if not text.endswith(('!', '?', '...')):
            if random.random() < 0.6:
                result = result.rstrip('.') + '!'
        
        return result
    
    def _reduce_emotional_intensity(self, text: str) -> str:
        """Reduce emotional intensity for flat/controlled characters."""
        # Remove intensifiers
        intensity_removals = [
            r'\b(absolutely|completely|utterly|totally|damn|really|very)\s+',
            r'!+',  # Remove exclamation marks
            r'\.\.\.+'  # Remove excessive ellipses
        ]
        
        result = text
        for pattern in intensity_removals:
            if pattern == r'!+':
                result = re.sub(pattern, '.', result)
            elif pattern == r'\.\.\.+':
                result = re.sub(pattern, '.', result)
            else:
                result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        return result.strip()
    
    def analyze_dialogue_line(self, speaker: str, text: str, context: str = "") -> Dict:
        """Analyze a line of dialogue and provide feedback with alternatives."""
        analysis = {
            "speaker": speaker,
            "text": text,
            "word_count": len(text.split()),
            "sentence_count": len([s for s in re.split(r'[.!?]+', text) if s.strip()]),
            "cliches_detected": self._detect_cliches(text),
            "tropes_detected": self._detect_tropes(text),
            "emotional_tone": self._analyze_tone(text),
            "character_consistency": self._check_character_consistency(speaker, text),
            "pacing_analysis": self._analyze_pacing(text),
            "dialogue_alternatives": self.generate_dialogue_alternatives(speaker, text),
            "suggestions": []
        }
        
        # Generate suggestions based on analysis
        analysis["suggestions"] = self._generate_suggestions(analysis)
        
        # Store dialogue line
        dialogue_line = DialogueLine(
            speaker=speaker,
            text=text,
            context=context,
            emotional_tone=analysis["emotional_tone"],
            timestamp=datetime.now().isoformat(),
            scene_position=len(self.dialogue_history)
        )
        self.dialogue_history.append(dialogue_line)
        
        # Update character voice patterns
        self._update_character_patterns(speaker, text)
        
        return analysis
    
    def _detect_cliches(self, text: str) -> List[Dict]:
        """Detect clichéd phrases in dialogue."""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.cliche_patterns:
            if re.search(pattern, text_lower):
                detected.append({
                    "pattern": pattern,
                    "severity": "medium",
                    "suggestion": "Consider rephrasing to be more original"
                })
        
        return detected
    
    def _detect_tropes(self, text: str) -> List[Dict]:
        """Detect common dialogue tropes."""
        detected = []
        text_lower = text.lower()
        
        for trope_type, patterns in self.trope_database.items():
            for pattern in patterns:
                if pattern in text_lower:
                    detected.append({
                        "trope": trope_type,
                        "pattern": pattern,
                        "severity": "low" if trope_type in ["romantic_tension"] else "medium"
                    })
        
        return detected
    
    def _analyze_tone(self, text: str) -> str:
        """Analyze the emotional tone of dialogue."""
        text_lower = text.lower()
        tone_scores = {}
        
        for tone, keywords in self.tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                tone_scores[tone] = score
        
        if not tone_scores:
            return "neutral"
        
        return max(tone_scores, key=tone_scores.get)
    
    def _check_character_consistency(self, speaker: str, text: str) -> Dict:
        """Check if dialogue is consistent with character's established voice."""
        if speaker not in self.characters:
            return {"consistent": True, "notes": "New character - establishing voice"}
        
        character = self.characters[speaker]
        analysis = {
            "consistent": True,
            "notes": [],
            "voice_drift_warnings": []
        }
        
        # Analyze sentence length consistency
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        current_avg_length = statistics.mean(len(s.split()) for s in sentences) if sentences else 0
        
        if character.avg_sentence_length > 0:
            length_diff = abs(current_avg_length - character.avg_sentence_length)
            if length_diff > 3:  # Significant change in verbosity
                analysis["voice_drift_warnings"].append(
                    f"Sentence length deviation: {length_diff:.1f} words from character norm"
                )
        
        return analysis
    
    def _analyze_pacing(self, text: str) -> Dict:
        """Analyze dialogue pacing and rhythm."""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        return {
            "sentence_count": len(sentences),
            "avg_sentence_length": statistics.mean(len(s.split()) for s in sentences) if sentences else 0,
            "rhythm_variety": len(set(len(s.split()) for s in sentences)),
            "interruptions": text.count("--") + text.count("..."),
            "emphasis": text.count("!") + text.count("?"),
            "pacing_score": self._calculate_pacing_score(text)
        }
    
    def _calculate_pacing_score(self, text: str) -> float:
        """Calculate a pacing score (0-1) based on rhythm and flow."""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if not sentences:
            return 0.5
        
        lengths = [len(s.split()) for s in sentences]
        variety = len(set(lengths)) / len(lengths) if lengths else 0
        avg_length = statistics.mean(lengths)
        
        # Good pacing has variety and appropriate length
        ideal_length = 8  # words per sentence
        length_score = 1 - abs(avg_length - ideal_length) / ideal_length
        
        return (variety * 0.6 + length_score * 0.4)
    
    def _update_character_patterns(self, speaker: str, text: str) -> None:
        """Update character voice patterns based on new dialogue."""
        if speaker not in self.characters:
            return
        
        character = self.characters[speaker]
        character.dialogue_count += 1
        
        # Update average sentence length
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            current_avg = statistics.mean(sentence_lengths)
            
            # Running average
            total_sentences = character.dialogue_count
            character.avg_sentence_length = (
                (character.avg_sentence_length * (total_sentences - 1) + current_avg) 
                / total_sentences
            )
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate writing suggestions based on analysis."""
        suggestions = []
        
        # Cliché suggestions with alternatives
        if analysis["cliches_detected"]:
            cliche_count = len(analysis['cliches_detected'])
            suggestions.append(
                f"Found {cliche_count} cliché(s). Check the dialogue_alternatives section "
                "for fresh, character-appropriate alternatives."
            )
        
        # Alternative suggestions
        if analysis["dialogue_alternatives"]:
            suggestions.append(
                "Multiple voice-adapted alternatives provided. Choose ones that best "
                "fit your character's personality and the scene's mood."
            )
        
        # Pacing suggestions
        pacing = analysis["pacing_analysis"]
        if pacing["pacing_score"] < 0.4:
            suggestions.append(
                "Dialogue pacing could be improved. Try varying sentence lengths "
                "and adding more rhythm through punctuation and pauses."
            )
        
        # Tone consistency
        if self.scene_context and analysis["emotional_tone"] != "neutral":
            if self.scene_context.tension_level > 7 and analysis["emotional_tone"] in ["happy", "romantic"]:
                suggestions.append(
                    "Emotional tone might not match the high-tension scene context. "
                    "Consider adjusting to match the scene's intensity."
                )
        
        return suggestions
    
    def suggest_improved_dialogue(self, speaker: str, original_text: str) -> Dict:
        """Provide a comprehensive improvement suggestion for a dialogue line."""
        alternatives = self.generate_dialogue_alternatives(speaker, original_text)
        
        # Create improved versions by replacing clichés
        improved_versions = []
        
        if alternatives:
            # Generate multiple improved versions
            for version_num in range(min(3, max(len(alt.character_voice_adjusted) for alt in alternatives))):
                improved_text = original_text
                
                # Replace each cliché with a character-adapted alternative
                for alt in alternatives:
                    if version_num < len(alt.character_voice_adjusted):
                        # Use case-sensitive replacement to maintain original capitalization context
                        original_phrase = alt.original_phrase
                        replacement = alt.character_voice_adjusted[version_num]
                        
                        # Preserve capitalization of first letter if it was capitalized
                        if original_phrase and original_phrase[0].isupper():
                            replacement = replacement[0].upper() + replacement[1:] if len(replacement) > 1 else replacement.upper()
                        
                        improved_text = improved_text.replace(original_phrase, replacement)
                
                # Clean up any double punctuation or spacing issues
                improved_text = re.sub(r'[!]{2,}', '!', improved_text)
                improved_text = re.sub(r'\s+', ' ', improved_text)
                improved_text = improved_text.strip()
                
                improved_versions.append(improved_text)
        
        return {
            "original": original_text,
            "cliche_alternatives": alternatives,
            "improved_versions": improved_versions,
            "character_voice_notes": self._get_voice_guidance(speaker),
            "scene_context_advice": self._get_scene_context_advice()
        }
    
    def _get_voice_guidance(self, speaker: str) -> List[str]:
        """Get voice guidance specific to the character."""
        if speaker not in self.characters:
            return ["Character not established yet - focus on defining their unique voice."]
        
        character = self.characters[speaker]
        guidance = []
        
        formality = character.voice_patterns.get("formality", 0.5)
        verbosity = character.voice_patterns.get("verbosity", 0.5)
        emotion = character.voice_patterns.get("emotion_intensity", 0.5)
        
        if formality > 0.7:
            guidance.append("Maintain formal speech patterns - avoid contractions and slang")
        elif formality < 0.3:
            guidance.append("Keep it casual - use contractions and informal language")
        
        if verbosity > 0.7:
            guidance.append("Character tends to be wordy - elaborate and explain")
        elif verbosity < 0.3:
            guidance.append("Character is economical with words - keep it brief and direct")
        
        if emotion > 0.7:
            guidance.append("Character is emotionally expressive - use strong language and punctuation")
        elif emotion < 0.3:
            guidance.append("Character is emotionally restrained - keep tone measured")
        
        return guidance
    
    def _get_scene_context_advice(self) -> List[str]:
        """Get advice based on current scene context."""
        if not self.scene_context:
            return ["Set scene context for more targeted advice"]
        
        advice = []
        
        if self.scene_context.tension_level > 7:
            advice.append("High tension - use shorter, more urgent dialogue")
        elif self.scene_context.tension_level < 3:
            advice.append("Low tension - allow for longer, more contemplative dialogue")
        
        if self.scene_context.mood == "romantic":
            advice.append("Romantic scene - focus on subtext and emotional vulnerability")
        elif self.scene_context.mood == "mysterious":
            advice.append("Mysterious mood - use hints and implications rather than direct statements")
        
        return advice
    
    def generate_context_aware_suggestion(self, speaker: str, context_hint: str = "") -> Dict:
        """Generate dialogue suggestions based on current context and character."""
        if not self.scene_context:
            return {"error": "No scene context set. Use set_scene_context() first."}
        
        suggestions = {
            "speaker": speaker,
            "context_factors": [],
            "suggested_directions": [],
            "tone_recommendations": [],
            "pacing_advice": [],
            "voice_guidance": self._get_voice_guidance(speaker)
        }
        
        # Context-based suggestions
        if self.scene_context.tension_level > 7:
            suggestions["suggested_directions"].append(
                "High tension scene - consider shorter, punchier dialogue with interruptions"
            )
            suggestions["tone_recommendations"].append("urgent, intense, or confrontational")
        
        if self.scene_context.mood == "romantic":
            suggestions["tone_recommendations"].extend(["intimate", "vulnerable", "tender"])
        
        # Character-specific suggestions
        if speaker in self.characters:
            character = self.characters[speaker]
            if character.voice_patterns.get("formality", 0.5) > 0.7:
                suggestions["pacing_advice"].append(
                    "Character tends toward formal speech - consider longer, more structured sentences"
                )
        
        return suggestions
    
    def get_character_voice_summary(self, speaker: str) -> Dict:
        """Get a summary of a character's established voice patterns."""
        if speaker not in self.characters:
            return {"error": f"Character {speaker} not found"}
        
        character = self.characters[speaker]
        
        # Analyze dialogue history for this character
        character_lines = [line for line in self.dialogue_history if line.speaker == speaker]
        
        tone_frequency = Counter(line.emotional_tone for line in character_lines)
        
        return {
            "name": character.name,
            "dialogue_count": character.dialogue_count,
            "avg_sentence_length": round(character.avg_sentence_length, 1),
            "common_tones": dict(tone_frequency.most_common(3)),
            "voice_patterns": character.voice_patterns,
            "consistency_score": self._calculate_consistency_score(character_lines)
        }
    
    def _calculate_consistency_score(self, character_lines: List[DialogueLine]) -> float:
        """Calculate how consistent a character's voice has been."""
        if len(character_lines) < 2:
            return 1.0
        
        # Simple consistency metric based on tone variation
        tones = [line.emotional_tone for line in character_lines]
        unique_tones = len(set(tones))
        
        # More variety in appropriate contexts is good, but not too much
        consistency = 1 - (unique_tones / len(tones)) * 0.5
        return max(0.0, min(1.0, consistency))
    
    def export_analysis_report(self) -> str:
        """Export a comprehensive analysis report."""
        report = {
            "dialogue_analysis_report": {
                "generated_at": datetime.now().isoformat(),
                "total_dialogue_lines": len(self.dialogue_history),
                "characters_analyzed": len(self.characters),
                "scene_context": asdict(self.scene_context) if self.scene_context else None,
                "character_summaries": {
                    name: self.get_character_voice_summary(name) 
                    for name in self.characters.keys()
                },
                "overall_patterns": self._analyze_overall_patterns()
            }
        }
        
        return json.dumps(report, indent=2)
    
    def _analyze_overall_patterns(self) -> Dict:
        """Analyze patterns across all dialogue."""
        if not self.dialogue_history:
            return {}
        
        all_tones = [line.emotional_tone for line in self.dialogue_history]
        tone_distribution = Counter(all_tones)
        
        total_cliches = sum(
            len(self.analyze_dialogue_line(line.speaker, line.text)["cliches_detected"])
            for line in self.dialogue_history
        )
        
        return {
            "tone_distribution": dict(tone_distribution),
            "cliche_frequency": total_cliches / len(self.dialogue_history) if self.dialogue_history else 0,
            "avg_dialogue_length": statistics.mean(
                len(line.text.split()) for line in self.dialogue_history
            ) if self.dialogue_history else 0
        }

# Example usage and demonstration
def demo_dialogue_composer():
    """Demonstrate the enhanced Dialogue Composer functionality."""
    
    # Initialize the composer
    composer = DialogueComposer()
    
    # Add characters with distinct voice patterns
    composer.add_character("Sarah", {
        "formality": 0.3,  # casual
        "verbosity": 0.6,  # somewhat verbose
        "emotion_intensity": 0.8,  # very emotional
        "interruption_tendency": 0.4,
        "question_frequency": 0.3
    })
    
    composer.add_character("Detective Martinez", {
        "formality": 0.8,  # formal
        "verbosity": 0.4,  # concise
        "emotion_intensity": 0.2,  # controlled
        "interruption_tendency": 0.1,
        "question_frequency": 0.7
    })
    
    composer.add_character("Tommy", {
        "formality": 0.1,  # very casual
        "verbosity": 0.3,  # terse
        "emotion_intensity": 0.6,  # moderate emotion
        "interruption_tendency": 0.6,
        "question_frequency": 0.2
    })
    
    # Set scene context
    composer.set_scene_context(
        setting="Police station interrogation room",
        mood="tense",
        tension=8,
        characters=["Sarah", "Detective Martinez", "Tommy"],
        plot_points=["Sarah is hiding something", "Time is running out"]
    )
    
    # Analyze dialogue with clichés
    cliched_dialogue_examples = [
        ("Sarah", "Look, you can't judge a book by its cover! I'm not what you think!", "defensive response"),
        ("Detective Martinez", "In the nick of time, we found the evidence. What goes around comes around.", "confrontational"),
        ("Tommy", "This is a perfect storm, man. Like a kid in a candy store, but everything's going wrong!", "overwhelmed"),
        ("Sarah", "Ignorance is bliss, Detective. I think you should think outside the box here.", "deflecting"),
    ]
    
    print("=== ENHANCED DIALOGUE COMPOSER DEMO ===\n")
    print("🎭 ANALYZING CLICHÉD DIALOGUE WITH ALTERNATIVES\n")
    
    for speaker, text, context in cliched_dialogue_examples:
        print(f"Original: {speaker}: \"{text}\"")
        
        # Get full analysis with alternatives
        analysis = composer.analyze_dialogue_line(speaker, text, context)
        
        print(f"  📊 Tone: {analysis['emotional_tone']}")
        print(f"  📈 Pacing Score: {analysis['pacing_analysis']['pacing_score']:.2f}")
        
        if analysis['cliches_detected']:
            print(f"  ⚠️  Clichés detected: {len(analysis['cliches_detected'])}")
        
        # Show dialogue alternatives
        if analysis['dialogue_alternatives']:
            print(f"  🔄 FRESH ALTERNATIVES:")
            for i, alt in enumerate(analysis['dialogue_alternatives']):
                print(f"    Cliché: \"{alt.original_phrase}\"")
                print(f"    Character-adapted alternatives:")
                for j, adapted in enumerate(alt.character_voice_adjusted[:3], 1):
                    print(f"      {j}. \"{adapted}\"")
                print()
        
        # Show improved dialogue suggestions
        improvement = composer.suggest_improved_dialogue(speaker, text)
        if improvement['improved_versions']:
            print(f"  ✨ IMPROVED VERSIONS:")
            for i, improved in enumerate(improvement['improved_versions'][:3], 1):
                print(f"    {i}. \"{improved}\"")
        
        print(f"  💡 Voice guidance: {improvement['character_voice_notes'][0] if improvement['character_voice_notes'] else 'None'}")
        print("-" * 80)
        print()
    
    # Show character voice summaries
    print("=== CHARACTER VOICE SUMMARIES ===")
    for character_name in composer.characters.keys():
        summary = composer.get_character_voice_summary(character_name)
        print(f"\n{character_name}:")
        print(f"  Dialogue lines: {summary['dialogue_count']}")
        print(f"  Avg sentence length: {summary['avg_sentence_length']} words")
        print(f"  Common tones: {summary['common_tones']}")
        print(f"  Voice consistency: {summary['consistency_score']:.2f}")
        
        # Show voice pattern details
        patterns = summary['voice_patterns']
        print(f"  Voice Profile:")
        print(f"    Formality: {patterns['formality']:.1f} ({'Formal' if patterns['formality'] > 0.6 else 'Casual' if patterns['formality'] < 0.4 else 'Neutral'})")
        print(f"    Verbosity: {patterns['verbosity']:.1f} ({'Verbose' if patterns['verbosity'] > 0.6 else 'Terse' if patterns['verbosity'] < 0.4 else 'Moderate'})")
        print(f"    Emotion: {patterns['emotion_intensity']:.1f} ({'Intense' if patterns['emotion_intensity'] > 0.6 else 'Flat' if patterns['emotion_intensity'] < 0.4 else 'Balanced'})")
    
    # Demonstrate context-aware suggestions
    print(f"\n=== CONTEXT-AWARE SUGGESTIONS ===")
    suggestion = composer.generate_context_aware_suggestion("Sarah")
    print(f"Suggestions for Sarah in current scene:")
    for direction in suggestion['suggested_directions']:
        print(f"  • {direction}")
    
    if suggestion['voice_guidance']:
        print(f"  Voice guidance:")
        for guidance in suggestion['voice_guidance']:
            print(f"    - {guidance}")
    
    print(f"\n✅ DEMO COMPLETE - Enhanced dialogue composer with alternatives generator ready!")
    print(f"🚀 Use composer.analyze_dialogue_line() to get alternatives for any dialogue!")
    print(f"📝 Use composer.suggest_improved_dialogue() for complete rewrites!")

if __name__ == "__main__":
    demo_dialogue_composer()