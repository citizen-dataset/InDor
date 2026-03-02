import json
import os
import concurrent.futures
from typing import List, Dict, Tuple

from dotenv import load_dotenv
from tqdm import tqdm
from sklearn.metrics import f1_score, accuracy_score

from llm.llm_client import LLMClient
from prompt.prompt_manager import PromptManager
from utils.config import load_config
from utils.models import Config, ExperimentConfig, Task1ExperimentResult, Task2ExperimentResult, PromptModel
from utils.data import load_and_prepare_data
from utils.evaluation import calculate_bert_score, calculate_token_match_accuracy
from utils.tools import load_json_file, save_json_file, parse_llm_output, parse_task1_llm_output

load_dotenv()

def run_inference(prompt: str, llm_client: LLMClient, model_name: str) -> str:
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = llm_client.complete(
        model=model_name,
        messages=messages,
    )
    return response

def get_all_prompts(config: Config, prompt_manager: PromptManager) -> PromptModel:
    if config.task == "task1":
        task_1_prompt_zero_shot = prompt_manager.get_prompt(
            f"{config.task_1_prompt_zero_shot}_{config.data_language}").strip()
        task_1_prompt_few_shots = prompt_manager.get_prompt(
            f"{config.task_1_prompt_few_shots}_{config.data_language}").strip()
        task_1_retry_prompt = prompt_manager.get_prompt(config.task_1_retry_prompt).strip()
        return PromptModel(
            task_1_prompt_zero_shot=task_1_prompt_zero_shot,
            task_1_prompt_few_shots=task_1_prompt_few_shots,
            task_1_retry_prompt=task_1_retry_prompt
        )
    spans_prompt_zero_shot = prompt_manager.get_prompt(
        f"{config.spans_task_prompt_zero_shot}_{config.data_language}").strip()
    rationales_prompt_zero_shot = prompt_manager.get_prompt(
        f"{config.rationales_task_prompt_zero_shot}_{config.data_language}").strip()
    spans_prompt_few_shots = prompt_manager.get_prompt(
        f"{config.spans_task_prompt_few_shots}_{config.data_language}").strip()
    rationales_prompt_few_shots = prompt_manager.get_prompt(
        f"{config.rationales_task_prompt_few_shots}_{config.data_language}").strip()
    retry_prompt = prompt_manager.get_prompt(config.retry_prompt).strip()
    return PromptModel(
        spans_prompt_zero_shot=spans_prompt_zero_shot,
        spans_prompt_few_shots=spans_prompt_few_shots,
        rationales_prompt_zero_shot=rationales_prompt_zero_shot,
        rationales_prompt_few_shots=rationales_prompt_few_shots,
        retry_prompt=retry_prompt
    )

def run_inference_spans(
    config: Config, 
    llm_client: LLMClient,
    experiment_configs: List[ExperimentConfig], 
    experiment_results: Dict[str, Task2ExperimentResult]
) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.threads) as executor:
        futures = {}
        for e_config in experiment_configs:
            if e_config.text_id not in experiment_results:
                futures[executor.submit(run_inference, e_config.prompts.spans_prompt_zero_shot, llm_client, config.model_name)] = (e_config, "zero_shot")
                futures[executor.submit(run_inference, e_config.prompts.spans_prompt_few_shots, llm_client, config.model_name)] = (e_config, "few_shots")
            elif experiment_results[e_config.text_id].spans_output_zero_shot is None:
                futures[executor.submit(run_inference, e_config.prompts.spans_prompt_zero_shot, llm_client, config.model_name)] = (e_config, "zero_shot")
            elif experiment_results[e_config.text_id].spans_output_few_shots is None:
                futures[executor.submit(run_inference, e_config.prompts.spans_prompt_few_shots, llm_client, config.model_name)] = (e_config, "few_shots")
        print(f"Running inference on {len(futures)} tasks...")
        completed_count = 0
        success_count = 0
        error_count = 0
        for future in concurrent.futures.as_completed(futures):
            e_config: ExperimentConfig = futures[future][0]
            prompt_type: str = futures[future][1]
            try:
                result = future.result()
                parsed_output = parse_llm_output(result, tag="<SPANS>")
                success_count += 1
            except Exception as e:
                print(f"\nError, Start to retry with llm")
                retry_prompt = e_config.prompts.retry_prompt.format(tag="<SPANS>", model_output=result)
                retry_result = run_inference(retry_prompt, llm_client, "meta-llama/llama-4-maverick")
                try:
                    parsed_output = json.loads(retry_result)
                    success_count += 1
                    print("Retry success")
                    print(parsed_output)
                except Exception as e:
                    parsed_output = None
                    error_count += 1
                    print("Error after retry")
            finally:
                completed_count += 1
                if completed_count % 50 == 0:
                    print(f"Completed {completed_count}/{len(futures)} samples")
                    print(f"Success: {success_count}, Error: {error_count}")
                    experiment_results_json = {text_id: e_result.model_dump() for text_id, e_result in experiment_results.items()}
                    save_json_file(experiment_results_json, config.results_path)
                if e_config.text_id not in experiment_results:
                    experiment_results[e_config.text_id] = Task2ExperimentResult(**e_config.model_dump())
                if prompt_type == "zero_shot":
                    experiment_results[e_config.text_id].spans_output_zero_shot=parsed_output
                else:
                    experiment_results[e_config.text_id].spans_output_few_shots=parsed_output
    print("\nInference complete.\n")
    
def run_inference_rationales(
    config: Config, 
    llm_client: LLMClient,
    experiment_configs: List[ExperimentConfig], 
    experiment_results: Dict[str, Task2ExperimentResult]
) -> None:

    with concurrent.futures.ThreadPoolExecutor(max_workers=config.threads) as executor:
        futures = {}
        for e_config in experiment_configs:
            if e_config.text_id not in experiment_results:
                continue
            spans_output_zero_shot = experiment_results[e_config.text_id].spans_output_zero_shot
            spans_output_few_shots = experiment_results[e_config.text_id].spans_output_few_shots
            rationales_output_zero_shot = experiment_results[e_config.text_id].rationales_output_zero_shot
            rationales_output_few_shots = experiment_results[e_config.text_id].rationales_output_few_shots
            if spans_output_zero_shot and rationales_output_zero_shot is None:
                futures[executor.submit(
                    run_inference, 
                    e_config.prompts.rationales_prompt_zero_shot.format(
                        instance=e_config.original_context,
                        spans=spans_output_zero_shot), 
                    llm_client, 
                    config.model_name
                )] = (e_config, "zero_shot")
                
            if spans_output_few_shots and rationales_output_few_shots is None:
                futures[executor.submit(
                    run_inference, 
                    e_config.prompts.rationales_prompt_few_shots.format(
                        instance=e_config.original_context,
                        spans=spans_output_few_shots), 
                    llm_client, 
                    config.model_name
                )] = (e_config, "few_shots")

        print(f"Running inference on {len(futures)} tasks...")
        completed_count = 0
        success_count = 0
        error_count = 0
        for future in concurrent.futures.as_completed(futures):
            e_config: ExperimentConfig = futures[future][0]
            prompt_type: str = futures[future][1]
            try:
                result = future.result()
                parsed_output = parse_llm_output(result, tag="<RATIONALES>")
                success_count += 1
            except Exception as e:
                print(f"\nError, Start to retry with llm")
                retry_prompt = e_config.prompts.retry_prompt.format(tag="<RATIONALES>", model_output=result)
                retry_result = run_inference(retry_prompt, llm_client, "meta-llama/llama-4-maverick")
                try:
                    parsed_output = json.loads(retry_result)
                    success_count += 1
                    print("Retry success")
                    print(parsed_output)
                except Exception as e:
                    parsed_output = None
                    error_count += 1
                    print("Error after retry")
            finally:
                completed_count += 1
                if completed_count % 50 == 0:
                    print(f"Completed {completed_count}/{len(futures)} samples")
                    print(f"Success: {success_count}, Error: {error_count}")
                    experiment_results_json = {text_id: e_result.model_dump() for text_id, e_result in experiment_results.items()}
                    save_json_file(experiment_results_json, config.results_path)
                if prompt_type == "zero_shot":
                    experiment_results[e_config.text_id].rationales_output_zero_shot=parsed_output
                else:
                    experiment_results[e_config.text_id].rationales_output_few_shots=parsed_output

    print("\nRationales Inference complete.\n")

def run_inference_task1(
    config: Config, 
    llm_client: LLMClient,
    experiment_configs: List[ExperimentConfig], 
    experiment_results: Dict[str, Task1ExperimentResult]
) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.threads) as executor:
        futures = {}
        for e_config in experiment_configs:
            if e_config.text_id not in experiment_results:
                futures[executor.submit(run_inference, e_config.prompts.task_1_prompt_zero_shot, llm_client, config.model_name)] = (e_config, "zero_shot")
                futures[executor.submit(run_inference, e_config.prompts.task_1_prompt_few_shots, llm_client, config.model_name)] = (e_config, "few_shots")
            elif experiment_results[e_config.text_id].classification_output_zero_shot is None:
                futures[executor.submit(run_inference, e_config.prompts.task_1_prompt_zero_shot, llm_client, config.model_name)] = (e_config, "zero_shot")
            elif experiment_results[e_config.text_id].classification_output_few_shots is None:
                futures[executor.submit(run_inference, e_config.prompts.task_1_prompt_few_shots, llm_client, config.model_name)] = (e_config, "few_shots")
        print(f"Running inference on {len(futures)} tasks...")
        completed_count = 0
        success_count = 0
        error_count = 0
        for future in concurrent.futures.as_completed(futures):
            e_config: ExperimentConfig = futures[future][0]
            prompt_type: str = futures[future][1]
            try:
                result = future.result()
                parsed_output = parse_task1_llm_output(result)
                success_count += 1
            except Exception as e:
                print(f"\nError, Start to retry with llm")
                retry_prompt = e_config.prompts.task_1_retry_prompt.format(model_output=result)
                retry_result = run_inference(retry_prompt, llm_client, config.model_name)
                try:
                    parsed_output = parse_task1_llm_output(retry_result)
                    success_count += 1
                    print("Retry success")
                    print(parsed_output)
                except Exception as e:
                    parsed_output = None
                    error_count += 1
                    print("Error after retry")
            finally:
                completed_count += 1
                if completed_count % 50 == 0:
                    print(f"Completed {completed_count}/{len(futures)} samples")
                    print(f"Success: {success_count}, Error: {error_count}")
                    experiment_results_json = {text_id: e_result.model_dump() for text_id, e_result in experiment_results.items()}
                    save_json_file(experiment_results_json, config.results_path)
                if e_config.text_id not in experiment_results:
                    experiment_results[e_config.text_id] = Task1ExperimentResult(**e_config.model_dump())
                if prompt_type == "zero_shot":
                    experiment_results[e_config.text_id].classification_output_zero_shot=parsed_output
                else:
                    experiment_results[e_config.text_id].classification_output_few_shots=parsed_output
    print("\nInference complete.\n")

def reformat_experiment_results_for_task1(experiment_results: Dict[str, Task1ExperimentResult]) -> Tuple:
    result_mapping = {
        "none": 0,
        "slightly": 1,
        "moderately": 2,
        "highly": 3
    }
    output_classification_zero_shot = []
    output_classification_few_shots = []
    output_classification_ground_truth = []
    for _, e_result in experiment_results.items():
        output_classification_zero_shot.append(result_mapping[e_result.classification_output_zero_shot])
        output_classification_few_shots.append(result_mapping[e_result.classification_output_few_shots])
        output_classification_ground_truth.append(result_mapping[e_result.classification_label])
    return (
        output_classification_zero_shot,
        output_classification_few_shots,
        output_classification_ground_truth
    )

def reformat_experiment_results_for_task2(experiment_results: Dict[str, Task2ExperimentResult]) -> Tuple:
    output_spans_zero_shot = []
    output_spans_few_shots = []
    output_spans_ground_truth = []
    output_rationales_zero_shot = []
    output_rationales_few_shots = []
    output_rationales_ground_truth = []
    for _, e_result in experiment_results.items():
        output_spans_zero_shot.append(e_result.spans_output_zero_shot)
        output_spans_few_shots.append(e_result.spans_output_few_shots)
        output_spans_ground_truth.append(e_result.spans_label)
        output_rationales_zero_shot.append(e_result.rationales_output_zero_shot)
        output_rationales_few_shots.append(e_result.rationales_output_few_shots)
        output_rationales_ground_truth.append(e_result.rationales_label)
    return (
        output_spans_zero_shot, 
        output_spans_few_shots, 
        output_spans_ground_truth, 
        output_rationales_zero_shot, 
        output_rationales_few_shots, 
        output_rationales_ground_truth
    )

def get_mapped_model_name(model_name: str) -> str:
    if model_name == "meta-llama/llama-4-maverick":
        return "llama"
    elif model_name == "qwen/qwen3-235b-a22b":
        return "qwen"
    elif model_name == "mistralai/mixtral-8x22b-instruct":
        return "mistral"

def main():
    # --- 1. Load Configuration ---
    config_dict = load_config("config.yaml")
    config = Config(**config_dict)
    config.data_path = config.data_path.format(language=config.data_language)
    config.results_path = config.results_path.format(
        task=config.task,
        model=get_mapped_model_name(config.model_name),
        language=config.data_language)
    config.evaluation_results_path = config.evaluation_results_path.format(
        task=config.task,
        model=get_mapped_model_name(config.model_name),
        language=config.data_language)

    prompt_manager = PromptManager()
    prompt_model = get_all_prompts(config, prompt_manager)

    # --- 2. Load and Prepare Data ---
    print(f"Loading data from: {config.data_path}")
    experiment_configs: List[ExperimentConfig] = load_and_prepare_data(
        config, 
        prompt_model
    )
    print(f"{config.task}: Loaded {len(experiment_configs)} experiment configs.")
    experiment_results = {}
    if os.path.exists(config.results_path):
        experiment_results = load_json_file(config.results_path)
        if config.task == "task1":
            experiment_results = {text_id: Task1ExperimentResult(**e_result) for text_id, e_result in experiment_results.items()}
        elif config.task == "task2":
            for i, (text_id, e_result) in enumerate(experiment_results.items()):
                try:
                    experiment_results[text_id] = Task2ExperimentResult(**e_result)
                except Exception as e:
                    pass
                    
            # experiment_results = {text_id: Task2ExperimentResult(**e_result) for text_id, e_result in experiment_results.items()}
        print(f"Loaded {len(experiment_results)} experiment results.")
    else:
        print(f"No experiment results found at: {config.results_path}, initializing empty results.")
    
    if os.path.exists(config.evaluation_results_path):
        evaluation_results = load_json_file(config.evaluation_results_path)
    else:
        evaluation_results = {}


    # --- 3. Initialize LLM Client ---
    llm_client = LLMClient()
    print(f"Using LLM: {config.model_name}")

    # --- 4. Run Inference for spans detection ---
    print(f"Starting inference on {len(experiment_configs)} samples with {config.threads} threads...")
    if config.task == "task1":
        run_inference_task1(config, llm_client, experiment_configs, experiment_results)
    elif config.task == "task2":
        run_inference_spans(config, llm_client, experiment_configs, experiment_results)
        experiment_results_json = {text_id: e_result.model_dump() for text_id, e_result in experiment_results.items()}
        save_json_file(experiment_results_json, config.results_path)
        run_inference_rationales(config, llm_client, experiment_configs, experiment_results)
        experiment_results_json = {text_id: e_result.model_dump() for text_id, e_result in experiment_results.items()}
        save_json_file(experiment_results_json, config.results_path)

    # # --- 5. Evaluate Results ---
    print("\nStarting evaluation...")
    # if config.task == "task1":
    #     reformatted_output = reformat_experiment_results_for_task1(experiment_results)
    #     try:
    #         if f"classification_zero_shot_f1_score_{config.data_language}" not in evaluation_results:
    #             classification_zero_shot_f1_score = f1_score(reformatted_output[2], reformatted_output[0], average="weighted")
    #             print(f"\nEvaluation Classification Zero Shot F1 Score: {classification_zero_shot_f1_score}")
    #             evaluation_results[f"classification_zero_shot_f1_score_{config.data_language}"] = classification_zero_shot_f1_score
    #         if f"classification_few_shots_f1_score_{config.data_language}" not in evaluation_results:
    #             classification_few_shots_f1_score = f1_score(reformatted_output[2], reformatted_output[1], average="weighted")
    #             print(f"\nEvaluation Classification Few Shots F1 Score: {classification_few_shots_f1_score}")
    #             evaluation_results[f"classification_few_shots_f1_score_{config.data_language}"] = classification_few_shots_f1_score
    #         if f"classification_zero_shot_accuracy_{config.data_language}" not in evaluation_results:
    #             classification_zero_shot_accuracy = accuracy_score(reformatted_output[2], reformatted_output[0])
    #             print(f"\nEvaluation Classification Zero Shot Accuracy: {classification_zero_shot_accuracy}")
    #             evaluation_results[f"classification_zero_shot_accuracy_{config.data_language}"] = classification_zero_shot_accuracy
    #         if f"classification_few_shots_accuracy_{config.data_language}" not in evaluation_results:
    #             classification_few_shots_accuracy = accuracy_score(reformatted_output[2], reformatted_output[1])
    #             print(f"\nEvaluation Classification Few Shots Accuracy: {classification_few_shots_accuracy}")
    #             evaluation_results[f"classification_few_shots_accuracy_{config.data_language}"] = classification_few_shots_accuracy
    #     except Exception as e:
    #         print(f"\nError: {e}")
    #         save_json_file(evaluation_results, config.evaluation_results_path)
            
    # if config.task == "task2":
    #     reformatted_output = reformat_experiment_results_for_task2(experiment_results)
    #     try:
    #         if f"spans_zero_shot_bert_score_{config.data_language}" not in evaluation_results:
    #             spans_zero_shot_bert_score = calculate_bert_score(reformatted_output[0], reformatted_output[2])
    #             print(f"\nEvaluation Spans Zero Shot Bert Scores: {spans_zero_shot_bert_score}")
    #             evaluation_results[f"spans_zero_shot_bert_score_{config.data_language}"] = spans_zero_shot_bert_score
    #         if f"spans_few_shots_bert_score_{config.data_language}" not in evaluation_results:
    #             spans_few_shots_bert_score = calculate_bert_score(reformatted_output[1], reformatted_output[2])
    #             print(f"\nEvaluation Spans Few Shots Bert Scores: {spans_few_shots_bert_score}")
    #             evaluation_results[f"spans_few_shots_bert_score_{config.data_language}"] = spans_few_shots_bert_score
    #         if f"rationales_zero_shot_bert_score_{config.data_language}" not in evaluation_results:
    #             rationales_zero_shot_bert_score = calculate_bert_score(reformatted_output[3], reformatted_output[5])
    #             print(f"\nEvaluation Rationales Zero Shot Bert Scores: {rationales_zero_shot_bert_score}")
    #             evaluation_results[f"rationales_zero_shot_bert_score_{config.data_language}"] = rationales_zero_shot_bert_score
    #         if f"rationales_few_shots_bert_score_{config.data_language}" not in evaluation_results:
    #             rationales_few_shots_bert_score = calculate_bert_score(reformatted_output[4], reformatted_output[5])
    #             print(f"\nEvaluation Rationales Few Shots Bert Scores: {rationales_few_shots_bert_score}")
    #             evaluation_results[f"rationales_few_shots_bert_score_{config.data_language}"] = rationales_few_shots_bert_score
            # if f"spans_zero_shot_token_match_accuracy_{config.data_language}" not in evaluation_results:
            #     spans_zero_shot_token_match_accuracy = calculate_token_match_accuracy(reformatted_output[0], reformatted_output[2])
            #     print(f"\nEvaluation Spans Zero Shot Token Match Accuracy: {spans_zero_shot_token_match_accuracy}")
            #     evaluation_results[f"spans_zero_shot_token_match_accuracy_{config.data_language}"] = spans_zero_shot_token_match_accuracy
            # if f"spans_few_shots_token_match_accuracy_{config.data_language}" not in evaluation_results:
            #     spans_few_shots_token_match_accuracy = calculate_token_match_accuracy(reformatted_output[1], reformatted_output[2])
            #     print(f"\nEvaluation Spans Few Shots Token Match Accuracy: {spans_few_shots_token_match_accuracy}")
            #     evaluation_results[f"spans_zero_shot_token_match_accuracy_{config.data_language}"] = spans_zero_shot_token_match_accuracy
            # if f"rationales_zero_shot_token_match_accuracy_{config.data_language}" not in evaluation_results:
            #     rationales_zero_shot_token_match_accuracy = calculate_token_match_accuracy(reformatted_output[3], reformatted_output[5])
            #     print(f"\nEvaluation Rationales Zero Shot Token Match Accuracy: {rationales_zero_shot_token_match_accuracy}")
            #     evaluation_results[f"rationales_zero_shot_token_match_accuracy_{config.data_language}"] = rationales_zero_shot_token_match_accuracy
            # if f"rationales_few_shots_token_match_accuracy_{config.data_language}" not in evaluation_results:
            #     rationales_few_shots_token_match_accuracy = calculate_token_match_accuracy(reformatted_output[4], reformatted_output[5])
            #     print(f"\nEvaluation Rationales Few Shots Token Match Accuracy: {rationales_few_shots_token_match_accuracy}")
            #     evaluation_results[f"rationales_few_shots_token_match_accuracy_{config.data_language}"] = rationales_few_shots_token_match_accuracy
        # except Exception as e:
        #     print(f"\nError: {e}")
        #     save_json_file(evaluation_results, config.evaluation_results_path)

    # --- 6. Save Results ---
    # save_json_file(evaluation_results, config.evaluation_results_path)
    experiment_results_json = {text_id: e_result.model_dump() for text_id, e_result in experiment_results.items()}
    save_json_file(experiment_results_json, config.results_path)


if __name__ == "__main__":
    main()
