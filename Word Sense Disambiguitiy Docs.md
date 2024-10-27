#### Name- Aditya Kumar Tiwari
#### Roll no.- MSA23023



# Word Sense Disambiguitiy Docs

## Overview

WSD (Word Sense Disambiguation) tries to find correct word meanings. Techniques compare performance in **accuracy, precision, recall**, and **F1** score.

### Techniques Covered

1. **Lesk Algorithm**: Checks words' meanings using dictionary definitions and context. Simple, but only average for big context.
2. **MEMM (Max Entropy Markov Model)**: Uses POS, word surroundings, and synsets to learn meanings. Not always accurate if features aren’t ideal.
3. **Baseline WSD**: Picks most common word sense always, works okay as a basic reference.
4. **Decision Trees**: Tree-based to pick senses, based on context. Struggles with complex text.
5. **Neural Networks**: Deep learning for complex patterns but need huge data.

### Dataset & Process

Compare each algorithm on dataset:
- Take word, analyze for right meaning.
- Model learns with features like word itself and context.

### Model Performnace 

#### Lesk Algoritm
- **Accuracy**: 50%
- **Precision**: 50%
- **Recall**: 50%
- **F1 Score**: 50%

Shows Lesk is basic, good but only if context isn’t deep.

#### MEMM
- **Accuracy**: Low, about 20%
- **Struggles**: Needs more features, possibly too simple for hard meanings.

#### Baseline WSD
- **Accuracy**: 60%
- **Best in frequent words**, but misses in rare meanings.

#### Decision Tree
- **Accuracy**: Low, struggles like MEMM
- **Precision**: 0.33 for common words

#### Neural Network
- **Accuracy**: 40%, does better than MEMM/Decision Trees
- **Complexity helps but limited w/ training size**

## Analysis Points

### Feature Impact
Models depend heavy on features (POS, synsets). MEMM, Decision Trees weaker in complex situations, while Neural Nets manage well.

### Data Size
**More Data, Better Results**: Neural networks benefit most, small datasets weak.

### Complexity
Lesk: Simple but doesn’t do modern tricks.
MEMM & Decision Trees: Try complex ideas, fail w/ tiny data.
Neural: Best but data-hungry.

## Conclusion
Modern deep models do better but need good training sets and complex features. Future work could add larger sets or better feature extraction.
