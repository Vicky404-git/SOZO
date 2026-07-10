import subprocess
import time
import sys

def run_test():
    print("🚀 STARTING SŌZŌ SYSTEM DIAGNOSTICS...\n")
    
    commands = [
        ("1. ADD EVENT", 'sozo add test "Running automated system diagnostics" -t debug,qa -f qa_test.py'),
        ("2. LIST TODAY", 'sozo today'),
        ("3. SEARCH", 'sozo search "diagnostics"'),
        ("4. TIMELINE", 'sozo timeline week -t qa'),
        ("5. STATS", 'sozo stats'),
        ("6. FILE HISTORY", 'sozo file "qa_test.py"'),
        ("7. DASHBOARD", 'sozo dash'),
        ("8. EXPORT", 'sozo export -t qa -o qa_export.md'),
        ("9. ASCII GRAPH", 'sozo graph'),
        ("10. 2D GRAPH EXPORT", 'sozo graph --export')
    ]

    for name, cmd in commands:
        print(f"\n{'-'*50}")
        print(f"🔵 TESTING: {name}")
        print(f"💻 RUNNING: {cmd}")
        print(f"{'-'*50}\n")
        
        # Use subprocess and check for failure
        result = subprocess.run(cmd, shell=True)
        
        if result.returncode != 0:
            print(f"\n❌ FATAL ERROR: Command '{name}' failed!")
            sys.exit(1)  # This tells GitHub Actions to FAIL the workflow
        
        time.sleep(2)

    print("\n" + "="*50)
    print("✅ AUTOMATED DIAGNOSTICS COMPLETE!")
    print("="*50)

if __name__ == "__main__":
    run_test()
