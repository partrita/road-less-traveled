import re
import os
import sys

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text

def split_book(cleaned_path, output_dir):
    with open(cleaned_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    chapters = []
    current_chapter = {'title': None, 'content': []}
    seen_headers = set()
    
    for line in lines:
        clean_line = line.strip()
        match = re.match(r'^#\s+(.+)$', clean_line)
        
        if match:
            # Header found
            raw_title = match.group(1).strip()
            # Remove leading numbers/symbols but keep keeping text
            # e.g. "1 GRACE" -> "GRACE", "1. Intro" -> "Intro"
            # But preserve "The 4 Hour Work Week"
            # Heuristic: Remove ^\d+[\.\s]*
            title_clean = re.sub(r'^\d+[\.\s]*', '', raw_title)
            
            norm = title_clean.lower()
            
            if norm in seen_headers:
                continue # Duplicate header
                
            # It's a new chapter
            if current_chapter['title'] is not None or (current_chapter['title'] is None and any(l.strip() for l in current_chapter['content'])):
                # If we have a previous chapter with content (or a titled chapter even if empty), save it.
                # If untitled and empty, we just overwrite it (start of file case).
                if current_chapter['title'] is None:
                     current_chapter['title'] = "Preface" # Default if text before first header
                
                chapters.append(current_chapter)
                
            current_chapter = {'title': title_clean, 'content': []}
            seen_headers.add(norm)
            
        else:
            current_chapter['content'].append(line)
            
    # Append last chapter
    if current_chapter['title'] or any(l.strip() for l in current_chapter['content']):
        if current_chapter['title'] is None:
            current_chapter['title'] = "Preface"
        chapters.append(current_chapter)

    # Write files
    qmd_files = []
    generated_chapters = []
    
    # We want index.qmd to be the first one.
    # Usually the first chapter found.
    
    for idx, chap in enumerate(chapters):
        safe_title = chap['title'].replace('"', '\\"')
        slug = slugify(chap['title'])
        
        if idx == 0:
            filename = "index.qmd"
        else:
            filename = f"{idx:02d}-{slug}.qmd"
            
        filepath = os.path.join(output_dir, filename)
        generated_chapters.append(filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: \"{chap['title']}\"\n---\n\n")
            f.writelines(chap['content'])
            
    return generated_chapters

def update_quarto_yml(yml_path, new_chapters):
    with open(yml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Manual YAML update to avoid dependency issues
    # Find "chapters:" block and replace it
    # We assume standard formatting:
    # book:
    #   chapters:
    #     - file.qmd
    
    if 'chapters:' not in content:
        # Append if missing (but it should be there)
        # Hacky append
        pass
    
    # Identify lines to replace
    lines = content.split('\n')
    new_lines = []
    in_chapters = False
    indent = "    " # default indent for chapters
    
    for line in lines:
        if line.strip().startswith('chapters:'):
            in_chapters = True
            new_lines.append(line)
            # Add new chapters here
            for chap in new_chapters:
                new_lines.append(f"{indent}- {chap}")
        elif in_chapters:
            # Skip old chapters (indented lines following chapters:)
            if line.strip().startswith('-'):
                continue
            else:
                # End of chapters block
                if line.strip(): # If text exists and not dash, block ended
                   in_chapters = False
                   new_lines.append(line)
                else:
                   # Empty line, maybe still in block or not. 
                   # Safe to keep empties if we are sure?
                   # Actually, let's just skip empties in chapters block.
                   pass
        else:
            new_lines.append(line)
            
    with open(yml_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    src = '/home/fkt/Documents/repo/road-less-traveled/mybook/cleaned.qmd'
    out_dir = '/home/fkt/Documents/repo/road-less-traveled/mybook'
    yml = '/home/fkt/Documents/repo/road-less-traveled/mybook/_quarto.yml'
    
    if not os.path.exists(src):
        # Fallback to index.qmd if cleaned doesn't exist (e.g. if I ran clean in previous turn but session reset?)
        # But I see cleaned.qmd was created.
        print("Cleaned file not found!")
        sys.exit(1)
        
    print(f"Reading from {src}")
    chapters = split_book(src, out_dir)
    print(f"Generated {len(chapters)} chapters.")
    update_quarto_yml(yml, chapters)
