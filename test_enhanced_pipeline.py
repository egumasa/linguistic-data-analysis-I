#!/usr/bin/env python3
"""
Test script for the enhanced Japanese NLP pipeline with UniDic integration.

This script demonstrates the functionality and validates the integration
between GiNZA, fugashi/UniDic, and frequency matching.
"""

import sys
from pathlib import Path
import pandas as pd
from japanese_nlp_enhanced import (
    create_enhanced_japanese_pipeline,
    process_corpus,
    export_frequency_table
)


def create_mock_frequency_data():
    """Create mock CSJ/BCCWJ frequency data for testing."""
    mock_data = [
        ('て', 'テ', '助詞-接続助詞', '', '和', 267358, 35744.1328768),
        ('の', 'ノ', '助詞-格助詞', '', '和', 267155, 35716.9930157),
        ('だ', 'ダ', '助動詞', '', '和', 243097, 32500.585245),
        ('と', 'ト', '助詞-格助詞', '', '和', 231324, 30926.6069973),
        ('に', 'ニ', '助詞-格助詞', '', '和', 207133, 27692.4179384),
        ('日頃', 'ヒゴロ', '名詞-普通名詞', '一般', '和', 1250, 167.2),
        ('本', 'ホン', '名詞-普通名詞', '一般', '和', 8500, 1137.6),
        ('読む', 'ヨム', '動詞-一般', '自立', '和', 3200, 428.3),
        ('好き', 'スキ', '形容動詞-語幹', '', '和', 2100, 281.2),
        ('勉強', 'ベンキョウ', '名詞-普通名詞', '一般', '和', 4200, 562.3),
        ('大切', 'タイセツ', '形容動詞-語幹', '', '和', 1800, 241.0),
        ('思う', 'オモウ', '動詞-一般', '自立', '和', 9500, 1272.0),
        ('東京', 'トウキョウ', '名詞-固有名詞', '地名', '和', 4800, 642.9),
        ('技術', 'ギジュツ', '名詞-普通名詞', '一般', '漢', 3900, 522.3),
        ('進歩', 'シンポ', '名詞-普通名詞', '一般', '漢', 1100, 147.3)
    ]
    
    # Create DataFrame
    df = pd.DataFrame(mock_data, columns=[
        'lemma', 'lForm', 'pos', 'subLemma', 'wType', 'frequency', 'pmw'
    ])
    df['rank'] = range(1, len(df) + 1)
    
    # Save to file
    output_path = "mock_frequency_data.tsv"
    df.to_csv(output_path, sep='\t', index=False)
    print(f"Created mock frequency data: {output_path}")
    return output_path


def test_basic_functionality():
    """Test basic UniDic enrichment without frequency matching."""
    print("\n=== Test 1: Basic UniDic Enrichment ===")
    
    # Create pipeline without frequency matching
    nlp = create_enhanced_japanese_pipeline(add_frequency=False)
    
    # Test text with variant forms and complex morphology
    test_text = "彼は日ごろから本を読むのが好きです。日頃の勉強が大切だと思います。"
    
    print(f"Input text: {test_text}")
    doc = nlp(test_text)
    
    print("\nToken analysis:")
    for token in doc:
        if token._.unidic_entries:
            print(f"\n  Token: '{token.text}' (GiNZA: {token.lemma_} [{token.pos_}])")
            print(f"    UniDic entries: {len(token._.unidic_entries)}")
            for i, entry in enumerate(token._.unidic_entries):
                print(f"      {i+1}. lemma='{entry['lemma']}', lForm='{entry['lForm']}', pos1='{entry['pos1']}'")
                print(f"         subLemma='{entry['subLemma']}', goshu='{entry['goshu']}'")
            
            # Test key generation
            short_keys = token._.short_unit_keys
            long_keys = token._.long_unit_keys
            print(f"    Short-unit keys: {short_keys}")
            print(f"    Long-unit keys: {long_keys}")
    
    return nlp


def test_frequency_matching():
    """Test frequency matching with mock data."""
    print("\n=== Test 2: Frequency Matching ===")
    
    # Create mock frequency data
    freq_file = create_mock_frequency_data()
    
    # Create pipeline with frequency matching
    nlp = create_enhanced_japanese_pipeline(add_frequency=True, frequency_file=freq_file)
    
    # Test texts
    test_texts = [
        "彼は日ごろから本を読むのが好きです。",
        "日頃の勉強が大切だと思います。",
        "東京の技術が進歩している。"
    ]
    
    print("Processing texts with frequency matching:")
    for text in test_texts:
        print(f"\nText: {text}")
        doc = nlp(text)
        
        # Show frequency statistics
        if doc._.frequency_stats:
            stats = doc._.frequency_stats
            print(f"  Coverage: {stats['matched_tokens']}/{stats['total_tokens']} "
                  f"({stats['coverage_percent']:.1f}%)")
        
        # Show tokens with frequency info
        for token in doc:
            if token._.frequency_info:
                freq = token._.frequency_info
                print(f"  '{token.text}': freq={freq['frequency']}, pmw={freq['pmw']:.1f}, rank={freq['rank']}")
    
    # Clean up
    Path(freq_file).unlink()
    return nlp


def test_corpus_processing():
    """Test batch corpus processing."""
    print("\n=== Test 3: Corpus Processing ===")
    
    # Create mock frequency data
    freq_file = create_mock_frequency_data()
    
    # Create pipeline
    nlp = create_enhanced_japanese_pipeline(add_frequency=True, frequency_file=freq_file)
    
    # Create a small corpus
    corpus = [
        "彼は日ごろから本を読むのが好きです。",
        "日頃の勉強が大切だと思います。",
        "東京の技術が進歩している。",
        "機械学習について勉強しています。",
        "この本は本当に面白いと思う。"
    ] * 3  # Repeat to simulate frequency variation
    
    print(f"Processing corpus of {len(corpus)} texts...")
    
    # Process corpus
    frequency_counter, variant_map = process_corpus(corpus, nlp, batch_size=5)
    
    # Show results
    print(f"\nTop 10 most frequent items:")
    for i, (key, count) in enumerate(frequency_counter.most_common(10)):
        lemma, lForm, pos1, subLemma, goshu = key
        print(f"  {i+1:2d}. {lemma} ({lForm}) [{pos1}] - {count} times")
    
    print(f"\nVariant examples:")
    for base_key, variants in list(variant_map.items())[:5]:
        if len(variants) > 1:
            lemma, lForm, pos1 = base_key
            print(f"  {lemma} ({lForm}): {', '.join(variants)}")
    
    # Export frequency table
    total_tokens = sum(frequency_counter.values())
    export_frequency_table(frequency_counter, total_tokens, "test_output_frequency.tsv")
    
    # Clean up
    Path(freq_file).unlink()
    Path("test_output_frequency.tsv").unlink()
    
    return frequency_counter, variant_map


def test_backward_compatibility():
    """Test that English pipelines still work."""
    print("\n=== Test 4: Backward Compatibility ===")
    
    try:
        import spacy
        
        # Test English pipeline (should work normally)
        nlp_en = spacy.load("en_core_web_sm")
        text_en = "This is a test sentence in English."
        doc_en = nlp_en(text_en)
        
        print(f"English text: {text_en}")
        print("English tokens:")
        for token in doc_en:
            print(f"  {token.text} -> {token.lemma_} [{token.pos_}]")
            # UniDic extensions should exist but be empty
            print(f"    unidic_entries: {token._.unidic_entries}")
            print(f"    frequency_info: {token._.frequency_info}")
        
        print("✓ English pipeline works correctly with extensions")
        
    except ImportError:
        print("English model not available - skipping compatibility test")


def test_feature_discovery():
    """Test the feature discovery functionality."""
    print("\n=== Test 5: Feature Discovery ===")
    
    nlp = create_enhanced_japanese_pipeline(add_frequency=False)
    
    # Get the enricher component
    enricher = nlp.get_pipe("unidic_enricher")
    
    if enricher.available:
        features = enricher.discover_features("日本語解析テスト")
        print("Available UniDic features:")
        print(f"  Surface attributes: {features['surface_attrs'][:10]}...")
        print(f"  Feature attributes: {features['feature_attrs']}")
        print(f"  Sample values: {features['sample_values']}")
    else:
        print("UniDic enricher not available")


def run_all_tests():
    """Run all test functions."""
    print("Enhanced Japanese NLP Pipeline Test Suite")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_frequency_matching()
        test_corpus_processing()
        test_backward_compatibility()
        test_feature_discovery()
        
        print("\n" + "=" * 50)
        print("✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
