# sendAudio

Envia arquivo de áudio pra aparecer no player de música do cliente Telegram. Formato deve ser `.MP3` ou `.M4A`. Retorna a `Message` enviada em `result` no sucesso. Máx 50 MB.

Pra nota de voz, usar `sendVoice` em vez desse.

Request: `multipart/form-data` (ou JSON com `file_id`/URL no lugar de upload).

Campos comuns (`chat_id`, `caption`, `parse_mode`, `caption_entities`, `disable_notification`, `reply_to_message_id`, `allow_sending_without_reply`, `reply_markup`, `send_at`) — ver [README.md](README.md).

Específico de sendAudio:

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `audio` | InputFile ou String | Sim | Áudio a enviar. `file_id` (String) pra reenviar áudio já no servidor do Telegram (recomendado), URL HTTP (String) pra baixar da internet, ou upload via `multipart/form-data` |
| `duration` | Integer | Não | Duração do áudio em segundos |
| `performer` | String | Não | Artista/performer |
| `title` | String | Não | Nome da faixa |
| `thumb` | InputFile ou String | Não | Miniatura do arquivo. JPEG, < 200 kB, largura/altura ≤ 320. Ignorada se o arquivo não for enviado via `multipart/form-data`. Não pode ser reaproveitada de outro arquivo — sempre upload novo, ou `attach://<file_attach_name>` se enviada junto no mesmo `multipart/form-data` |

**Regra de tratamento**: `chat_id` e `audio` são os únicos obrigatórios. `thumb` só tem efeito em upload direto (`multipart/form-data`), é ignorado se `audio` for `file_id`/URL.

**JSON de exemplo**:

```json
{
  "chat_id": 123456789,
  "audio": "https://example.com/audio.mp3",
  "duration": 180,
  "performer": "Banda Exemplo",
  "title": "Faixa Exemplo"
}
```
