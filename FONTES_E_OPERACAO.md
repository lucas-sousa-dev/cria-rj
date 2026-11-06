# Central de Notícias — Fontes e operação

## Atualização automática
- GitHub Actions agenda a coleta a cada 30 minutos: `*/30 * * * *`. O GitHub pode atrasar ou pular execuções agendadas, especialmente em horários de pico; não há garantia de atualização exata.
- Script: `scripts/atualizar_noticias.py`; saída: `noticias.json`.
- O site consulta `noticias.json` quando abre e reconsulta enquanto permanece aberto. A coleta de fontes acontece no GitHub Actions, não no navegador.
- Para conferir a execução: GitHub → Actions → Atualizar notícias da Central de Notícias. Pode disparar manualmente com Run workflow.
- Se houver erro de push: Settings → Actions → General → Workflow permissions → Read and write permissions (quando disponível).

## Fontes de descoberta
- RSS Agência Brasil.
- Google Notícias RSS, com buscas direcionadas a gshow, LeoDias, CARAS, Quem, SBT, O Dia, Extra, g1, Metrópoles, Terra, CNN Brasil, Correio Braziliense, Estadão, Senado, Câmara, ge, ESPN, Valor, InfoMoney, Fiocruz, Ministério da Saúde, BBC, DW, Tecnoblog, Canaltech e Olhar Digital.
- São fontes candidatas via resultados agregados: **não existe garantia de cobertura, inclusão, autorização de republicação nem disponibilidade permanente**.
- Os links do agregador podem abrir uma página intermediária antes do veículo original.
- Editorias são aproximadas; revisar resultados e corrigir erros de classificação quando necessário.

## Direitos e transparência
- Publicar apenas título de referência, veículo, data e link, sem copiar corpo de matéria, descrição nem imagens de terceiros.
- Fotos somente com licença/autorização adequada, inclusive para uso comercial; crédito sozinho não substitui autorização.
- Notícias de celebridades: atribuir rumores, não apresentar alegações não confirmadas como fatos e evitar conteúdo invasivo ou difamatório.
- O arquivo JSON não equivale a apuração jornalística independente: são manchetes indexadas de fontes externas.
- Não inventar preços de afiliados nem misturar publicidade com notícia sem identificação.
