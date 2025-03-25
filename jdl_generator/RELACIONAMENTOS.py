import os

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
    output_file = os.path.join(base_dir, "RELACIONAMENTOS.jdl")

    jdl_content = generate_relationships()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(jdl_content)

    print(f"Arquivo 'RELACIONAMENTOS.jdl' gerado/atualizado!")

if __name__ == "__main__":
    main()