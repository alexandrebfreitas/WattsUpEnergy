import os
import re
import pandas as pd

def snake_to_camel_case(s: str) -> str:
    """
    Converte uma string snake_case para camelCase.
    Ex.: 'profile_custom' -> 'profileCustom'
    """
    parts = s.split('_')
    if not parts:
        return s
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def main():
    """
    Este script lê o arquivo ENTIDADES.jdl (já existente, contendo apenas as definições de entidades)
    e a planilha 'TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx' (aba 'CAMPOS'), inserindo os campos no formato
    JDL, removendo 'nan' quando necessário, e gerando pattern(/regex/) SEM aspas.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1) Arquivo de entrada JDL (apenas entidades)
    jdl_file_name = "ENTIDADES.jdl"
    jdl_file_path = os.path.join(base_dir, jdl_file_name)
    if not os.path.exists(jdl_file_path):
        print(f"[ERRO] Arquivo '{jdl_file_path}' não foi encontrado. Execute primeiro o script que gera ENTIDADES.jdl.")
        return

    # 2) Nome do arquivo da planilha e aba
    excel_file_name = "TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx"
    excel_file_path = os.path.join(base_dir, excel_file_name)
    aba_campos = "CAMPOS"
    if not os.path.exists(excel_file_path):
        print(f"[ERRO] Arquivo de planilha '{excel_file_path}' não encontrado.")
        return

    # Lê o conteúdo original do ENTIDADES.jdl
    with open(jdl_file_path, "r", encoding="utf-8") as f:
        original_jdl = f.read()

    # Lê a planilha com os campos, converte tudo para string, substitui NaN por ""
    df = pd.read_excel(excel_file_path, sheet_name=aba_campos, dtype=str)
    df = df.fillna("")

    def clean_nan(val: str) -> str:
        val = val.strip()
        return "" if val.lower() == "nan" else val

    campos_by_entity = {}

    for _, row in df.iterrows():
        entity       = clean_nan(row.get("Entity", ""))
        field_name   = clean_nan(row.get("Field Name", ""))
        field_type   = clean_nan(row.get("Field Type", ""))
        required_raw = clean_nan(row.get("Required", "")).lower()
        required     = required_raw in ["yes", "true", "1", "sim"]

        field_annotation   = clean_nan(row.get("Field Annotation(s)", ""))
        comment_str        = clean_nan(row.get("Field Javadoc/Comment", ""))
        observacao_exemplo = clean_nan(row.get("Observações/Exemplo", ""))

        minlength  = clean_nan(row.get("Minlength", ""))
        maxlength  = clean_nan(row.get("Maxlength", ""))
        pattern    = clean_nan(row.get("Pattern", ""))       # e.g. ^[A-Z][a-z]+$, sem slashes
        unique_raw = clean_nan(row.get("Unique", "")).lower()
        minval     = clean_nan(row.get("Min", ""))
        maxval     = clean_nan(row.get("Max", ""))
        minbytes   = clean_nan(row.get("Minbytes", ""))
        maxbytes   = clean_nan(row.get("Maxbytes", ""))

        unique_val = unique_raw in ["yes", "true", "1", "sim"]

        # Se não houver nome de entidade ou campo, pula
        if not entity or not field_name:
            continue

        # Monta as validações de acordo com a sintaxe do JDL
        validations = []
        if required:
            validations.append("required")
        if minlength.isdigit():
            validations.append(f"minlength({minlength})")
        if maxlength.isdigit():
            validations.append(f"maxlength({maxlength})")
        # pattern deve ficar assim: pattern(/^[A-Z][a-z]+\d$/)
        if pattern:
            # Garantimos que, se o usuário não incluiu as barras, nós as adicionamos
            # Ex.: "^[A-Z][a-z]+\d$" -> "/^[A-Z][a-z]+\d$/"
            # Mas no JDL final, queremos pattern(/^[A-Z][a-z]+\d$/) sem aspas
            # Então montamos pattern(/padrão/)
            regex_clean = pattern.strip()
            if regex_clean:
                # Adicionamos manualmente / e / se não estiverem presentes,
                # mas se o usuário já incluiu, não duplicamos
                if not regex_clean.startswith("/"):
                    regex_clean = "/" + regex_clean
                if not regex_clean.endswith("/"):
                    regex_clean += "/"
                validations.append(f"pattern({regex_clean})")
        if minval:
            validations.append(f"min({minval})")
        if maxval:
            validations.append(f"max({maxval})")
        if minbytes:
            validations.append(f"minbytes({minbytes})")
        if maxbytes:
            validations.append(f"maxbytes({maxbytes})")
        if unique_val:
            validations.append("unique")

        # Ex.: "name String required minlength(2) maxlength(40)"
        field_line = f"{field_name} {field_type}"
        if validations:
            field_line += " " + " ".join(validations)

        # Inclui comentários Javadoc antes do campo, se houver
        comment_lines = []
        if field_annotation:
            comment_lines.append(f"Annotations: {field_annotation}")
        if comment_str:
            comment_lines.append(f"Comment: {comment_str}")
        if observacao_exemplo:
            comment_lines.append(f"Example: {observacao_exemplo}")

        if comment_lines:
            doc_comment = "  /**\n"
            for c_line in comment_lines:
                doc_comment += f"   * {c_line.replace('\"', '\\\"')}\n"
            doc_comment += "   */\n"
            final_line = doc_comment + f"  {field_line}"
        else:
            final_line = f"  {field_line}"

        campos_by_entity.setdefault(entity, []).append(final_line)

    # Regex para capturar cada entidade e substituir bloco interno
    pattern_entity = re.compile(
        r'(entity\s+(\w+)\s*\(([^)]*)\)\s*\{)([^}]*)(\})',
        re.IGNORECASE | re.DOTALL
    )

    def replacer(match):
        entity_decl   = match.group(1)
        entity_name   = match.group(2)
        entity_alias  = match.group(3)
        middle        = match.group(4)
        closing_brace = match.group(5)

        alias_camel = snake_to_camel_case(entity_alias)
        entity_first_line = f"entity {entity_name} ({alias_camel})" + "{"

        fields_list = campos_by_entity.get(entity_name, [])
        if not fields_list:
            # Se não há campos, apenas corrige alias
            return f"{entity_first_line}{middle}{closing_brace}"

        fields_str = "\n".join(fields_list)
        return f"{entity_first_line}\n{fields_str}\n{closing_brace}"

    new_jdl = pattern_entity.sub(replacer, original_jdl)

    # Não fazemos substituição de aspas ao redor do pattern, pois precisamos dele sem aspas
    # Se quiser converter outras aspas simples, poderíamos fazê-lo, mas vamos omitir
    # pois o requisito pede "pattern(/regex/) sem aspas".

    with open(jdl_file_path, "w", encoding="utf-8") as f:
        f.write(new_jdl)

    print(f"[INFO] Script concluído. Arquivo '{jdl_file_name}' atualizado removendo 'nan' e configurando pattern(/regex/) sem aspas.")

if __name__ == "__main__":
    main()
