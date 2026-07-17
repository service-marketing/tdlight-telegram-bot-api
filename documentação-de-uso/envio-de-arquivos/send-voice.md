# sendVoice

Envia arquivo de áudio pra aparecer como nota de voz (player redondo) no cliente Telegram. Pra isso, o áudio precisa ser `.OGG` codificado em OPUS — outros formatos são enviados como `Audio` ou `Document` em vez de nota de voz (ver [README.md](README.md), seção "Enviando por URL"). Retorna a `Message` enviada em `result` no sucesso. Máx 50 MB.

Request: `multipart/form-data` (ou JSON com `file_id`/URL no lugar de upload).

Campos comuns (`chat_id`, `caption`, `parse_mode`, `caption_entities`, `disable_notification`, `reply_to_message_id`, `allow_sending_without_reply`, `reply_markup`, `send_at`) — ver [README.md](README.md).

Específico de sendVoice:

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `voice` | InputFile ou String | Sim | Nota de voz a enviar. `file_id` (String) pra reenviar nota já no servidor do Telegram (recomendado), URL HTTP (String) pra baixar da internet, ou upload via `multipart/form-data` |
| `duration` | Integer | Não | Duração da nota de voz em segundos |

**Regra de tratamento**: `chat_id` e `voice` são os únicos obrigatórios. Formato errado (não `.ogg`/OPUS) não dá erro — Telegram só entrega como `audio`/`document` em vez de `voice`, então trate isso no seu dispatcher (ver checklist em `WEBHOOK_PAYLOADS.md`).

**JSON de exemplo**:

```json
{
  "chat_id": 123456789,
  "voice": "https://example.com/nota-de-voz.ogg",
  "duration": 12
}
```
