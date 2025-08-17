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
