# Mobility-Cars

<div align="center">
<img src="images/capa.webp" width="700px">
</div>
</br>

# 1. Problema de Negócio
  
<img src="images/vendedor_de_carros.jpeg" width="300px" align='right'>
<p align = 'left'>

A Mobility Cars é uma empresa tradicional do segmentos de compra e venda de veículos. Basicamente seu modelo de negócio consiste em comprar veículos usados no mercado e revende-los à outros motoristas. 

Com dificuldades de atingir suas metas de vendas, a Mobility Cars tem procurado estratégias para alavancar ainda mais sua revenda de carros, visando ampliar sua receita para então renovar sua frota de veículos. Para isso, ela decidiu agir com maior inteligência no momento da revenda dos carros

<br>
<img src="images/venda_de_carro.jpg" width="350px" align='left'>

<p align = 'right'>

No mercado de Venda de Automóveis, a tabela FIPE é uma referência fundamental para todas as regociações envolvendo veículos usados, semi-novos e novos. Criada pela Fundação Instituto de Pesquisas Econômicas (FIPE), contempla o preço médio de veículos anunciados pelos vendedores no mercado nacional, porém, a tabela FIPE não necessariamente reflete os preços finais de negociação dos veículos e por isso não costuma ser uma referência assertiva para os valores praticados no mercado

Para gerar mais inteligência no processo de vendas, a Mobility Cars busca uma forma mais assertiva, baseada no comportamento do mercado, de prever o valor das negociações. Tendo uma referência de preço mais fidedigna, baseada nos valores praticados no mercado, será possível sair na frente nas negociações, se planejar financeiramente e ser mais rápido no processo venda.

Assim, a Mobility Cars contratou um time de cientista de dados para a construção de um modelo predição de valor de venda de automóveis.

# 2. Estratégia de Solução

Este projeto foi desenvolvido baseado na metodologia CRISP-DM (*Cross Industry Standard Process for Data Mining)* que consiste em um conjunto de etapas para a execução de um projeto de ciência de dados. A vantagem desse método é que possui uma metodologia cíclica, permitindo uma rápida entrega de valor para as áreas envolvidas.

Neste projeto, o CRISP-DM foi desenvolvido em 9 etapas que são ilustradas e detalhadas abaixo:

<img src="images/CRISP-DM.png" width="300px" align='right'>

## 1.1. Questão de Negócio
Nesta etapa, nos deparamos com a questão de negócio que irá nortear todo o projeto. No caso deste projeto, essa questão é a situação da Mobility Cars que foi ilustrada no tópico anterior, onde a Mobility Cars ve a necessidade de aumentar as suas vendas. Para isso, enxerga a oportunidade de não ter como referência apenas a tabela FIPE que serve como referência para a venda de qualquer veículo novo e semi-novo

## 1.2. Entendimento do Negócio
Com a questão de negócio em mente, precisamos entender: como podemos solucionar esse problema? Foi sugerido a construção de um modelo preditivo de preço de venda dos carros, mas será que essa realmente seria a melhor solução? Nesta etapa precisamos questionar as soluções em vista antes de iniciarmos o desenvolvimento. No caso deste projeto, entendemos que prever o preço de venda dos veículos seria uma vantagem competitiva muito importante para a Mobility Cars, que solucionaria a dor que foi trazida pela empresa, e ,por isso, essa é a solução que irá nortear todo o projeto

## 1.3. Coleta de Dados
Nesta etapa, serão coletados dados de diversas fontes para gerar um conjunto de dados robusto para o desenvolvimento do projeto.

## 1.4. Descrição dos Dados
Nesta fase, o principal objetivo é fazer a limpeza dos dados, o que envolveu principalmente:
  1. **Descrição dos Dados:** Foram checados os tipos das váriáveis disponíveis no conjunto de dados e transformados para os tipos mais convenientes.
  2. **Filtragem dos Dados:** A conjuto de dados possui uma série de colunas com uma grande quantidade de valores nulos. Por entender que essas colunas não trariam valor significativo para o projeto e que demandariam muito esforço para seu tratamento, elas foram removidas do dataset
        
## 1.5. Feature Engineering
Com o objetivo que facilitar a futura etapa de análise exploratória de dados, foram criadas uma série de features baseadas nas variáveis já presentes no dataset. Nessa etapa, a ideia é deixar as variáveis explicitas e de fácil acesso para as análises que serão feitas ao longo do projeto
    
## 1.6. *Exploração dos Dados*
Para avaliar o comportamento das variáveis em relação à si mesmas e à variável resposta, foi realizada uma exploração dos dados, focando em análises univariadas, para entender brevemente a distruibuição das variáveis, e em análises bivariadas, para entender como a variável em questão impacta na variável resposta.
    
## 1.7. *Modelagem dos dados*
Para a apliação de algoritmos de Machine Learning é necessário transformar todas as variáveis em variáveis numéricas. Este dataset em particular possui uma grande quantidade de variáveis categoricas, portanto, foram aplicados técnicas de Encoding. Para as variáveis numéricas presentes, foram aplicadas técnicas de Rescaling
    
Para a escolha das técnicas de Rescalings e Encoding, os critérios utilizados foram:
1. Robust Scaler: Para variáveis com muito outliers
2. Frequency Encode: Para variáveis onde se entende que sua frequencia está relacionada com a variável resposta
3. Target Encode: Para variáveis que possuiam muitas categorias
4. One Hot Encode: Para variáveis que representem uma ideia de estado
        
## 1.8. Feature Selection
Aqui, foram selecionadas as features mais relevantes para o modelo baseado em duas metodologias: Boruta e Importancia das Árvores

## 1.9. *Algoritmos de Machine Learning*
Nesta fase foram testados 4 modelos de machine learning para o desenvolvimento da solução

## 1.10. *Avaliação do Algoritmo*
Os algoritmos testados foram avaliados com base nas métricas de erro mais comuns em regressão (MAE, MAPE e RMSE) e então o melhor modelo foi adotado

## 1.11. Hyperparameters Fine Tuning
Após a escolha do melhor modelo para o nosso projeto, nesta etapa foram selecionados os parametros para o modelo que maximizam os resultados

## 1.12. *Modelo em Produção*
O modelo foi publicado em um ambiente cloud chamado [Render.com](http://Render.com) para que outras pessoas e serviços possam consultá-lo e utilizar suas predições para tomar melhores decisões
