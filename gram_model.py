# Grammar Model Training and Demo
# This notebook demonstrates the enhanced grammar correction system

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Import our grammar correction system
from grammar_model_demo import (
    HybridGrammarCorrector, 
    JFLEGDataset, 
    CorrectionResult,
    TRANSFORMERS_AVAILABLE
)

print("Grammar Correction System Loaded")
print(f"ML Components Available: {TRANSFORMERS_AVAILABLE}")

# Initialize the system
jfleg_handler = JFLEGDataset()
grammar_corrector = HybridGrammarCorrector(use_ml=TRANSFORMERS_AVAILABLE)

# Load and explore the JFLEG dataset
print("Loading JFLEG dataset...")
train_data, eval_data = jfleg_handler.load_data()

if train_data is not None:
    print(f"\nDataset Statistics:")
    print(f"Training examples: {len(train_data)}")
    print(f"Evaluation examples: {len(eval_data) if eval_data is not None else 0}")
    
    # Display sample data
    print("\nSample training data:")
    print(train_data.head())
    
    # Analyze error patterns
    print("\nAnalyzing error patterns...")
    error_patterns = jfleg_handler.analyze_common_errors()
    
    # Visualize top error patterns
    if len(error_patterns) > 0:
        top_errors = dict(list(error_patterns.items())[:15])
        
        plt.figure(figsize=(12, 8))
        plt.barh(list(top_errors.keys()), list(top_errors.values()))
        plt.title('Most Common Error Patterns in JFLEG Dataset')
        plt.xlabel('Frequency')
        plt.tight_layout()
        plt.show()
    
    # Show detailed error analysis
    print(f"\nTop 20 Error Patterns:")
    for i, (pattern, count) in enumerate(list(error_patterns.items())[:20], 1):
        print(f"{i:2d}. {pattern}: {count}")

# Interactive correction demo
print("\n" + "="*60)
print("INTERACTIVE GRAMMAR CORRECTION DEMO")
print("="*60)

# Test various types of grammatical errors
test_cases = [
    {
        'category': 'Article Errors',
        'examples': [
            "I saw a elephant in the zoo.",
            "She wants an university degree.",
            "He bought a hour ago."
        ]
    },
    {
        'category': 'Subject-Verb Agreement',
        'examples': [
            "She don't like coffee.",
            "They is coming to the party.",
            "He have many books."
        ]
    },
    {
        'category': 'Preposition Errors',
        'examples': [
            "I go to school at Monday.",
            "We meet at the morning.",
            "She sleeps in the night."
        ]
    },
    {
        'category': 'Word Choice/Spelling',
        'examples': [
            "I recieve your message.",
            "This is definately correct.",
            "We are seperate now."
        ]
    },
    {
        'category': 'Complex Errors',
        'examples': [
            "There is many student in the class who has problem with grammar.",
            "I don't have no time for this kind of thing.",
            "She are going to the store for buy some food."
        ]
    }
]

# Function to demonstrate corrections with detailed analysis
def demonstrate_correction(text, method='hybrid'):
    """Demonstrate correction with detailed analysis"""
    result = grammar_corrector.correct(text, method=method)
    
    print(f"\nOriginal:    '{result.original}'")
    print(f"Corrected:   '{result.corrected}'")
    print(f"Method:      {result.method_used}")
    print(f"Confidence:  {result.confidence:.3f}")
    
    if result.corrections_made:
        print(f"Changes:     {', '.join(result.corrections_made)}")
    else:
        print("Changes:     None detected")
    
    # Highlight differences
    if result.original != result.corrected:
        orig_words = result.original.split()
        corr_words = result.corrected.split()
        
        print("Differences:")
        for i, (orig, corr) in enumerate(zip(orig_words, corr_words)):
            if orig != corr:
                print(f"  Position {i+1}: '{orig}' → '{corr}'")
    
    return result

# Run demonstrations by category
for category_data in test_cases:
    print(f"\n{category_data['category'].upper()}")
    print("-" * len(category_data['category']))
    
    for example in category_data['examples']:
        demonstrate_correction(example)
        print()

# Batch processing demo
print("\n" + "="*60)
print("BATCH PROCESSING DEMO")
print("="*60)

batch_sentences = [
    "I has many friend who like to play game.",
    "She don't want to go there because its dangerous.",
    "There is a lot of people who thinks this way.",
    "He are very good at play football and basketball.",
    "We was hoping to see you at the meeting yesterday."
]

print(f"Processing {len(batch_sentences)} sentences in batch...")
batch_results = grammar_corrector.batch_correct(batch_sentences)

for i, result in enumerate(batch_results, 1):
    print(f"\n{i}. Original:  {result.original}")
    print(f"   Corrected: {result.corrected}")
    print(f"   Confidence: {result.confidence:.3f}")

# Method comparison
print("\n" + "="*60)
print("METHOD COMPARISON")
print("="*60)

comparison_sentence = "I don't have no money and she don't want to help me."
print(f"Test sentence: '{comparison_sentence}'\n")

methods = ['rule-based']
if TRANSFORMERS_AVAILABLE:
    methods.append('ml')
methods.append('hybrid')

for method in methods:
    print(f"{method.upper()} METHOD:")
    try:
        result = grammar_corrector.correct(comparison_sentence, method=method)
        print(f"  Result:     '{result.corrected}'")
        print(f"  Confidence: {result.confidence:.3f}")
        print(f"  Changes:    {len(result.corrections_made)}")
    except Exception as e:
        print(f"  Error: {e}")
    print()

# Model evaluation (if eval data is available)
if eval_data is not None and len(eval_data) > 0:
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("n=60")
    
    print("Evaluating model performance on test data...")
    eval_results = grammar_corrector.evaluate(eval_data)
    
    print(f"\nEvaluation Results:")
    for metric, value in eval_results.items():
        if isinstance(value, float):
            print(f"{metric.replace('_', ' ').title()}: {value:.3f}")
        else:
            print(f"{metric.replace('_', ' ').title()}: {value}")
    
    # Detailed evaluation on a subset
    print(f"\nDetailed Analysis (First 10 examples):")
    print("-" * 80)
    
    for idx, (_, row) in enumerate(eval_data.head(10).iterrows()):
        original = str(row.get('original', row.get('sentence', '')))
        expected = str(row.get('corrected', row.get('corrections', '')))
        
        result = grammar_corrector.correct(original)
        
        print(f"\nExample {idx + 1}:")
        print(f"  Original:  '{original}'")
        print(f"  Expected:  '{expected}'")
        print(f"  Generated: '{result.corrected}'")
        print(f"  Match:     {'✓' if result.corrected.strip().lower() == expected.strip().lower() else '✗'}")
        print(f"  Confidence: {result.confidence:.3f}")

# Training demo (if ML components available)
if TRANSFORMERS_AVAILABLE and train_data is not None:
    print("\n" + "="*60)
    print("ML MODEL TRAINING DEMO")
    print("="*60)
    
    print("Note: This would train a T5 model on the JFLEG dataset.")
    print("Training can take significant time and computational resources.")
    print("\nTo train the model, uncomment the following line:")
    print("# grammar_corrector.train_ml_component(train_data)")
    
    # Uncomment the next line to actually train (warning: this takes time!)
    # grammar_corrector.train_ml_component(train_data)

print("\n" + "="*60)
print("DEMO COMPLETE")
print("="*60)

print("\nThe grammar correction system includes:")
print("✓ Rule-based corrections for common errors")
print("✓ Vocabulary and spelling corrections")
print("✓ Subject-verb agreement fixes")
print("✓ Article error corrections")
if TRANSFORMERS_AVAILABLE:
    print("✓ Machine learning model support (T5-based)")
print("✓ Hybrid approach combining rule-based and ML")
print("✓ Batch processing capabilities")
print("✓ Performance evaluation metrics")
print("✓ Detailed error analysis")

print(f"\nTo use the system in your application:")
print("1. Import: from grammar_model_demo import HybridGrammarCorrector")
print("2. Initialize: corrector = HybridGrammarCorrector()")
print("3. Correct text: result = corrector.correct('your text here')")
print("4. Access corrected text: result.corrected")