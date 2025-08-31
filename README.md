# Dialogue Composer - AI-Driven Story Writing Coach
- An intelligent Python tool that helps writers craft engaging dialogues, maintain authentic character voices, and avoid overused expressions in novels and scripts.

## 🌟 Features
### Core Capabilities
- **Context-Aware Suggestions**: Dynamic recommendations that evolve with your plot
- **Character Voice Monitoring**: Maintains authentic character speech patterns
- **Cliché Detection**: Identifies and suggests alternatives for overused phrases
- **Pacing Analysis**: Evaluates dialogue rhythm and flow
- **Tone Consistency**: Ensures emotional authenticity across scenes

### Advanced Features
- **Smart Alternative Generator**: Provides character-specific replacements for clichéd dialogue
- **Voice Pattern Tracking**: Learns and maintains each character's unique speech style
- **Scene Context Integration**: Adapts suggestions based on setting, mood, and tension
- **Comprehensive Reporting**: Export a detailed analysis of your dialogue patterns

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/yourusername/dialogue-composer
cd dialogue-composer
python main.py
```

### Basic Usage

```python
from dialogue_composer import DialogueComposer

# Initialize the composer
composer = DialogueComposer()

# Add characters with voice patterns
composer.add_character("Sarah", {
    "formality": 0.3,      # 0=casual, 1=formal
    "verbosity": 0.6,      # 0=terse, 1=verbose
    "emotion_intensity": 0.8
})

# Set scene context
composer.set_scene_context(
    setting="Police station",
    mood="tense", 
    tension=8,
    characters=["Sarah", "Detective Martinez"]
)

# Analyze dialogue and get feedback
analysis = composer.analyze_dialogue_line(
    speaker="Sarah",
    text="Look, ignorance is bliss, but I'm not stupid!",
    context="defensive response"
)

print(f"Tone: {analysis['emotional_tone']}")
print(f"Clichés detected: {len(analysis['cliches_detected'])}")
print(f"Suggestions: {analysis['suggestions']}")
```

## 📊 Output Examples

### Real-Time Dialogue Analysis
```
Analyzing: Sarah: "You can't judge a book by its cover! I'm innocent!"
  Tone: defensive
  Pacing Score: 0.85
  ⚠️ Clichés detected: 1
  💡 Suggestions:
    - Consider avoiding 1 clichéd phrase. Try expressing the same idea in a fresh, character-specific way.
    - Alternative suggestions: Things aren't always what they seem, Don't trust what you see, Look deeper before you decide
```

### Character Voice Summary
```
Sarah:
  Dialogue lines: 3
  Avg sentence length: 6.7 words
  Common tones: {'defensive': 2, 'neutral': 1}
  Voice consistency: 0.67
```

### Context-Aware Suggestions
```
Suggestions for Sarah in the current scene:
  • High tension scene - consider shorter, punchier dialogue with interruptions
```

## 🎭 Character Voice Patterns
- Define how each character speaks by setting voice pattern values (0.0 to 1.0):
- **formality**: 0=very casual ("yeah, whatever") → 1=very formal ("I must respectfully disagree")
- **verbosity**: 0=terse ("No.") → 1=verbose ("Well, I suppose one could argue...")
- **emotion_intensity**: 0=flat delivery → 1=dramatic expression
- **interruption_tendency**: How likely to cut others off
- **question_frequency**: How often they ask questions

## 🔍 Cliché Detection
- The system detects common overused expressions including:
- "Think outside the box"
- "Ignorance is bliss"
- "You can't judge a book by its cover"
- "In the nick of time"
- "What goes around comes around"
- And 15+ more patterns

## 🎯 Scene Context Types

Set scene context to get targeted suggestions:

```python
# High tension scene
composer.set_scene_context("Warehouse", "dangerous", 9, ["Hero", "Villain"])

# Romantic scene  
composer.set_scene_context("Cafe", "intimate", 3, ["Love Interest A", "Love Interest B"])

# Mystery reveal
composer.set_scene_context("Library", "mysterious", 6, ["Detective", "Suspect"])
```

## 📈 Analysis Metrics

### Pacing Score (0-1)
- **0.0-0.3**: Poor pacing, needs rhythm improvement
- **0.4-0.6**: Acceptable pacing
- **0.7-1.0**: Excellent rhythm and flow

### Voice Consistency (0-1)
- **0.0-0.4**: Character voice is inconsistent
- **0.5-0.7**: Moderate consistency
- **0.8-1.0**: Strong, consistent character voice

## 📁 Project Structure

```
dialogue-composer/
├── main.py              # Main DialogueComposer class
├── README.md           # This file
├── examples/           # Usage examples
└── tests/              # Unit tests
```

## 🛠️ API Reference

### Core Methods

#### `add_character(name: str, voice_description: Dict)`
Add a new character with voice patterns.

#### `set_scene_context(setting: str, mood: str, tension: int, characters: List[str])`
Define the current scene context for context-aware suggestions.

#### `analyze_dialogue_line(speaker: str, text: str, context: str) -> Dict`
Analyze a single line of dialogue and return comprehensive feedback.

#### `suggest_alternatives(cliched_text: str, character: str) -> List[str]`
Generate character-specific alternatives to clichéd dialogue.

#### `get_character_voice_summary(speaker: str) -> Dict`
Get detailed analysis of a character's established voice patterns.

#### `export_analysis_report() -> str`
Export comprehensive JSON report of all dialogue analysis.

## 🎨 Example Workflow

1. **Setup**: Create characters and set scene context
2. **Write**: Compose dialogue naturally
3. **Analyze**: Get real-time feedback on each line
4. **Improve**: Use suggested alternatives for clichéd phrases
5. **Track**: Monitor character voice consistency over time
6. **Export**: Generate reports for revision and editing

## 🔧 Customization

### Adding New Clichés
Extend the `_load_cliche_patterns()` method with your own overused phrases.

### Custom Tone Keywords
Modify `_load_tone_keywords()` to recognize genre-specific emotional indicators.

### Character Voice Templates
Create pre-defined voice pattern templates for common character archetypes.

## 🎯 Use Cases

- **Novel Writing**: Maintain consistent character voices across chapters
- **Screenplay Development**: Ensure authentic dialogue in scripts
- **Creative Writing Classes**: Teaching tool for dialogue craft
- **Editing & Revision**: Identify weak dialogue during editing process
- **Character Development**: Track voice evolution throughout story arcs

## 🤝 Contributing
- We welcome contributions! Areas for enhancement:
- Genre-specific cliché databases
- Additional tone detection patterns
- Character archetype templates
- Export format options (Final Draft, Fountain, etc.)

## 📝 License
- MIT License - see LICENSE file for details

## 🙏 Acknowledgments
- Built for writers who want to craft authentic, engaging dialogue while avoiding the pitfalls of overused expressions and inconsistent character voices.

---

**Happy Writing!** 📚✨
