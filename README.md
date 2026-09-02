# Security Code Analyzer

Ferramenta experimental de análise de segurança desenvolvida em Python para identificar possíveis vulnerabilidades em funções escritas em C e C++ por meio de aprendizado de máquina.

O sistema utiliza o **GraphCodeBERT** para transformar o código-fonte em representações vetoriais e, a partir dessas representações, realizar uma classificação entre código potencialmente seguro e código potencialmente vulnerável.

## Sobre o projeto

A identificação de vulnerabilidades diretamente no código-fonte é uma tarefa que pode exigir uma análise detalhada de grandes quantidades de código.

Este projeto explora uma abordagem baseada em Machine Learning na qual um modelo especializado em código aprende padrões presentes em exemplos previamente classificados.

O objetivo não é substituir ferramentas tradicionais de análise de segurança, mas demonstrar como modelos de linguagem para código podem ser utilizados como uma camada complementar de análise.

## Fluxo de processamento

O funcionamento pode ser dividido em quatro etapas:

```text
Codigo C/C++
     |
     v
Tokenizacao
     |
     v
GraphCodeBERT
     |
     v
Representacao do codigo
     |
     v
Classificador
     |
     +--------> Seguro
     |
     +--------> Vulneravel
```

Durante o treinamento, diferentes estratégias são utilizadas para transformar a saída do Transformer em uma representação adequada para o classificador.

## Estratégias de representação

O projeto permite comparar cinco métodos de pooling:

### Mean Pooling

Calcula a média das representações produzidas para os tokens do código.

### Max Pooling

Seleciona os maiores valores encontrados nas representações dos tokens.

### CLS Pooling

Utiliza a representação associada ao token de classificação.

### AvgMax Pooling

Combina informações obtidas por Mean Pooling e Max Pooling.

### Attention Pooling

Utiliza pesos de atenção para determinar quais partes da representação possuem maior relevância para a classificação.

A comparação dessas abordagens permite avaliar como diferentes formas de agregação das informações influenciam o resultado final do modelo.

## Classificação

O sistema utiliza uma classificação binária:

```text
0 = Seguro
1 = Vulneravel
```

Os exemplos de treinamento são armazenados em formato JSON, contendo o código da função e seu respectivo rótulo.

Exemplo:

```json
[
    {
        "func": "void example() { ... }",
        "target": 0
    },
    {
        "func": "void example() { ... }",
        "target": 1
    }
]
```

O arquivo `sample_data.json` fornece exemplos do formato esperado pelo sistema.

## Avaliação

O desempenho do modelo é analisado utilizando métricas comuns em problemas de classificação:

* Precision
* Recall
* F1-Score
* Matriz de Confusão

Também são utilizados mecanismos de **early stopping** e armazenamento dos melhores checkpoints durante o treinamento.

Essas métricas permitem avaliar não apenas a quantidade de classificações corretas, mas também a capacidade do modelo de identificar corretamente exemplos vulneráveis.

## Organização

```text
Security-code-analyzer/
|
+-- vulnerability_detection_improved.py
|       Treinamento e avaliacao dos modelos
|
+-- inference_example.py
|       Exemplo de inferencia
|
+-- sample_data.json
|       Dados de exemplo
|
+-- requirements.txt
|       Dependencias Python
|
+-- setup.sh
|       Configuracao auxiliar
|
+-- README.md
        Documentacao
```

## Ambiente

O projeto utiliza:

| Componente    | Funcao                                |
| ------------- | ------------------------------------- |
| Python        | Desenvolvimento da aplicacao          |
| PyTorch       | Treinamento dos modelos               |
| Transformers  | Utilizacao de modelos Transformer     |
| GraphCodeBERT | Representacao do codigo-fonte         |
| JSON          | Armazenamento dos exemplos            |
| CUDA          | Aceleracao por GPU, quando disponivel |

Uma GPU compatível com CUDA é recomendada para reduzir o tempo de treinamento, embora o projeto também possa ser executado utilizando CPU.

## Configuração

Clone este repositório:

```bash
git clone https://github.com/SeraphimBite/Security-code-analyzer.git
cd Security-code-analyzer
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Treinamento

Com o ambiente configurado, o treinamento pode ser iniciado com:

```bash
python vulnerability_detection_improved.py
```

O programa executa o treinamento das diferentes estratégias de pooling e permite comparar os resultados obtidos por cada abordagem.

Os melhores estados dos modelos são preservados durante o processo para utilização posterior.

## Inferência

Depois de treinado, o modelo pode ser utilizado para analisar novas funções.

Um exemplo básico:

```python
from inference_example import predict_vulnerability

code = """
void test() {
    char buffer[10];
    strcpy(buffer, input);
}
"""

result = predict_vulnerability(code)

print(result["is_vulnerable"])
print(result["confidence"])
```

O resultado fornece uma classificação juntamente com uma estimativa de confiança.

Essa estimativa deve ser interpretada como uma saída probabilística do modelo e não como uma comprovação definitiva da existência ou ausência de uma vulnerabilidade.

## Dataset

O projeto trabalha com exemplos de funções de código-fonte acompanhadas por rótulos de segurança.

A estrutura foi preparada para trabalhar com conjuntos de dados voltados à detecção de vulnerabilidades, incluindo dados no formato utilizado em pesquisas relacionadas ao **Devign**.

O sistema também pode ser adaptado para conjuntos de dados próprios, desde que os exemplos sigam a estrutura esperada pelo treinamento.

## Casos de uso

A implementação pode ser utilizada como base para:

* Estudos de Machine Learning aplicado à segurança;
* Classificação automatizada de código;
* Pesquisa em detecção de vulnerabilidades;
* Experimentação com Transformers para código;
* Desenvolvimento de ferramentas de apoio a Code Review;
* Avaliação de diferentes estratégias de representação de código.

## Limitações

O modelo possui limitações inerentes a sistemas de aprendizado de máquina.

Uma previsão pode resultar em:

* falso positivo;
* falso negativo;
* baixa confiança;
* desempenho inferior em códigos diferentes daqueles utilizados no treinamento.

A qualidade do modelo também depende da quantidade, diversidade e qualidade dos exemplos utilizados no treinamento.

Por esse motivo, os resultados devem ser utilizados como **auxílio à análise**, e não como substituição de ferramentas especializadas ou revisão de segurança.

## Possíveis evoluções

O projeto pode ser ampliado com diferentes técnicas e componentes, incluindo:

* utilização de datasets maiores;
* classificação por tipo de vulnerabilidade;
* comparação com outros modelos especializados em código;
* análise de arquivos completos;
* criação de uma API de inferência;
* desenvolvimento de uma interface web;
* integração com pipelines de CI/CD;
* geração de explicações para as previsões;
* combinação com ferramentas tradicionais de análise estática.

## Referências técnicas

O projeto utiliza tecnologias e conceitos provenientes de pesquisas e ferramentas públicas relacionadas a:

* GraphCodeBERT;
* Transformers;
* PyTorch;
* detecção de vulnerabilidades em código;
* aprendizado profundo aplicado à análise de software.

Essas referências representam as tecnologias utilizadas pelo projeto e não indicam que este repositório seja uma cópia ou um fork de outro projeto.

## Licença

Consulte os arquivos de licença presentes neste repositório antes de utilizar, modificar ou redistribuir o código.
