# macro_processor.py
# MiniMacro Two-Pass Macro Processor
# SPCC Practical - BTech CSE

# ─────────────────────────────────────────────
# MiniMacro Language — 5 Predefined Keywords:
#   MACRO  - begins a macro definition
#   MEND   - ends a macro definition
#   CALL   - invokes a macro
#   SET    - assigns a value to a variable
#   PRINT  - prints a value
# ─────────────────────────────────────────────

KEYWORDS = ['MACRO', 'MEND', 'CALL', 'SET', 'PRINT']


class MacroProcessor:
    def __init__(self):
        # MNT: Macro Name Table  → { macro_name: { params, mdt_start, mdt_end } }
        self.mnt = {}
        # MDT: Macro Definition Table → list of body lines (with parameter placeholders)
        self.mdt = []

    # ── PASS 1 ──────────────────────────────────────────────────────────────
    def pass1(self, lines):
        """
        Scan source for MACRO definitions.
        Populate MNT and MDT. Everything inside MACRO...MEND is stored.
        """
        errors = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # skip blanks and comments
            if not line or line.startswith(';'):
                i += 1
                continue

            tokens = line.split()

            if tokens[0] == 'MACRO':
                if len(tokens) < 2:
                    errors.append(f"[Pass1] Line {i+1}: MACRO keyword missing a name.")
                    i += 1
                    continue

                # Parse:  MACRO  name(p1, p2, ...)
                header = ' '.join(tokens[1:])
                if '(' in header and ')' in header:
                    name = header[:header.index('(')].strip().upper()
                    params_raw = header[header.index('(') + 1: header.index(')')].strip()
                    params = [p.strip().upper() for p in params_raw.split(',')] if params_raw else []
                else:
                    name = header.strip().upper()
                    params = []

                if name in self.mnt:
                    errors.append(f"[Pass1] Line {i+1}: Macro '{name}' already defined (duplicate).")
                    i += 1
                    continue

                mdt_start = len(self.mdt)
                i += 1
                found_mend = False

                # Collect body until MEND
                while i < len(lines):
                    body_line = lines[i].strip()
                    if body_line.upper() == 'MEND':
                        found_mend = True
                        i += 1
                        break
                    if body_line and not body_line.startswith(';'):
                        self.mdt.append(body_line)
                    i += 1

                if not found_mend:
                    errors.append(f"[Pass1] Macro '{name}' has no MEND statement.")
                    continue

                self.mnt[name] = {
                    'params': params,
                    'mdt_start': mdt_start,
                    'mdt_end': len(self.mdt)
                }

            else:
                i += 1

        return errors

    # ── PASS 2 ──────────────────────────────────────────────────────────────
    def pass2(self, lines):
        """
        Scan source again. Skip macro definitions.
        Expand CALL statements using MNT + MDT.
        """
        output = []
        errors = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if not line or line.startswith(';'):
                output.append(line)
                i += 1
                continue

            tokens = line.split()
            keyword = tokens[0].upper()

            # Skip over macro definitions (already processed in Pass 1)
            if keyword == 'MACRO':
                while i < len(lines) and lines[i].strip().upper() != 'MEND':
                    i += 1
                i += 1   # skip MEND line itself
                continue

            # Expand macro invocations
            elif keyword == 'CALL':
                call_expr = ' '.join(tokens[1:])

                if '(' in call_expr and ')' in call_expr:
                    name = call_expr[:call_expr.index('(')].strip().upper()
                    args_raw = call_expr[call_expr.index('(') + 1: call_expr.index(')')].strip()
                    args = [a.strip() for a in args_raw.split(',')] if args_raw else []
                else:
                    name = call_expr.strip().upper()
                    args = []

                # Error: undefined macro
                if name not in self.mnt:
                    errors.append(f"[Pass2] Line {i+1}: Undefined macro '{name}'.")
                    i += 1
                    continue

                macro = self.mnt[name]

                # Error: wrong number of arguments
                if len(args) != len(macro['params']):
                    errors.append(
                        f"[Pass2] Line {i+1}: Macro '{name}' expects "
                        f"{len(macro['params'])} parameter(s), got {len(args)}."
                    )
                    i += 1
                    continue

                # Substitute parameters → arguments and emit expanded lines
                param_map = dict(zip(macro['params'], args))
                output.append(f"; [Expansion of {name}({', '.join(args)})]")

                for mdt_line in self.mdt[macro['mdt_start']: macro['mdt_end']]:
                    expanded = mdt_line
                    for param, arg in param_map.items():
                        # whole-word replacement to avoid partial matches
                        import re
                        expanded = re.sub(rf'\b{param}\b', arg, expanded)
                    output.append(expanded)

                output.append(f"; [End of {name}]")

            else:
                # Regular (non-macro) statement — pass through as-is
                output.append(line)

            i += 1

        return output, errors


# ── Pretty Printers ──────────────────────────────────────────────────────────

def print_tables(processor):
    print("\n╔══════════════════════════════════════════╗")
    print("║        Macro Name Table  (MNT)           ║")
    print("╠══════════════════════════════════════════╣")
    print(f"  {'Name':<15} {'Params':<20} {'MDT Range'}")
    print(f"  {'────':<15} {'──────':<20} {'─────────'}")
    for name, info in processor.mnt.items():
        params_str = ', '.join(info['params']) if info['params'] else '(none)'
        mdt_range = f"[{info['mdt_start']} – {info['mdt_end'] - 1}]"
        print(f"  {name:<15} {params_str:<20} {mdt_range}")
    print()

    print("╔══════════════════════════════════════════╗")
    print("║       Macro Definition Table (MDT)       ║")
    print("╠══════════════════════════════════════════╣")
    print(f"  {'Idx':<5} {'Statement'}")
    print(f"  {'───':<5} {'─────────'}")
    for idx, line in enumerate(processor.mdt):
        print(f"  [{idx}]   {line}")
    print()


def run(source, label=""):
    print("=" * 50)
    if label:
        print(f"  {label}")
    print("=" * 50)

    print("\n── Source Code ──────────────────────────────")
    for i, line in enumerate(source.strip().split('\n'), 1):
        print(f"  {i:>3}  {line}")

    processor = MacroProcessor()
    lines = source.strip().split('\n')

    print("\n── PASS 1 : Building MNT & MDT ─────────────")
    p1_errors = processor.pass1(lines)

    if p1_errors:
        print("  Errors found in Pass 1:")
        for e in p1_errors:
            print(f"    ✗ {e}")
    else:
        print("  Pass 1 complete — no errors.")

    print_tables(processor)

    print("── PASS 2 : Macro Expansion ─────────────────")
    expanded, p2_errors = processor.pass2(lines)

    if p2_errors:
        print("  Errors found in Pass 2:")
        for e in p2_errors:
            print(f"    ✗ {e}")

    if expanded:
        print("\n  Expanded Output:")
        for line in expanded:
            if line:
                print(f"    {line}")

    print()
    return processor, expanded, p1_errors + p2_errors
