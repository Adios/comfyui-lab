#!/usr/bin/env python3
"""
ComfyUI Workflow Sanitizer
--------------------------
Removes sensitive prompt text and local file paths from ComfyUI workflow JSONs.
Useful for preparing workflows for public sharing.

Usage:
    python3 scripts/sanitize_workflow.py input_workflow.json
    python3 scripts/sanitize_workflow.py input.json -o output.json
"""

import json
import copy
import argparse
import sys
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# Map node types to safe placeholder filenames
FILE_NODE_TYPES = {
    "Checkpoint Loader with Name (Image Saver)": "sanitized_checkpoint.safetensors",
    "LoraLoader": "sanitized_lora.safetensors",
    "IPAdapterModelLoader": "sanitized_ipadapter.bin",
    "CLIPVisionLoader": "sanitized_clipvision.safetensors",
    "ControlNetLoader": "sanitized_controlnet.safetensors",
    "UltralyticsDetectorProvider": "sanitized_bbox_model.pt",
    "SAMLoader": "sanitized_sam_model.pth",
    "LoadImage": "sanitized_image.png",
    "CheckpointLoaderSimple": "sanitized_checkpoint.safetensors",
    "VAELoader": "sanitized_vae.safetensors"
}

# ---------------------------------------------------------
# LOGIC
# ---------------------------------------------------------

def sanitize_json(data, verbose=False):
    workflow = copy.deepcopy(data)
    nodes = {node["id"]: node for node in workflow["nodes"]}
    links = {link[0]: link for link in workflow["links"]} # link_id -> [id, origin, origin_slot, target, target_slot, type]

    def get_upstream_node(node, input_name):
        inputs = node.get("inputs", [])
        target_link_id = next((inp["link"] for inp in inputs if inp["name"] == input_name), None)
        
        if target_link_id is None: 
            return None
            
        link = links.get(target_link_id)
        if not link: 
            return None
            
        return nodes.get(link[1])

    def clear_upstream_text(node):
        if not node: return

        node_type = node.get("type", "")
        
        # A. Stop Condition: Primitive String / CLIP Text
        if "PrimitiveString" in node_type or "CLIPTextEncode" in node_type:
            if "widgets_values" in node and len(node["widgets_values"]) > 0:
                current_val = node["widgets_values"][0]
                if current_val != "":
                    if verbose: print(f"  [Text] Clearing node {node['id']} ({node_type})")
                    node["widgets_values"][0] = ""
            return

        # B. Recursive Step: Trace logic nodes
        upstream_inputs = []
        if "PromptGenerator" in node_type:
            upstream_inputs = ["prompt"]
        elif "RegexReplace" in node_type:
            upstream_inputs = ["string"]
        elif "StringConcatenate" in node_type:
            upstream_inputs = ["string_a", "string_b"]
        elif "ImpactSwitch" in node_type:
            upstream_inputs = [f"input{i}" for i in range(1, 20)]
        
        for input_name in upstream_inputs:
            clear_upstream_text(get_upstream_node(node, input_name))

    # 1. Sanitize Paths
    if verbose: print("--- Sanitizing Paths ---")
    for node in workflow["nodes"]:
        node_type = node.get("type")
        if node_type in FILE_NODE_TYPES:
            replacement = FILE_NODE_TYPES[node_type]
            if "widgets_values" in node and len(node["widgets_values"]) > 0:
                if verbose: print(f"  [Path] Resetting node {node['id']} ({node_type}) -> {replacement}")
                node["widgets_values"][0] = replacement

    # 2. Sanitize Prompts (Reverse Trace)
    if verbose: print("\n--- Sanitizing Prompts ---")
    generators = [n for n in workflow["nodes"] if "PromptGenerator" in n.get("type", "")]
    for gen in generators:
        if verbose: print(f"Found Generator {gen['id']}, tracing upstream...")
        clear_upstream_text(gen)

    return workflow

# ---------------------------------------------------------
# CLI ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sanitize ComfyUI workflows for public release.")
    parser.add_argument("input_file", help="Path to the input JSON workflow.")
    parser.add_argument("-o", "--output", help="Path to the output JSON file. Defaults to input_sanitized.json")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print details of sanitized nodes.")
    
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
        sanitized_data = sanitize_json(data, verbose=args.verbose)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sanitized_data, f, indent=2)
            
        print(f"Success: Saved to {output_path}")
        
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.input_file}' is not a valid JSON file.")
        sys.exit(1)

