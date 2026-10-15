import struct

def ler_completo(sock, total_esperado):
    """
    Acumula os retornos de recv até completar o total esperado.
    """
    dados = b''
    while len(dados) < total_esperado:
        # Pede no máximo os bytes que faltam
        pacote = sock.recv(total_esperado - len(dados))
        if not pacote: # Se retornar vazio, a ligação caiu
            return None 
        dados += pacote
    return dados

def receber_mensagem(sock):
    """
    Lê os 4 bytes do cabeçalho para descobrir o tamanho, depois lê a imagem.
    """
    # Lê os 4 bytes de cabeçalho
    cabecalho = ler_completo(sock, 4)
    if not cabecalho:
        return None
        
    # Desempacota usando big-endian unsigned int ('>I')
    tamanho = struct.unpack('>I', cabecalho)[0]
    
    # Lê o restante da mensagem com o tamanho descoberto
    return ler_completo(sock, tamanho)

def enviar_mensagem(sock, dados):
    """
    Empacota o tamanho da mensagem em 4 bytes e envia tudo com sendall.
    """
    tamanho = len(dados)
    # Codifica o tamanho em 4 bytes (big-endian unsigned int)
    cabecalho = struct.pack('>I', tamanho)
    
    # Envia cabeçalho + dados da imagem
    sock.sendall(cabecalho + dados)