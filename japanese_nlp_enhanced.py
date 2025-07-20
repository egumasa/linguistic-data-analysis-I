"""
Enhanced Japanese NLP Pipeline with UniDic Integration

This module provides spaCy components for integrating fugashi/UniDic morphological 
analysis with GiNZA, enabling frequency analysis using CSJ/BCCWJ frequency data.
"""

import warnings
from typing import List, Dict, Tuple, Optional, Any, Set
from collections import Counter, defaultdict
import pandas as pd
import spacy
from spacy.language import Language
from spacy.tokens import Token, Doc
import fugashi
import unidic


# Register token extensions (global, but only populated for Japanese)
if not Token.has_extension("unidic_entries"):
    Token.set_extension("unidic_entries", default=[])
if not Token.has_extension("frequency_info"):
    Token.set_extension("frequency_info", default=None)
if not Token.has_extension("short_unit_keys"):
    Token.set_extension("short_unit_keys", getter=lambda t: get_short_unit_keys(t))
if not Token.has_extension("long_unit_keys"):
    Token.set_extension("long_unit_keys", getter=lambda t: get_long_unit_keys(t))

# Register doc extensions
if not Doc.has_extension("frequency_stats"):
    Doc.set_extension("frequency_stats", default=None)
if not Doc.has_extension("variant_map"):
    Doc.set_extension("variant_map", default={})


def get_short_unit_keys(token: Token) -> List[Tuple[str, str, str, str, str]]:
    """Generate short-unit frequency keys (lemma, lForm, pos1, subLemma, goshu)."""
    keys = []
    for entry in token._.unidic_entries:
        key = (
            entry.get('lemma', ''),
            entry.get('lForm', ''),
            entry.get('pos1', ''),
            entry.get('subLemma', ''),
            entry.get('goshu', '')
        )
        keys.append(key)
    return keys


def get_long_unit_keys(token: Token) -> List[Tuple[str, str, str, str]]:
    """Generate long-unit frequency keys (lemma, lForm, pos1, goshu) - without subLemma."""
    keys = []
    for entry in token._.unidic_entries:
        key = (
            entry.get('lemma', ''),
            entry.get('lForm', ''),
            entry.get('pos1', ''),
            entry.get('goshu', '')
        )
        keys.append(key)
    return keys


class UnidicEnricher:
    """
    spaCy component that enriches tokens with UniDic morphological features.
    
    This component runs after GiNZA's parser and aligns fugashi/UniDic tokens
    with spaCy tokens using character offset matching.
    """
    
    def __init__(self, nlp: Language, name: str = "unidic_enricher"):
        """
        Initialize the UniDic enricher.
        
        Args:
            nlp: spaCy Language object
            name: Component name
        """
        self.nlp = nlp
        self.name = name
        self.sublemma_source = "pos2"  # Default configuration
        self.tagger = None
        self.available = False
        
        # Only initialize for Japanese
        if nlp.lang == "ja":
            try:
                self.tagger = fugashi.Tagger(f'-d "{unidic.DICDIR}"')
                self.available = True
                print(f"UniDic enricher initialized with dictionary: {unidic.DICDIR}")
            except Exception as e:
                warnings.warn(f"Failed to initialize UniDic: {e}")
                self.available = False
        else:
            # For non-Japanese languages, component does nothing
            self.available = False
    
    def __call__(self, doc: Doc) -> Doc:
        """Process document and enrich tokens with UniDic features."""
        # Skip processing for non-Japanese or if UniDic unavailable
        if not self.available or doc.lang_ != "ja":
            return doc
        
        # Build character offset map for spaCy tokens
        start_map = {tok.idx: tok for tok in doc}
        
        # Track processed spans to avoid duplicates
        processed = set()
        
        # Process text with fugashi/UniDic
        cursor = 0
        for unidic_token in self.tagger(doc.text):
            surface = unidic_token.surface
            if not surface.strip():  # Skip empty tokens
                continue
            
            # Find character position in text
            start = doc.text.find(surface, cursor)
            if start < 0:
                continue
            
            cursor = start + len(surface)
            
            # Align with spaCy token
            spacy_token = self._align_token(unidic_token, start_map, start, doc)
            if spacy_token:
                # Check for duplicates
                span_key = (start, start + len(surface))
                entry = self._extract_unidic_entry(unidic_token)
                dup_key = (span_key, entry.get('lemma', ''))
                
                if dup_key not in processed:
                    spacy_token._.unidic_entries.append(entry)
                    processed.add(dup_key)
        
        return doc
    
    def _align_token(self, unidic_token, start_map: Dict[int, Token], 
                     start: int, doc: Doc) -> Optional[Token]:
        """Align UniDic token with spaCy token using character offsets."""
        surface = unidic_token.surface
        
        # Primary: exact start position match
        if start in start_map:
            return start_map[start]
        
        # Fallback: containment-based matching
        end = start + len(surface)
        for idx, spacy_token in start_map.items():
            token_end = idx + len(spacy_token.text)
            # Check if UniDic token is contained within spaCy token
            if idx <= start < token_end and end <= token_end:
                return spacy_token
        
        return None
    
    def _extract_unidic_entry(self, token) -> Dict[str, Any]:
        """Extract UniDic features using named attributes with fallbacks."""
        feature = token.feature
        
        # Choose subLemma source based on configuration
        sublemma = ""
        if self.sublemma_source == "pos2":
            sublemma = getattr(feature, 'pos2', '')
        elif self.sublemma_source == "pos3":
            sublemma = getattr(feature, 'pos3', '')
        else:
            # Fallback to pos2, then pos3
            sublemma = getattr(feature, 'pos2', '') or getattr(feature, 'pos3', '')
        
        return {
            "surface": token.surface,
            "lemma": getattr(feature, 'lemma', token.surface),
            "lForm": getattr(feature, 'lForm', ''),  # reading/pronunciation
            "pos1": getattr(feature, 'pos1', '未知語'),
            "pos2": getattr(feature, 'pos2', ''),
            "pos3": getattr(feature, 'pos3', ''),
            "pos4": getattr(feature, 'pos4', ''),
            "subLemma": sublemma,
            "goshu": getattr(feature, 'goshu', ''),  # word type
            "orth": getattr(feature, 'orth', token.surface),
            "orthBase": getattr(feature, 'orthBase', ''),
            "cType": getattr(feature, 'cType', ''),  # conjugation type
            "cForm": getattr(feature, 'cForm', ''),  # conjugation form
            # Additional useful fields for CSJ/BCCWJ matching
            "pronunciation": getattr(feature, 'pron', ''),
            "kana": getattr(feature, 'kana', ''),
            "kanaBase": getattr(feature, 'kanaBase', '')
        }
    
    def discover_features(self, sample_text: str = "日本語") -> Dict[str, Any]:
        """Discover available UniDic feature attributes for debugging."""
        if not self.available:
            return {"error": "UniDic not available"}
        
        token = next(iter(self.tagger(sample_text)))
        feature_attrs = [attr for attr in dir(token.feature) if not attr.startswith('_')]
        
        return {
            'surface_attrs': [attr for attr in dir(token) if not attr.startswith('_')],
            'feature_attrs': feature_attrs,
            'sample_values': {attr: getattr(token.feature, attr, 'N/A') for attr in feature_attrs[:15]}
        }


@Language.factory("unidic_enricher")
def create_unidic_enricher(nlp: Language, name: str):
    """Factory function for creating UnidicEnricher component."""
    return UnidicEnricher(nlp, name)


class FrequencyMatcher:
    """
    spaCy component that matches tokens with frequency data from CSJ/BCCWJ.
    
    This component should run after the UnidicEnricher to access unidic_entries.
    """
    
    def __init__(self, nlp: Language, name: str = "frequency_matcher"):
        """
        Initialize the frequency matcher.
        
        Args:
            nlp: spaCy Language object
            name: Component name
        """
        self.nlp = nlp
        self.name = name
        self.frequency_data = {}
        self.variant_map = defaultdict(set)
        self.pos_exclusions = {'記号', '補助記号', '空白'}
        self.frequency_file = None
    
    def set_frequency_file(self, frequency_file: str):
        """Set the frequency file and load data."""
        self.frequency_file = frequency_file
        if frequency_file:
            self.load_frequency_data(frequency_file)
    
    def load_frequency_data(self, file_path: str) -> None:
        """Load CSJ/BCCWJ frequency data from TSV file."""
        try:
            df = pd.read_csv(file_path, sep='\t')
            print(f"Loading frequency data from {file_path}")
            print(f"Columns: {list(df.columns)}")
            
            # Assume the format matches your provided sample:
            # rank, lForm, lemma, pos, subLemma, wType, frequency, pmw, ...
            for _, row in df.iterrows():
                # Create lookup key (lemma, lForm, pos)
                key = (str(row['lemma']), str(row['lForm']), str(row['pos']))
                
                self.frequency_data[key] = {
                    'frequency': row['frequency'],
                    'pmw': row['pmw'],
                    'rank': row['rank'],
                    'subLemma': row.get('subLemma', ''),
                    'wType': row.get('wType', ''),
                    'goshu': row.get('wType', '')  # Assuming wType is goshu
                }
            
            print(f"Loaded {len(self.frequency_data)} frequency entries")
            
        except Exception as e:
            warnings.warn(f"Failed to load frequency data: {e}")
    
    def __call__(self, doc: Doc) -> Doc:
        """Process document and attach frequency information to tokens."""
        if not self.frequency_data:
            return doc
        
        # Process each token
        total_tokens = 0
        matched_tokens = 0
        variant_map = defaultdict(set)
        
        for token in doc:
            if not token._.unidic_entries:
                continue
            
            # Look up frequency for each UniDic entry
            freq_matches = []
            for entry in token._.unidic_entries:
                # Skip excluded POS categories
                if entry.get('pos1', '') in self.pos_exclusions:
                    continue
                
                total_tokens += 1
                
                # Create lookup key
                key = (entry['lemma'], entry['lForm'], entry['pos1'])
                
                if key in self.frequency_data:
                    freq_info = self.frequency_data[key].copy()
                    freq_info['unidic_entry'] = entry
                    freq_matches.append(freq_info)
                    matched_tokens += 1
                
                # Track variants
                base_key = (entry['lemma'], entry['lForm'], entry['pos1'])
                variant_map[base_key].add(entry['orth'])
            
            # Attach best frequency match (highest frequency if multiple)
            if freq_matches:
                token._.frequency_info = max(freq_matches, key=lambda x: x['frequency'])
        
        # Store document-level statistics
        coverage = (matched_tokens / total_tokens * 100) if total_tokens > 0 else 0
        doc._.frequency_stats = {
            'total_tokens': total_tokens,
            'matched_tokens': matched_tokens,
            'coverage_percent': coverage
        }
        doc._.variant_map = dict(variant_map)
        
        return doc


@Language.factory("frequency_matcher")
def create_frequency_matcher(nlp: Language, name: str):
    """Factory function for creating FrequencyMatcher component."""
    return FrequencyMatcher(nlp, name)


def create_enhanced_japanese_pipeline(add_frequency: bool = True, 
                                    frequency_file: Optional[str] = None,
                                    sublemma_source: str = "pos2") -> Language:
    """
    Factory function to create a Japanese pipeline with UniDic enrichment.
    
    Args:
        add_frequency: Whether to add frequency matching component
        frequency_file: Path to CSJ/BCCWJ frequency data
        sublemma_source: Which POS field to use for subLemma
    
    Returns:
        Enhanced spaCy Language pipeline
    """
    # Load base GiNZA pipeline
    nlp = spacy.load("ja_ginza")
    
    # Add UniDic enricher after parser
    nlp.add_pipe("unidic_enricher", after="parser")
    
    # Configure the enricher
    enricher = nlp.get_pipe("unidic_enricher")
    enricher.sublemma_source = sublemma_source
    
    # Add frequency matcher if requested
    if add_frequency:
        nlp.add_pipe("frequency_matcher", after="unidic_enricher")
        freq_matcher = nlp.get_pipe("frequency_matcher")
        if frequency_file:
            freq_matcher.set_frequency_file(frequency_file)
    
    return nlp


def process_corpus(texts: List[str], nlp: Language, batch_size: int = 100) -> Tuple[Counter, Dict]:
    """
    Process multiple texts efficiently and collect frequency statistics.
    
    Args:
        texts: List of texts to process
        nlp: Enhanced Japanese pipeline
        batch_size: Number of texts to process per batch
    
    Returns:
        Tuple of (frequency_counter, variant_map)
    """
    frequency_counter = Counter()
    variant_collector = defaultdict(set)
    
    print(f"Processing {len(texts)} texts in batches of {batch_size}")
    
    # Process in batches
    for i, doc in enumerate(nlp.pipe(texts, batch_size=batch_size)):
        if i % 100 == 0:
            print(f"Processed {i}/{len(texts)} texts")
        
        # Collect short-unit frequencies
        for token in doc:
            for key in token._.short_unit_keys:
                if key[0]:  # Only count if lemma is not empty
                    frequency_counter[key] += 1
            
            # Collect variants
            for entry in token._.unidic_entries:
                base_key = (entry['lemma'], entry['lForm'], entry['pos1'])
                variant_collector[base_key].add(entry['orth'])
    
    return frequency_counter, dict(variant_collector)


def export_frequency_table(counter: Counter, total_tokens: int, output_path: str) -> None:
    """
    Export frequency analysis to TSV format compatible with CSJ format.
    
    Args:
        counter: Frequency counter for (lemma, lForm, pos1, subLemma, goshu) tuples
        total_tokens: Total number of tokens for PMW calculation
        output_path: Output file path
    """
    rows = []
    for rank, ((lemma, lForm, pos1, subLemma, goshu), count) in enumerate(counter.most_common(), 1):
        pmw = (count / total_tokens) * 1000000  # per million words
        rows.append({
            'rank': rank,
            'lForm': lForm,
            'lemma': lemma,
            'pos': pos1,
            'subLemma': subLemma,
            'wType': goshu,
            'frequency': count,
            'pmw': pmw
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, sep='\t', index=False)
    print(f"Exported {len(rows)} frequency entries to {output_path}")


def demo_enhanced_pipeline():
    """Demonstrate the enhanced Japanese pipeline functionality."""
    print("=== Enhanced Japanese NLP Pipeline Demo ===")
    
    # Create enhanced pipeline
    nlp = create_enhanced_japanese_pipeline(add_frequency=False)  # No frequency file for demo
    
    # Test texts with various phenomena
    test_texts = [
        "彼は日ごろから本を読むのが好きです。",
        "日頃の勉強が大切だと思います。",
        "東京オリンピックについて話しましょう。",
        "機械学習の技術が進歩している。"
    ]
    
    for text in test_texts:
        print(f"\nAnalyzing: {text}")
        doc = nlp(text)
        
        for token in doc:
            if token._.unidic_entries:
                print(f"  {token.text}")
                print(f"    GiNZA: {token.lemma_} [{token.pos_}]")
                print(f"    UniDic entries: {len(token._.unidic_entries)}")
                for entry in token._.unidic_entries:
                    print(f"      - {entry['lemma']} ({entry['lForm']}) [{entry['pos1']}]")
                print(f"    Short-unit keys: {token._.short_unit_keys}")
    
    return nlp


if __name__ == "__main__":
    demo_enhanced_pipeline()
