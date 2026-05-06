# main.py
# Entry point — menu-driven: run demos, enter custom input, or read from file

import sys
from macro_processor import run

# ── Demo Programs (Tasks 1-4 from the question) ─────────────────────────────

SAMPLE_PROGRAM = """
; MiniMacro sample program

MACRO ADD(A, C)
    SET RESULT = A + C
    PRINT RESULT
MEND

MACRO SWAP(X, Y)
    SET TEMP = X
    SET X = Y
    SET Y = TEMP
    PRINT X
    PRINT Y
MEND

MACRO GREET(NAME)
    PRINT Hello SPCC
MEND

SET P = 10
SET Q = 20

CALL ADD(P, Q)
CALL SWAP(P, Q)
CALL GREET(MANWA)

PRINT Done
"""

UNDEFINED_MACRO_PROGRAM = """
MACRO ADD(A, C)
    SET RESULT = A + C
    PRINT RESULT
MEND

CALL ADD(5, 10)
CALL MULTIPLY(3, 4)
"""

WRONG_PARAMS_PROGRAM = """
MACRO ADD(A, C)
    SET RESULT = A + C
    PRINT RESULT
MEND

CALL ADD(5, 10, 15)
"""

MISSING_MEND_PROGRAM = """
MACRO ADD(A, C)
    SET RESULT = A + C
    PRINT RESULT

CALL ADD(5, 10)
"""


def run_all_demos():
    """Run all 4 pre-defined demonstration scenarios."""
    run(SAMPLE_PROGRAM,            label="TASK 1 & 3 — Macro Definition, Invocation & Expansion")
    run(UNDEFINED_MACRO_PROGRAM,   label="TASK 4a — Error: Undefined Macro")
    run(WRONG_PARAMS_PROGRAM,      label="TASK 4b — Error: Incorrect Parameter Count")
    run(MISSING_MEND_PROGRAM,      label="TASK 4c — Error: Missing MEND")


def read_from_file(filepath):
    """Read a MiniMacro program from a file and process it."""
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        run(source, label=f"File: {filepath}")
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")


def interactive_input():
    """Let the user type/paste a MiniMacro program at runtime."""
    print("Enter your MiniMacro program below.")
    print("Type 'END' on a new line when finished.\n")

    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break

    source = '\n'.join(lines)
    if source.strip():
        run(source, label="User-Defined Program")
    else:
        print("No input provided.")


def show_menu():
    print("=" * 46)
    print("      MiniMacro Two-Pass Macro Processor")
    print("=" * 46)
    print()
    print("  1. Run all 4 demonstration tasks")
    print("  2. Enter your own MiniMacro program")
    print("  3. Read MiniMacro program from a file")
    print("  4. Exit")
    print()


def main():
    while True:
        show_menu()
        choice = input("Enter choice (1-4): ").strip()
        print()

        if choice == '1':
            run_all_demos()
        elif choice == '2':
            interactive_input()
        elif choice == '3':
            filepath = input("Enter file path (e.g., program.txt): ").strip()
            read_from_file(filepath)
        elif choice == '4':
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

        print("\n" + "─" * 46 + "\n")


if __name__ == "__main__":
    main()
