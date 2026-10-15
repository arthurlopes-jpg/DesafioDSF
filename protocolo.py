import struct

def ler_completo(sock, total_esperado):
    """
    Lê exatamente a quantidade de bytes especificada em total_esperado.
    Implementa o laço while conforme o Passo 2.
    """
    dados = b''
    while len(dados) < total_esperado:
        # Lê apenas a quantidade de bytes que falta para completar o total esperado
        pacote = sock.recv(total_esperado - len(dados))
        
        # Se recv retornar b'' antes do fim, a conexão caiu ou houve falha
        if not pacote: 
            return None 
            
        dados += pacote
        
    return dados

def receber_mensagem(sock):
    """
    Lê o cabeçalho de 4 bytes e depois lê o tamanho da imagem em si.
    """
    # 1. Lê os 4 bytes do cabeçalho
    cabecalho = ler_completo(sock, 4)
    if not cabecalho:
        return None
        
    # Desempacota os 4 bytes (big-endian unsigned int '>I')
    tamanho = struct.unpack('>I', cabecalho)[0]
    
    # 2. Usa o tamanho lido para ler os dados completos da imagem
    return ler_completo(sock, tamanho)

def enviar_mensagem(sock, dados):
    """
    Codifica o tamanho em 4 bytes e envia o cabeçalho junto com os dados usando sendall.
    """
    tamanho = len(dados)
    # Empacota o tamanho em 4 bytes (big-endian unsigned int '>I')
    cabecalho = struct.pack('>I', tamanho)
    
    # Envia o cabeçalho e o conteúdo usando sendall
    sock.sendall(cabecalho + dados)