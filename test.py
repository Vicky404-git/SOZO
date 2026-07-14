import subprocess
import time
import sys

def run_test():
    print("🚀 STARTING SŌZŌ SYSTEM INTEGRATION DIAGNOSTICS...\n")
    
    # 1. CORE TIMELINE & DATABASE
    core_commands = [
        ("1. ADD EVENT", 'sozo add test "Running automated system diagnostics" --tags debug,qa --files qa_test.py'),
        ("2. LIST TODAY", 'sozo today'),
        ("3. SEARCH DB", 'sozo search "diagnostics"'),
        ("4. TIMELINE", 'sozo timeline --period week --tag debug'),
        ("5. STATS", 'sozo stats'),
        ("6. FILE HISTORY", 'sozo file "qa_test.py"'),
        ("7. DASHBOARD", 'sozo dash'),
        ("8. EXPORT TIMELINE", 'sozo export --tag qa --out qa_export.md'),
    ]

    # 2. VAULT & SECOND BRAIN
    vault_commands = [
        ("9. ASCII GRAPH", 'sozo graph'),
        ("10. 2D GRAPH EXPORT", 'sozo graph --export'),
        ("11. CONCEPT ENGINE", 'sozo concept "test"'),
        ("12. NOTES DIRECTORY", 'sozo notes'),
        ("13. BRAIN SEARCH", 'sozo brain "diagnostics"'),
    ]

    # 3. DEV TOOLS (Safe variations that don't trigger actual pushes or API tokens)
    dev_commands = [
        ("14. GIT PASSTHROUGH", 'sozo git status'),
        ("15. HELP MENU (Core)", 'sozo --help'),
        ("16. HELP MENU (Bridge)", 'sozo bridge --help'),
    ]

    # Combine all test suites
    all_commands = core_commands + vault_commands + dev_commands

    for name, cmd in all_commands:
        print(f"\n{'-'*60}")
        print(f"🔵 TESTING: {name}")
        print(f"💻 RUNNING: {cmd}")
        print(f"{'-'*60}\n")
        
        result = subprocess.run(cmd, shell=True)
        
        if result.returncode != 0:
            print(f"\n❌ FATAL ERROR: Command '{name}' failed!")
            sys.exit(1)
            
        time.sleep(1)

    print("\n" + "="*60)
    print("✅ AUTOMATED INTEGRATION DIAGNOSTICS COMPLETE!")
    print("="*60)
    print("\n⚠️ NOTE: The following commands require manual API/Interactive testing:")
    print("  - AI SERVICES: sozo log, sozo ingest, sozo reflect, sozo commit, sozo docs")
    print("  - INTERACTIVE: sozo note, sozo rewrite, sozo push, sozo release")
    print("  - DAEMONS:     sozo kosmo, sozo bridge")

if __name__ == "__main__":
    run_test()
