"""
Enhanced English Assistant with Comprehensive Grammar Patterns
Age-appropriate grammar checking with 150+ patterns
"""

import streamlit as st
import spacy
import re
from typing import List, Dict, Tuple
from grammar_patterns import ALL_GRAMMAR_PATTERNS

# Load spaCy model
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_lg")
    except OSError:
        st.error("Please install: python -m spacy download en_core_web_lg")
        st.stop()

nlp = load_spacy_model()

# Age-based pattern filtering
def get_patterns_by_age(age: int) -> Dict[str, str]:
    """Filter patterns based on user age"""
    if age <= 10:
        # Basic patterns for young children
        basic_keywords = ['i\\s+are', 'you.*is', 'he.*are', 'she.*are', 'we.*is', 'they.*is',
                         'dont', 'cant', 'wont', 'didnt', 'i\\s+', 'your.*happy', 'there.*house',
                         'ba\\s+apple', 'an\\s+cat']
        return {p: r for p, r in ALL_GRAMMAR_PATTERNS.items() 
                if any(keyword in p.lower() for keyword in basic_keywords)}
    
    elif age <= 14:
        # Intermediate patterns
        exclude_advanced = ['i\\s+think', 'in\\s+my\\s+opinion', 'very\\s+unique', 
                           'academic', 'formal']
        return {p: r for p, r in ALL_GRAMMAR_PATTERNS.items() 
                if not any(keyword in p.lower() for keyword in exclude_advanced)}
    
    else:
        # All patterns for advanced users
        return ALL_GRAMMAR_PATTERNS

# Enhanced error detection
def detect_comprehensive_errors(text: str, age: int = 12) -> List[Dict]:
    """Detect errors using age-appropriate patterns"""
    corrections = []
    patterns = get_patterns_by_age(age)
    
    # Apply pattern matching
    for pattern, replacement in patterns.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in matches:
            try:
                if callable(replacement):
                    corrected = replacement(match)
                else:
                    corrected = re.sub(pattern, replacement, match.group(), flags=re.IGNORECASE)
                
                corrections.append({
                    'type': get_error_type(pattern),
                    'original': match.group().strip(),
                    'suggestion': corrected.strip(),
                    'position': match.span(),
                    'explanation': get_explanation(pattern, match.group()),
                    'severity': get_severity(pattern)
                })
            except Exception as e:
                continue
    
    # SpaCy-based checks
    doc = nlp(text)
    corrections.extend(spacy_structure_check(doc))
    
    return corrections

def get_error_type(pattern: str) -> str:
    """Categorize error types based on pattern"""
    if any(keyword in pattern.lower() for keyword in ['are', 'is', 'have', 'has']):
        return 'Subject-Verb Agreement'
    elif any(keyword in pattern.lower() for keyword in ['\\ba\\s', '\\ban\\s']):
        return 'Article Usage'
    elif any(keyword in pattern.lower() for keyword in ['your', 'its', 'there', 'to']):
        return 'Word Confusion'
    elif any(keyword in pattern.lower() for keyword in ['dont', 'cant', 'wont']):
        return 'Contractions'
    elif 'than' in pattern.lower() or 'better' in pattern.lower():
        return 'Comparatives'
    elif any(keyword in pattern.lower() for keyword in ['of', 'have']):
        return 'Modal Verbs'
    else:
        return 'Grammar'

def get_explanation(pattern: str, original: str) -> str:
    """Generate kid-friendly explanations"""
    explanations = {
        'Subject-Verb Agreement': f"'{original}' doesn't match. Remember: I am, You are, He/She/It is!",
        'Article Usage': f"Use 'an' before vowel sounds (a, e, i, o, u) and 'a' before consonant sounds.",
        'Word Confusion': f"These words sound similar but mean different things. Check the meaning!",
        'Contractions': f"Don't forget the apostrophe (') when combining words!",
        'Comparatives': f"Don't use 'more' with words that already show comparison like 'better'.",
        'Modal Verbs': f"Use 'have' not 'of' after words like should, could, would.",
        'Grammar': f"This is a common grammar mistake. Practice makes perfect!"
    }
    
    error_type = get_error_type(pattern)
    return explanations.get(error_type, "This needs to be corrected for proper English.")

def get_severity(pattern: str) -> str:
    """Determine error severity for scoring"""
    high_severity = ['subject.*verb', 'are.*is', 'double.*negative']
    medium_severity = ['article', 'contraction', 'word.*confusion']
    
    pattern_lower = pattern.lower()
    if any(keyword in pattern_lower for keyword in high_severity):
        return 'high'
    elif any(keyword in pattern_lower for keyword in medium_severity):
        return 'medium'
    else:
        return 'low'

def spacy_structure_check(doc) -> List[Dict]:
    """Additional spaCy-based structure checks"""
    corrections = []
    
    for sent in doc.sents:
        sent_text = sent.text.strip()
        
        # Check for missing subjects
        has_subject = any(token.dep_ == "nsubj" or token.dep_ == "nsubjpass" for token in sent)
        has_verb = any(token.pos_ == "VERB" for token in sent)
        
        if has_verb and not has_subject and len(sent_text.split()) > 3:
            # Skip questions and imperatives
            question_words = ['what', 'where', 'when', 'why', 'how', 'who', 'which']
            if not any(sent_text.lower().startswith(word) for word in question_words):
                corrections.append({
                    'type': 'Sentence Structure',
                    'original': sent_text,
                    'suggestion': f"Add a subject: '{sent_text}'",
                    'position': (sent.start_char, sent.end_char),
                    'explanation': 'Complete sentences need a subject (who or what is doing the action)',
                    'severity': 'high'
                })
        
        # Check for run-on sentences (very simple check)
        if len(sent_text.split()) > 25 and sent_text.count(',') < 2:
            corrections.append({
                'type': 'Sentence Length',
                'original': sent_text[:50] + "..." if len(sent_text) > 50 else sent_text,
                'suggestion': "Consider breaking this into shorter sentences",
                'position': (sent.start_char, sent.end_char),
                'explanation': 'Long sentences can be hard to read. Try shorter ones!',
                'severity': 'low'
            })
    
    return corrections

def apply_comprehensive_corrections(text: str, age: int, corrections: List[Dict]) -> str:
    """Apply all corrections to text"""
    corrected = text
    
    # Apply pattern-based corrections first
    patterns = get_patterns_by_age(age)  # Use age-appropriate patterns
    for pattern, replacement in patterns.items():
        try:
            corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
        except:
            continue
    
    # Fix capitalization at sentence beginnings
    sentences = re.split(r'([.!?]+)', corrected)
    result = []
    for i, part in enumerate(sentences):
        if i % 2 == 0 and part.strip():  # Sentence content
            part = part.strip()
            if part:
                part = part[0].upper() + part[1:] if len(part) > 1 else part.upper()
        result.append(part)
    
    return ''.join(result)

def calculate_comprehensive_score(user_sentence: str, corrections: List[Dict]) -> int:
    """Enhanced scoring based on error severity"""
    user_words = user_sentence.split()
    original_length = len(user_words)
    if original_length == 0:
        return 0
    base_score = 100
    severity_penalties = {'high': 15, 'medium': 10, 'low': 5}
    total_penalty = sum(severity_penalties.get(c.get('severity', 'medium'), 10) 
                       for c in corrections)
    # Length bonus for complexity
    length_bonus = min(15, original_length // 8)
    # Variety bonus for using different words
    unique_words = len(set(user_words))
    variety_bonus = min(10, unique_words // 10)
    final_score = max(0, min(100, base_score - total_penalty + length_bonus + variety_bonus))
    return final_score

def generate_detailed_feedback(score: int, corrections: List[Dict], age: int) -> str:
    """Generate age-appropriate detailed feedback"""
    if age <= 10:
        # Simple feedback for young children
        if score >= 90:
            feedback = "🌟 WOW! You're an amazing writer!"
        elif score >= 75:
            feedback = "😊 Great job! You're getting better!"
        elif score >= 60:
            feedback = "👍 Good work! Let's fix a few things."
        else:
            feedback = "🤗 Keep trying! You're learning!"
    
    elif age <= 14:
        # More detailed feedback for middle schoolers
        if score >= 90:
            feedback = "🌟 Excellent writing! Your grammar is really strong."
        elif score >= 75:
            feedback = "😊 Good work! Just a few small grammar points to improve."
        elif score >= 60:
            feedback = "👍 Nice effort! Let's work on these grammar areas together."
        else:
            feedback = "📚 Keep practicing! Grammar takes time to master."
    
    else:
        # Detailed feedback for advanced learners
        if score >= 90:
            feedback = "🌟 Outstanding! Your English demonstrates strong command of grammar."
        elif score >= 75:
            feedback = "😊 Well done! Minor corrections will polish your writing."
        elif score >= 60:
            feedback = "👍 Good foundation! Focus on these specific grammar points."
        else:
            feedback = "📖 Solid effort! These corrections will strengthen your writing."
    
    error_count = len(corrections)
    if error_count > 0:
        feedback += f" I found {error_count} area{'s' if error_count > 1 else ''} to improve."
    
    return feedback

def generate_targeted_suggestions(corrections: List[Dict], age: int) -> List[str]:
    """Generate specific suggestions based on error types found"""
    suggestions = []
    error_types = [c.get('type', 'Grammar') for c in corrections]
    
    # Suggestions based on error patterns
    if 'Subject-Verb Agreement' in error_types:
        if age <= 10:
            suggestions.append("🗣️ Say your sentence out loud. Does it sound right?")
        else:
            suggestions.append("📝 Practice matching subjects with verbs: I am, You are, He/She is")
    
    if 'Article Usage' in error_types:
        if age <= 10:
            suggestions.append("🔤 Remember: 'an apple' but 'a banana'")
        else:
            suggestions.append("📖 Use 'an' before vowel sounds and 'a' before consonant sounds")
    
    if 'Word Confusion' in error_types:
        suggestions.append("📚 Make flashcards for confusing words like your/you're, its/it's")
    
    if 'Contractions' in error_types:
        suggestions.append("✍️ Don't forget apostrophes in contractions: don't, can't, won't")
    
    if 'Sentence Structure' in error_types:
        if age <= 10:
            suggestions.append("🏗️ Every sentence needs someone doing something!")
        else:
            suggestions.append("🔧 Check that each sentence has a subject and predicate")
    
    # General suggestions if no specific errors
    if not suggestions:
        if age <= 10:
            suggestions.extend([
                "⭐ Try writing about your favorite things!",
                "📖 Read books to see how good sentences look!"
            ])
        elif age <= 14:
            suggestions.extend([
                "📚 Read your writing aloud to catch mistakes",
                "✨ Try using more descriptive words in your sentences"
            ])
        else:
            suggestions.extend([
                "📖 Consider varying your sentence structure for better flow",
                "🎯 Focus on precision in word choice and grammar"
            ])
    
    return suggestions[:3]  # Limit to 3 suggestions

# Enhanced Streamlit Interface
def main():
    st.set_page_config(
        page_title="Advanced English Assistant",
        page_icon="🌟",
        layout="wide"
    )
    
    # Enhanced CSS
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .age-selector {
            background-color: #F0F8FF;
            padding: 1rem;
            border-radius: 10px;
            border: 2px solid #87CEEB;
            margin-bottom: 1rem;
        }
        .error-severity-high {
            background-color: #FFE4E1;
            border: 2px solid #FF6B6B;
        }
        .error-severity-medium {
            background-color: #FFF8DC;
            border: 2px solid #FFD700;
        }
        .error-severity-low {
            background-color: #F0FFF0;
            border: 2px solid #90EE90;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🌟 Advanced English Learning Assistant 🌟</h1>', 
                unsafe_allow_html=True)
    st.markdown("### AI-powered grammar checker with 150+ rules, personalized for your age!")
    
    # Age selector
    st.markdown('<div class="age-selector">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        age = st.selectbox(
            "👶 How old are you?",
            options=list(range(6, 19)),
            index=6,  # Default to age 12
            help="This helps me give you the right level of feedback!"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current level
    if age <= 10:
        level = "Beginner (Basic grammar rules)"
        level_color = "#90EE90"
    elif age <= 14:
        level = "Intermediate (More grammar rules)"
        level_color = "#FFD700"
    else:
        level = "Advanced (All grammar rules)"
        level_color = "#FF6B6B"
    
    st.markdown(f'<p style="text-align: center; color: {level_color}; font-weight: bold; font-size: 1.1rem;">Current Level: {level}</p>', 
                unsafe_allow_html=True)
    
    # Input section
    st.markdown("---")
    st.markdown("## ✏️ Write Your Text")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your text here:",
            height=120,
            placeholder="Example: I are going to the store with my friend and we is very excited...",
            help="Write anything! The more you write, the more I can help you learn."
        )
    
    with col2:
        st.markdown("### 💡 Writing Tips:")
        if age <= 10:
            st.markdown("• Write about fun things")
            st.markdown("• Use complete sentences")
            st.markdown("• Don't worry about mistakes!")
        elif age <= 14:
            st.markdown("• Check your spelling")
            st.markdown("• Read it out loud")
            st.markdown("• Use different words")
        else:
            st.markdown("• Vary sentence length")
            st.markdown("• Check grammar carefully")
            st.markdown("• Use precise vocabulary")
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Analyze My Writing!", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner("Analyzing your writing... 🤔"):
                    # Detect errors with age-appropriate patterns
                    corrections = detect_comprehensive_errors(user_input, age)
                    
                    # Apply corrections
                    corrected_text = apply_comprehensive_corrections(user_input, age, corrections)
                    
                    # Calculate score
                    score = calculate_comprehensive_score(user_input, corrections)
                    
                    # Generate feedback
                    feedback = generate_detailed_feedback(score, corrections, age)
                    suggestions = generate_targeted_suggestions(corrections, age)
                    
                    # Store results
                    st.session_state.result = {
                        'original': user_input,
                        'corrected': corrected_text,
                        'corrections': corrections,
                        'score': score,
                        'feedback': feedback,
                        'suggestions': suggestions,
                        'age': age
                    }
            else:
                st.warning("Please write something first! 😊")
    
    # Results display
    if hasattr(st.session_state, 'result') and st.session_state.result:
        result = st.session_state.result
        
        st.markdown("---")
        st.markdown("## 📊 Your Writing Analysis")
        
        # Score with stars
        stars = "⭐" * max(1, min(5, round(result['score'] / 20)))
        st.markdown(
            f"""
            <div style="text-align: center; background-color: #E6F3FF; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                <h2 style="color: #1E90FF;">Score: {result['score']}/100</h2>
                <h3 style="font-size: 2rem;">{stars}</h3>
                <p style="font-size: 1.3rem; color: #333; margin: 0;">{result['feedback']}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Before/After comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Your Original Text:")
            st.markdown(
                f'<div style="background-color: #FFE4E4; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF9999;">'
                f'<p style="font-size: 1.1rem; line-height: 1.6; margin: 0;">{result["original"]}</p></div>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown("### ✨ Corrected Version:")
            st.markdown(
                f'<div style="background-color: #E4FFE4; padding: 1.5rem; border-radius: 10px; border: 2px solid #99FF99;">'
                f'<p style="font-size: 1.1rem; line-height: 1.6; margin: 0;">{result["corrected"]}</p></div>',
                unsafe_allow_html=True
            )
        
        # Detailed corrections
        if result['corrections']:
            st.markdown("### 🔍 Detailed Corrections:")
            
            # Group corrections by type
            corrections_by_type = {}
            for correction in result['corrections']:
                error_type = correction.get('type', 'Grammar')
                if error_type not in corrections_by_type:
                    corrections_by_type[error_type] = []
                corrections_by_type[error_type].append(correction)
            
            for error_type, corrections in corrections_by_type.items():
                st.markdown(f"#### {error_type} ({len(corrections)} error{'s' if len(corrections) > 1 else ''})")
                
                for i, correction in enumerate(corrections, 1):
                    severity = correction.get('severity', 'medium')
                    severity_class = f"error-severity-{severity}"
                    
                    severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    
                    st.markdown(
                        f"""
                        <div class="{severity_class}" style="padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                            <h5>{severity_emoji[severity]} Correction #{i}</h5>
                            <p><strong>Change:</strong> "{correction['original']}" 
                            <span style="color: green; font-weight: bold;">→ "{correction['suggestion']}"</span></p>
                            <p><strong>Explanation:</strong> {correction['explanation']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
        # Learning suggestions
        st.markdown("### 💡 Personalized Learning Tips:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            st.markdown(f"**{i}.** {suggestion}")
        
        # Progress tracking
        if len(result['corrections']) == 0:
            st.balloons()
            st.success("🎉 Perfect! No corrections needed!")
        
        # Clear button
        if st.button("🔄 Try Another Text", type="secondary"):
            if hasattr(st.session_state, 'result'):
                del st.session_state.result
            st.rerun()

if __name__ == "__main__":
    main()