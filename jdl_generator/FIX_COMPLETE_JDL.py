import re
import os

def snake_to_camel_case(s: str) -> str:
    """
    Converts snake_case to camelCase.
    E.g.: 'profile_custom' -> 'profileCustom'
    """
    parts = s.split('_')
    if not parts:
        return s
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def fix_jdl_content(content: str) -> str:
    """
    Fixes only:
      - 'nan' or empty values in validations (min(nan), pattern('/nan/'), etc.)
      - alias name from snake_case to camelCase in "entity X (alias) { ... }"
    It does NOT remove line breaks, braces, or parentheses.
    """

    # 1. Remove isolated "nan" (case-insensitive)
    content = re.sub(r'\bnan\b', '', content, flags=re.IGNORECASE)

    # 2. Remove pattern('/nan/')
    content = re.sub(r"pattern\('/nan/'\)", '', content, flags=re.IGNORECASE)

    # 3. Remove min(nan), max(nan), minbytes(nan), maxbytes(nan) if present
    content = re.sub(r'(min|max|minbytes|maxbytes)\(\s*n(an)?\s*\)', '', content, flags=re.IGNORECASE)

    # 4. Remove leftover empty parentheses from validations (e.g. min(), max())
    #    leaving parentheses that are necessary for other parts of the JDL untouched.
    content = re.sub(r'\b(min|max|minbytes|maxbytes|pattern)\(\s*\)', '', content, flags=re.IGNORECASE)

    # 5. Convert entity alias snake_case -> camelCase
    #    Matches lines like "entity SomeEntity (some_alias){"
    pattern_alias = re.compile(r'(entity\s+\w+\s*\()([A-Za-z0-9_]+)(\)\s*\{?)', re.IGNORECASE)
    def alias_replacer(match):
        prefix = match.group(1)        # e.g. "entity Profile("
        alias_snake = match.group(2)  # e.g. "profile_custom"
        suffix = match.group(3)       # e.g. "){"
        alias_camel = snake_to_camel_case(alias_snake)
        return f"{prefix}{alias_camel}{suffix}"

    content = pattern_alias.sub(alias_replacer, content)

    # Return the updated content without altering line breaks, braces, or parentheses
    return content


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "complete.jdl")
    output_file = os.path.join(base_dir, "complete_fixed.jdl")

    if not os.path.exists(input_file):
        print(f"[ERRO] Arquivo '{input_file}' não encontrado.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    fixed_content = fix_jdl_content(content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(fixed_content)

    print(f"[INFO] Arquivo corrigido gerado: {output_file}")


if __name__ == "__main__":
    main()