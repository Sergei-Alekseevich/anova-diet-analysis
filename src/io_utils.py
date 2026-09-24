"""
Interactive input utilities.

Provides helpers for:
- parsing free-form numeric strings (commas, spaces, decimal commas)
- yes/no prompts
- group and variable metadata entry
"""

from src.config import DEFAULT_VARIABLE_NAME, DEFAULT_VARIABLE_UNIT


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """Prompt the user for yes/no. Empty input returns `default`."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        ans = input(prompt + suffix).strip().lower()
        if ans == "":
            return default
        if ans in ("y", "yes", "д", "да"):
            return True
        if ans in ("n", "no", "н", "нет"):
            return False
        print("Please answer 'y' or 'n'.")


def parse_values(raw: str) -> list:
    """
    Parse a free-form numeric string into a list of floats.

    Handles comma, semicolon, and space separators, as well as
    decimal commas (e.g. "1,5" -> 1.5).

    Raises:
        ValueError: if any token cannot be parsed as a float.
    """
    raw = raw.strip()
    if not raw:
        return []

    text = raw.replace(";", ",").replace("\t", " ")
    while ",," in text:
        text = text.replace(",,", ",")

    if "," not in text:
        parts = text.split()
    else:
        parts = [t.strip() for t in text.split(",") if t.strip() != ""]

    values = []
    for p in parts:
        p = p.strip().replace(",", ".")
        try:
            values.append(float(p))
        except ValueError:
            raise ValueError(f"Cannot parse number: '{p}'")
    return values


def ask_groups() -> dict:
    """Interactively collect group names and their values."""
    print("\n" + "=" * 70)
    print("  ENTER YOUR DATA")
    print("=" * 70)
    print("You can use decimal point (1.5) or decimal comma (1,5).")
    print("Separate values by commas, semicolons, or spaces.\n")

    while True:
        try:
            n = int(input("How many groups? ").strip())
            if n < 2:
                print("Need at least 2 groups.")
                continue
            if n > 50:
                print("That's a lot. Are you sure? (max 50)")
                continue
            break
        except ValueError:
            print("Please enter an integer (e.g. 3).")

    data = {}
    for i in range(1, n + 1):
        while True:
            name = input(f"\nName of group {i} (e.g. 'Control'): ").strip()
            if not name:
                name = f"Group {i}"
            if name in data:
                print(f"Name '{name}' already used. Try another.")
                continue

            raw = input(f"Values for '{name}' (comma/space separated): ").strip()
            try:
                values = parse_values(raw)
            except ValueError as e:
                print(f"Error: {e}. Try again.")
                continue

            if len(values) < 2:
                print(f"Need at least 2 values, got {len(values)}. Try again.")
                continue

            data[name] = values
            print(f"  Added '{name}' with {len(values)} values.")
            break

    return data


def ask_variable_label() -> tuple:
    """Ask for the measured variable's name and unit (optional)."""
    print("\n" + "-" * 70)
    name = input(f"Variable name (empty = '{DEFAULT_VARIABLE_NAME}'): ").strip()
    if not name:
        name = DEFAULT_VARIABLE_NAME

    unit = input(f"Unit (empty = '{DEFAULT_VARIABLE_UNIT}'): ").strip()

    bad = (
        not unit
        or len(unit) > 20
        or "\n" in unit
        or "import" in unit
        or "from" in unit
        or "(" in unit
        or ")" in unit
    )
    if bad and unit:
        print("  Unit looks invalid - ignored.")
        unit = DEFAULT_VARIABLE_UNIT
    return name, unit