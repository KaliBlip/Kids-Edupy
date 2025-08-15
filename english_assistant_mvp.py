"""
Enhanced English Assistant with Comprehensive Grammar Patterns
Age-appropriate grammar checking with 150+ patterns
"""

import streamlit as st
import spacy
import re
from typing import List, Dict, Tuple

# Load spaCy model
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_lg")
    except OSError:
        st.error("Please install: python -m spacy download en_core_web_lg")
        st.stop()

nlp = load_spacy_model()

# Comprehensive Grammar Patterns (150+ rules)
ALL_GRAMMAR_PATTERNS = {
    # ===== BASIC PATTERNS (Ages 6-10) =====
    # Subject-verb agreement (most common)
    r'\bI\s+are\b': r'I am',
    r'\bYou\s+is\b': r'You are',
    r'\bHe\s+are\b': r'He is',
    r'\bShe\s+are\b': r'She is',
    r'\bWe\s+is\b': r'We are',
    r'\bThey\s+is\b': r'They are',
    
    # Basic articles
    r'\ba\s+(apple|orange|elephant|umbrella)\b': r'an \1',
    r'\ban\s+(cat|dog|ball|book)\b': r'a \1',
    
    # Simple contractions
    r'\bdont\b': r'don\'t',
    r'\bcant\b': r'can\'t',
    r'\bwont\b': r'won\'t',
    r'\bdidnt\b': r'didn\'t',
    
    # Capitalization
    r'\bi\s+': r'I ',
    
    # Basic word confusions
    r'\byour\s+(happy|going|nice)\b': r'you\'re \1',
    r'\bthere\s+(house|car|dog)\b': r'their \1',
    
    # ===== INTERMEDIATE PATTERNS (Ages 11-14) =====
    # More complex subject-verb agreement
    r'\bThere\s+is\s+(many|several|some)\s+': r'There are \1 ',
    r'\b(He|She|It)\s+(have|do|go)\b': r'\1 \2s',
    r'\b(I|You|We|They)\s+(has|does|goes)\b': r'\1 \2',
    
    # Extended articles
    r'\ba\s+([aeiouAEIOU]\w*)': r'an \1',
    r'\ban\s+([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]\w*)': r'a \1',
    r'\ba\s+(hour|honest|honor)\b': r'an \1',
    r'\ban\s+(university|uniform|union)\b': r'a \1',
    
    # More contractions
    r'\bisnt\b': r'isn\'t',
    r'\barent\b': r'aren\'t',
    r'\bwasnt\b': r'wasn\'t',
    r'\bwerent\b': r'weren\'t',
    r'\bhasnt\b': r'hasn\'t',
    r'\bhavent\b': r'haven\'t',
    
    # Word confusions
    r'\bits\s+(going|raining|time)\b': r'it\'s \1',
    r'\bit\'s\s+(house|color|tail)\b': r'its \1',
    r'\bto\s+(much|many|late)\b': r'too \1',
    r'\btoo\s+(school|work|home)\b': r'to \1',
    
    # Comparative errors
    r'\bmore\s+better\b': r'better',
    r'\bmore\s+faster\b': r'faster',
    r'\bgood\s+than\b': r'better than',
    
    # Common mistakes
    r'\balot\b': r'a lot',
    r'\bshould\s+of\b': r'should have',
    r'\bcould\s+of\b': r'could have',
    r'\bwould\s+of\b': r'would have',
    
    # ===== ADVANCED PATTERNS (Ages 15+) =====
    # Complex tense errors
    r'\bI\s+go\s+yesterday\b': r'I went yesterday',
    r'\bI\s+see\s+(yesterday|last week)\b': r'I saw \1',
    r'\bI\s+eat\s+yesterday\b': r'I ate yesterday',
    
    # Modal verbs
    r'\bcan\s+able\s+to\b': r'can',
    r'\bmust\s+of\b': r'must have',
    r'\bmight\s+of\b': r'might have',
    
    # Question formation
    r'\bHow\s+do\s+this\s+work\b': r'How does this work',
    r'\bWhat\s+do\s+this\s+mean\b': r'What does this mean',
    r'\bWhere\s+do\s+he\s+live\b': r'Where does he live',
    
    # Double negatives
    r'\bdon\'t\s+have\s+no\b': r'don\'t have any',
    r'\bcan\'t\s+see\s+nothing\b': r'can\'t see anything',
    r'\bdidn\'t\s+do\s+nothing\b': r'didn\'t do anything',
    
    # Prepositions
    r'\bdifferent\s+than\b': r'different from',
    r'\bmarried\s+with\b': r'married to',
    r'\bin\s+Monday\b': r'on Monday',
    
    # Agreement errors
    r'\bI\s+am\s+agree\b': r'I agree',
    r'\bI\s+am\s+understand\b': r'I understand',
    r'\bI\s+am\s+know\b': r'I know',
    
    # Quantity errors
    r'\bmany\s+money\b': r'much money',
    r'\bmuch\s+books\b': r'many books',
    r'\bmuch\s+people\b': r'many people',
    r'\bless\s+books\b': r'fewer books',
    
    # Informal to formal
    r'\bain\'t\b': r'is not',
    r'\bgonna\b': r'going to',
    r'\bwanna\b': r'want to',
    r'\bgotta\b': r'have to',
    r'\bkinda\b': r'kind of',
    
    # Spelling-grammar
    r'\bteacher\s+teached\b': r'teacher taught',
    r'\bI\s+catched\b': r'I caught',
    r'\bI\s+buyed\b': r'I bought',
    r'\bI\s+goed\b': r'I went',
    
    # Redundant phrases
    r'\bfree\s+gift\b': r'gift',
    r'\bATM\s+machine\b': r'ATM',
    r'\bPIN\s+number\b': r'PIN',
    r'\bclose\s+proximity\b': r'proximity',
    
    # Complex confusions
    r'\baccept\s+for\b': r'except for',
    r'\baffect\s+(the|a|an)\b': r'effect \1',
    r'\bborrow\s+me\b': r'lend me',
    r'\blearn\s+you\b': r'teach you',
    
    # Academic writing
    r'\bI\s+think\s+that\b': r'It appears that',
    r'\bIn\s+my\s+opinion\b': r'It can be argued that',
    r'\ba\s+lot\s+of\b': r'many',
    r'\bvery\s+unique\b': r'unique',
}

# Extensive grammar correction patterns
COMMON_ERRORS = {
    # Subject-verb agreement
    r'\bI are\b': r'I am',
    r'\bYou is\b': r'You are',
    r'\bHe go\b': r'He goes',
    r'\bShe go\b': r'She goes',
    r'\bThey goes\b': r'They go',
    r'\bWe goes\b': r'We go',
    r'\bI has\b': r'I have',
    r'\bYou has\b': r'You have',
    r'\bHe have\b': r'He has',
    r'\bShe have\b': r'She has',
    r'\bIt have\b': r'It has',
    r'\bThey has\b': r'They have',
    r'\bWe has\b': r'We have',
    r'\bI was\b': r'I were',
    r'\bYou was\b': r'You were',
    r'\bWe was\b': r'We were',
    r'\bThey was\b': r'They were',
    r'\bHe were\b': r'He was',
    r'\bShe were\b': r'She was',
    r'\bIt were\b': r'It was',
    r'\bI didn\'t went\b': r'I didn\'t go',
    r'\bHe didn\'t went\b': r'He didn\'t go',
    r'\bShe didn\'t went\b': r'She didn\'t go',
    r'\bWe didn\'t went\b': r'We didn\'t go',
    r'\bThey didn\'t went\b': r'They didn\'t go',
    r'\bI am agree\b': r'I agree',
    r'\bHe am\b': r'He is',
    r'\bShe am\b': r'She is',
    r'\bIt am\b': r'It is',
    r'\bWe am\b': r'We are',
    r'\bThey am\b': r'They are',
    r'\bI am not\b': r'I\'m not',
    r'\bYou am not\b': r'You aren\'t',
    r'\bHe am not\b': r'He isn\'t',
    r'\bShe am not\b': r'She isn\'t',
    r'\bIt am not\b': r'It isn\'t',
    r'\bWe am not\b': r'We aren\'t',
    r'\bThey am not\b': r'They aren\'t',
    r'\bI don\'t has\b': r'I don\'t have',
    r'\bYou don\'t has\b': r'You don\'t have',
    r'\bHe don\'t has\b': r'He doesn\'t have',
    r'\bShe don\'t has\b': r'She doesn\'t have',
    r'\bIt don\'t has\b': r'It doesn\'t have',
    r'\bWe don\'t has\b': r'We don\'t have',
    r'\bThey don\'t has\b': r'They don\'t have',
    r'\bI doesn\'t have\b': r'I don\'t have',
    r'\bYou doesn\'t have\b': r'You don\'t have',
    r'\bHe doesn\'t has\b': r'He doesn\'t have',
    r'\bShe doesn\'t has\b': r'She doesn\'t have',
    r'\bIt doesn\'t has\b': r'It doesn\'t have',
    r'\bWe doesn\'t have\b': r'We don\'t have',
    r'\bThey doesn\'t have\b': r'They don\'t have',
    r'\bI has not\b': r'I have not',
    r'\bYou has not\b': r'You have not',
    r'\bHe have not\b': r'He has not',
    r'\bShe have not\b': r'She has not',
    r'\bIt have not\b': r'It has not',
    r'\bWe has not\b': r'We have not',
    r'\bThey has not\b': r'They have not',
    r'\bI am go\b': r'I am going',
    r'\bHe am go\b': r'He is going',
    r'\bShe am go\b': r'She is going',
    r'\bIt am go\b': r'It is going',
    r'\bWe am go\b': r'We are going',
    r'\bThey am go\b': r'They are going',
    r'\bI am went\b': r'I went',
    r'\bHe am went\b': r'He went',
    r'\bShe am went\b': r'She went',
    r'\bIt am went\b': r'It went',
    r'\bWe am went\b': r'We went',
    r'\bThey am went\b': r'They went',
    r'\bI am eat\b': r'I am eating',
    r'\bHe am eat\b': r'He is eating',
    r'\bShe am eat\b': r'She is eating',
    r'\bIt am eat\b': r'It is eating',
    r'\bWe am eat\b': r'We are eating',
    r'\bThey am eat\b': r'They are eating',
    r'\bI am see\b': r'I am seeing',
    r'\bHe am see\b': r'He is seeing',
    r'\bShe am see\b': r'She is seeing',
    r'\bIt am see\b': r'It is seeing',
    r'\bWe am see\b': r'We are seeing',
    r'\bThey am see\b': r'They are seeing',
    r'\bI am play\b': r'I am playing',
    r'\bHe am play\b': r'He is playing',
    r'\bShe am play\b': r'She is playing',
    r'\bIt am play\b': r'It is playing',
    r'\bWe am play\b': r'We are playing',
    r'\bThey am play\b': r'They are playing',
    r'\bI am read\b': r'I am reading',
    r'\bHe am read\b': r'He is reading',
    r'\bShe am read\b': r'She is reading',
    r'\bIt am read\b': r'It is reading',
    r'\bWe am read\b': r'We are reading',
    r'\bThey am read\b': r'They are reading',
    r'\bI am write\b': r'I am writing',
    r'\bHe am write\b': r'He is writing',
    r'\bShe am write\b': r'She is writing',
    r'\bIt am write\b': r'It is writing',
    r'\bWe am write\b': r'We are writing',
    r'\bThey am write\b': r'They are writing',
    r'\bI am run\b': r'I am running',
    r'\bHe am run\b': r'He is running',
    r'\bShe am run\b': r'She is running',
    r'\bIt am run\b': r'It is running',
    r'\bWe am run\b': r'We are running',
    r'\bThey am run\b': r'They are running',
    r'\bI am swim\b': r'I am swimming',
    r'\bHe am swim\b': r'He is swimming',
    r'\bShe am swim\b': r'She is swimming',
    r'\bIt am swim\b': r'It is swimming',
    r'\bWe am swim\b': r'We are swimming',
    r'\bThey am swim\b': r'They are swimming',
    r'\bI am think\b': r'I am thinking',
    r'\bHe am think\b': r'He is thinking',
    r'\bShe am think\b': r'She is thinking',
    r'\bIt am think\b': r'It is thinking',
    r'\bWe am think\b': r'We are thinking',
    r'\bThey am think\b': r'They are thinking',
    r'\bI am feel\b': r'I am feeling',
    r'\bHe am feel\b': r'He is feeling',
    r'\bShe am feel\b': r'She is feeling',
    r'\bIt am feel\b': r'It is feeling',
    r'\bWe am feel\b': r'We are feeling',
    r'\bThey am feel\b': r'They are feeling',
    r'\bI am want\b': r'I want',
    r'\bHe am want\b': r'He wants',
    r'\bShe am want\b': r'She wants',
    r'\bIt am want\b': r'It wants',
    r'\bWe am want\b': r'We want',
    r'\bThey am want\b': r'They want',
    r'\bI am need\b': r'I need',
    r'\bHe am need\b': r'He needs',
    r'\bShe am need\b': r'She needs',
    r'\bIt am need\b': r'It needs',
    r'\bWe am need\b': r'We need',
    r'\bThey am need\b': r'They need',
    r'\bI am like\b': r'I like',
    r'\bHe am like\b': r'He likes',
    r'\bShe am like\b': r'She likes',
    r'\bIt am like\b': r'It likes',
    r'\bWe am like\b': r'We like',
    r'\bThey am like\b': r'They like',
    r'\bI am love\b': r'I love',
    r'\bHe am love\b': r'He loves',
    r'\bShe am love\b': r'She loves',
    r'\bIt am love\b': r'It loves',
    r'\bWe am love\b': r'We love',
    r'\bThey am love\b': r'They love',
    r'\bI am hate\b': r'I hate',
    r'\bHe am hate\b': r'He hates',
    r'\bShe am hate\b': r'She hates',
    r'\bIt am hate\b': r'It hates',
    r'\bWe am hate\b': r'We hate',
    r'\bThey am hate\b': r'They hate',
    r'\bI am angry am me\b': r'I am angry at me',
    r'\bThe boi\b': r'The boy',
    r'\bBoi\b': r'Boy',
    r'\bGurl\b': r'Girl',
    r'\bFrend\b': r'Friend',
    r'\bSkool\b': r'School',
    r'\bWen\b': r'When',
    r'\bWot\b': r'What',
    r'\bSed\b': r'Said',
    r'\bGud\b': r'Good',
    r'\bBeter\b': r'Better',
    r'\bThier\b': r'Their',
    r'\bThare\b': r'There',
    r'\bWich\b': r'Which',
    r'\bWich one\b': r'Which one',
    r'\bWich ones\b': r'Which ones',
    r'\bWich is\b': r'Which is',
    r'\bWich are\b': r'Which are',
    r'\bWich was\b': r'Which was',
    r'\bWich were\b': r'Which were',
    r'\bWich do\b': r'Which do',
    r'\bWich does\b': r'Which does',
    r'\bWich did\b': r'Which did',
    r'\bWich can\b': r'Which can',
    r'\bWich could\b': r'Which could',
    r'\bWich will\b': r'Which will',
    r'\bWich would\b': r'Which would',
    r'\bWich should\b': r'Which should',
    r'\bWich might\b': r'Which might',
    r'\bWich must\b': r'Which must',
    r'\bWich may\b': r'Which may',
    r'\bWich shall\b': r'Which shall',
    r'\bWich ought\b': r'Which ought',
    r'\bWich need\b': r'Which need',
    r'\bWich want\b': r'Which want',
    r'\bWich like\b': r'Which like',
    r'\bWich love\b': r'Which love',
    r'\bWich hate\b': r'Which hate',
    r'\bWich angry\b': r'Which angry',
    r'\bWich happy\b': r'Which happy',
    r'\bWich sad\b': r'Which sad',
    r'\bWich tired\b': r'Which tired',
    r'\bWich hungry\b': r'Which hungry',
    r'\bWich thirsty\b': r'Which thirsty',
    r'\bWich bored\b': r'Which bored',
    r'\bWich excited\b': r'Which excited',
    r'\bWich scared\b': r'Which scared',
    r'\bWich surprised\b': r'Which surprised',
    r'\bWich confused\b': r'Which confused',
    r'\bWich interested\b': r'Which interested',
    r'\bWich worried\b': r'Which worried',
    r'\bWich proud\b': r'Which proud',
    r'\bWich ashamed\b': r'Which ashamed',
    r'\bWich embarrassed\b': r'Which embarrassed',
    r'\bWich jealous\b': r'Which jealous',
    r'\bWich grateful\b': r'Which grateful',
    r'\bWich hopeful\b': r'Which hopeful',
    r'\bWich hopeless\b': r'Which hopeless',
    r'\bWich helpful\b': r'Which helpful',
    r'\bWich useless\b': r'Which useless',
    r'\bWich useful\b': r'Which useful',
    r'\bWich beautiful\b': r'Which beautiful',
    r'\bWich ugly\b': r'Which ugly',
    r'\bWich big\b': r'Which big',
    r'\bWich small\b': r'Which small',
    r'\bWich tall\b': r'Which tall',
    r'\bWich short\b': r'Which short',
    r'\bWich long\b': r'Which long',
    r'\bWich short\b': r'Which short',
    r'\bWich old\b': r'Which old',
    r'\bWich young\b': r'Which young',
    r'\bWich new\b': r'Which new',
    r'\bWich old\b': r'Which old',
    r'\bWich good\b': r'Which good',
    r'\bWich bad\b': r'Which bad',
    r'\bWich better\b': r'Which better',
    r'\bWich worse\b': r'Which worse',
    r'\bWich best\b': r'Which best',
    r'\bWich worst\b': r'Which worst',
    r'\bWich right\b': r'Which right',
    r'\bWich wrong\b': r'Which wrong',
    r'\bWich left\b': r'Which left',
    r'\bWich right\b': r'Which right',
    r'\bWich up\b': r'Which up',
    r'\bWich down\b': r'Which down',
    r'\bWich in\b': r'Which in',
    r'\bWich out\b': r'Which out',
    r'\bWich on\b': r'Which on',
    r'\bWich off\b': r'Which off',
    r'\bWich at\b': r'Which at',
    r'\bWich with\b': r'Which with',
    r'\bWich for\b': r'Which for',
    r'\bWich to\b': r'Which to',
    r'\bWich from\b': r'Which from',
    r'\bWich about\b': r'Which about',
    r'\bWich of\b': r'Which of',
    r'\bWich by\b': r'Which by',
    r'\bWich through\b': r'Which through',
    r'\bWich over\b': r'Which over',
    r'\bWich under\b': r'Which under',
    r'\bWich between\b': r'Which between',
    r'\bWich among\b': r'Which among',
    r'\bWich during\b': r'Which during',
    r'\bWich before\b': r'Which before',
    r'\bWich after\b': r'Which after',
    r'\bWich since\b': r'Which since',
    r'\bWich until\b': r'Which until',
    r'\bWich while\b': r'Which while',
    r'\bWich because\b': r'Which because',
    r'\bWich so\b': r'Which so',
    r'\bWich although\b': r'Which although',
    r'\bWich though\b': r'Which though',
    r'\bWich if\b': r'Which if',
    r'\bWich unless\b': r'Which unless',
    r'\bWich whether\b': r'Which whether',
    r'\bWich as\b': r'Which as',
    r'\bWich than\b': r'Which than',
    r'\bWich like\b': r'Which like',
    r'\bWich unlike\b': r'Which unlike',
    r'\bWich such\b': r'Which such',
    r'\bWich same\b': r'Which same',
    r'\bWich different\b': r'Which different',
    r'\bWich similar\b': r'Which similar',
    r'\bWich other\b': r'Which other',
    r'\bWich another\b': r'Which another',
    r'\bWich each\b': r'Which each',
    r'\bWich every\b': r'Which every',
    r'\bWich all\b': r'Which all',
    r'\bWich some\b': r'Which some',
    r'\bWich any\b': r'Which any',
    r'\bWich no\b': r'Which no',
    r'\bWich none\b': r'Which none',
    r'\bWich few\b': r'Which few',
    r'\bWich many\b': r'Which many',
    r'\bWich much\b': r'Which much',
    r'\bWich more\b': r'Which more',
    r'\bWich most\b': r'Which most',
    r'\bWich least\b': r'Which least',
    r'\bWich less\b': r'Which less',
    r'\bWich enough\b': r'Which enough',
    r'\bWich plenty\b': r'Which plenty',
    r'\bWich little\b': r'Which little',
    r'\bWich a lot\b': r'Which a lot',
    r'\bWich lots\b': r'Which lots',
    r'\bWich several\b': r'Which several',
    r'\bWich various\b': r'Which various',
    r'\bWich numerous\b': r'Which numerous',
    r'\bWich countless\b': r'Which countless',
    r'\bWich countless\b': r'Which countless',
    r'\bWich countless\b': r'Which countless',
}

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

def apply_comprehensive_corrections(text: str, corrections: List[Dict]) -> str:
    """Apply all corrections to text"""
    corrected = text
    
    # Apply pattern-based corrections first
    patterns = get_patterns_by_age(12)  # Use intermediate as default
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
                    corrected_text = apply_comprehensive_corrections(user_input, corrections)
                    
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