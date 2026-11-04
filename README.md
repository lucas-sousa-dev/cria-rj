# Cria RJ

Portal independente de notícias com foco no Rio de Janeiro, cobertura do Brasil, tecnologia, saúde, cotidiano e ofertas de afiliados.

## Estado atual

- Primeira versão visual responsiva em `index.html` criada no GitHub.
- Abas: Início, Rio de Janeiro, Brasil, Tecnologia, Saúde, Cotidiano, Ofertas e Sobre.
- Sem notícias fictícias nem links comerciais inventados: as seções exibem avisos até a integração com fontes reais e ofertas verificadas.
- Painel de **rascunhos locais** acessível no rodapé. Salva no `localStorage` do próprio navegador, **não publica para visitantes e não sincroniza dispositivos**. Não é um painel administrativo seguro de produção.
- Publicação no GitHub Pages **ainda precisa ser ativada** nas configurações do repositório.

## Como publicar no GitHub Pages

1. No repositório, abra **Settings → Pages**.
2. Em **Build and deployment**, escolha **Deploy from a branch**.
3. Selecione **main** e pasta **/(root)**; clique em **Save**.
4. Aguarde o GitHub indicar o endereço publicado. URL esperada: https://lucas-sousa-dev.github.io/cria-rj/ (não confirmada até ativar).

## Próximas etapas

1. Validar o layout no celular e a publicação do Pages.
2. Definir fontes RSS/APIs permitidas, com data, créditos, links e curadoria editorial; evitar cópia integral de reportagens e imagens sem licença.
3. Criar um painel autenticado e armazenamento compartilhado para publicar conteúdo de verdade. O protótipo local não substitui backend.
4. Integrar ofertas de afiliados da Shopee e Mercado Livre com links rastreáveis autorizados, identificação de publicidade e preços atualizados.
5. Criar gerador de artes para Instagram (Stories 1080×1920, posts 1080×1350), usando imagens com permissão de uso.
6. Desenvolver busca, SEO, acessibilidade e análises de visitas.

## Arquitetura inicial

- `index.html`: HTML, CSS e JavaScript sem dependências. Menu por categorias, seções vazias honestas e editor local de rascunhos.
- Sem backend, contas de usuários, scraping ou custos de IA nesta versão.

## Princípios

Rio em primeiro plano; Brasil em segundo; fatos verificados; fonte clara; publicidade identificada; boa experiência no celular.

## Identidade visual aprovada (03/11/2026)

Layout renovado com cabeçalho azul de praia, logotipo Cria RJ em destaque, menu azul-marinho, cards coloridos por categoria, seção especial Rio e Brasil e vitrine amarela de ofertas. Interface responsiva implementada em `index.html`. A foto de capa é carregada de um serviço externo (Unsplash) e pode depender da disponibilidade da imagem; os mapas ilustrados da referência ainda não foram implementados como vetores. O portal continua sem notícias e ofertas reais até integração de fontes e cadastro. A referência visual é um conceito, não um compromisso de reprodução pixel a pixel.
