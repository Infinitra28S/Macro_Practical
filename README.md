# MiniMacro — Two-Pass Macro Processor
### SPCC Practical | System Programming & Compiler Construction
#### BTech CSE — 3rd Year

---

## Overview

This project implements a **two-pass macro processor** for a simple user-defined language called **MiniMacro**.

A macro processor reads source code containing macro definitions and macro calls, and produces an expanded version where every macro call is replaced with the corresponding macro body — with actual arguments substituted for formal parameters.

---

## MiniMacro Language

MiniMacro has exactly **5 predefined keywords**:

| Keyword | Role |
|---------|------|
| `MACRO` | Starts a macro definition |
| `MEND`  | Ends a macro definition |
| `CALL`  | Invokes a macro by name |
| `SET`   | Variable assignment |
| `PRINT` | Output statement |

Lines starting with `;` are **comments** and are ignored.

### Macro Definition Syntax

```
MACRO MacroName(PARAM1, PARAM2)
    SET RESULT = PARAM1 + PARAM2
    PRINT RESULT
MEND
```

- Starts with `MACRO`, followed by name and parameters in parentheses.
- Body contains regular statements using parameter names as placeholders.
- Must be closed with `MEND`.

### Macro Invocation Syntax

```
CALL MacroName(value1, value2)
```

- `CALL` followed by macro name and actual arguments.
- Number of arguments must match the number of parameters.

---

## Project Structure

```
├── macro_processor.py   — Core engine: MacroProcessor class with pass1() and pass2()
├── main.py              — Demo runner: all 4 tasks from the practical question
├── CLAUDE.md            — Development notes
└── README.md            — This file
```

---

## Two-Pass Algorithm

### Pass 1 — Discovery

Scan source for `MACRO` definitions and populate two tables:

1. **MNT (Macro Name Table)**: Stores macro name, parameters, and MDT range.
2. **MDT (Macro Definition Table)**: Stores body lines with parameter placeholders.

### Pass 2 — Expansion

Scan source again:
- Skip `MACRO...MEND` blocks (already processed).
- On `CALL`: look up macro in MNT, substitute arguments for parameters, emit expanded lines.
- All other lines pass through unchanged.

---

## Error Handling

| Error | Pass | Message |
|-------|------|---------|
| `MACRO` with no name | 1 | `[Pass1] MACRO keyword missing a name` |
| Duplicate macro | 1 | `[Pass1] Macro 'X' already defined` |
| Missing `MEND` | 1 | `[Pass1] Macro 'X' has no MEND statement` |
| Undefined macro | 2 | `[Pass2] Undefined macro 'X'` |
| Wrong argument count | 2 | `[Pass2] Macro 'X' expects N parameter(s), got M` |

---

## How to Run

Requires **Python 3.6+**. No external libraries.

```bash
python main.py
```

A menu appears with 4 options:

| Option | What it does |
|--------|-------------|
| **1** | Run all 4 pre-defined demonstration tasks |
| **2** | Type/paste your own MiniMacro program interactively |
| **3** | Read a MiniMacro program from a file |
| **4** | Exit |

### Option 1 — Run Demos

Demonstrates all 4 tasks from the question:

1. **Task 1 & 3** — Normal macro definition, invocation, and expansion
2. **Task 4a** — Error: undefined macro
3. **Task 4b** — Error: incorrect parameter count
4. **Task 4c** — Error: missing MEND

### Option 2 — Interactive Input

Type or paste your MiniMacro program directly. Type `END` on a new line when finished.

Example session:
```
Enter your MiniMacro program below.
Type 'END' on a new line when finished.

MACRO SQUARE(N)
    SET RESULT = N * N
    PRINT RESULT
MEND

CALL SQUARE(5)
END
```

### Option 3 — Read from File

Provide a file path (e.g., `program.txt`) containing your MiniMacro program.

Example `program.txt`:
```
MACRO CUBE(N)
    SET RESULT = N * N * N
    PRINT RESULT
MEND

CALL CUBE(3)
```

---

## Sample Output (Task 1 & 3)

```
── PASS 1 : Building MNT & MDT ─────────────
  Pass 1 complete — no errors.

  MNT:
    ADD      A, B     [0 – 1]
    SWAP     X, Y     [2 – 6]
    GREET    NAME     [7 – 7]

  MDT:
    [0]   SET RESULT = A + B
    [1]   PRINT RESULT
    [2]   SET TEMP = X
    ...

── PASS 2 : Macro Expansion ─────────────────
  Expanded Output:
    SET P = 10
    SET Q = 20
    ; [Expansion of ADD(P, Q)]
    SET RESULT = P + Q
    PRINT RESULT
    ; [End of ADD]
    ...
```

---

## Data Structures

**MNT** — Python dictionary:
```python
mnt["ADD"] = { "params": ["A", "B"], "mdt_start": 0, "mdt_end": 2 }
```

**MDT** — Python list of strings:
```python
mdt = [
    "SET RESULT = A + B",   # index 0
    "PRINT RESULT",         # index 1
]
```

---

## Limitations (Intentional — College Level)

- Macros must be defined before they are called.
- No nested macro calls inside macro bodies.
- No actual execution — the processor only expands, does not run the output.
- Parameters must be single tokens.

---

*Submitted as part of SPCC Practical — BTech CSE 3rd Year*
