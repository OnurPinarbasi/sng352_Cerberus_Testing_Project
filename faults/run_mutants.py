#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def get_leading_whitespace(line):
    return line[:len(line) - len(line.lstrip())]

def load_mutants(index_path):
    mutants = []
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found.")
        sys.exit(1)
        
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    for line in content.splitlines():
        if line.startswith("|") and not "Mutation ID" in line and not "---" in line:
            parts = [p.strip() for p in line.split("|")][1:-1]
            if len(parts) >= 6:
                mutants.append({
                    "id": parts[0],
                    "class": parts[1],
                    "target_file": parts[2],
                    "target_function": parts[3],
                    "killing_test": parts[4],
                    "folder": parts[5]
                })
    return mutants

def apply_mutation(target_file, clean_code_lines, clean_target_lines, m_id, func_name, orig_content, mut_content):
    orig_lines = [l for l in orig_content.splitlines() if l.strip()]
    clean_orig = [l.strip() for l in orig_lines]
    
    # Find the function definition
    func_def_prefix = f"def {func_name}("
    func_idx = -1
    for idx, line in enumerate(clean_code_lines):
        if func_def_prefix in line:
            func_idx = idx
            break
            
    if func_idx == -1:
        return False, f"Function definition for {func_name} not found"
        
    # Search for the original block starting from func_idx
    match_idx = -1
    n = len(clean_orig)
    for i in range(func_idx, len(clean_target_lines) - n + 1):
        match = True
        for k in range(n):
            if clean_target_lines[i + k] != clean_orig[k]:
                match = False
                break
        if match:
            match_idx = i
            break
            
    if match_idx == -1:
        return False, f"Original block of {m_id} not found in function {func_name}"
        
    # Indent mutated code appropriately
    target_indentation = get_leading_whitespace(clean_code_lines[match_idx])
    mutated_lines = mut_content.splitlines()
    if not mutated_lines:
        return False, "mutated.py is empty"
        
    first_mutated_indent = get_leading_whitespace(mutated_lines[0])
    
    replacement_lines = []
    for line in mutated_lines:
        if not line.strip():
            replacement_lines.append("")
        else:
            mut_indent = get_leading_whitespace(line)
            if mut_indent.startswith(first_mutated_indent):
                rel_indent = mut_indent[len(first_mutated_indent):]
            else:
                rel_indent = mut_indent
            replacement_lines.append(target_indentation + rel_indent + line.lstrip())
            
    # Rebuild code
    new_lines = clean_code_lines[:match_idx] + replacement_lines + clean_code_lines[match_idx + n:]
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
        
    return True, None

def run_mutant(m, project_root, original_code_backup):
    m_id = m["id"]
    func_name = m["target_function"]
    killing_test = m["killing_test"]
    folder = m["folder"]
    
    m_dir = os.path.join(project_root, folder)
    orig_file = os.path.join(m_dir, "original.py")
    mut_file = os.path.join(m_dir, "mutated.py")
    target_file = os.path.join(project_root, m["target_file"])
    
    if not os.path.exists(orig_file) or not os.path.exists(mut_file):
        return "ERROR", "original.py or mutated.py missing"
        
    with open(orig_file, "r", encoding="utf-8") as f:
        orig_content = f.read()
    with open(mut_file, "r", encoding="utf-8") as f:
        mut_content = f.read()
        
    # Parse target file
    with open(target_file, "r", encoding="utf-8") as f:
        code_content = f.read()
        
    clean_code_lines = code_content.splitlines()
    clean_target_lines = [l.strip() for l in clean_code_lines]
    
    # Apply mutant
    success, err_msg = apply_mutation(
        target_file, clean_code_lines, clean_target_lines,
        m_id, func_name, orig_content, mut_content
    )
    
    if not success:
        return "ERROR", err_msg
        
    # Run test
    # If the test is TODO, run the entire test suite to see if any test catches the mutant
    if killing_test.startswith("TODO"):
        cmd = ["pytest", "tests/", "-q"]
    else:
        cmd = ["pytest", killing_test, "-q"]
        
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
    
    # Restore original file immediately
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(original_code_backup)
        
    if res.returncode != 0:
        return "KILLED", None
    else:
        return "SURVIVED", None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    index_path = os.path.join(script_dir, "INDEX.md")
    mutants = load_mutants(index_path)
    
    # Check if a specific mutant is requested
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    if target_id:
        mutants = [m for m in mutants if m["id"].upper() == target_id.upper()]
        if not mutants:
            print(f"Error: Mutant {target_id} not found in INDEX.md")
            sys.exit(1)
            
    print("======================================================================")
    print("                      MUTATION TEST RUNNER                            ")
    print("======================================================================")
    if target_id:
        print(f"Running single mutant: {target_id.upper()}")
    else:
        print(f"Running all {len(mutants)} mutants...")
    print("----------------------------------------------------------------------")
    
    # Store clean backups of target files (currently all mutants target cerberus/validator.py)
    validator_path = os.path.join(project_root, "cerberus/validator.py")
    with open(validator_path, "r", encoding="utf-8") as f:
        original_validator_code = f.read()
        
    results = []
    killed_count = 0
    survived_count = 0
    error_count = 0
    
    for m in mutants:
        m_id = m["id"]
        print(f"Running mutant {m_id:6} | {m['class']:4} | {m['target_function']}... ", end="", flush=True)
        
        status, detail = run_mutant(m, project_root, original_validator_code)
        
        if status == "KILLED":
            print("\033[92mKILLED\033[0m")
            killed_count += 1
        elif status == "SURVIVED":
            print("\033[91mSURVIVED\033[0m")
            survived_count += 1
        else:
            print(f"\033[93mERROR: {detail}\033[0m")
            error_count += 1
            
        results.append({
            "id": m_id,
            "class": m["class"],
            "function": m["target_function"],
            "status": status,
            "detail": detail
        })
        
    print("----------------------------------------------------------------------")
    print("                          SUMMARY REPORT                              ")
    print("----------------------------------------------------------------------")
    print(f"Total Mutants Checked: {len(results)}")
    print(f"Killed (Detected):     {killed_count} ({(killed_count/len(results)*100):.1f}%)")
    print(f"Survived (Undetected): {survived_count}")
    print(f"Errors/Skipped:        {error_count}")
    print("======================================================================")
    
    # If any mutant survived (except TODO mutants if they are not expected to be killed by the current suite),
    # or if errors occurred, report appropriate exit code.
    if error_count > 0:
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
