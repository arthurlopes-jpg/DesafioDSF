# DesafioDSF - Processamento de Imagens


# Processamento de Imagens


## Como rodar
1. Instale as libs: `pip install -r requirements.txt`
2. Abra dois terminais: rode `python servidor.py` em um e `python cliente.py` no outro.

## Testes Manuais
1. **Com face:** Cliente recebeu a imagem com retângulos verdes. [tests/com_face.png]
2. **Sem face:** A imagem retornou normal, sem marcações. [tests/sem_face.png]
3. **Dois clientes:** Com o `time.sleep(5)`, o servidor atendeu os dois ao mesmo tempo sem travar (ver prints do terminal). [tests/dois_clientes.png]

## Respostas

1. **Onde o tamanho da imagem é enviado e como o laço sabe que recebeu tudo?**
O tamanho vai em um cabeçalho de 4 bytes via `protocolo.py`. O laço `while` usa `recv` repetidamente até a quantidade de dados recebida bater com o tamanho informado no cabeçalho.

2. **Onde a thread é criada e por que o servidor pode atender outro cliente enquanto a primeira espera?**
A thread é criada no `while True` do servidor logo após o `accept()`. Como não usamos `join()`, o código principal não fica travado esperando a thread terminar e já volta a escutar novos clientes.

3. **Diferença entre commit, push e PR?**
**Commit** salva a alteração no seu PC. **Push** envia isso pra sua branch no GitHub. **PR (Pull Request)** é o pedido para juntar o código da sua branch com a principal (`main`).

## Uso de IA
Usamos IA para ajudar com erros do Git, separar os código nos arquivos da pasta `utils` e aplicar o `threading` no servidor. A parte que exigiu mais atenção foi entender como o laço `while` de leitura do protocolo não bloqueava a rede.
