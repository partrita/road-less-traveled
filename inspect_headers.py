import re
import sys

def inspect_headers(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []

    print(f"Total lines: {len(lines)}")
    headers = []
    
    # Simple regex for page number artifacts like "Problems and Pain 75."
    pagenum_pattern = re.compile(r'^.* \d+\.?$')

    for i, line in enumerate(lines):
        orig_line = line
        line = line.strip()
        
        # Check standard headers
        if line.startswith('# '):
            # Check context: is it likely a page header artifact?
            # e.g. if previous line was blank and next line is blank, maybe okay.
            # But if it's identical to the previous H1 seen recently...
            headers.append((i + 1, "H1", line))
        
        # Check capitalized lines that might be headers but missing #
        elif re.match(r'^[A-Z\s]+$', line) and len(line) > 4:
            headers.append((i+1, "CAPS", line))

        # Check for page number artifacts
        elif pagenum_pattern.match(line):
             headers.append((i+1, "PAGENUM_ARTIFACT?", line))

    return headers

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else '/home/fkt/Documents/repo/road-less-traveled/mybook/index.qmd'
    results = inspect_headers(target)
    for ln, kind, txt in results:
        print(f"Line {ln} [{kind}]: {txt}")
