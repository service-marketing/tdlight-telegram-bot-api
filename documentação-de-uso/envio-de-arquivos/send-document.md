# sendDocument

Envia arquivo genérico. Retorna a `Message` enviada em `result` no sucesso. Máx 50 MB.

Request: `multipart/form-data` (ou JSON com `file_id`/URL no lugar de upload).

Campos comuns (`chat_id`, `caption`, `parse_mode`, `caption_entities`, `disable_notification`, `reply_to_message_id`, `allow_sending_without_reply`, `reply_markup`, `send_at`) — ver [README.md](README.md).

Específico de sendDocument:

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `document` | InputFile ou String | Sim | Arquivo a enviar. `file_id` (String) pra reenviar arquivo já no servidor do Telegram (recomendado), URL HTTP (String) pra baixar da internet (só `.pdf`/`.zip`, ver [README.md](README.md)), ou upload via `multipart/form-data` |
| `thumb` | InputFile ou String | Não | Miniatura do arquivo. JPEG, < 200 kB, largura/altura ≤ 320. Ignorada se o arquivo não for enviado via `multipart/form-data`. Não pode ser reaproveitada de outro arquivo — sempre upload novo, ou `attach://<file_attach_name>` se enviada junto no mesmo `multipart/form-data` |
| `disable_content_type_detection` | Boolean | Não | Desativa detecção automática de content-type no servidor, pra arquivos enviados via `multipart/form-data` |

**Regra de tratamento**: `chat_id` e `document` são os únicos obrigatórios. `thumb` e `disable_content_type_detection` só têm efeito em upload direto (`multipart/form-data`).

**JSON de exemplo**:

```json
{
  "chat_id": 123456789,
  "document": "https://example.com/arquivo.pdf",
  "caption": "Meu documento"
}
```
