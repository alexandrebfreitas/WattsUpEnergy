import os

def main():
    """
    Este script concatena todos os arquivos *.jdl (exceto 'complete.jdl' e 'complete_fixed.jdl') 
    em um único arquivo 'complete.jdl', garantindo que não haja duplicação de blocos de configuração.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excluded_files = ['complete.jdl', 'complete_fixed.jdl']
    jdl_files = [f for f in os.listdir(base_dir) if f.endswith('.jdl') and f not in excluded_files]
    
    # Ordenar os arquivos para garantir que APP.jdl venha primeiro
    jdl_files.sort()
    if 'APP.jdl' in jdl_files:
        jdl_files.remove('APP.jdl')
        jdl_files.insert(0, 'APP.jdl')
    
    output_file = os.path.join(base_dir, 'complete.jdl')
    
    # Rastrear se já incluímos um bloco de configuração de aplicação
    app_config_included = False
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for jdl_file in jdl_files:
            file_path = os.path.join(base_dir, jdl_file)
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                
                # Verificar se este arquivo contém um bloco de configuração de aplicação
                if 'application {' in content and app_config_included and jdl_file != 'APP.jdl':
                    # Remover o bloco de configuração duplicado
                    start_idx = content.find('application {')
                    end_idx = content.find('}', content.find('}', start_idx) + 1) + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        content = content[end_idx:].strip()
                        if not content:
                            continue  # Pular este arquivo se não sobrar nada após remover o bloco
                
                # Marcar que já incluímos um bloco de configuração
                if 'application {' in content and jdl_file == 'APP.jdl':
                    app_config_included = True
                
                # Se o conteúdo não terminar com newline, adiciona
                if content and not content.endswith('\n'):
                    content += '\n'
                
                # Escreve o conteúdo do arquivo atual
                if content.strip():
                    outfile.write(content)
                    outfile.write('\n')  # Linha extra para separar arquivos

    print("Arquivo 'complete.jdl' concatenado com sucesso!")

if __name__ == "__main__":
    main()
