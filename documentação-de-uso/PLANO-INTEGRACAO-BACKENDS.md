# Plano — Integração Telegram (tdlight-telegram-bot-api) nos backends

## Contexto

O repo `tdlight-telegram-bot-api` (em `c:/Users/leoar/Gits/SM/tdlight-telegram-bot-api`, fora do `Back/`) é um fork self-hosted do Telegram Bot API que expõe webhooks e campos extras (`is_outgoing`, `user_status`, `edited_message` com localização em tempo real, `checklist`, etc.), documentados em `documentação-de-uso/webhooks/` e `documentação-de-uso/envio-de-arquivos/`. O objetivo é ligar essa API como um **novo canal de mensageria** na plataforma SM Click, ao lado dos canais já existentes (WhatsApp QR Code via WppConnect/Wuzapi, WhatsApp API Oficial via Meta, Instagram).

A arquitetura de canais já é bem estabelecida e se repete de forma idêntica para cada provedor novo (Instagram foi o último adicionado). Telegram vai seguir exatamente esse mesmo padrão, adicionando um `Instance.type = "telegram"` e implementando os 4 pontos que todo canal precisa: (1) recebimento de webhook, (2) transformação do payload pro formato interno, (3) processamento/persistência da mensagem, (4) envio de mensagens de saída.

**Decisões confirmadas com o usuário:**
- Escopo também inclui subir a infra do `tdlight-telegram-bot-api` (docker-compose já existe no repo, falta só configurar `.env` com `TELEGRAM_API_ID`/`TELEGRAM_API_HASH` de https://my.telegram.org e decidir onde hospedar).
- Primeira leva de tipos de mensagem (MVP): texto, foto, vídeo, documento, áudio, voice, sticker, location, contact. Poll, checklist, reações e citações ficam para uma segunda etapa, seguindo o mesmo padrão já implementado.
- Multi-tenant simples: **um único servidor tdlight compartilhado** (host:port fixo, via env, tipo `URL_WPPCONNECT_HOST` mas sem node por cliente); cada `Instance` Telegram guarda só o seu próprio bot `token` (campo que já existe no model). Sem necessidade de um "TelegramNode" novo.

Front-end fica para depois, será tratado numa etapa separada assim que este plano de back-end for aprovado.

## Repos envolvidos

1. `tdlight-telegram-bot-api` — infra (deploy do servidor)
2. `sm-click-tools` — model `Instance`, funções de envio por provedor (lib compartilhada)
3. `sm-click-back-utils` — recebe webhooks HTTP e empilha na fila SQS
4. `sm-click-back-attendances` — consome a fila, transforma e persiste mensagens; worker de envio
5. `sm-click-back-app` — endpoint de conexão da instância (salvar token + `setWebhook`)

---

## Fase A — Infra: subir o tdlight-telegram-bot-api

- Preencher `.env` a partir de `.env.example` (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`).
- Rodar via `docker-compose.yml` já existente — sobe 3 serviços: `bot-api` (porta 8081 HTTP + 8082 stats), `file-server` (porta 8084, serve mídia recebida via filesystem, com `DELETE_AFTER_SERVE=1`), `swagger-ui` (8083, documentação da API local).
- Definir onde hospedar (mesma máquina/rede dos nós WppConnect existentes, ver `dev-tools/contabo` e `dev-tools/wppconnect` para o padrão de infra atual).
- Expor porta 8081 pro backend Django alcançar (chamadas de envio `/bot<token>/sendX`) e garantir que o host tdlight consiga alcançar de volta a URL pública de `sm-click-back-utils` pra registrar o webhook.
- `TELEGRAM_LOCAL=1` está fixo no compose — mídia recebida fica só no filesystem do container (sem endpoint HTTP `/file/`), acessível via o `file-server` container. Isso importa pra Fase E (download de mídia recebida).

## Fase B — Model `Instance` (sm-click-tools)

Arquivo: `sm-click-tools/sm_click_tools/models/instance/instances.py:92-96`

- Adicionar `("telegram", "telegram")` em `TYPE_CHOICES`.
- Reusar o campo `token` já existente (`instances.py:122-124`) para guardar o bot token do Telegram — mesmo campo usado por `whatsapp-api-official`/`instagram`.
- Gerar migration do Django pra refletir a mudança de `choices` do campo `type`.
- Em `sm-click-tools/sm_click_tools/params.py`, adicionar ao lado das URLs de outros provedores (linhas 5-100):
  ```
  URL_TELEGRAM_HOST = get_env("TELEGRAM_BOT_API_URL", "http://localhost:8081")
  URL_TELEGRAM = URL_TELEGRAM_HOST + "/bot{token}/"
  URL_TELEGRAM_SEND_TEXT = URL_TELEGRAM + "sendMessage"
  URL_TELEGRAM_SEND_PHOTO = URL_TELEGRAM + "sendPhoto"
  URL_TELEGRAM_SEND_VIDEO = URL_TELEGRAM + "sendVideo"
  URL_TELEGRAM_SEND_DOCUMENT = URL_TELEGRAM + "sendDocument"
  URL_TELEGRAM_SEND_VOICE = URL_TELEGRAM + "sendVoice"
  URL_TELEGRAM_SEND_AUDIO = URL_TELEGRAM + "sendAudio"
  URL_TELEGRAM_SET_WEBHOOK = URL_TELEGRAM + "setWebhook"
  URL_TELEGRAM_GET_ME = URL_TELEGRAM + "getMe"
  URL_TELEGRAM_GET_FILE = URL_TELEGRAM + "getFile"
  TELEGRAM_API_TIMEOUT = 30
  ```

## Fase C — Envio de mensagens (sm-click-tools)

Novo módulo `sm-click-tools/sm_click_tools/functions/instances/telegram/messages.py`, seguindo o padrão de `functions/instances/instagram/messages.py`:

- `send_telegram_text(instance, telephone, message)` → POST `URL_TELEGRAM_SEND_TEXT`, `{chat_id: telephone, text: message}`.
- `send_telegram_image`, `send_telegram_video`, `send_telegram_file` (document), `send_telegram_voice`, `send_telegram_audio` — todas aceitam `file_id`/URL/base64 conforme regras de `documentação-de-uso/envio-de-arquivos/README.md` (URL é o caminho mais simples pra MVP, já que o conteúdo já costuma estar no S3 do SM Click).
- `chat_id` = identificador do destinatário (o parâmetro genérico `telephone` já é reaproveitado como ID pro Instagram — mesma convenção pro Telegram, aceita negativo pra grupos).

Depois, plugar essas funções no dispatcher central `sm-click-tools/sm_click_tools/functions/instances/messages.py`, adicionando `elif instance.type == "telegram":` em cada função que já ramifica por tipo:
`send_text` (:57), `send_file` (:91), `send_video` (:133), `send_image` (:174), `send_voice` (:214), `send_list` (:264, fora do MVP — pode retornar 405 por enquanto), `send_quoted_message` (:340), `delete_message` (:375), `edit_message` (:403).

Também tratar `instance.instance.type == "telegram"` no worker de envio `sm-click-back-attendances/app/processor/sender.py:129,261-334` (conversões de conteúdo tipo HEIC e extração do ID da mensagem enviada — Telegram Bot API retorna `result.message_id` no sucesso).

## Fase D — Recebimento do webhook (sm-click-back-utils)

**Decisão de design importante**: diferente do Meta/Instagram (que mandam um `business_acc_id`/`phone_id` dentro do próprio payload pra identificar a instância), o payload do tdlight não carrega identificador de qual bot recebeu a mensagem. Solução: **URL do webhook por instância**, incluindo o `instance_id` no path — mesmo padrão de URL usado no `getWebhookInfo`/`setWebhook` do Telegram real.

- `sm-click-back-utils/app/services/views/local/webhooks.py`: nova `TelegramWebhookAPIView(APIView)` com só `post()` (sem handshake GET, diferente de Meta/Instagram — Telegram não usa `hub.challenge`):
  ```python
  class TelegramWebhookAPIView(APIView):
      def post(self, request, instance_id):
          data = request.data.copy()
          data["instance_id"] = str(instance_id)
          receive_message_task.delay("telegram", data, None)
          return Response(status=status.HTTP_200_OK)
  ```
- `sm-click-back-utils/app/services/urls.py`: `path("webhooks/telegram/<uuid:instance_id>/", TelegramWebhookAPIView.as_view())`.

## Fase E — Processamento (sm-click-back-attendances)

- `sm-click-back-attendances/app/processor/receiver.py:18-36`: adicionar `elif origin == "telegram": process_telegram_wb(data)`.
- Novo pacote `sm-click-back-attendances/app/processor/networks/telegram/`, espelhando a estrutura do Instagram (arquivo mais próximo como referência):
  - `functions/transform_telegram_callback_message.py` — normaliza o `Update` (chaves `message`/`edited_message`/`deleted_messages`, ver `documentação-de-uso/webhooks/README.md`) pro formato interno `{instance, event, origin, payload: {message: {...}, chat: {...}}}` usado por todos os canais. Busca a `Instance` direto por `data["instance_id"]` (não precisa procurar por campo de negócio, já que veio na URL — mais simples que o fluxo do Instagram).
  - `events/get_event.py` — mapeia o `Update` recebido pro evento interno:
    - `message` com `is_outgoing: false` → `on_message`
    - `message` com `is_outgoing: true` → `on_self_message`
    - `edited_message` → `on_message_edited` (novo evento — não existe ainda nos outros canais; ou reaproveitar `onack` se o resto do pipeline tratar edição da mesma forma)
    - `deleted_messages` → `on_message_revoked`
  - `events/process_on_message.py` — mesma lógica de `get_or_create_chat` → `create_new_message` → `execute_bot`/`evaluate_chat`, igual ao `process_instagram_onmessage` (`sm-click-back-attendances/app/processor/networks/instagram/events/process_on_message.py:37-138`).
  - `process_telegram_wb.py` — dispatcher principal, mesmo esqueleto de `process_instagram_wb.py`.
- Tabela de mapeamento de tipo de conteúdo (MVP) — `message.text/photo/video/document/audio/voice/sticker/location/contact` → `type`/`content` interno usado por `create_new_message`. Documentado campo a campo em `documentação-de-uso/webhooks/README.md` (seção "Tipos de conteúdo de mensagem").
- **Mídia recebida**: como `TELEGRAM_LOCAL=1`, arquivos não vêm por URL HTTP direta — é preciso chamar `getFile` (usando `URL_TELEGRAM_GET_FILE`) pra resolver o `file_id` num caminho local, servido pelo container `file-server` (porta 8084, ver Fase A), baixar dali e subir pro S3 (mesmo padrão de `upload_instagram_media_to_s3` em `processor/functions/message/get_instagram_post_infos.py`) antes de persistir a mensagem.

## Fase F — Conexão da instância (sm-click-back-app)

Arquivo: `sm-click-back-app/app/instances/views/instances.py` (mesmo padrão de `meta_test_credentials` :214-232 e `instagram_test_credentials` :662).

- Nova action `@action(detail=True, methods=["post"], url_path="telegram/connect")`:
  1. Recebe o bot `token` (obtido pelo cliente via @BotFather).
  2. Valida chamando `getMe` no tdlight (`URL_TELEGRAM_GET_ME`) — se falhar, erro 400.
  3. Salva `instance.token = token`.
  4. Chama `setWebhook` (`URL_TELEGRAM_SET_WEBHOOK`) apontando pra `https://<host-sm-click-back-utils>/webhooks/telegram/<instance.id>/`.
- Em `sm-click-back-app/app/instances/controller/instances/update.py:18-64`, adicionar tratamento de troca de tipo pra/de `"telegram"` (limpar `token` ao sair do tipo, seguindo o mesmo padrão já usado pros outros tipos).

---

## Ordem de execução sugerida

1. Fase A (infra) — sem isso nada mais pode ser testado ponta a ponta.
2. Fase B (model) — habilita o novo `type` em todos os repos que dependem de `sm-click-tools`.
3. Fase D + E (webhook + processamento) — testável isoladamente enviando payloads de exemplo (já tem em `documentação-de-uso/webhooks/exemplos/*.jsonc`) direto pra fila, sem precisar de bot real ainda.
4. Fase C (envio) + Fase F (conexão) — fecha o ciclo completo (enviar e receber).

## Verificação

- Subir o `docker-compose.yml` do tdlight localmente, criar um bot de teste via @BotFather, rodar `telegram/connect` contra ele e confirmar que `getWebhookInfo` no tdlight mostra a URL certa.
- Mandar mensagem real pro bot (texto + uma foto) e conferir que a mensagem aparece na tela de atendimento (`sm-click-back-attendances`) com o conteúdo/mídia corretos.
- Responder pela tela de atendimento e confirmar que chega no Telegram.
- Rodar os testes de integração existentes de `sm-click-back-app/app/instances/tests/integration/` como referência de padrão pra escrever os equivalentes de Telegram.
