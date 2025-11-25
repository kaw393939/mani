import pandas as pd
import re
import os

def load_taxonomy(filepath):
    """
    Loads the taxonomy CSV and creates a dictionary of keywords for each class.
    """
    # Read the file, skipping initial header rows if necessary, but pandas usually handles it if we inspect
    # Based on previous `read_file`, the header is effectively on line 3 (0-indexed), but let's read all and filter.
    df = pd.read_csv(filepath, header=None)
    
    taxonomy = {}
    
    # Iterate through rows
    for index, row in df.iterrows():
        # Column 1 is Class Code, Column 2 is Major Class, Column 3 is Sub Class
        try:
            code = row[1]
            major_class = str(row[2]) if pd.notna(row[2]) else ""
            sub_class = str(row[3]) if pd.notna(row[3]) else ""
            
            # Check if code is a number (it's read as float or string usually)
            # We want 2 digit codes like 11, 40.
            if pd.isna(code):
                continue
                
            try:
                code_int = int(float(code))
                if code_int < 10 or code_int > 99: # Basic validation for 2 digit codes
                    continue
            except ValueError:
                continue
                
            full_desc = f"{major_class} - {sub_class}"
            
            # Generate keywords from the description
            # Combine major and sub class for keywords
            text_for_keywords = f"{major_class} {sub_class}"
            
            # Simple keyword extraction: split by non-alphanumeric, lowercase, remove short words
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text_for_keywords.lower())
            
            # Add some specific manual keywords if needed, or just rely on the description
            # For now, we rely on the description words.
            # We can weight them? No, simple count for now.
            
            taxonomy[code_int] = {
                'desc': full_desc,
                'keywords': set(words)
            }
            
        except Exception as e:
            continue
            
    return taxonomy

def score_abstract(abstract, taxonomy):
    """
    Scores an abstract against all taxonomy classes.
    Returns a sorted list of (code, score) tuples.
    """
    if pd.isna(abstract):
        return []
    
    abstract_lower = str(abstract).lower()
    scores = []
    
    for code, data in taxonomy.items():
        score = 0
        keywords = data['keywords']
        
        for word in keywords:
            # Simple word matching
            if word in abstract_lower:
                score += 1
                # Boost for exact phrase matching if we had phrases, but we have words.
                # We could count frequency:
                score += abstract_lower.count(word) * 0.5
        
        if score > 0:
            scores.append((code, score))
            
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def classify_papers():
    # File paths
    taxonomy_path = 'data/processed/KW_CLASSIFICATION_OF_FERROFLUIDS_LITERATURE/Sheet1.csv'
    papers_path = 'data/processed/KW_PAPERS_scopus (1)/KW_PAPERS_scopus 1.csv'
    output_path = 'data/processed/classified_papers.csv'
    
    print("Loading taxonomy...")
    taxonomy = load_taxonomy(taxonomy_path)
    print(f"Loaded {len(taxonomy)} classification codes.")
    
    print("Loading papers...")
    try:
        papers_df = pd.read_csv(papers_path)
    except Exception as e:
        print(f"Error reading papers file: {e}")
        return

    print(f"Processing {len(papers_df)} papers...")
    
    results = []
    
    for index, row in papers_df.iterrows():
        doi = row.get('DOI', '')
        title = row.get('Title', 'No Title')
        year = row.get('Year', '')
        abstract = row.get('Abstract', '')
        
        # Score the abstract
        scores = score_abstract(abstract, taxonomy)
        
        # Get top 3
        primary = scores[0] if len(scores) > 0 else (None, 0)
        secondary = scores[1] if len(scores) > 1 else (None, 0)
        tertiary = scores[2] if len(scores) > 2 else (None, 0)
        
        # Prepare result row
        result_row = {
            'DOI': doi,
            'Year': year,
            'Title': title,
            'Primary_Class': primary[0] if primary[0] else '',
            'Primary_Desc': taxonomy[primary[0]]['desc'] if primary[0] else '',
            'Secondary_Class': secondary[0] if secondary[0] else '',
            'Secondary_Desc': taxonomy[secondary[0]]['desc'] if secondary[0] else '',
            'Tertiary_Class': tertiary[0] if tertiary[0] else '',
            'Tertiary_Desc': taxonomy[tertiary[0]]['desc'] if tertiary[0] else '',
            'Confidence_Score': round(primary[1], 2),
            'Abstract': abstract
        }
        results.append(result_row)
        
        if index % 100 == 0:
            print(f"Processed {index} papers...")

    # Create DataFrame and save
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)
    print(f"Classification complete. Saved to {output_path}")

if __name__ == "__main__":
    classify_papers()
