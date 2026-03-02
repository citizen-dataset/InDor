from typing import List, Optional
from pydantic import BaseModel

class Config(BaseModel):
    task: str
    spans_task_prompt_zero_shot: str
    spans_task_prompt_few_shots: str
    rationales_task_prompt_zero_shot: str
    rationales_task_prompt_few_shots: str
    retry_prompt: str
    task_1_prompt_zero_shot: str
    task_1_prompt_few_shots: str
    task_1_retry_prompt: str
    data_path: str
    results_path: str
    evaluation_results_path: str
    model_name: str
    threads: int
    data_language: str

class PromptModel(BaseModel):
    spans_prompt_zero_shot: Optional[str] = None
    spans_prompt_few_shots: Optional[str] = None
    rationales_prompt_zero_shot: Optional[str] = None
    rationales_prompt_few_shots: Optional[str] = None
    retry_prompt: Optional[str] = None
    task_1_prompt_zero_shot: Optional[str] = None
    task_1_prompt_few_shots: Optional[str] = None
    task_1_retry_prompt: Optional[str] = None

class ExperimentConfig(BaseModel):
    text_id: str
    original_context: str
    prompts: PromptModel = PromptModel()
    spans_label: Optional[List[str]] = None
    rationales_label: Optional[List[str]] = None
    label: Optional[str] = None


class Task1ExperimentResult(ExperimentConfig):
    classification_output_zero_shot: Optional[str] = None
    classification_output_few_shots: Optional[str] = None

class Task2ExperimentResult(ExperimentConfig):
    spans_output_zero_shot: Optional[List[str]] = None
    spans_output_few_shots: Optional[List[str]] = None
    rationales_output_zero_shot: Optional[List[str]] = None
    rationales_output_few_shots: Optional[List[str]] = None