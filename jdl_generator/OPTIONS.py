import os

def generate_options():
    """
    Gera as linhas de opções (dto, service, paginate, search, etc.) sem 'false' fora de contexto.
    """
    jdl_text = """dto Author with mapstruct
service Author with serviceClass
paginate Author with pagination
search Author with elasticsearch
microservice Author with mySuperMS
angularSuffix Author with Author
clientRootFolder Author with client
readOnly Author

dto Book with no
service Book with serviceClass
paginate Book with infinite-scroll
search Book with elasticsearch
readOnly Book

dto Profile with mapstruct
service Profile with serviceImpl
paginate Profile with no pagination
skipClient Profile
microservice Profile with myOtherMS
angularSuffix Profile with Profile
clientRootFolder Profile with account
"""
    return jdl_text

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(base_dir, "OPTIONS.jdl")

    jdl_content = generate_options()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(jdl_content)

    print(f"Arquivo 'OPTIONS.jdl' gerado/atualizado!")

if __name__ == "__main__":
    main()
