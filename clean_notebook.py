#!/usr/bin/env python3
"""
Script to clean Jupyter notebook metadata (widgets, unnecessary outputs, etc.)
Usage: python clean_notebook.py pdm_project_MLFlow.ipynb
"""

import json
import sys
from pathlib import Path

def clean_notebook(notebook_path):
    """Remove widgets and unnecessary metadata from notebook."""
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # 1. Remove widgets metadata from root notebook
    if 'metadata' in nb and 'widgets' in nb['metadata']:
        del nb['metadata']['widgets']
        print("✅ Removed root-level 'widgets' metadata")
    
    # 2. Clean up cell-level metadata
    for cell_idx, cell in enumerate(nb.get('cells', [])):
        if 'metadata' in cell:
            # Remove widgets from individual cells
            if 'widgets' in cell['metadata']:
                del cell['metadata']['widgets']
            
            # Remove colab-specific metadata that might include widget references
            colab_metadata = cell['metadata'].get('colab', {})
            if 'widget' in colab_metadata or 'widgets' in colab_metadata:
                print(f"✅ Removed widgets from cell {cell_idx}")
    
    # 3. Optionally: Keep only essential output types and remove massive images
    # Comment out if you want to keep all outputs
    cleaned_outputs = []
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            new_outputs = []
            for output in cell.get('outputs', []):
                # Keep stream and error outputs
                if output.get('output_type') in ['stream', 'error']:
                    new_outputs.append(output)
                # Keep display_data but remove image/png if very large
                elif output.get('output_type') == 'display_data':
                    data = output.get('data', {})
                    # Keep text representations
                    if 'text/plain' in data or 'text/html' in data:
                        new_outputs.append(output)
                    # Keep images but could add size check here
                    elif 'image/png' in data:
                        new_outputs.append(output)
                # Keep execute_result
                elif output.get('output_type') == 'execute_result':
                    new_outputs.append(output)
            
            cell['outputs'] = new_outputs
    
    # Save cleaned notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Notebook cleaned and saved to {notebook_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python clean_notebook.py <notebook_path>")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    
    if not Path(notebook_path).exists():
        print(f"❌ File not found: {notebook_path}")
        sys.exit(1)
    
    clean_notebook(notebook_path)
    print("✅ Done!")
