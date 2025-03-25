import os
import pandas as pd

def generate_app_jdl(**config_params):
    """
    Gera o bloco de application { config { ... } } com base nos parâmetros fornecidos.
    Ignora parâmetros cujo valor é None ou que sejam explicitamente a string "none".
    """
    lines = []
    lines.append("application {")
    lines.append("  config {")

    for key, value in config_params.items():
        # Se for None ou string "none" (ignorando maiúsculas/minúsculas), pula a linha
        if value is None or (isinstance(value, str) and value.lower() == "none"):
            continue
            
        # Formata valores booleanos como 'true' ou 'false'
        if isinstance(value, bool):
            value = str(value).lower()
            
        # Formata listas como [item1, item2]
        if isinstance(value, list):
            value = f"[{', '.join(value)}]"
            
        lines.append(f"    {key} {value}")

    lines.append("  }")
    lines.append("}")

    return "\n".join(lines) + "\n"

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file_name = "TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx"
    excel_file_path = os.path.join(base_dir, excel_file_name)
    aba_app = "APP"
    output_file = os.path.join(base_dir, "APP.jdl")
    
    if not os.path.exists(excel_file_path):
        print(f"[ERRO] Arquivo de planilha '{excel_file_path}' não encontrado.")
        return
    
    try:
        # Lê a planilha com as configurações da aplicação
        df = pd.read_excel(excel_file_path, sheet_name=aba_app, dtype=str)
        
        # Verifica se a planilha tem o formato esperado (uma linha por parâmetro)
        if 'Parameter' in df.columns and 'Value' in df.columns:
            # Formato: Parameter | Value
            config = {}
            for _, row in df.iterrows():
                param = row.get("Parameter", "").strip()
                value = row.get("Value", "").strip()
                
                if param:
                    # Converte valores booleanos e numéricos
                    if value.lower() in ["true", "yes", "1"]:
                        value = True
                    elif value.lower() in ["false", "no", "0"]:
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    elif value.lower() == "none":
                        value = None
                    elif "," in value and not value.startswith("["):
                        # Converte strings separadas por vírgula em listas
                        value = [item.strip() for item in value.split(",")]
                    
                    config[param] = value
        else:
            # Formato: uma coluna por parâmetro, uma linha de valores
            config = {}
            # Pega a primeira linha de dados (assumindo que é a linha de valores)
            if len(df) > 0:
                for col in df.columns:
                    param = col.strip()
                    value = str(df.iloc[0][col]).strip() if not pd.isna(df.iloc[0][col]) else None
                    
                    if param and value is not None:
                        # Converte valores booleanos e numéricos
                        if value.lower() in ["true", "yes", "1"]:
                            value = True
                        elif value.lower() in ["false", "no", "0"]:
                            value = False
                        elif value.isdigit():
                            value = int(value)
                        elif value.lower() == "none":
                            value = None
                        elif "," in value and not value.startswith("["):
                            # Converte strings separadas por vírgula em listas
                            value = [item.strip() for item in value.split(",")]
                        
                        # Converte snake_case para camelCase para os parâmetros
                        parts = param.split('_')
                        camel_param = parts[0] + ''.join(word.capitalize() for word in parts[1:])
                        
                        config[camel_param] = value
        
        # Gera o JDL com os parâmetros da planilha
        jdl_content = generate_app_jdl(**config)
        
    except Exception as e:
        print(f"[ERRO] Falha ao processar configurações da aplicação: {str(e)}")
        return
    
    # Escreve no arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(jdl_content)
        
    print(f"Arquivo 'APP.jdl' gerado/atualizado!")

if __name__ == "__main__":
    main()
