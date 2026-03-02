# Materials for the InDor corpus creation and experiments

## Overview

This repository contains resources for experiments with InDor, a multilingual dataset of news excerpts annotated as false or biased.  
The resources support research on natural language understanding, bias detection, and disinformation detection.

## Materials
- `annotation_guidelines.pdf`
- `surveys_and_focus_group.pdf` reports the contents of the Pre-annotation and Post-annotation surveys and focus group discussion questions aimed at fostering discussions about the perception of problematic language and framing in news articles.
- `prompts.py`

## Annotation guidelines
The main dataset consists of annotated news excerpts. For each excerpt, annotators highlight spans of text that may convey biased or misleading information and provide a rationale in a structured **“if [...] / then [...]”** format. Annotations focus on:

- **Eventive elements**: How events are described, including causality and agency.
- **Attributive elements**: How people or entities are described, including appearance, emotions, and relationships.

### Prompts
Two prompts were used in experiments for classifying the severity of problematic language:

1. **Zero-Shot Prompt** – Classifies severity without examples.  
2. **Few-Shot Prompt** – Classifies severity with examples for context.

Both prompts instruct models to return **one of four severity labels**:

- `none`
- `slightly`
- `moderately`
- `highly`

Output must strictly follow:
<PREDICTED_LABEL>: [label]

No additional text, explanation, or commentary should be included.

## Intended Use

These resources can be used for:

- Research on bias, framing, and misrepresentation in news articles.  
- Development of AI systems for detecting problematic language.  
- Training models to generate structured explanations for bias or disinformation.  
- Studying human perception of problematic content across languages and news types.

## Citation

Please cite the accompanying paper when using these resources.  

---

*This repository is intended for research purposes only.*










