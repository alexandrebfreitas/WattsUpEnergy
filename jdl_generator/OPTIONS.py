import os
import pandas as pd

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file_name = "TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx"
    excel_file_path = os.path.join(base_dir, excel_file_name)
    aba_options = "OPTIONS"
    output_file = os.path.join(base_dir, "OPTIONS.jdl")
    
    if not os.path.exists(excel_file_path):
        print(f"[ERRO] Arquivo de planilha '{excel_file_path}' não encontrado.")
        return
    
    try:
        # Lê a planilha com as opções
        df = pd.read_excel(excel_file_path, sheet_name=aba_options, dtype=str)
        df = df.fillna("")
        
        # Gera o conteúdo JDL baseado nos dados da planilha
        jdl_content = ""
        for _, row in df.iterrows():
            entity = row.get("Entity", "").strip()
            option_type = row.get("Option Type", "").strip()  # dto, service, paginate, etc.
            option_value = row.get("Option Value", "").strip()  # mapstruct, serviceClass, etc.
            
            if not entity or not option_type:
                continue
                
            # Constrói a linha de opção
            if option_value:
                jdl_line = f"{option_type} {entity} with {option_value}\n"
            else:
                jdl_line = f"{option_type} {entity}\n"
                
            jdl_content += jdl_line
        
        # Escreve no arquivo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(jdl_content)
            
        print(f"Arquivo 'OPTIONS.jdl' gerado/atualizado!")
        
    except Exception as e:
        print(f"[ERRO] Falha ao processar opções: {str(e)}")

if __name__ == "__main__":
    main()
