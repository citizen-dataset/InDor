from evaluate import load
import numpy as np
from tqdm import tqdm

def calculate_bert_score(outputs, list_spans):
    import itertools  
    bertscore = load("bertscore")

    all_f1 = []
    for i, spans in tqdm(enumerate(list_spans), total=len(list_spans), desc="Calculating BERT Score"):
        list_level_f1 = []
        # compute couples: generated output with the most corresponding annotation by means of bertscore
        couples = list(itertools.product(spans, outputs[i]))
        scores = []
        for p in couples:
            if '0' not in p:
                score = bertscore.compute(predictions=[p[0]], references=[p[1]], lang="en")["f1"]
                scores.append(score)
            else:
                scores.append([0.0])
        scores = np.array(scores)
        unflatten_scores = scores.reshape(len(spans), -1).T # N_output X N_spans

        # reduce matrix to the most relevant couples
        for j in range(max(len(spans), len(outputs[i]))):
            # Take the max 
            max_score_indices = np.unravel_index(unflatten_scores.argmax(), unflatten_scores.shape)
            max_ = unflatten_scores[max_score_indices[0],max_score_indices[1]]
            list_level_f1.append(max_)
            unflatten_scores[max_score_indices[0],:] = 0
            unflatten_scores[:,max_score_indices[1]] = 0

        all_f1.append(np.mean(list_level_f1))
    f1 = np.average(all_f1)
    return f1

def calculate_selfblue_score(predictions):
    '''
    Regarding one sentence as hypothesis and the others as reference, we can calculate BLEU score for every generated sentence, 
    and define the average BLEU score to be the Self-BLEU of the document.
    predictions = list containing the model-generated text
    references = list containing the rest of model-generated texts
    '''
    # blue score from hf evalutate doesn't allow the comparison between lists of different length
    # nltk report an issue with sqlite3: from nltk.translate import bleu
    bleu = load("bleu")

    print('\n comparing: 1 vs. all')
    results = []
    couples = []
    for i in range(len(predictions)):
        for j in range(1, len(predictions)):
            if i+j in range(len(predictions)):
                if (i,j) not in couples:
                    # print(i, j)
                    results.append(bleu.compute(predictions=[predictions[i]], references=[predictions[i+j]])['bleu'])
                    couples.append((j,i))

    return np.average(results)

def calculate_token_match_accuracy(predictions, humans):
    from thefuzz import fuzz
    scores = []
    for i in tqdm(predictions, total=len(predictions), desc="Calculating Token Match Accuracy"):
        score = fuzz.token_sort_ratio(i, humans[i])
        scores.append(score)

    acc = np.average(scores)
    return acc