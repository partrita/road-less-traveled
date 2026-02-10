import re
import sys

def is_page_number_line(line):
    # Matches "75" or "Problems and Pain 75."
    # Be careful not to match strict text ending in a number like "Chapter 1"
    # Usually page headers are "Title Number" or "Number Title" or just "Number"
    # "Problems and Pain 75." ends with a dot.
    
    clean = line.strip()
    if re.match(r'^\d+$', clean): 
        return True
    
    # "Title 123" or "Title 123."
    # Heuristic: if it ends with a number (and optional dot), and the text part matches a known header or is short.
    if re.match(r'^.* \d+\.?$', clean):
        return True
        
    return False

def clean_file(filepath, outpath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    cleaned_lines = []
    
    # We need a lookahead or buffer. simpler to iterate with index
    i = 0
    total = len(lines)
    
    while i < total:
        line = lines[i].rstrip() # remove trailing newline for checks
        original_line = lines[i]
        
        # Skip empty lines? No, keep them for paragraph structure but maybe collapse multiple.
        if not line:
            cleaned_lines.append(original_line)
            i += 1
            continue

        # Check for page number artifacts
        if is_page_number_line(line):
             # If it's a header line that cuts a sentence, we definitely want to drop it.
             # If it's just a number in between paragraphs, it's a page num -> drop.
             pass # -> Don't append
             i += 1
             continue

        # Check for Headers that interrupt sentences
        # Heuristic: 
        #   Current line starts with #
        #   Previous (non-empty) line did NOT end with punctuation (. ! ? " ' :)
        #   Next (non-empty) line starts with lowercase letter
        if line.startswith('# '):
            # Find previous non-empty line in cleaned_lines
            prev_text = ""
            for p in reversed(cleaned_lines):
                if p.strip():
                    prev_text = p.strip()
                    break
            
            # Find next non-empty line in source
            next_text = ""
            j = i + 1
            while j < total:
                if lines[j].strip():
                    next_text = lines[j].strip()
                    break
                j += 1
            
            is_interrupting = False
            if prev_text and next_text:
                # Check previous ending
                if not re.search(r'[.!?:"\']$', prev_text):
                    # Check next starting
                    # If next starts with lowercase, it's definitely a continuation
                    if next_text[0].islower():
                        is_interrupting = True
            
            if is_interrupting:
                print(f"Removing interrupting header at line {i+1}: {line}")
                i += 1
                continue
            
            # Also, check for repetitive Headers (PART headers) that appear frequently
            # E.g. "# DISCIPLINE"
            # If we see "# DISCIPLINE" but we are already inside "Problems and Pain", it's likely a header.
            # But maybe we just keep unique headers for now?
            # Actually, the "Sentence Interrupting" check is the strongest signal.
            
            # There's also the case where a header is on a line by itself between paragraphs (page break).
            # e.g. paragraph.
            # # DISCIPLINE
            # New paragraph.
            # In this case, "DISCIPLINE" is likely a running header if it repeats.
            
            pass 
        
        cleaned_lines.append(original_line)
        i += 1

    with open(outpath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

if __name__ == "__main__":
    src = '/home/fkt/Documents/repo/road-less-traveled/mybook/index.qmd'
    dst = '/home/fkt/Documents/repo/road-less-traveled/mybook/cleaned.qmd'
    clean_file(src, dst)
