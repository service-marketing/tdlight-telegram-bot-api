# sendPhoto

Envia foto. Retorna a `Message` enviada em `result` no sucesso.

Request: `multipart/form-data` (ou JSON com `file_id`/URL no lugar de upload).

Campos comuns (`chat_id`, `caption`, `parse_mode`, `caption_entities`, `disable_notification`, `reply_to_message_id`, `allow_sending_without_reply`, `reply_markup`, `send_at`) — ver [README.md](README.md).

Específico de sendPhoto:

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `photo` | InputFile ou String | Sim | Foto a enviar. `file_id` (String) pra reenviar foto já no servidor do Telegram (recomendado), URL HTTP (String) pra baixar da internet, ou upload via `multipart/form-data`. Máx 10 MB. Soma largura+altura ≤ 10000px. Proporção largura/altura ≤ 20 |

**Regra de tratamento**: `chat_id` e `photo` são os únicos obrigatórios — todo resto pode ser omitido.

**JSON de exemplo**:

```json
{
  "chat_id": 123456789,
  "photo": "https://example.com/foto.jpg",
  "caption": "Minha foto"
}
```
