import os
import subprocess
import re
import sys

def parse_output(output):
    results = {}
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('var'):
            var_part = line.split(':')[0] if ':' in line else line.split(' ')[0]
            var_num = re.search(r'var(\d+)', var_part)
            if not var_num: continue
            v = var_num.group(1)
            
            mem_match = re.search(r'mem\s*=\s*(\d+)\s*bytes?', line)
            mem_val = f"{mem_match.group(1)} bytes" if mem_match else "N/A"
            
            time_match = re.search(r'time\s*=\s*([\d\.]+)\s*(µs|us)', line)
            time_val = f"{time_match.group(1)} µs" if time_match else "N/A"
            
            if v not in results:
                results[v] = {"mem": "N/A", "time": "N/A"}
            
            if mem_val != "N/A": results[v]["mem"] = mem_val
            if time_val != "N/A": results[v]["time"] = time_val
            
    return results

def process_file(filepath):
    print(f"Processing {filepath}...")
    if filepath.endswith('.py'):
        cmd = ['python3', filepath]
        comment_prefix = '#'
    elif filepath.endswith('.cpp'):
        compile_cmd = ['g++', '-std=c++17', '-O3', filepath, '-o', '/tmp/bench_bin']
        ret = subprocess.run(compile_cmd, capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"Compilation failed for {filepath}:\n{ret.stderr}")
            return
        cmd = ['/tmp/bench_bin']
        comment_prefix = '//'
    else:
        return

    ret = subprocess.run(cmd, capture_output=True, text=True)
    if ret.returncode != 0:
        print(f"Execution failed for {filepath}:\n{ret.stderr}")
        return
        
    out = ret.stdout
    results = parse_output(out)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    changed = False
    for i, line in enumerate(lines):
        if line.strip().startswith(comment_prefix) and 'var' in line and ('mem =' in line or 'time =' in line):
            var_num = re.search(r'var(\d+)', line)
            if var_num:
                v = var_num.group(1)
                if v in results:
                    mem = results[v]["mem"]
                    tim = results[v]["time"]
                    new_line = f"{comment_prefix} var{v} mem = {mem} and time = {tim}"
                    if lines[i] != new_line:
                        lines[i] = new_line
                        changed = True

    if changed:
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        print(f"  -> Updated {filepath}")
    else:
        print(f"  -> No changes needed for {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 benchmark_runner.py <directory>")
        return
    directory = sys.argv[1]
    
    for root, dirs, files in os.walk(directory):
        files = sorted(files)
        for f in files:
            if f.endswith('.py') or f.endswith('.cpp'):
                process_file(os.path.join(root, f))

if __name__ == "__main__":
    main()
