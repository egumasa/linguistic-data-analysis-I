
# Linguistic Data Analysis I - Web Application for In-Class Tutorials

This document specifies a web application for teaching linguistic data analysis using Python and Streamlit.

## Overview

The web application provides two main features:

1. **Lexical Sophistication Analysis** - Calculates and visualizes lexical sophistication indices
2. **POS and Dependency Parsing** - Performs multilingual part-of-speech tagging and dependency parsing

Each feature supports two modes:
- **Single Text Mode**: Educational mode showing detailed calculation steps
- **Batch Analysis Mode**: Processes multiple text files and returns downloadable results

## Project Structure

```
project/
├── backend/
│   ├── lexical_sophistication.py
│   └── pos_parser.py
├── frontend/
│   └── app.py
└── resources/
    └── reference_lists/
        ├── en/
        └── ja/
```

## Technical Architecture

### Core Requirements

- **Backend Framework**: SpaCy for all NLP processing
- **Frontend Framework**: Streamlit for web interface
- **Separation of Concerns**: Backend modules must not import Streamlit; frontend imports backend modules
- **Languages Supported**: English and Japanese

### State Management

- **Result Caching**: Disabled (do not cache results)
- **Session Data**: Clear on language switch, 10-minute retention
- **SpaCy Models**: 
  - Users select between 'lg' and 'trf' models via dropdown
  - Models are reloaded on selection to minimize memory usage
  - All models pre-installed via requirements.txt

### Performance Requirements

- **Expected Load**: 100 files × 1000 words each
- **Response Time**: 2-3 minutes for batch processing
- **Concurrent Users**: Supported via session isolation
- **Progress Feedback**: 
  - Real-time progress bar during batch processing
  - File counter display (e.g., "Processing file 23/100")

### Deployment

- **Platform**: Hugging Face Spaces
- **Resources**: Free tier (2 vCPU, 16GB RAM)
- **Authentication**: Not required

### Error Handling

#### Batch Processing Errors
- Continue processing remaining files after errors
- Include error placeholder rows in output CSV
- Display error summary after completion
- Make partial results downloadable

#### Reference List Validation
- **Invalid Format**: Show error message and reject the file
- **Duplicate Entries**: Use first occurrence only
- **Case Sensitivity**: Convert to lowercase (except pronouns)

## Feature 1: Lexical Sophistication Analysis

### Definition

Lexical sophistication measures quantify the type of vocabulary used in text through frequency, concreteness, and other psycholinguistic properties. Indices are typically calculated as mean scores across all tokens.

### Processing Pipeline

1. **Tokenization and Parsing**
   - Use SpaCy to tokenize and parse input text
   - Distinguish content words (CW) from function words (FW)
   - Generate unigrams, bigrams, and trigrams

2. **Score Retrieval**
   - Match tokens and lemmas against appropriate reference files:
     - **Unigrams**: Look up token in token file, lemma in lemma file
     - **N-grams**: Look up constructed n-gram in corresponding n-gram file
   - Available reference databases:
     - COCA-Spoken, SUBTLEXus, BNC-Spoken, Brown (frequency/range)
     - MRC Psycholinguistic Database (imageability, concreteness, meaningfulness)
     - Age of Acquisition datasets (e.g., Kuperman et al.)
     - Association strength metrics (MI, MI², T-score, Delta P)
   - Apply log₁₀ transformation when log version is selected
   - For n-gram files with multiple columns, extract specified measure

3. **Score Aggregation**
   - Calculate mean scores across all tokens
   - Generate text-level scores for each index
   - Provide breakdowns by word type (CW/FW) if requested

### Token Processing Rules

#### N-gram Generation
- **Single words**: Process through standard tokenization
- **Multi-word expressions**: Join with underscore (e.g., "is_to", "to_what_extent")
- **Bigrams/Trigrams**: Generate with overlap (e.g., "I saw him" → "I_saw", "saw_him")
- **Punctuation**: Exclude from n-grams
- **Sentence boundaries**: N-grams must not cross sentences
  - ❌ Invalid: "Hello_world", "world_How" (crosses sentence boundary)
  - ✅ Valid: "Hello_world", "How_are", "are_you"

#### POS Classification
- **Content Words (CW)**: NOUN, VERB, ADJ, ADV
- **Function Words (FW)**: DET, PRON, ADP, CONJ
- Classification configurable via SpaCy's `tag_` or `pos_` attributes

### Input Configuration

#### Text Input
- **Single Text Mode**: Upload individual .txt file
- **Batch Mode**: Upload folder or .zip containing multiple .txt files
- **Languages**: English, Japanese

#### Reference Vocabulary Lists

**Resource Types and File Formats**

1. **Unigram Resources** (require two separate files per index)
   - **Token file**: Scores for surface forms before lemmatization
     - Column A: Token (e.g., "running", "saw")
     - Column B: Score (frequency, concreteness, etc.)
   - **Lemma file**: Scores for lemmatized forms
     - Column A: Lemma (e.g., "run", "see")
     - Column B: Score
   - File naming: `indexname_token.csv`, `indexname_lemma.csv`

2. **N-gram Resources** (single file per n-gram type)
   - **Bigram/Trigram files**: 
     - Column A: N-gram with underscore separator (e.g., "in_the", "how_are_you")
     - Column B+: Multiple score columns allowed
       - Frequency of word1
       - Frequency of word2 (and word3 for trigrams)
       - N-gram frequency
       - N-gram range
       - Association measures (T-score, MI, Delta P, etc.)
   - File naming: `indexname_bigram.csv`, `indexname_trigram.csv`
   - Note: Same file used for both token and lemma matching

**General Format Rules**
- CSV or TSV format accepted
- Missing words marked as "NA" in output (excluded from calculations)
- Reference lists cannot be downloaded or viewed by users
- First row should contain column headers

**File Naming Convention Examples**

For an index called "COCA_spoken":
- `COCA_spoken_token.csv` - Unigram token scores
- `COCA_spoken_lemma.csv` - Unigram lemma scores  
- `COCA_spoken_bigram.csv` - Bigram scores (multi-column)
- `COCA_spoken_trigram.csv` - Trigram scores (multi-column)

For user uploads, the system extracts base name:
- Upload: `MyCorpus_token.csv` → Index name: "MyCorpus"
- Upload: `academic_words_lemma.csv` → Index name: "academic_words"

**English Configuration**
- Default lists: Two placeholder checkboxes ("Index 1", "Index 2")
- Custom lists: File upload option
  - System automatically groups files with same base name
  - User selects which indices to apply to the text

**Japanese Configuration**
- File upload only (no default lists)
- Same file structure and naming conventions as English
- Extensible design for future additions



### Output Modes

#### Single Text Mode (Educational)

Displays three components to help users understand calculations:

1. **Summary Results**
   - Final text-level scores for each selected index

2. **Diagnostic Table**
   - Detailed token-by-token breakdown
   - Columns dynamically generated based on selected indices
   
   Example with multiple indices selected:
   | id | token | lemma | COCA_freq_token | COCA_freq_lemma | BNC_concrete_token | BNC_concrete_lemma |
   |---|---|---|---|---|---|---|
   | 1 | I | i | 1030 | 1030 | NA | NA |
   | 2 | saw | see | 440 | 602 | 3.5 | 3.2 |
   | 3 | that | that | 890 | 890 | 1.2 | 1.2 |
   
   Note: Column headers follow pattern: `IndexName_measure_type` where type is either "token" or "lemma"

3. **Density Plot**
   - One plot per index showing score distribution
   - X-axis: Lexical sophistication score
   - Y-axis: Density
   - Interactive Plotly visualization (ggplot-style)
   - Plot function exposed in source code for customization

#### Batch Mode

Processes multiple files and returns aggregated results:

- **Input**: Folder or .zip file containing .txt files
- **Output**: Downloadable CSV with text-level scores

**CSV Output Column Naming:**
- Unigram indices: `IndexName_wordtype[_log]`
  - Example: `COCA_freq_CW`, `COCA_freq_CW_log`, `COCA_freq_FW`
- N-gram indices: `IndexName_ngramtype_measure`
  - Example: `COCA_bigram_MI`, `COCA_bigram_Tscore`, `COCA_trigram_freq`

**CSV Format Example:**
```csv
filename,COCA_freq_CW,COCA_freq_CW_log,COCA_freq_FW,COCA_freq_FW_log,COCA_bigram_MI,COCA_bigram_Tscore,BNC_concrete_CW
text1.txt,4.52,1.65,5.23,1.72,3.45,2.89,3.12
text2.txt,4.13,1.61,5.01,1.70,3.22,2.75,2.98
```

Note: The system automatically generates appropriate column names based on:
- Index name (from filename base)
- Word type (CW/FW for unigrams)
- Measure type (for n-grams with multiple columns)
- Transform applied (e.g., _log suffix)



## Feature 2: POS and Dependency Parser

Uses SpaCy for multilingual part-of-speech tagging and dependency parsing.

### Supported Languages
- English
- Japanese

### Input Options
- **Single Text**: Individual .txt file
- **Batch Processing**: Folder or .zip file

### Output Formats

#### Single Text Mode

1. **Token Analysis Table**
   | Token | Lemma | POS | Tag | Dependency | Named Entity |
   |-------|-------|-----|-----|------------|--------------|
   | The | the | DET | DT | det | - |
   | cat | cat | NOUN | NN | nsubj | - |
   | sat | sit | VERB | VBD | ROOT | - |

2. **DisplaCy Visualization**
   - Process text sentence by sentence
   - For each sentence, display:
     - Original text
     - Dependency arcs with POS tags (using `tag_` not `pos_`)
   - Static image output
   - Maximum 30 words per sentence

#### Batch Mode

- **Output**: Downloadable .zip file
- **Format**: One TSV file per input text
- **Columns**: Token, Lemma, POS, Tag, Dependency, Named Entity

## User Interface Specifications

### File Upload Constraints
- **Maximum Size**: 100 MB per upload
- **Accepted Formats**: .txt files only
- **Text Encoding**: UTF-8 or UTF-16
- **Zip File Handling**: Skip non-text files silently

### Navigation Flow

1. **Main Navigation**
   - Sidebar with tool selection (Lexical Sophistication | POS Parser)

2. **Language Selection**
   - Display warning before switching languages
   - Clear all inputs/outputs on language change

3. **Reference List Interface (English)**
   - Placeholder names: "Index 1", "Index 2"
   - Multiple selection allowed via checkboxes

4. **File Upload Interface**
   - Display total file count
   - Show estimated processing time
   - No individual file removal after upload

### Output Specifications

#### Download Options
- All results downloadable as CSV/TSV/ZIP
- Include filename column in all outputs
- Display clear error messages for debugging

#### Session Management
- **Data Retention**: 10 minutes
- **Language Switch**: Clears all session data
- **Progress Display**: Real-time updates during processing
