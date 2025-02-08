# 3. Transformers

## Análise do artigo

O artigo [Attention is all you need](https://arxiv.org/abs/1706.03762), publicado em 2017 por Vaswani et al., introduz o **Transformer**, um novo modelo de redes neurais para tarefas de transdução de sequência, como tradução automática. Diferente dos modelos anteriores baseados em redes recorrentes (RNNs) ou convolucionais (CNNs), o Transformer se baseia inteiramente em **mecanismos de atenção**.

### Inovações

O **Transformer** representou uma mudança de paradigma em modelos de processamento de linguagem natural (NLP), substituindo redes neurais recorrentes (**RNNs**) e convolucionais (**CNNs**) pelo mecanismo de **self-attention**. Suas principais diferenças e vantagens em relação aos modelos anteriores incluem:

- **Paralelização** → Enquanto RNNs processam sequências palavra por palavra, o Transformer processa 
toda a sequência de uma vez, acelerando o treinamento.  
- **Atenção Global** → RNNs capturam dependências sequencialmente, enquanto o Transformer permite que cada palavra interaja diretamente com qualquer outra.  
- **Eficiência Computacional** → O Transformer reduz drasticamente o tempo de treinamento e melhora o desempenho em tradução, resumo e outras tarefas de NLP.

O Transformer revolucionou o NLP, dando origem a modelos como **BERT, GPT, T5 e outros**, que hoje dominam o campo de aprendizado de máquina e inteligência artificial.

## Arquitetura do transformer
A **arquitetura do Transformer** segue um modelo **encoder-decoder**, projetado para processar sequências de maneira eficiente, eliminando a recorrência e as convoluções usadas em modelos anteriores. Seu principal diferencial é o uso exclusivo do **mecanismo de atenção** para modelar relações entre palavras na sequência.



### **Estrutura Geral**

O Transformer é composto por duas grandes partes:

-   **Encoder (codificador)**: Processa a entrada e gera uma representação contextualizada.
-   **Decoder (decodificador)**: Utiliza essa representação para gerar a saída, palavra por palavra.

Cada um desses componentes é formado por **6 camadas idênticas**, contendo mecanismos de atenção e redes neurais totalmente conectadas.

----------

### **Componentes do Encoder**

O **encoder** recebe a sequência de entrada e passa por várias etapas de transformação. Cada uma das **6 camadas** do encoder contém:z

#### **Multi-Head Self-Attention**

-   Cada palavra da entrada pode interagir com todas as outras palavras da sequência.
-   Isso permite capturar relações de longo alcance entre palavras, algo difícil para RNNs.
-   Usa o **Scaled Dot-Product Attention**, onde cada palavra é representada como um vetor de **chave (key)**, **consulta (query)** e **valor (value)** para calcular a importância das palavras umas em relação às outras.

#### **Feed-Forward Network (Rede densa)**

-   Após a etapa de atenção, cada posição da sequência passa por uma rede totalmente conectada (MLP) independente das demais.
-   Essa rede possui uma camada oculta com ativação ReLU e uma camada final linear.

#### **Residual Connection e Normalização**

-   Para facilitar o aprendizado e a propagação do gradiente, as saídas do **self-attention** e da **rede feed-forward** são somadas às suas entradas originais antes da normalização.

----------

### **Componentes do Decoder**

O **decoder** recebe a saída do encoder e gera a sequência de saída passo a passo. Ele tem três subcamadas principais:

#### **Masked Multi-Head Self-Attention**

-   Similar à atenção do encoder, mas com um **mascaramento** que impede a atenção a palavras futuras, garantindo que o modelo gere a saída de forma autoregressiva.

#### **Encoder-Decoder Attention**

-   Conecta o encoder ao decoder, permitindo que cada posição da saída se atente às informações da entrada.

#### **Feed-Forward Network**

-   Igual à do encoder, aplicada independentemente a cada posição da sequência.

Assim como no encoder, cada subcamada do decoder também possui **conexões residuais e normalização**.

----------

### **Self-Attention e Multi-Head Attention**

O **self-attention** é um dos principais mecanismos do Transformer. Ele calcula pesos de atenção para cada palavra em relação às demais da sequência, permitindo que o modelo aprenda dependências de longo alcance.

Para aumentar a capacidade de aprendizado, o Transformer usa **Multi-Head Attention**, onde diferentes "cabeças" de atenção operam em subespaços distintos da representação, permitindo capturar diversos tipos de relações entre palavras.

----------

### **Positional Encoding**

Como o Transformer não possui recorrência, ele precisa de uma maneira de representar a ordem das palavras na sequência. Para isso, ele utiliza **positional encoding**, onde um vetor de senoides e cossenoides é somado às embeddings das palavras para indicar suas posições na sequência.

----------

### **Fluxo de Dados no Transformer**

1.  A sequência de entrada passa pelo **positional encoding** e pelas camadas do **encoder**, gerando uma representação contextualizada.
2.  O **decoder** recebe essa representação junto com as palavras já geradas e aplica suas camadas de atenção e feed-forward.
3.  O resultado final é passado por uma camada softmax, que gera probabilidades para a próxima palavra da saída.
4.  O processo se repete até que a sequência completa seja gerada.

----------

### **Vantagens do Transformer**

-   **Processamento Paralelo**: Como toda a sequência é processada de uma vez, o treinamento é muito mais rápido do que em RNNs.
-   **Melhor Capacidade de Capturar Dependências**: O self-attention permite aprendizado de relações entre palavras distantes na sequência.
-   **Eficiência Computacional**: Reduz a complexidade computacional em comparação com redes recorrentes.


## Resultados experimentais

O modelo **Transformer (big)** superou os melhores modelos anteriores no conjunto de dados WMT 2014 para tradução de inglês para alemão, alcançando um **BLEU de 28.4**, um aumento de mais de **2.0 BLEU** sobre o estado da arte anterior.
	 Para a tradução de inglês para francês, o modelo **big** atingiu um **BLEU de 41.0**, superando todos os modelos individuais anteriores com menos de **1/4 do custo de treinamento** do modelo anterior mais avançado.
-   O treinamento do Transformer (big) levou **3,5 dias** em **8 GPUs P100**.

| Modelo                           | BLEU (EN-DE) | BLEU (EN-FR) | Custo de treino (FLOPs) EN-DE | Custo de treino (FLOPs) EN-FR |
|---------------------------------|--------------|--------------|-----------------------------|-----------------------------|
| ByteNet                    | 23.75        | -            | -                           | 1.0 · 10²⁰                  |
| Deep-Att + PosUnk          | -            | 39.2         | -                           | 1.0 · 10²⁰                  |
| GNMT + RL                   | 24.6         | 39.92        | 2.3 · 10¹⁹                  | 1.4 · 10²⁰                  |
| ConvS2S                      | 25.16        | 40.46        | 9.6 · 10¹⁸                  | 1.5 · 10²⁰                  |
| MoE                         | 26.03        | 40.56        | 2.0 · 10¹⁹                  | 1.2 · 10²⁰                  |
| Deep-Att + PosUnk Ensemble  | -            | 40.4         | -                           | 8.0 · 10²⁰                  |
| GNMT + RL Ensemble         | 26.30        | 41.16        | 1.8 · 10²⁰                  | 1.0 · 10²¹                  |
| ConvS2S Ensemble             | 26.36        | 41.29        | 7.7 · 10¹⁹                  | 1.2 · 10²¹                  |
| **Transformer (base model)**     | **27.3**     | **38.1**     | **3.3 · 10¹⁸**              | -                           |
| **Transformer (big)**            | **28.4**     | **41.8**     | **2.3 · 10¹⁹**              | -                           |
 ### Resultado do teste F1
 A tabela mostram que, apesar da falta de ajuste específico para a tarefa, o modelo apresenta um desempenho surpreendentemente bom, superando todos os modelos previamente relatados, com exceção da Recurrent Neural Network Grammar .

Em contraste com os modelos RNN de sequência para sequência , o Transformer supera o Berkeley-Parser [29] mesmo quando treinado apenas no conjunto de treinamento WSJ, composto por 40 mil sentenças.

| Parser                                | Training                  | WSJ 23 F1 |
|---------------------------------------|---------------------------|-----------|
| Vinyals & Kaiser et al. (2014)   | WSJ only, discriminative  | 88.3      |
| Petrov et al. (2006)             | WSJ only, discriminative  | 90.4      |
| Zhu et al. (2013)                | WSJ only, discriminative  | 90.4      |
| Dyer et al. (2016)                | WSJ only, discriminative  | 91.7      |
| **Transformer (4 layers)**            | WSJ only, discriminative  | **91.3**  |
| Zhu et al. (2013)                | semi-supervised           | 91.3      |
| Huang & Harper (2009)            | semi-supervised           | 91.3      |
| McClosky et al. (2006)           | semi-supervised           | 92.1      |
| Vinyals & Kaiser et al. (2014)  | semi-supervised           | 92.1      |
| **Transformer (4 layers)**            | semi-supervised           | **92.7**  |
| Luong et al. (2015)             | multi-task                | 93.0      |
| Dyer et al. (2016)               | generative                | 93.3      |

## Implementação


### Passo 1: Instalar dependências

Certifique-se de ter o TensorFlow instalado:
