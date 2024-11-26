## Grupo 3 - IHC
#### Membros:
André João Cordeiro Gomes - 211061402\
Gabriela Tiago de Araújo - 190028475\
Hauedy Wegener Soares - 211030792\
Jesus Gabriel Carvalho Ventura - 211062956\
Lucas Heler Lopes - 202016800\
Víctor Augusto de Sousa Câmara - 221031238

### **Checklist - Guia HTML do CEWEB.br**  

#### **1. Estruturação do conteúdo**  
- [ ] As páginas começam com a declaração de tipo de documento correta (`<!DOCTYPE html>`).  
- [ ] A tag `<html>` define corretamente o idioma do documento com o atributo `lang` (ex.: `lang="pt-br"`).  
- [ ] O elemento `<head>` inclui metadados essenciais como charset (`<meta charset="UTF-8">`).  
- [ ] Elementos `<section>`, `<article>`, e `<aside>` são utilizados para organizar o conteúdo por relevância.  
- [ ] Cada `<article>` e `<section>` possui títulos próprios utilizando tags de cabeçalho (ex.: `<h2>`).  
- [ ] O rodapé da página contém informações importantes ou links úteis, como contatos ou políticas.  

#### **2. Acessibilidade e inclusão**  
- [ ] Há contraste suficiente entre texto e fundo, atendendo ao nível AA da WCAG 2.2.  
- [ ] Os links possuem descrições significativas, evitando textos genéricos como "clique aqui".  
- [ ] Formulários utilizam mensagens de erro claras e acessíveis para leitores de tela.  
- [ ] Componentes dinâmicos, como modais ou menus, informam seu estado aos usuários (ex.: abertos ou fechados).  
- [ ] A ordem do foco ao navegar com teclado é lógica e intuitiva.  
- [ ] Conteúdos animados ou interativos têm opção de pausar, parar ou ocultar a animação.  
- [ ] O tempo de resposta ao usuário (ex.: timeout) é ajustável, evitando ações não intencionais.  

#### **3. Design responsivo e visual**  
- [ ] O layout utiliza unidades flexíveis como porcentagens e `em` ao invés de pixels fixos.  
- [ ] O conteúdo não ultrapassa as margens da tela em dispositivos móveis.  
- [ ] Imagens e vídeos utilizam tamanhos responsivos com o atributo `max-width: 100%`.  
- [ ] Elementos como menus ou sliders possuem opções amigáveis para telas menores (ex.: menus hambúrguer).  
- [ ] Os textos permanecem legíveis em qualquer tamanho de tela, respeitando boas práticas tipográficas.  

#### **4. SEO e indexação**  
- [ ] A tag `<meta name="description">` descreve adequadamente o propósito da página.  
- [ ] Links externos utilizam o atributo `rel="nofollow"` quando necessário.  
- [ ] Todas as URLs são amigáveis e evitam parâmetros desnecessários.  
- [ ] Imagens têm descrições adequadas usando `alt` e utilizam atributos de largura e altura para carregamento otimizado.  
- [ ] Vídeos incorporados utilizam tags `<track>` para legendas automáticas quando disponíveis.  
- [ ] Títulos `<title>` de páginas são únicos e refletem o conteúdo principal da página.  

#### **5. Validação de código**  
- [ ] O código foi verificado quanto a erros de sintaxe e formatação.  
- [ ] Todas as tags abertas possuem fechamento apropriado (mesmo em XHTML).  
- [ ] Não há elementos descontinuados, como `<font>`, `<center>` ou `<marquee>`.  
- [ ] Scripts externos são carregados de maneira assíncrona ou diferida para melhorar o desempenho.  
- [ ] CSS e JavaScript são minificados e otimizados para reduzir o tempo de carregamento.  

#### **6. Conteúdo multimídia e gráficos**  
- [ ] Cada vídeo possui uma descrição textual ou transcrição associada para acessibilidade.  
- [ ] Elementos gráficos (como SVG) utilizam títulos e descrições acessíveis.  
- [ ] Mídias pesadas são carregadas de forma preguiçosa (lazy loading) para otimizar o desempenho.  
- [ ] Áudios e vídeos possuem controles visíveis e utilizáveis tanto com mouse quanto teclado.  
- [ ] Há uma indicação clara quando o conteúdo está carregando (ex.: ícones de progresso).  

#### **7. Interatividade e experiência do usuário (UX)**  
- [ ] Botões utilizam texto ou ícones compreensíveis ao invés de caracteres arbitrários.  
- [ ] Feedback visual (ex.: mudança de cor) é dado ao interagir com botões ou links.  
- [ ] Campos obrigatórios em formulários estão claramente indicados.  
- [ ] Há mensagens de confirmação para ações importantes, como exclusões de dados.  
- [ ] Pop-ups ou modais aparecem em contextos claros, com botão de fechar acessível.  
- [ ] O tempo de resposta do site é adequado (ex.: menos de 2 segundos para carregamento).  

#### **8. Documentação e manutenção**  
- [ ] A estrutura do projeto segue boas práticas de organização, como separação entre HTML, CSS e JavaScript.  
- [ ] Comentários no código explicam trechos complexos ou menos intuitivos.  
- [ ] O guia inclui exemplos práticos para casos de uso comuns.  
- [ ] Atualizações do projeto são fáceis de aplicar com base na estrutura e documentação.  

#### **9. Segurança**  
- [ ] Formulários utilizam validação no lado cliente e servidor.  
- [ ] O site protege contra ataques comuns, como injeção de scripts (XSS) e CSRF.  
- [ ] Dados sensíveis não são exibidos no HTML ou acessíveis por meio de inspeção de elementos.  
- [ ] Todas as conexões utilizam HTTPS.  

#### **10. Testes e monitoramento**  
- [ ] Testes de usabilidade foram conduzidos com usuários reais.  
- [ ] O desempenho foi analisado usando ferramentas como Google Lighthouse ou GTmetrix.  
- [ ] Ferramentas de análise e logs de erros estão configurados (ex.: Google Analytics).  
- [ ] O site foi testado em diferentes navegadores e dispositivos para verificar compatibilidade.  

---  
