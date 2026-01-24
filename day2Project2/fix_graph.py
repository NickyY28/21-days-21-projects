import json

notebook_path = r'c:\Users\nicky\OneDrive\Desktop\21 projects 21 days\day2Project2\NetflixAnalysis.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Find the code cell with the plotting logic
    code_cell_found = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            # Look for the characteristic line
            if any('directors_df = netflix_df.dropna(subset=[\'director\']).copy()' in line for line in source):
                print("Found code cell.")
                # Check if already patched to avoid duplicates
                if not any('directors_df[directors_df[\'director\'] != \'Unknown\']' in line for line in source):
                    # Find insertion point
                    for i, line in enumerate(source):
                        if 'directors_df = netflix_df.dropna(subset=[\'director\']).copy()' in line:
                            # Insert the filter line after the exploded view calculation usually, 
                            # but filtering BEFORE explode or immediately after copy is safest given 'Unknown' is a single string filler.
                            # Based on previous context: 
                            # directors_df['director'] = directors_df['director'].str.split(', ')
                            # directors_df = directors_df.explode('director')
                            # 'Unknown' was filled earlier.
                            
                            # Let's insert it immediately after the copy for safety, assuming 'Unknown' is the full string.
                            # Wait, earlier code was: netflix_df['director'] = netflix_df['director'].fillna('Unknown')
                            
                            # Inserting after copy
                            source.insert(i + 1, "\n")
                            source.insert(i + 2, "directors_df = directors_df[directors_df['director'] != 'Unknown']\n")
                            print("Applied code patch.")
                            code_cell_found = True
                            break
                else:
                    print("Code already patched.")
                    code_cell_found = True

    # Find the last markdown cell (which was empty)
    # Ideally it's the one after the graph
    if nb['cells'][-1]['cell_type'] == 'markdown':
        print("Found last markdown cell.")
        nb['cells'][-1]['source'] = [
            "#### Top Directors on Netflix\n",
            "\n",
            "After excluding titles with unknown directors, we identify the most prolific filmmakers on the platform.\n",
            "\n",
            "**Key Findings:**\n",
            "- **Rajiv Chilaka** leads with the highest number of titles, primarily known for animation content like *Chhota Bheem*.\n",
            "- **Jan Suter** and **Raúl Campos** frequently collaborate, focusing on Spanish-language stand-up comedy and specials.\n",
            "- **Marcus Raboy** is another top name, specializing in comedy specials for major comedians.\n",
            "- The list is dominated by directors of **international TV shows** and **comedy specials**, showing Netflix's strategy of banking on niche but high-volume genres rather than just big-budget Hollywood movies."
        ]
        print("Updated markdown content.")

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    
    print("Notebook updated successfully.")

except Exception as e:
    print(f"Error: {e}")
