<h1>Aluno: José Anderson da Silva 

<h1>FinBuddy — Chatbot de Finanças Pessoais em Python</h1>

<h2>Descrição do projeto</h2>
<p>
O FinBuddy é um chatbot simples desenvolvido em Python que atua como um assistente financeiro básico.
Ele responde dúvidas sobre finanças pessoais, como orçamento, economia, juros simples e compostos,
organização de gastos e definição de metas. A aplicação integra uma interface gráfica desenvolvida em
Tkinter com um modelo de IA acessado via API da OpenRouter.
</p>
<p>
O foco do projeto é aplicar conceitos de engenharia de prompt e consumo de API de modelos de linguagem,
mantendo a solução simples, funcional e com interface amigável para o usuário final.
</p>

<h2>Estratégia de implementação</h2>
<ul>
  <li><b>Engenharia de Prompt:</b> o chatbot é configurado como um “assistente financeiro básico”, limitado a explicações educacionais e sem recomendações de investimentos específicos.</li>
  <li><b>Histórico de Conversa:</b> o contexto é mantido em memória em uma lista de mensagens (system, user, assistant), permitindo que a IA responda considerando interações anteriores.</li>
  <li><b>Interface Gráfica (Tkinter):</b> implementa uma área de conversa rolável, campo de entrada de texto e botões para envio de mensagem, limpeza da conversa, salvamento do histórico e saída.</li>
  <li><b>Comunicação com a API:</b> o envio de mensagens é feito via HTTP (POST) usando <code>urllib.request</code>, com dados JSON contendo modelo, mensagens e parâmetros (max_tokens, temperature).</li>
  <li><b>Tratamento de Erros:</b> respostas de erro são exibidas na própria interface em caso de falha de conexão ou erro HTTP.</li>
</ul>

<h3>Principais componentes da aplicação</h3>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>Componente</th>
      <th>Responsabilidade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>FinancialChatBot</code></td>
      <td>Gerencia o histórico de mensagens, monta a requisição JSON, chama a API da OpenRouter e retorna o texto da resposta.</td>
    </tr>
    <tr>
      <td><code>FinBuddyGUI</code></td>
      <td>Implementa a interface em Tkinter, exibe as mensagens na área de texto, lida com botões (Enviar, Limpar, Salvar, Sair).</td>
    </tr>
    <tr>
      <td>Variável <code>API_KEY</code></td>
      <td>Armazena a chave de API da OpenRouter (deve ser preenchida pelo usuário antes da execução).</td>
    </tr>
    <tr>
      <td>Histórico (<code>self.history</code>)</td>
      <td>Lista de mensagens no formato esperado pela API (role/content), incluindo o prompt do sistema e as interações.</td>
    </tr>
  </tbody>
</table>

<h2>Fluxo de funcionamento</h2>
<ol>
  <li>O usuário digita uma pergunta na interface gráfica.</li>
  <li>A GUI chama o método <code>send_message()</code> do objeto <code>FinancialChatBot</code>.</li>
  <li>A mensagem é adicionada ao histórico e enviada à API da OpenRouter em formato JSON.</li>
  <li>O modelo de IA retorna uma resposta textual.</li>
  <li>A resposta é adicionada ao histórico e exibida na área de conversa da interface.</li>
  <li>O usuário pode continuar conversando, limpar o histórico ou salvar a conversa em um arquivo <code>.txt</code>.</li>
</ol>

<h2>Tabela de funcionalidades da interface</h2>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>Elemento</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Área de conversa</td>
      <td>Mostra todas as mensagens trocadas entre o usuário e o FinBuddy.</td>
    </tr>
    <tr>
      <td>Campo de entrada</td>
      <td>Onde o usuário digita a pergunta ou mensagem.</td>
    </tr>
    <tr>
      <td>Botão "Enviar"</td>
      <td>Envia o texto digitado para o modelo de IA e exibe a resposta.</td>
    </tr>
    <tr>
      <td>Botão "Limpar"</td>
      <td>Limpa a área de conversa e reinicia o histórico (mantendo apenas o prompt do sistema).</td>
    </tr>
    <tr>
      <td>Botão "Salvar conversa"</td>
      <td>Abre um diálogo para salvar todo o histórico atual em um arquivo de texto.</td>
    </tr>
    <tr>
      <td>Botão "Sair"</td>
      <td>Fecha a aplicação.</td>
    </tr>
  </tbody>
</table>

<h2>Como executar</h2>
<ol>
  <li><b>Pré-requisitos</b>
    <ul>
      <li>Python 3.8 ou superior instalado.</li>
      <li>Conexão com a internet.</li>
      <li>Conta e chave de API válidas da OpenRouter.</li>
    </ul>
  </li>
  <li><b>Configurar chave da API</b>
    <ul>
      <li>Abra o arquivo <code>finbuddy_chatbot.py</code>.</li>
      <li>Substitua o valor da constante <code>API_KEY</code> pela sua chave pessoal, por exemplo:<br>
        <code>API_KEY = "SUA_CHAVE_AQUI"</code>
      </li>
    </ul>
  </li>
  <li><b>Executar a aplicação</b>
    <ul>
      <li>Abra o terminal/prompt na pasta onde o arquivo está salvo.</li>
      <li>Execute:<br>
        <code>python finbuddy_chatbot.py</code>
      </li>
      <li>A janela do FinBuddy será aberta automaticamente.</li>
    </ul>
  </li>
  <li><b>Operação</b>
    <ul>
      <li>Digite perguntas sobre finanças pessoais no campo inferior.</li>
      <li>Clique em "Enviar" para receber as respostas do chatbot.</li>
      <li>Use "Limpar" para reiniciar a conversa.</li>
      <li>Use "Salvar conversa" para guardar o histórico em um arquivo.</li>
    </ul>
  </li>
</ol>

<h2>Resultado</h2>
<p>
O FinBuddy demonstra, de forma prática, a criação de um chatbot simples em Python com interface gráfica,
integração com modelo de IA via API e aplicação de engenharia de prompt. Ele atende aos requisitos do
Projeto Final, permitindo interação contínua com o usuário até que este deseje encerrar a aplicação.
</p>
