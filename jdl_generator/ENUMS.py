import os
import re
import pandas as pd

def main():
    """
    Este script (re)cria (ou atualiza) as definições de enums no arquivo ENTIDADES.jdl
    a partir da aba 'ENUMS' da planilha TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx.

    Estrutura esperada na planilha (aba 'ENUMS'):
      - Enum Name         (ex: Country)
      - Enum Key          (ex: BELGIUM) [em UPPERCASE, se possível]
      - Enum Value        (opcional, ex: Belgium ou "中国" se usar caracteres especiais)
      - Comentário        (comentário para a chave do enum)
      - Observações       (observações adicionais)

    A sintaxe JDL para enums é:
        enum NomeDoEnum {
          CHAVE1 (OpcionalValue1)
          CHAVE2 (OpcionalValue2)
          ...
        }
    E não se usam vírgulas depois de cada enum key.

    Exemplo final:
        /**
         * Comentário geral do enum
         */
        enum Country {
          /**
           * Ex: Representa a Bélgica
           * Valor explícito; se omitido, usa o próprio nome da chave
           */
          BELGIUM ("Belgium")

          /**
           * Representa a China
           */
          CHINA ("中国")
        }
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Nome do arquivo JDL principal (entidades + enums)
    jdl_file_name = "ENTIDADES.jdl"
    jdl_file_path = os.path.join(base_dir, jdl_file_name)
    if not os.path.exists(jdl_file_path):
        print(f"[ERRO] Arquivo '{jdl_file_path}' não encontrado. Gere primeiro o ENTIDADES.jdl.")
        return

    # Nome do arquivo Excel e aba
    excel_file_name = "TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx"
    excel_file_path = os.path.join(base_dir, excel_file_name)
    aba_enums       = "ENUMS"
    if not os.path.exists(excel_file_path):
        print(f"[ERRO] Arquivo de planilha '{excel_file_path}' não encontrado.")
        return

    # Lê o conteúdo atual do ENTIDADES.jdl
    with open(jdl_file_path, "r", encoding="utf-8") as f:
        original_jdl = f.read()

    # Lê a planilha, transformando tudo em string, substitui NaN por ""
    df = pd.read_excel(excel_file_path, sheet_name=aba_enums, dtype=str)
    df = df.fillna("")

    # Montamos um dict:
    #   { "Country": [ {"key": "BELGIUM", "value": "Belgium", "comment": "...", "obs": "..."} ], ... }
    enum_map = {}

    for _, row in df.iterrows():
        enum_name = row.get("Enum Name", "").strip()
        enum_key  = row.get("Enum Key", "").strip().upper()  # forçar uppercase
        enum_val  = row.get("Enum Value (opcional)", "").strip()
        comment   = row.get("Comentário", "").strip()
        obs       = row.get("Observações", "").strip()

        # Se não tiver pelo menos o nome do enum e a chave, pula
        if not enum_name or not enum_key:
            continue

        item = {
            "key": enum_key,
            "value": enum_val,
            "comment": comment,
            "obs": obs
        }
        enum_map.setdefault(enum_name, []).append(item)

    # Regex para encontrar blocos enum existentes:
    #   /* Comentários ... */
    #   enum NOMEENUM {
    #       ...
    #   }
    # e capturar (group3) = NOMEENUM
    enum_block_pattern = re.compile(
        r'(^\s*((?:/\*\*?[\s\S]*?\*/\s*)?)enum\s+(\w+)\s*\{\s*([\s\S]*?)\s*\})',
        re.MULTILINE
    )

    # Vamos salvar aqui o que gera cada enum:
    new_enum_texts = {}

    def build_enum_block(enum_name, enum_items):
        """
        Constrói o bloco textual do enum no estilo JDL, sem vírgulas, e com comentários JavaDoc.
        Exemplo:

            enum Country {
              /**
               * Comentário e observações
               */
              BELGIUM ("Belgium")

              /**
               * Outro
               */
              FRANCE ("France")
            }
        """
        lines = []
        lines.append(f"enum {enum_name} {{")
        for it in enum_items:
            lines_comment = []
            if it["comment"] or it["obs"]:
                # Se há comentários/observações, criar bloco /** ... */
                doc_comment = "  /**\n"
                if it["comment"]:
                    doc_comment += f"   * {it['comment']}\n"
                if it["obs"]:
                    doc_comment += f"   * {it['obs']}\n"
                doc_comment += "   */"
                lines_comment.append(doc_comment)

            # Monta algo como:   BELGIUM ("Belgium")
            # Se enum_val tem aspas simples, convertemos para duplas
            enum_key = it["key"]
            enum_val = it["value"]
            if enum_val:
                # Remove aspas simples das extremidades, e envolve em aspas duplas
                enum_val = enum_val.strip("'")
                enum_val = f"\"{enum_val}\""
                enum_def = f"  {enum_key} ({enum_val})"
            else:
                # Sem value
                enum_def = f"  {enum_key}"

            if lines_comment:
                lines.append(lines_comment[0])
                lines.append(enum_def)
            else:
                lines.append(enum_def)
        lines.append("}")
        return "\n".join(lines)

    # Para cada nome de enum no enum_map, gera o bloco
    for nome_enum, items in enum_map.items():
        new_enum_texts[nome_enum] = build_enum_block(nome_enum, items)

    # Agora, substituímos os enums existentes no ENTIDADES.jdl e adicionamos
    # novos (que não existiam) ao final.
    found_enums = set()  # para sabermos quais enums já existiam

    def enum_replacer(match):
        """
        match.group(1) = todo o bloco "enum NomeEnum { ... }"
        match.group(2) = comentários/whitespace antes de enum (ex.: /** doc */)
        match.group(3) = NomeEnum
        match.group(4) = corpo do enum
        """
        entire_block = match.group(1)
        # comments_part = match.group(2)
        enum_name = match.group(3)

        if enum_name in new_enum_texts:
            found_enums.add(enum_name)
            return new_enum_texts[enum_name]
        else:
            # se não existir no novo dicionário, deixa como estava
            return entire_block

    updated_jdl = enum_block_pattern.sub(enum_replacer, original_jdl)

    # Se há novos enums que não estavam no arquivo, append ao final
    for e_name, e_text in new_enum_texts.items():
        if e_name not in found_enums:
            updated_jdl += "\n\n" + e_text

    # Salva o resultado
    with open(jdl_file_path, "w", encoding="utf-8") as f:
        f.write(updated_jdl)

    print("[INFO] ENUMs atualizados com sucesso no arquivo ENTIDADES.jdl.")
    if found_enums:
        print("      (Substituídos/encontrados):", ", ".join(found_enums))
    novos = set(new_enum_texts.keys()) - found_enums
    if novos:
        print("      (Adicionados ao final):", ", ".join(novos))
    print("[INFO] Fim.")

if __name__ == "__main__":
    main()