# Detecção de Vulnerabilidades em Código-Fonte

Projeto de aprendizado de máquina voltado à identificação automatizada de vulnerabilidades de segurança em código-fonte C/C++.

A solução utiliza o modelo Transformer **GraphCodeBERT**, pré-treinado para compreensão de código, como base para a classificação binária de funções entre código seguro e código potencialmente vulnerável.

O projeto também compara diferentes estratégias de pooling para avaliar como a representação produzida pelo modelo influencia o desempenho da classificação.

## Visão geral

A revisão manual de código pode ser um processo demorado, principalmente em projetos de grande escala. Este projeto investiga a utilização de modelos de aprendizado profundo como uma camada adicional de análise durante a identificação de possíveis vulnerabilidades.

O processo pode ser resumido em quatro etapas:

```text
Código-fonte
     |
     v
Tokenização
     |
     v
GraphCodeBERT
     |
     v
Estratégia de Pooling
     |
     v
Classificação
     |
     +---- 0: Seguro
     |
     +---- 1: Vulnerável
```

O modelo recebe uma função como entrada e produz uma classificação binária indicando se o código apresenta características associadas a uma vulnerabilidade.

## Arquitetura

O projeto utiliza o GraphCodeBERT como extrator de características. A saída do Transformer é processada por diferentes estratégias de pooling antes de ser encaminhada ao classificador.

Foram implementadas cinco abordagens:

| Estratégia        | Descrição                                                        |
| ----------------- | ---------------------------------------------------------------- |
| Mean Pooling      | Calcula a média das representações dos tokens                    |
| Max Pooling       | Seleciona os maiores valores das representações                  |
| CLS Pooling       | Utiliza a representação associada ao token CLS                   |
| AvgMax Pooling    | Combina as representações obtidas por média e máximo             |
| Attention Pooling | Utiliza pesos de atenção para determinar a relevância dos tokens |

A comparação entre essas estratégias permite avaliar diferentes formas de transformar a representação gerada pelo Transformer em uma entrada adequada para classificação.

## Métricas

O treinamento utiliza diferentes métricas para avaliar o desempenho dos modelos:

* Precision
* Recall
* F1-Score
* Matriz de Confusão

Além da avaliação, o projeto implementa mecanismos de early stopping e salvamento dos melhores checkpoints durante o treinamento.

## Dataset

Os dados utilizados seguem uma estrutura simples baseada em funções de código-fonte e seus respectivos rótulos.

O formato esperado é:

```json
[
    {
        "func": "void vulnerable() { char buf[10]; gets(buf); }",
        "target": 1
    },
    {
        "func": "void safe() { char buf[10]; fgets(buf, 10, stdin); }",
        "target": 0
    }
]
```

Os valores de `target` representam:

```text
0 = Seguro
1 = Vulnerável
```

O projeto utiliza uma versão parcial do dataset associado ao **Devign**, podendo também ser adaptado para outros conjuntos de dados ou bases próprias de código rotulado.

## Estrutura do projeto

```text
vulnerability-detection-codet5/
│
├── vulnerability_detection_improved.py
├── inference_example.py
├── sample_data.json
├── requirements.txt
├── setup.sh
└── README.md
```

### Principais arquivos

**vulnerability_detection_improved.py**

Contém a implementação principal do treinamento, avaliação e comparação das estratégias de pooling.

**inference_example.py**

Fornece um exemplo de utilização de um modelo treinado para realizar previsões sobre novas funções.

**sample_data.json**

Contém exemplos de dados utilizados para demonstrar o formato esperado pelo sistema.

**requirements.txt**

Lista as dependências necessárias para executar o projeto.

**setup.sh**

Script auxiliar para configuração do ambiente.

## Requisitos

Para executar o projeto são necessários:

* Python 3.8 ou superior
* PyTorch
* Transformers
* Bibliotecas listadas em `requirements.txt`
* 8 GB ou mais de RAM
* GPU compatível com CUDA recomendada para treinamento

O projeto também pode ser executado em CPU, embora o treinamento possa ser significativamente mais lento.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/ShamaSharma/vulnerability-detection-codet5.git
cd vulnerability-detection-codet5
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

Com o ambiente configurado e o dataset preparado, execute:

```bash
python vulnerability_detection_improved.py
```

O processo de treinamento executa os modelos utilizando as diferentes estratégias de pooling e armazena os melhores checkpoints.

Os resultados também podem ser utilizados para comparar o desempenho das abordagens utilizadas.

## Inferência

Após o treinamento, o modelo pode ser utilizado para analisar novas funções.

Exemplo:

```python
from inference_example import predict_vulnerability

code = """
void test() {
    char buffer[10];
    strcpy(buffer, input);
}
"""

result = predict_vulnerability(code)

print(f"Vulnerable: {result['is_vulnerable']}")
print(f"Confidence: {result['confidence']:.2%}")
```

A saída contém uma classificação e uma estimativa de confiança produzida pelo modelo.

A confiança não deve ser interpretada como uma garantia de que o código é seguro ou vulnerável. O resultado deve ser utilizado como suporte para processos adicionais de análise e revisão.

## Aplicações

A abordagem utilizada neste projeto pode servir como base para diferentes aplicações relacionadas à segurança de software, incluindo:

* Análise automatizada de código-fonte
* Auxílio em processos de Code Review
* Pesquisa em segurança de software
* Classificação de código utilizando modelos Transformer
* Experimentação com Machine Learning aplicado à Cybersecurity
* Desenvolvimento de ferramentas de análise estática baseadas em IA
* Integração futura com pipelines de CI/CD

## Possíveis extensões

O projeto pode ser expandido para investigar diferentes modelos, datasets e técnicas de classificação.

Algumas possibilidades incluem:

* Comparação entre GraphCodeBERT, CodeBERT e CodeT5
* Utilização de datasets maiores
* Classificação por categorias específicas de vulnerabilidade
* Análise de arquivos completos
* Desenvolvimento de uma API para inferência
* Criação de uma interface web
* Integração com ferramentas de CI/CD
* Geração de explicações para as previsões
* Combinação de análise estática tradicional com modelos de aprendizado profundo

## Limitações

O modelo não substitui ferramentas especializadas de análise de segurança nem revisão realizada por profissionais.

Como qualquer sistema de classificação baseado em aprendizado de máquina, os resultados podem apresentar falsos positivos e falsos negativos. O desempenho também depende diretamente da qualidade, diversidade e representatividade dos dados utilizados durante o treinamento.

Consequentemente, as previsões devem ser consideradas como um mecanismo de apoio à análise e não como uma confirmação definitiva da existência ou ausência de uma vulnerabilidade.

## Objetivo do projeto

O objetivo principal é investigar a aplicação de modelos Transformer especializados em código para a detecção automatizada de vulnerabilidades e avaliar diferentes estratégias de representação para essa tarefa.

O projeto combina conceitos de:

```text
Machine Learning
Deep Learning
Transformers
Processamento de Código
Cybersecurity
Classificação de Texto
Análise de Vulnerabilidades
```

## Referências

* GraphCodeBERT — modelo Transformer pré-treinado para compreensão de código.
* Devign — conjunto de dados utilizado para pesquisas relacionadas à detecção de vulnerabilidades.
* Hugging Face Transformers — biblioteca utilizada para trabalhar com modelos Transformer.

## Licença

Consulte a licença disponibilizada no repositório antes de utilizar, modificar ou redistribuir o projeto.
