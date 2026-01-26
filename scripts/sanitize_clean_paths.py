#!/usr/bin/env python3
"""
ComfyUI Workflow Path Sanitizer & Flattener
-------------------------------------------
1. Strictly sanitizes specific nodes (Prompt Readers, Loaders) with placeholders.
2. Flattens file paths in all other nodes (keeping only filenames).
3. Preserves prompt text in other nodes.

Usage:
    python3 scripts/sanitize_clean_paths.py input.json -o output.json
"""

import json
import argparse
import sys
import os

# Strict rules: Node Type -> { widget_index: replacement_value }
STRICT_REPLACEMENTS = {
    "SDPromptReader": {
        0: "sanitized_image.png",
        3: "", # Positive
        4: "", # Negative
        5: ""  # Metadata
    },
    "SDBatchLoader": {
        0: "sanitized_input_path/",
        3: "sanitized_image.png"
    },
    "LoadImage": {
        0: "sanitized_image.png"
    },
    "LoraLoader": {
        0: "sanitized_lora.safetensors"
    }
}

def sanitize_paths(data, verbose=False):
    workflow = data # Modify in place
    
    print("--- Starting Sanitization ---")
    
    for node in workflow.get("nodes", []):
        node_type = node.get("type", "")
        node_id = node.get("id")
        
        # SKIP Rule 1: CLIP Text Nodes (User explicit instruction)
        if "CLIPTextEncode" in node_type:
            if verbose: print(f"Skipping Node {node_id} ({node_type}) - Explicit exclusion")
            continue
        
        # Strategy 1: Strict Replacement (for specific nodes)
        if node_type in STRICT_REPLACEMENTS:
            if "widgets_values" in node:
                rules = STRICT_REPLACEMENTS[node_type]
                for idx, replacement in rules.items():
                    # Ensure index exists
                    if idx < len(node["widgets_values"]):
                        old_val = node["widgets_values"][idx]
                        node["widgets_values"][idx] = replacement
                        if verbose: print(f"  [Strict Node {node_id} ({node_type})] Idx {idx}: '{old_val}' -> '{replacement}'")
            continue # Skip flattening for these nodes to avoid double processing or conflicts

        # Strategy 2: Path Flattening (for everything else)
        if "widgets_values" in node:
            new_values = []
            for i, val in enumerate(node["widgets_values"]):
                # We only care about strings
                if isinstance(val, str):
                    # Check for path-like characteristics
                    
                    # 1. Must contain a separator
                    has_separator = "/" in val or "\\" in val
                    
                    # 2. Heuristics to identify TEXT/PROMPTS (and ignore them)
                    is_text = ("\n" in val) or ("," in val) or ("(" in val) or (")" in val) or (" w/ " in val)
                    
                    if has_separator and not is_text:
                        # Logic: Unify separators, strip trailing slash (for folders), get last segment
                        normalized = val.replace("\\", "/")
                        stripped = normalized.rstrip("/")
                        basename = stripped.split("/")[-1]
                        
                        if basename != val: # Only update if changed
                            if verbose: print(f"  [Flatten Node {node_id}] '{val}' -> '{basename}'")
                            val = basename
                            
                new_values.append(val)
            node["widgets_values"] = new_values

    return workflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sanitize ComfyUI workflows.")
    parser.add_argument("input_file", help="Path to the input JSON workflow.")
    parser.add_argument("-o", "--output", help="Path to the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print details of changes.")
    
    args = parser.parse_args()

    # Determine Output Filename
    if args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(args.input_file)
        output_path = f"{base}_template{ext}"

    # Execution
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"Processing: {args.input_file}")
        sanitized_data = sanitize_paths(data, verbose=args.verbose)
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sanitized_data, f, indent=2)
            
        print(f"Success: Saved to {output_path}")
        
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.input_file}' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)