#### Name- Aditya Kumar Tiwari
#### Roll no.- MSA23023


# Named Enitity Reconition usin BERT 

### Descprition

Named Entitiy Recognition (NER) is all about recognisin the big, special words in text. Like names, or places, or what not. With BERT, we train on like, CoNNL dataset? It has all these words all lined up with labels so model can learn better. 

1. **Tokenize Text**
    - You tokenize it, means the words get broken down to tiny pieces BERT gets. Like, it can split one word into few. But they gotta be aligned with labels. Align it using `align_targets` func. 

2. **Model Set-up**
    - Model prepped up with tokens, types, etc., and it gets to recognizng. Classify tokens as the entities type.

3. **Training**
    - Train with epochs on the train and validation datasets, to get best accuracy, and then test for predicted labels to real ones.

4. **Evalute**
    - Use Precision, Recall and F1-Scores. Good numbers mean BERT can spot named entites well. If not, oh well need better data.

### Libraries

- `load_dataset`: get datasets, `pandas`, `numpy` for manipulation.
- **Important Functions**
    - `AutoTokenizer`, `load_metric`, `SparseCategoricalCrossentropy`: good for trainin purposes

### Data Loadin

    - CoNNL dataset is usually for NER. Loading with `load_dataset('conll2003')`

#### Model Checkpoint
    - BERT base case used, i.e. case-sensitive tokens, better for text w/ upper-lower case mix

### Tokenizations

    - Original Tokens to New Tokenized ones, gotta print and see if labels match up

#### Purpose:
    - Call `align_targets` to check aligned with human-readable labels
    - Outputs list of words, categories, and their labels 

### Training Prep

1. *Create Training Dataset*: Proper format, with `collate_fn` 
2. *Create Validation Dataset*: Same setup for validation data
3. *ID Mappings*: IDs to Labels map for model

#### Loss function

    - Compute loss function if tokens miss labels, ignore the empty or -100 classes

### Predict & Results 

1. Test dataset on unseen data, and see accuracy using:
    - `eval_metric` like F1, precision, etc., if high, model good; low, need more train data
2. Print Results with token IDs to actual word predictions.

---
