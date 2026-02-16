import os

# Your highly specific replacements map
REPLACEMENTS = {
    "WZML-X": "Professor-X",
    "WZML_X": "Professor_X",
    "wzmlx": "professorx",
    "WZ Bot": "Professor-X Bot",
    "WZML": "Professor-X",
    "@WZML": "@Professor-X",
    "SilentDemonSD": "Professor-X",
    "mysterysd": "professor-x"
}

WATERMARK = """# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================
"""

def process_directory(directory):
    files_modified = 0
    for root, dirs, files in os.walk(directory):
        # Skip hidden and cache folders
        if any(skip in root for skip in ['.git', '.venv', '__pycache__']):
            continue
            
        for file in files:
            # Only target specific file types
            if file.endswith(('.py', '.html', '.sh', '.md', 'Dockerfile', 'docker-compose.yml', 'ini', 'conf')):
                filepath = os.path.join(root, file)
                
                # Prevent modifying the rebrander itself
                if file == "rebrander.py":
                    continue
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content
                    
                    # Apply text replacements
                    for old, new in REPLACEMENTS.items():
                        content = content.replace(old, new)

                    # Inject Watermark into all python files if not present
                    if file.endswith('.py') and "PROFESSOR-X EDITION" not in content:
                        content = WATERMARK + content

                    # Save if modifications occurred
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ Rebranded & Watermarked: {filepath}")
                        files_modified += 1

                except Exception as e:
                    print(f"❌ Skipping {filepath} due to error: {e}")
                    
    print(f"\n🎉 Rebranding Complete! Successfully modified {files_modified} files.")

if __name__ == "__main__":
    print("🚀 Starting Professor-X Rebranding & Watermarking Process...")
    process_directory(".")
