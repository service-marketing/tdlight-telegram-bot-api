# sendAnimation

Envia animação (GIF ou vídeo sem som, até 200 MB). Retorna a `Message` enviada em `result` no sucesso.

Request: `multipart/form-data` (ou JSON com `file_id`/URL no lugar de upload).

Campos comuns (`chat_id`, `caption`, `parse_mode`, `caption_entities`, `disable_notification`, `reply_to_message_id`, `allow_sending_without_reply`, `reply_markup`, `send_at`) — ver [README.md](README.md).

Específico de sendAnimation:

| Parâmetro   | Tipo                | Obrigatório | Descrição                                                                                                                                                                                                                                                                       |
| ----------- | ------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `animation` | InputFile ou String | Sim         | Animação a enviar. `file_id` (String) pra reenviar animação já no servidor do Telegram (recomendado), URL HTTP (String) pra baixar da internet, ou upload via `multipart/form-data`                                                                                             |
| `duration`  | Integer             | Não         | Duração da animação em segundos                                                                                                                                                                                                                                                 |
| `width`     | Integer             | Não         | Largura da animação                                                                                                                                                                                                                                                             |
| `height`    | Integer             | Não         | Altura da animação                                                                                                                                                                                                                                                              |
| `thumb`     | InputFile ou String | Não         | Miniatura do arquivo. JPEG, < 200 kB, largura/altura ≤ 320. Ignorada se o arquivo não for enviado via `multipart/form-data`. Não pode ser reaproveitada de outro arquivo — sempre upload novo, ou `attach://<file_attach_name>` se enviada junto no mesmo `multipart/form-data` |

**Regra de tratamento**: `chat_id` e `animation` são os únicos obrigatórios. `width`/`height`/`duration`/`thumb` só têm efeito relevante em upload direto (`multipart/form-data`) — em `file_id`/URL o Telegram já conhece esses metadados.

**JSON de exemplo**:

```json
{
  "chat_id": 123456789,
  "animation": "https://example.com/animacao.gif",
  "duration": 30,
  "width": 480,
  "height": 320,
  "caption": "Minha animação"
}
```
