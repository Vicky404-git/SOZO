import os
import time

def run_test():
    print("🚀 STARTING SŌZŌ SYSTEM DIAGNOSTICS...\n")
    
    # 1. The Commands to test automatically
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
        
        # Execute the command directly in the terminal
        os.system(cmd)
        
        # Pause so you can visually inspect the output
        time.sleep(2)

    print("\n" + "="*50)
    print("✅ AUTOMATED DIAGNOSTICS COMPLETE!")
    print("="*50)
    print("\n⚠️ NOTE: Please test the following commands manually:")
    print("  1. 'sozo note \"Test\"' (Opens your text editor)")
    print("  2. 'sozo commit' (Uses Groq API tokens)")
    print("  3. 'sozo kosmo' (Runs an infinite background loop)")

if __name__ == "__main__":
    run_test()