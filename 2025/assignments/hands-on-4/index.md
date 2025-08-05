---
title: "Corpus Lab 4"
subtitle: "Analyzing grammatical features"
---


# Assignment Overview

This assignment aims to help you practice the following skills:

- extracting fine-grained grammatical features from either a Japanese or an English corpus.
- writing a short report describing the results and interpretation of the analysis results.


# Assignment Details

We have three tasks that builds on top of each other.

## Task 1: Research questions, Hypotheses and Methods

In this task you will describe research questions, hypothesis, and methods.

### Research questions

- Research questions should include:
  - type of features you are looking at (e.g., adverbial clauses)
  - situational variables that defines your sub-corpora (e.g., grade, genre, proficiency)

### Hypothesis

- Your research hypothesis should:
  - describe your predictions in terms of:
    - quantitative trends of the feature in relation to the factor you are interested in.

### Definitions and operationalization of grammatical features to extract 

- You must describe the specific grammatical features that you plan to extract.
- For example, for clausal features you need to specify if you are interested in :
  - subordinate clauses or embedded clauses
  - particular type of clauses

- Description of rules to identify desirable linguistic feature.
  - For example, you will need to specify `amod` for dependency label to extract `adjective + noun` phrase.


## Task 2: Fine-grained Descriptive grammatical features

- Once you articulated the information above, you will now conduct a search over the corpus.

- You should use either [simple text analyzer](https://huggingface.co/spaces/egumasa/simple-text-analyzer) or your own Colab Notebook.
  - I will specify which option should be used **by the time we start working on this assignment** (that is, this depends on your progress as a group.)


## Task 3: Results and interpretation

- Provide the results of your corpus analysis in a way you think is most effective to address your research questions. Make effective use of tables, plots, or other data presentation technique as you think.
- Provide descriptive paragraphs to walk the reader through the results and how to interprete that results.



::: {.callout-note}
## Submission

- A word file (`.docx` file) that addresses requirements in a written format (one or two pages depending on your analysis results.).
  - Screenshots of your search settings on the [simple text analyzer](https://huggingface.co/spaces/egumasa/simple-text-analyzer) tool.
- **IF you use colab**, Google Colab notebook (`.ipynb` file) with extraction code and results.

:::

::: {.callout-important}
# Success Criteria

Your submission ...

- [ ] outlines research questions and hypotheses
- [ ] selected syntactic feature and why you think that distinguishes the proficiency score
- [ ] provide description of your approach (algorithms and rules) to identify the desired linguistic structure.
- [ ] provides scatter plot examining the relationships and their interpretations in relation to the research questions

:::
