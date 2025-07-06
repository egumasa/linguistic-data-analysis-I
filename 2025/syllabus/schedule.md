---
title: "Course Schedule"
subtitle: "Detailed Daily Schedule and Session Topics"
toc: true
toc-depth: 3
---

## Overview

This intensive course meets for 5 days with 3 sessions per day.

## Course Schedule

This course covers foundational concepts in corpus linguistics, corpus analysis methods, and their research applications across the following four areas: vocabulary, multiword units, and grammar.

### Day1–Session 1: Introduction to corpus linguistics and learner corpus research (1)

**Objectives:**
By the end of this session, students will be able to:
- Define corpus linguistics as an empirical methodology
- Explain key limitations of introspection in linguistic research
- Describe the role of frequency data and patterns in corpus analysis
- Identify and explain the basic steps in corpus-based research
- Reflect on their own stance toward data, intuition, and linguistic evidence

Concepts covered:
- Corpus linguistics
- Balanced Corpus, Reference Corpus, Learner Corpus
- Corpus representativeness

Required Readings: 
- Stefanowitsch (2020) Ch. 1.
- Stefanowitsch (2020) Ch. 2.
- Skim Durrant (2023) Ch. 1.

### Day1–Session 2: Overview of corpus linguistic methods

#### **Objectives:**
By the end of this session, students will be able to:
- Explain how corpus linguistic approach is used in investigating the learner language development.
- Describe key methods to examine corpus data qualitatively.
- Explain different types of corpus linguistic analysis for different focus: frequency analysis, concordance analysis, collocation analysis, Part-Of-Speech Tagging, etc.

#### Concepts covered:
- Conceptual Overview of the corpus linguistic methods
- Tokenization
- Tagging and Parsing

#### Optional Readings:
- Davies (2015)

#### Notes:
- Needs analysis (After giving overview) is conducted at the end of this session.

### Day1–Session 3: Conducting the first corpus search!

**Objectives:**
By the end of this session, students will be able to:
- Conduct the KWIC search based on chosen corpus
- Run frequency analysis on a Web Corpus

#### Concepts covered:
- Key Words In Context (KWIC)
- Counting unit: Token, lemma, type

#### Tools used:
- BYU corpora

#### First mini assignment:
- Conduct KWIC search and make some observation on how a word is used.

### Day2–Session 4: Analyzing vocabulary (1) — Conceptual overview

**Objectives:**
By the end of this session, students will be able to:
- Understand historical overview of lexical richness measurement.
- Articulate definitions and examples of commonly used lexical measures.
- Explain how lexical measures are normally calculated.

#### Concepts covered:
- Lexical sophistication
- Lexical diversity

#### Reading: 
- Durrant Ch. 3.
- Skim Durrant Ch. 4. (Ignore R codes if you are not familiar.)

### Day2–Session 5: Analyzing vocabulary (2) — Hands-on activity 1

#### **Objectives:**
By the end of this session, students will be able to:
- Compute frequency of a single-word lexical item in reference corpora.
- Use AntConc/Web corpus to extract frequency data from a small corpus.
- Conduct lexical profiles using LexTutor and/or AntWordProfiler.

#### Concepts covered:
- Generating frequency lists based on reference corpora.
- Conduct lexical profiling

#### Tools used:
- AntConc
- BYU corpora

#### Optional Reading:
- Davies (2015)

### Day2–Session 6: Analyzing vocabulary (3) — Hands-on activity 2

#### **Objectives:**
By the end of this session, students will be able to:
- Examine differences between two or more groups of texts by computing a selected set of lexical richness indices
- Calculate lexical diversity measures using a spreadsheet software.
- Calculate simple lexical sophistication measures using dedicated web application.

#### Concepts covered:
- lexical diversity
- lexical sophistication
- learner corpus research

#### Reading:
- Eguchi & Kyle (2020).


### Day3–Session 7: Analyzing multiword units (1) — Conceptual overview

**Objectives:**
By the end of this session, students will be able to:
- Explain different types of multiword units: collocation, n-grams, lexical bundles.
- Demonstrate how major association strengths measures (t-score, Mutual Information, and LogDice) are calculated using examples.

#### Concepts covered:
- Types of multiword units
- Association strengths
- Three approaches:
    - Context window
    - Dependency bigram

#### Reading: 
- Durrant (2023) Ch. 7.
- Skim Durrant (2023) Ch. 8. (Ignore R codes if you are not familiar.)


### Day3–Session 8: Analyzing multiword units (2) — Hands-on activity

**Objectives:**
By the end of this session, students will be able to:
- Search for window-based collocations and n-grams in AntConc and/or BNC/COCA.
- Calculate commonly used strengths of association measures by hand using spreadsheet software.
- Discuss benefits and drawbacks of different strength of association measures.

#### Concepts covered:
- n-gram search
- Strengths of Association measures — T-score, Mutual Information, LogDice

#### Reading:
- Gablasova et al (2017)

### Day3–Session 9: Research Application — Lexical measures & In-class mini-project (1)

**Objectives:**
By the end of this session, students will be able to:
- Conduct a simple statistical analysis of selected corpus on small sets of lexical measures using JASP software.
- Articulate their mini-project research topic in group.
- Articulate their research questions and hypotheses in a 3-minute brief presentation.

#### Concepts covered:
- Linear regression analysis (group comparison or prediction)
- Introduction to in-class mini-project


### Day4–Session 10: Analyzing grammar (1) — Conceptual overview

**Objectives:**
By the end of this session, students will be able to:
- Understand different approaches to grammatical features.
    - Grammatical complexity research
    - Descriptive approaches
- Understand historical overview of the syntactic complexity research.
- Understand NLP tasks such as POS tagging and dependency parsing.
- Understand how automated parsing works.
- Understand current trends of syntactic complexity research.

#### Reading:
- Durrant Ch 5.
- Biber, D., Gray, B., Staples, S., & Egbert, J. (2020). Investigating grammatical complexity in L2 English writing research: Linguistic description versus predictive measurement. Journal of English for Academic Purposes, 46, 100869. https://doi.org/10.1016/j.jeap.2020.100869

### Day4–Session 11: Analyzing grammar (2) — Hands-on activity

**Objectives:**
By the end of this session, students will be able to:
- Conduct POS tagging with spaCy library in Python (through Google Colab).
- Conduct Dependency parsing with spaCy library in Python (through Google Colab).
- Conduct simple collostructional analysis.

*Note ^1*: All the python codes are prepared by the instructor and shared with the students. This session does not require ability to code.

*Note ^2*: The decision to use Python programming language rather than already available software is based on consideration that there is very little tools which provide stable access to the language analysis described here.

#### Concepts covered:
- POS tagging
- Dependency parsing

#### Reading:
- Skim Durrant Ch 6. (Ignore R codes if you are not familiar.)
- Skim Kyle & Eguchi (2023) 

### Day4–Session 12: Analyzing grammar (3) — Hands-on activity 

**Objectives:**
By the end of this session, students will be able to:
- Conduct linguistic complexity analysis using available tools such as TAASSC.

#### Readings:
- Kyle et al. (2021). _ETS Research Report Series._


### Day5–Session 13: Using Large Language Models (LLMs) for linguistic annotation

**Objectives:**
By the end of this session, students will be able to:
- Describe what LLMs are and how they are trained.
- Describe the current applications of LLMs in applied linguistic research.
- Provide definition of analysis tasks for LLMs supported linguistic analysis.
- Write a structured prompt to control LLM behavior.

#### Readings:
- Mizumoto (2025)
- Mizumoto et al. (2024) 

### Day5–Session 14:  In-class mini-project (2)

- Group project time.
- Please use the time wisely.


### Day5–Session 15: In-class mini-project (3) & Wrap-up

- Final presentation on group project


**Final Project**: [Guidelines](../assignments/final-project/) - Due 2 weeks after course

## Important Notes

- All times are Japan Standard Time (JST)
- Bring your laptop to all sessions
- Complete readings before each day (see [Readings](readings))
