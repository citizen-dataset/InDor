from typing import Dict, Any, List
import os
import re
import json

import langid

def save_json_file(data: Dict[str, Any], file_path: str):
    """save json file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Error saving json file: {e}")


def load_json_file(file_path: str) -> Dict[str, Any]:
    """load json file"""
    if not file_path or not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Error loading json file: {e}")

def check_language(language, data):
    print(data.shape)
    idx_to_remove = []
    for i, x in zip(data['text_id'].tolist(), data['rationales'].tolist()):
        if type(x) == list:
            lang = langid.classify(' '.join(x))[0]
            if lang != language:
                idx_to_remove.append(i)

    data = data[~data['text_id'].isin(idx_to_remove)]
    print('\n filtered by language: ', data.shape, '\n')
    return data

def parse_llm_output(output: str, tag: str = "<SPANS>") -> List[str]:
    """Parses the raw LLM output string into a list of labels."""
    if not output or not isinstance(output, str):
        raise ValueError(f"Invalid output: {output}")

    tag_pattern = rf"{tag}"
    # find all matches
    all_matches = list(re.finditer(tag_pattern, output, re.IGNORECASE))
    
    if all_matches:
        # use the last match
        last_match = all_matches[-1]
        match_output = output[last_match.end():].strip()
        if match_output.startswith(":"):
            match_output = match_output[1:].strip()
        if match_output.endswith("."):
            match_output = match_output[:-1].strip()
        try:
            labels = json.loads(match_output)
        except Exception as e:
            print(f"Error Output: {match_output}")
            raise ValueError(f"Invalid output: {output}")
    else:
        print(f"No {tag} tag found in LLM output: {output}")
        raise ValueError(f"Invalid output: {output}")

    return labels

def parse_task1_llm_output(output: str) -> List[str]:
    """Parses the raw LLM output string into a list of labels."""
    if not output or not isinstance(output, str):
        raise ValueError(f"Invalid output: {output}")
    if output.strip().lower() in ["none", "slightly", "moderately", "highly"]:
        return output.strip().lower()

    tag_pattern = r"<PREDICTED_LABEL>"
    # find all matches
    all_matches = list(re.finditer(tag_pattern, output, re.IGNORECASE))
    
    if all_matches:
        # use the last match
        last_match = all_matches[-1]
        match_output = output[last_match.end():].strip()
        if match_output.startswith(":"):
            match_output = match_output[1:].strip()
        if match_output.endswith("."):
            match_output = match_output[:-1].strip()
        if match_output not in ["none", "slightly", "moderately", "highly"]:
            raise ValueError(f"Invalid output: {output}")
        label = match_output.lower()
    else:
        raise ValueError(f"Invalid output: {output}")

    return label