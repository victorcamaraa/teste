# A Abrangência do Modelo de Acessibilidade em Governo Eletrônico e a Inclusão de Pessoas com Deficiência: Um Estudo Comparativo com a WCAG

## Acessibilidade Digital e Inclusão: Um Estudo sobre a Equidade nas Diretrizes WCAG e a eMAG brasileira

### 1. Introdução

Com o avanço das tecnologias, as sociedades têm adaptado cada vez mais suas atividades, dividindo-as entre serviços presenciais e digitais [15][16]. Essa crescente demanda por serviços por meio de diversos canais de comunicação tem levado tanto os prestadores de serviços, quanto a esferas governamentais a intensificarem seus esforços, oferecendo alternativas de acesso digital aos cidadãos para facilitar o atendimento [19].  No entanto, ainda existem muitas limitações no que se refere ao alcance desses serviços para todas as pessoas, especialmente para grupos vulneráveis, que se encontram à margem da inclusão digital, também conhecida como "digital divide" [17][8]. Entre esses grupos estão as pessoas com deficiência, que, por exemplo, muitas vezes não utilizam os serviços digitais do governo devido a dificuldades em navegar pela internet [17] ou em websites de governo eletrônico [4][8]. Estima-se que cerca de 16% da população mundial tenha algum tipo de deficiência que pode impactar diretamente o uso eficiente da web, o que equivale a 1 a cada 6 pessoas [18]. Entre essas deficiências estão as auditivas, cognitivas, físicas, de fala e visuais [1][11], o que ressalta a urgência de criar um ambiente digital acessível, especialmente no contexto de governo digital. 

Sabe-se que atualmente há um esforço mundial para que não se caracterize os indivíduos por suas deficiências, saindo do modelo biomédico de categorização para a implementação paulatina do CIF (Classificação Internacional de Funcionalidade, Incapacidade e Saúde) que classifica a deficiência de forma mais ampla. Contudo, no contexto da programação web, caracterizar personas torna-se fundamental para que os desenvolvedores consigam construir páginas acessíveis por todos. 

Como afirma Tim Berners-Lee, diretor do W3C e criador da World Wide Web: " The power of the Web is in its universality. Access by everyone regardless of disability is an essential aspect.". O acesso à Web, ao eliminar barreiras de comunicação, permite que as informações governamentais cheguem de maneira mais eficaz a toda a população [3][4]. Entretanto, garantir a acessibilidade total dos sites é um desafio contínuo para os governos, desenvolvedores e designers, visto que os métodos de desenvolvimento tradicionais não são suficientes para atender às inúmeras especificidades exigidas por um desenvolvimento acessível. Isso porque muitas pessoas com deficiência precisarão de mais de um tipo de auxílio para melhorar sua autonomia na web [19][2]. Para lidar com esse desafio, a W3C criou a WCAG (Web Content Accessibility Guidelines), um padrão internacional que busca atender às necessidades de grupos com deficiências no uso da Web [6]. A WCAG é composta por critérios de sucesso que definem níveis de acessibilidade (A, AA e AAA) e frequentemente serve como base para que os países desenvolvam suas próprias diretrizes de acessibilidade, que podem ou não ser adotadas como lei [6]. Com esse mesmo objetivo, o Brasil desenvolveu o Modelo de Acessibilidade em Governo Eletrônico (eMAG) em 2004 [5], a fim de orientar a criação de portais governamentais acessíveis, buscando contemplar as diversas deficiências de maneira eficiente. A versão mais recente dessa diretriz, eMAG 3.1, foi desenvolvida com base na WCAG 2.0 [7]. 

### 2. Trabalhos Relacionados e Motivação

pesar dos avanços proporcionados pela WCAG, como a implementação de leis de acessibilidade digital em paises que adotaram diretrizes de acessibilidade baseados nela [33][34][35], como a eMAG no Brasil, ainda há uma lacuna importante na investigação da equidade na distribuição dessas diretrizes entre os diferentes tipos de deficiência. A acessibilidade digital é essencial não apenas para garantir o acesso igualitário à informação, mas também para promover a participação plena de todas as pessoas na sociedade contemporânea, especialmente em um contexto em que os serviços digitais são cada vez mais necessários para o exercício da cidadania (CITAÇÃO TRABALHOS DE CIDADANIA DIGITAL). No entanto, a verdadeira inclusão digital vai além da mera presença de serviços online — ela demanda a construção de um ambiente virtual que atenda às necessidades de todos os cidadãos, inclusive aqueles que convivem com deficiências.  

As diretrizes de acessibilidade, como a WCAG, a Section 508 nos Estados Unidos [32], a Diretriz Francesa de Acessibilidade [30] e o European Accessibility Act [31], além do Modelo de Acessibilidade em Governo Eletrônico (eMAG) no Brasil, representam esforços globais e nacionais para criar condições equitativas de acesso à web. Contudo, a pluralidade de deficiências — sejam elas visuais, auditivas, físicas, cognitivas ou de outra natureza — demanda soluções personalizadas, que nem sempre recebem o mesmo nível de atenção ou priorização. Essa realidade levanta o questionamento se de fato todas as deficiências estão sendo contempladas de maneira justa. 

Uma abordagem equitativa na criação de políticas de acessibilidade digital é essencial para garantir que as tecnologias, que desempenham um papel cada vez mais central em nossas vidas, sejam acessíveis para todos. Ao investigar como a eMAG e a WCAG tratam as diferentes necessidades de pessoas com deficiência, pode-se identificar potenciais disparidades e, com isso, aprimorar as diretrizes para uma inclusão mais abrangente.  

A partir desse contexto, este estudo propõe realizar um mapeamento das deficiências abordadas pelos critérios de sucesso da WCAG, possibilitando, assim, o cruzamento dessas informações com o modelo brasileiro, questionando se algumas deficiências recebem mais atenção que outras e como isso pode impactar a inclusão digital. Essa preocupação também se aplica às diretrizes da WCAG, que serão analisadas paralelamente no artigo para proporcionar uma base comparativa e avaliar possíveis disparidades no tratamento das diversas deficiências. Nesse sentido, tem-se a pergunta que orienta esse artigo:  A eMAG atual adota uma abordagem equitativa em suas diretrizes no que se refere aos diferentes tipos de deficiência?  Quais são os tipos de deficiência mais frequentemente contemplados? 

Essas questões são fundamentais para oferecer uma visão abrangente que permita aos gestores e responsáveis pela formulação de políticas públicas refletirem sobre as áreas que ainda necessitam de atenção. Ao identificar essas lacunas, espera-se contribuir para o aprimoramento das diretrizes de acessibilidade, promovendo uma inclusão digital mais ampla e justa, que contemple a diversidade de pessoas com deficiência no Brasil, promovendo mais equidade para essas pessoas. Dessa forma, este estudo busca não apenas analisar as diretrizes existentes, mas também incentivar uma reflexão crítica sobre a aplicação dessas normas e o quanto elas estão ajustadas às necessidades reais da população.
Para mapear e relacionar cada critério de sucesso à um tipo de deficiência, este estudo adotou uma abordagem qualitativa e quantitativa descritiva. Na abordagem qualitativa, a coleta de dados foi realizada por meio de uma revisão documental das diretrizes da WCAG 2.0 e do eMAG 3.1.

### Background


#### Inclusão, Acessibilidade Digital, Equidade e o Desenvolvimento de sites 

 

A inclusão digital é um conceito que vai muito além do simples acesso à internet. Trata-se da capacidade de todos, especialmente daqueles em situações de vulnerabilidade, de utilizarem as ferramentas digitais de forma cidadã, promovendo autonomia e integração social [27] (outras referências).  

 

Nesse sentido, a acessibilidade digital pode contribuir para a inclusão já que ela visa remover barreiras e oferecer um ambiente igualitário e justo para pessoas com deficiências físicas, sensoriais, cognitivas ou múltiplas [27]. No entanto, essa "igualdade" não significa que todas as deficiências demandem os mesmos recursos ou esforços. Algumas deficiências, como as visuais, historicamente têm recebido mais atenção do que outras [25, 26]. Enquanto pessoas com deficiências visuais e auditivas contam com soluções relativamente estabelecidas, como legendas em vídeos e descrições textuais, os desafios enfrentados por aqueles com deficiências cognitivas são de outra ordem. Navegação simplificada, conteúdos claros e uma estrutura intuitiva são essenciais para esse público, mas as tecnologias e diretrizes voltadas para essas necessidades ainda estão em desenvolvimento. Estudos, como o de [26], evidenciam que a conformidade com as diretrizes de acessibilidade muitas vezes falha ao abordar de maneira eficaz todas as deficiências, especialmente as cognitivas. [25] reforça os achados de [26] enfatizando que as deficiências perceptuais (visão e audição) e físicas, têm sido mais abordadas pela tecnologia, mas as deficiências cognitivas continuam sendo um grande desafio. Além disso, seu artigo aponta para a importância de uma abordagem multissetorial, incluindo o governo, organizações e defensores, para melhorar a acessibilidade de maneira geral.  

 

No processo de acessibilidade digital, então, busca-se a equidade, ou seja, a garantia que todos tenham as mesmas oportunidades de acesso e sucesso nas plataformas digitais, independentemente de suas condições. Isso inclui, por exemplo, garantir que tanto as deficiências visuais quanto as cognitivas tenham adaptações adequadas e personalizadas, promovendo um ambiente digital verdadeiramente inclusivo [28]. 

 

Nesse sentido, conhecer esse público-alvo, bem como suas necessidades, é essencial para que desenvolvedores, designers e criadores de conteúdo possam oferecer uma experiência digital acessível e inclusiva. Diretrizes como a WCAG e eMAG orientam os profissionais nesse processo, fornecendo parâmetros claros sobre como garantir a acessibilidade para todos. Essas normas ajudam a eliminar barreiras e promovem um ambiente digital mais justo, onde cada pessoa, independentemente de suas limitações, pode acessar informações e serviços de maneira plena. 

  

Por meio da eMAG, o governo brasileiro tem buscado aplicar esses princípios acessíveis no desenvolvimento de plataformas governamentais. Contudo, a análise crítica dessas diretrizes é fundamental para garantir que nenhuma deficiência seja negligenciada. O papel do governo, nesse contexto, vai além da simples adoção dessas normas. Ele deve promover políticas públicas que assegurem a equidade na aplicação dessas diretrizes, garantindo que a inclusão digital seja plena para todos.  
### 3. Metodologia   

Para mapear e relacionar cada critério de sucesso à um tipo de deficiência, este estudo adotou uma abordagem qualitativa e quantitativa descritiva [29]. Na abordagem qualitativa, a coleta de dados foi realizada por meio de uma revisão documental das diretrizes da WCAG 2.0 e do eMAG 3.1. Os documentos foram analisados para identificar os critérios de acessibilidade e categorizá-los por tipo de deficiência (visual, auditiva, física, cognitiva etc.) de acordo com a classificação já determinada pela W3C [9] [10] [12] [13] [14]. Nesse sentido, tanto as diretrizes da WCAG (perceptível, Robusto, Operável e entendivel), quanto o documento correspondente no Brasil, a e-MAG, foram analisadas para se entender 
quantitativamente o direcionamento dos critérios estabelecidos. Para essa categorização utilizou-se a classificação padronizada pela W3C, conforme o quadro 1.
#### Quadro 1 – Tipos de deficiência (W3C, 2024)


| Deficiência | Característica |
|-------------|---------------|
| Auditory | "Auditory disabilities range from mild or moderate hearing loss in one or both ears..." |
| Cognitive and learning | "Cognitive and learning disabilities affect how people store, retrieve, or use information..." |
| Physical | "Physical disabilities include weakness and limitations of muscular control..." |
| Speech | "Speech disabilities include difficulty producing speech that is recognizable..." |
| Visual | "Visual disabilities range from mild or moderate vision loss in one or both eyes..." |

#### Quadro 2- Equiparação dos dados e-MAG e WCAG

| e-Mag 3.1 | WCAG 2.0 |
|-----------|----------|
| Recomendação 1.1 – Respeitar os Padrões Web | Critérios de Sucesso 4.1.1 e 4.1.2 |

#### Quadro 3 – e-Mag x WCAG 2.0

| e-Mag 3.1 | WCAG 2.0 |
|-----------|----------|
| Recomendação 1.1 – Respeitar os Padrões Web | Critérios de Sucesso 4.1.1 e 4.1.2 |
| Recomendação 1.2 – Organizar o código HTML de forma lógica e semântica | Critério de Sucesso 1.3.1 |
| Recomendação 1.3 – Utilizar corretamente os níveis de cabeçalho | Critérios de Sucesso 1.3.1 e 2.4.10 |

#### Quadro 4- Mapeamento de deficiências nas normas

| Critério WCAG 2.0                      | Visão | Audição | Cognitiva | Física | Fala | e-MAG |
|----------------------------------------|-------|---------|-----------|--------|------|-------|
| **1.1.1** Conteúdo não textual          | x     |         | x         |        |      | x     |
| **1.2.1** Legendas (pré-gravado)        |       | x       |           |        |      | x     |
| **1.2.2** Legendas (em tempo real)      |       | x       |           |        |      | x     |
| **1.2.3** Audiodescrição ou alternativa (pré-gravado) | x     | x       | x         |        |      | x     |
| **1.2.4** Alternativas para mídia em tempo real |       | x       |           |        |      | x     |
| **1.2.5** Audiodescrição (pré-gravado)  | x     | x       | x         |        |      | x     |
| **1.3.1** Informações e relacionamentos | x     |         | x         | x      |      | x     |
| **1.3.2** Sequência significativa       | x     |         | x         | x      |      | x     |
| **1.3.3** Características sensoriais    | x     |         | x         | x      |      | x     |
| **1.4.1** Uso de cor                    | x     |         | x         | x      |      | x     |
| **1.4.2** Controle de áudio             | x     | x       |           |        |      | x     |
| **1.4.3** Contraste (mínimo)            | x     |         | x         | x      |      | x     |
| **1.4.4** Redimensionamento do texto    | x     |         | x         | x      |      | x     |
| **1.4.5** Imagens de texto              | x     |         | x         | x      |      | x     |
| **2.1.1** Teclado                      | x     |         | x         | x      |      | x     |
| **2.1.2** Sem armadilha de teclado      | x     |         | x         | x      |      | x     |
| **2.2.1** Ajustável por tempo           | x     |         | x         | x      |      | x     |
| **2.2.2** Pausar, parar, ocultar        | x     |         | x         | x      |      | x     |
| **2.3.1** Transe untos de convulsão     | x     |         | x         | x      |      | x     |
| **2.4.1** Ignorar blocos                | x     |         | x         | x      |      | x     |
| **2.4.2** Títulos e rótulos             | x     |         | x         | x      |      | x     |
| **2.4.3** Ordem do foco                 | x     |         | x         | x      |      | x     |
| **2.4.4** Propósito do link (em contexto) | x   |         | x         |        |      | x     |
| **2.5.1** Gestos de ponteiro            | x     |         | x         | x      |      |       |
| **2.5.2** Cancelamento de ponteiro      | x     |         | x         | x      |      |       |
| **2.5.3** Rótulos no nome               | x     |         | x         |        |      | x     |
| **2.5.4** Ativação por movimento        |       |         | x         | x      |      | x     |
| **3.1.1** Idioma da página              | x     |         | x         |        |      | x     |
| **3.1.2** Idioma das partes             | x     |         | x         |        |      | x     |
| **3.2.1** Foco ao receber               | x     |         | x         |        |      | x     |
| **3.2.2** Alteração ao receber          | x     |         | x         |        |      | x     |
| **3.3.1** Identificação de erros        | x     |         | x         |        |      | x     |
| **3.3.2** Etiquetas ou instruções       | x     |         | x         |        |      | x     |
| **3.3.3** Sugestão de erro              | x     |         | x         |        |      | x     |
| **4.1.1** Análise sintática             |       |         | x         |        |      | x     |
| **4.1.2** Nome, função, valor           | x     |         | x         |        |      | x     |

### 4. Resultados e Discussão

As Tabelas 4 e 5 mostram, respectivamente, os tipos de deficiência mais frequentemente contemplados pela WCAG 2.0 e pela eMAG.

#### Tabela 4 - WCAG 2.0

| Visão | Audição | Cognitiva | Física | Fala |
|-------|----------|------------|---------|------|
| 70.97% | 17.74% | 74.19% | 38.71% | 0.00% |

#### Tabela 5 - e-mag

| Visão | Audição | Cognitiva | Física | Fala |
|-------|----------|------------|---------|------|
| 82.50% | 25.00% | 85.00% | 35.00% | 0.00% |

### 5. Conclusões

A análise realizada contribui significativamente para as pesquisas em acessibilidade na Web, especialmente no contexto governamental. Ela é essencial para compreender as lacunas que as normas de acessibilidade buscam preencher, com uma ênfase particular nas necessidades de pessoas com deficiências visuais e cognitivas.

### 6. Referências

[Lista de referências numeradas de 1 a 40]
