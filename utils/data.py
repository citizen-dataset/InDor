from datasets import load_dataset
from typing import List, Tuple
import random
import json
import os

import pandas as pd

from utils.models import Config, ExperimentConfig, PromptModel
from utils.tools import save_json_file, load_json_file, check_language

def load_data(config: Config) -> pd.DataFrame:
    """Loads data from a JSONL file."""
    try:
        dataset = load_dataset('json', data_files=config.data_path)
        df = pd.DataFrame(dataset['train'])
        return df
    except Exception as e:
        print(f"Error loading or processing data from {config.data_path}: {e}")
        raise

def data_cleaning_task1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame by merging entries with the same text_id
    """

    def custom_label_agg(labels_series: pd.Series) -> str | None:
        processed_labels = []
        for lbl in labels_series:
            if pd.notna(lbl):
                s_lbl = str(lbl).strip()
                if s_lbl not in ["none", "slightly", "moderately", "highly"]:
                    if s_lbl != "n/a":
                        print(s_lbl)
                if s_lbl:
                    processed_labels.append(s_lbl)

        if not processed_labels:
            return None

        unique_labels = sorted(list(set(processed_labels)))

        if len(unique_labels) == 1:
            if unique_labels[0] == "n/a":
                return None
            return unique_labels[0]
        else:
            return ",".join(unique_labels)

    aggregation_funcs = {
        col: 'first' for col in df.columns if col not in ['text_id', 'label']
    }
    aggregation_funcs['label'] = custom_label_agg

    df_agg = df.groupby('text_id', as_index=False).agg(aggregation_funcs)

    df_cleaned = df_agg[df_agg['label'].notna()]
    
    return df_cleaned

def data_cleaning(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    """
    Cleans the DataFrame by merging entries with the same text_id
    and filtering based on spans and rationales lengths.
    """
    # Define aggregation functions
    aggregation_funcs = {
        col: 'first' for col in df.columns if col not in ['text_id', 'spans', 'rationales']
    }
    # Use list concatenation and deduplication for spans and rationales, preserving order
    aggregation_funcs['spans'] = lambda x: list(dict.fromkeys(sum(x.tolist(), [])))
    aggregation_funcs['rationales'] = lambda x: list(dict.fromkeys(sum(x.tolist(), [])))

    # Group by text_id and aggregate
    df_agg = df.groupby('text_id', as_index=False).agg(aggregation_funcs)

    # Calculate lengths of spans and rationales
    df_agg['spans_len'] = df_agg['spans'].apply(len)
    df_agg['rationales_len'] = df_agg['rationales'].apply(len)

    # Filter out rows where spans or rationales are empty
    df_filtered = df_agg[(df_agg['spans_len'] > 0) & (df_agg['rationales_len'] > 0)]
    
    # Filter out rows where spans and rationales lengths differ
    df_filtered = df_filtered[df_filtered['spans_len'] == df_filtered['rationales_len']]

    # Drop temporary length columns
    df_cleaned = df_filtered.drop(columns=['spans_len', 'rationales_len'])

    # Filter out rows where language is not the same as the data language
    df_cleaned = check_language(config.data_language, df_cleaned)

    return df_cleaned

def prepare_task1_experiment_configs(
    config: Config, 
    prompt_model: PromptModel,
    experiment_configs: List[ExperimentConfig],
    df: pd.DataFrame
) -> None:
    for _, row in df.iterrows():
        text_id = row["text_id"]
        input_text = str(row["text"])
        task_1_prompt_zero_shot = prompt_model.task_1_prompt_zero_shot.format(instance=input_text)
        task_1_prompt_few_shots = prompt_model.task_1_prompt_few_shots.format(instance=input_text)
        task_1_retry_prompt = prompt_model.task_1_retry_prompt
        # Process labels
        if row["label"] is None:
            continue
        label = row["label"].lower()
        experiment_configs.append(
            ExperimentConfig(
                text_id=str(text_id), 
                original_context=input_text,
                prompts=PromptModel(
                    task_1_prompt_zero_shot=task_1_prompt_zero_shot,
                    task_1_prompt_few_shots=task_1_prompt_few_shots,
                    task_1_retry_prompt=task_1_retry_prompt
                ),
                label=label
            )
        )

def prepare_task2_experiment_configs(
    config: Config, 
    prompt_model: PromptModel,
    experiment_configs: List[ExperimentConfig],
    df: pd.DataFrame
) -> None:

    for _, row in df.iterrows():
        text_id = row["text_id"]
        input_text = str(row["text"])
        spans_prompt_zero_shot = prompt_model.spans_prompt_zero_shot.format(instance=input_text)
        spans_prompt_few_shots = prompt_model.spans_prompt_few_shots.format(instance=input_text)
        rationales_prompt_zero_shot = prompt_model.rationales_prompt_zero_shot
        rationales_prompt_few_shots = prompt_model.rationales_prompt_few_shots
        retry_prompt = prompt_model.retry_prompt
        # Process labels
        spans_labels = row["spans"]
        rationales_labels = row["rationales"]

        if isinstance(spans_labels, list):
            spans_label = [str(l) for l in spans_labels] if spans_labels else ['No']
        if isinstance(rationales_labels, list):
            rationales_label = [str(l) for l in rationales_labels] if rationales_labels else ['No']
            
        experiment_configs.append(
            ExperimentConfig(
                text_id=str(text_id), 
                original_context=input_text,
                prompts=PromptModel(
                    spans_prompt_zero_shot=spans_prompt_zero_shot, 
                    spans_prompt_few_shots=spans_prompt_few_shots,
                    rationales_prompt_zero_shot=rationales_prompt_zero_shot,
                    rationales_prompt_few_shots=rationales_prompt_few_shots,
                    retry_prompt=retry_prompt
                ),
                spans_label=spans_label,
                rationales_label=rationales_label
            )
        )

def load_and_prepare_data(
    config: Config, 
    prompt_model: PromptModel
) -> List[ExperimentConfig]:
    """Loads data from a JSONL file, prepares prompts, and extracts true labels."""

    df = load_data(config)

    experiment_configs = []
    if config.task == "task1":
        df = data_cleaning_task1(df)
        prepare_task1_experiment_configs(config, prompt_model, experiment_configs, df)
    elif config.task == "task2":
        df = data_cleaning(df, config)
        prepare_task2_experiment_configs(config, prompt_model, experiment_configs, df)
    return experiment_configs