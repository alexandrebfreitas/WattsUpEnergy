import os

def main():
    """
    Este script concatena todos os arquivos *.jdl (exceto 'complete.jdl') em um único arquivo 'complete.jdl'.
    Atualizado para garantir que cada arquivo seja separado por ao menos uma quebra de linha, evitando a fusão
    de chaves e resultando em chaves desequilibradas.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    jdl_files = [f for f in os.listdir(base_dir) if f.endswith('.jdl') and f != 'complete.jdl']
    jdl_files.sort()
    
    output_file = os.path.join(base_dir, 'complete.jdl')

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for jdl_file in jdl_files:
            file_path = os.path.join(base_dir, jdl_file)
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                
                # Se o conteúdo não terminar com newline, adiciona
                if not content.endswith('\n'):
                    content += '\n'
                
                # Escreve o conteúdo do arquivo atual
                outfile.write(content)
                
                # Garante uma linha extra para separar de próximo arquivo
                outfile.write('\n')

    print("Arquivo 'complete.jdl' concatenado com sucesso!")

if __name__ == "__main__":
    main()
