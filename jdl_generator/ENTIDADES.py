import os
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
    Este script (re)cria o arquivo ENTIDADES.jdl, contendo apenas as
    definições iniciais das entidades (sem campos). As entidades, com
    seus respectivos aliases, são lidas de uma planilha Excel, que deve
    conter ao menos duas colunas:
      - Entity (nome da Entidade, ex.: 'Profile')
      - Alias (nome do alias, ex.: 'profile_custom')
    
    Em seguida, o arquivo ENTIDADES.jdl pode ser complementado pelo
    script CAMPOS.py, que insere os campos, validações e comentários.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Nome do arquivo JDL que iremos (re)criar
    jdl_file_name = "ENTIDADES.jdl"
    jdl_file_path = os.path.join(base_dir, jdl_file_name)

    # Nome do arquivo da planilha e aba
    excel_file_name = "TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx"
    excel_file_path = os.path.join(base_dir, excel_file_name)
    aba_entidades   = "ENTIDADES"  # Ajuste conforme o nome real da aba

    # Se o arquivo Excel não existir, encerramos
    if not os.path.exists(excel_file_path):
        print(f"[ERRO] Arquivo de planilha '{excel_file_path}' não encontrado.")
        return

    # Lê a planilha com o nome das entidades
    df = pd.read_excel(excel_file_path, sheet_name=aba_entidades)

    # Prepara uma lista de (entity_name, alias_camel) a partir da planilha
    entidades_info = []
    for _, row in df.iterrows():
        entity = str(row.get("Entity", "")).strip()
        alias  = str(row.get("Alias", "")).strip()
        if not entity:
            continue
        # Se não foi definido um alias, podemos usar algo padronizado
        if not alias:
            alias = entity.lower()
        alias_camel = snake_to_camel_case(alias)
        entidades_info.append((entity, alias_camel))

    # Cria (ou recria) o arquivo ENTIDADES.jdl
    with open(jdl_file_path, "w", encoding="utf-8") as f:
        f.write("// ENTIDADES.jdl\n")
        f.write("// Gerado automaticamente. Este arquivo contém apenas as entidades básicas.\n")
        f.write("// Os campos e validações serão posteriormente adicionados via CAMPOS.py.\n\n")

        # Escreve cada entity com seu alias
        for (entidade, alias_camel) in entidades_info:
            f.write(f"entity {entidade} ({alias_camel}) {{\n")
            f.write("}\n\n")

    print(f"[INFO] Arquivo '{jdl_file_name}' foi recriado com as definições iniciais das entidades.")
    print("[INFO] Agora, execute o script CAMPOS.py para inserir os campos dentro de cada entidade.")

if __name__ == "__main__":
    main()
