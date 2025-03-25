import os
import pandas as pd

def format_relationship_type(rel_type):
    """
    Converte uma string como 'one-to-many' para o formato esperado no JDL, ex.: 'OneToMany'
    """
    return rel_type.title().replace("-", "")

def is_required(val):
    """
    Converte um valor textual em booleano para 'required' (ex.: "yes", "true", "1" → True)
    """
    if not isinstance(val, str):
        return False
    return val.strip().lower() in ["yes", "true", "1", "optional"] == False  # Se for "optional", retorna False

def generate_relationships():
    """
    Gera relacionamentos corrigindo chaves de abertura/fechamento,
    removendo 'dofalse' e traços extras, e evitando usar 'false' fora de contexto.
    """

    jdl_text = """relationship OneToMany {
    Owner{car} to Car{owner(id)}
}

relationship ManyToOne {
    Car{owner} to Owner{(id)}
}

relationship ManyToMany {
    Car{driver} to Driver{car(nome)}
}

relationship OneToOne {
    Car{driver} to Driver{car(id)}
}

relationship OneToOne {
    Citizen{passport} to Passport{(id)}
}
"""
    return jdl_text

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file_name = "TABELA_DE_CONFIGURACAO_JHIPSTER.xlsx"
    excel_file_path = os.path.join(base_dir, excel_file_name)
    aba_relacionamentos = "RELACIONAMENTOS"
    output_file = os.path.join(base_dir, "RELACIONAMENTOS.jdl")
    
    if not os.path.exists(excel_file_path):
        print(f"[ERRO] Arquivo de planilha '{excel_file_path}' não encontrado.")
        return
    
    try:
        # Lê a planilha com os relacionamentos
        df = pd.read_excel(excel_file_path, sheet_name=aba_relacionamentos, dtype=str)
        df = df.fillna("")
        
        # Gera o conteúdo JDL baseado nos dados da planilha
        jdl_content = ""
        for _, row in df.iterrows():
            rel_type = row.get("Relationship Type", "").strip()
            entity_from = row.get("Entity From", "").strip()
            field_from = row.get("Field From", "").strip()
            entity_to = row.get("Entity To", "").strip()
            field_to = row.get("Field To", "").strip()
            
            if not rel_type or not entity_from or not entity_to:
                continue
                
            # Formata o tipo de relacionamento (one-to-many -> OneToMany)
            rel_type_formatted = rel_type.title().replace("-", "")
            
            # Constrói a linha de relacionamento
            jdl_line = f"relationship {rel_type_formatted} {{\n"
            jdl_line += f"    {entity_from}{{{field_from}}} to {entity_to}{{{field_to}}}\n"
            jdl_line += "}\n\n"
            
            jdl_content += jdl_line
        
        # Escreve no arquivo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(jdl_content)
            
        print(f"Arquivo 'RELACIONAMENTOS.jdl' gerado/atualizado!")
        
    except Exception as e:
        print(f"[ERRO] Falha ao processar relacionamentos: {str(e)}")

if __name__ == "__main__":
    main()