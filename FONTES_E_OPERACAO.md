# Cria RJ — Fontes e operação

## Ativo: manchetes e links, sem cópia de matérias
- Agência Brasil (EBC): RSS https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml
- A cada duas horas o GitHub Actions tenta consultar o RSS e gravar `noticias.json`.
- A interface exibe título, veículo, data e link para o original. **Não copia corpo de texto, resumo nem imagem de terceiros.** Títulos são metadados de referência.
- A classificação por palavras-chave é aproximada; notícias podem aparecer em categorias inadequadas. Revisão editorial é recomendada.
- Se a fonte ficar fora do ar, a última lista permanece disponível. O agendamento do GitHub Actions não garante execução em horário exato.
- O workflow também pode ser executado manualmente em Actions → Atualizar notícias do Cria RJ → Run workflow.
- Para ver falhas: Actions → Atualizar notícias do Cria RJ → execução mais recente.
- É necessário que GitHub Actions tenha permissão de escrita para Contents. Caso o push falhe, ver Settings → Actions → General → Workflow permissions.

## Fontes candidatas para próxima avaliação
- Agência Brasil: consultar licenciamento@ebc.com.br **antes de republicar integralmente** textos ou fotos em portal com afiliados. A integração atual é somente linkagem.
- Prefeitura do Rio / COR-Rio: avisos públicos e serviços; validar API/feed e condições antes de automatizar.
- Diário Oficial do Município: atos e oportunidades; validar endpoint e classificação.
- IBGE / dados.gov.br: indicadores oficiais; dados abertos exigem conferência da licença específica.
- INMET: previsão e alertas oficiais; validar documentação, licença e formato antes da integração.
- Climatempo: não integrado, depende de permissão/API e regras comerciais.
- Open-Meteo: endpoint gratuito é não comercial; não ativar em portal monetizado sem licença apropriada.

## Segurança e transparência
- Não usar imagens ou texto integral de terceiros sem licença.
- Publicar crédito e link do veículo de origem; checar eventuais correções.
- Não confundir manchetes automáticas com notícias redigidas ou verificadas pela equipe Cria RJ.
- Nenhum preço de afiliado deve ser inventado.
- Este documento é o registro de desenvolvimento no repositório. **Não foi conectado ao Redmine.**
