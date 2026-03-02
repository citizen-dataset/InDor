"""
This file contains the exact prompts used in the experiments described in the paper.
All experiments were run with two LLMs:
    i. Llama 4 Maverick 400B
    ii. Mixtral Instruct 140B

Models were accessed via OpenRouter.ai with their default configurations.

Author(s): [Anonymous for review]
"""

"SPAN DETECTION"

spans_detection_zero_shot_en = """You are a framing and language bias expert. Your job is to analyze news excerpts and identify text spans that may be misleading, biased, speculative, emotionally charged or problematic.

TASK
- Identify only unique, non-overlapping spans that could affect reader perception.
- If no spans are found, write "No"

PROBLEMATIC SPANS INCLUDE:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual
OUTPUT FORMAT (strict):
If ONE span:
<SPANS>: ["..."]

If MULTIPLE spans:
<SPANS>: ["...", "..."]

If no spans:
<SPANS>: ["No"]

**Now process the following input:**
{instance}

Return answer with ONLY ONE <SPANS> block. Do NOT return multiple blocks. Do NOT repeat spans already listed. Ensure formatting is strictly followed. Do not add explanations.
"""

spans_detection_few_shots_en = """You are a framing and language bias expert. Your job is to analyze news excerpts and identify text spans that may be misleading, biased, speculative, emotionally charged or problematic.

TASK
- Identify only unique, non-overlapping spans that could affect reader perception.
- If no spans are found, write "No"

PROBLEMATIC SPANS INCLUDE:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual
OUTPUT FORMAT (strict):
If ONE span:
<SPANS>: ["..."]

If MULTIPLE spans:
<SPANS>: ["...", "..."]

If no spans:
<SPANS>: ["No"]

Return ONLY ONE <SPANS> block. Do NOT return multiple blocks. Do NOT repeat spans already listed. Ensure formatting is strictly followed.


Example 1 (for reference only — do NOT copy this):
Input:

News Excerpt: None
Spans: [ "" ]

Example 2 (for reference only — do NOT copy this):
Input:

News Excerpt: None
Spans: [ "" ]

Now analyze the following input and return ONLY the final <SPANS> output:
{instance}

Return answer with ONLY ONE <SPANS> block. Do NOT return multiple blocks. Do NOT repeat spans already listed. Ensure formatting is strictly followed. Do not add explanations.
"""


"RATIONALES GENERATION"

rationales_generation_zero_shot_en = """You are an expert in discourse framing and media bias. Your task is to explain why certain spans of text in a news excerpt may be misleading, biased, or problematic.

You are given:
1. A news excerpt with:
   - One TITLE line
   - Three SENTENCE lines (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. A list of exact spans extracted from that text.

Your goal is to generate **one rationale for each span**. Use this strict format:
→ "if [reference to the span in the text], then [implication or consequence]"

A span is problematic if it:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual

These Output Instructions must strictly followed:
- If spans are present, return one rationale per span, matching their order exactly
- If <SPANS>: ["No"], then return <RATIONALES>: ["No"]
- Do not generate a rationale if <SPANS>: ["No"]
- Each rationale must be wrapped in double quotes ("rationale1", "rationale2", ...)
- All rationales must be returned in a single <RATIONALES> list, matching the order of the spans and separating with a comma(,)
- Do not add ellipses or extra quotes inside the rationale (no "...if" or "...")
- Do not repeat spans or return any explanation outside the output block
- Do not skip or combine spans
- Do not explain your output — only return the formatted result below:

<RATIONALES>: ["if ..., then ...", "if ..., then ...", "..."]

News Excerpt: {instance}

Spans: {spans}

Now return final answer with <RATIONALES> tag, and No explanation"""

rationales_generation_few_shots_en = """You are an expert in discourse framing and media bias. Your task is to explain why certain spans of text in a news excerpt may be misleading, biased, or problematic.

You are given:
1. A news excerpt with:
   - One TITLE line
   - Three SENTENCE lines (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. A list of exact spans extracted from that text.

Your goal is to generate **one rationale for each span**. Use this strict format:
→ "if [reference to the span in the text], then [implication or consequence]"

A span is problematic if it:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual

These Output Instructions must strictly followed:
- If spans are present, return one rationale per span, matching their order exactly
- If <SPANS>: ["No"], then return <RATIONALES>: ["No"]
- Do not generate a rationale if <SPANS>: ["No"]
- Each rationale must be wrapped in double quotes ("rationale1", "rationale2", ...)
- All rationales must be returned in a single <RATIONALES> list, matching the order of the spans and separating with a comma(,)
- Do not add ellipses or extra quotes inside the rationale (no "...if" or "...")
- Do not repeat spans or return any explanation outside the output block
- Do not skip or combine spans
- Do not explain your output — only return the formatted result below:

<RATIONALES>: ["if ..., then ...", "if ..., then ...", "..."]

Example 1 (for reference only — do NOT copy this):
Input:

News Excerpt: None
Spans: [ "" ]

Output:
<RATIONALES>: [ "" ]

Example 2 (for reference only — do NOT copy this):

Input:

News Excerpt: None
Spans: [ "" ]

Output:
<RATIONALES>: [ "" ]


Now process the following input:

News Excerpt: {instance}

Spans: {spans}

Now return final answer with <RATIONALES> tag, and No explanation"""

"SEVERITY LABEL CLASSIFICATION"

ZERO_SHOT_PROMPT = """ You are a framing and language bias expert. Your task is to classify the severity of problematic
language in a news article excerpt. Each excerpt includes a title and up to three sentences.
Classify the severity based on the presence and impact of the following problematic characteristics:

Eventive bias: Describes or refers to events in a way that downplays or distorts responsibility.
Attributive bias: Describes or refers to people using emotionally charged, stereotypical, or exaggerated language.
Sensationalism: Exaggerates or dramatises facts.
Speculation: Uses vague or speculative statements as if they are factual.

SEVERITY LABELS:
“none” – No problematic characteristics are present. The text is factual, balanced, and neutral.
“slightly” – Minor problematic language is present (e.g., a single emotionally charged word or vague phrase),
             but the overall message remains mostly objective.
“moderately” – Multiple instances of bias or misleading language that may affect the reader’s understanding
                or promote subtle distortion.
“highly” – Severe and pervasive use of biased, speculative, or emotionally manipulative language.
           High risk of disinformation, misrepresentation, or harmful framing.

OUTPUT FORMAT:
Only return one of the four labels after the <PREDICTED_LABEL> tag, exactly as shown:
    <PREDICTED_LABEL>: none
    <PREDICTED_LABEL>: slightly
    <PREDICTED_LABEL>: moderately
    <PREDICTED_LABEL>: highly

- Do not add any extra text, explanation, label names, or commentary.
- Do not include anything before or after the double-quoted label.
- Only return one valid output.

Now process the following input: instance
"""

FEW_SHOT_PROMPT = """ You are a framing and language bias expert. Your task is to classify the severity of problematic
language in a news article excerpt. Each excerpt includes a title and up to three sentences.
Classify the severity based on the presence and impact of the following problematic characteristics:

Eventive bias: Describes or refers to events in a way that downplays or distorts responsibility.
Attributive bias: Describes or refers to people using emotionally charged, stereotypical, or exaggerated language.
Sensationalism: Exaggerates or dramatises facts.
Speculation: Uses vague or speculative statements as if they are factual.

SEVERITY LABELS:
“none” – No problematic characteristics are present. The text is factual, balanced, and neutral.
“slightly” – Minor problematic language is present (e.g., a single emotionally charged word or vague phrase),
             but the overall message remains mostly objective.
“moderately” – Multiple instances of bias or misleading language that may affect the reader’s understanding
                or promote subtle distortion.
“highly” – Severe and pervasive use of biased, speculative, or emotionally manipulative language.
           High risk of disinformation, misrepresentation, or harmful framing.

OUTPUT FORMAT:
Only return one of the four labels after the <PREDICTED_LABEL> tag, exactly as shown:
    <PREDICTED_LABEL>: none
    <PREDICTED_LABEL>: slightly
    <PREDICTED_LABEL>: moderately
    <PREDICTED_LABEL>: highly

- Do not add any extra text, explanation, label names, or commentary.
- Do not include anything before or after the double-quoted label.
- Only return one valid output.

Example 1 (for reference only — do NOT copy this): example <PREDICTED_LABEL>: none
Example 2 (for reference only — do NOT copy this): example <PREDICTED_LABEL>: none
Example 3 (for reference only — do NOT copy this): example <PREDICTED_LABEL>: none

Now process the following input: input: instance
"""
