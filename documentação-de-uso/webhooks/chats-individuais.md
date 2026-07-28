# Chats individuais (privados)

Exemplo completo: [exemplos/chats-individuais.jsonc](exemplos/chats-individuais.jsonc).

Campos comuns, objetos `User`/`Chat` e tipos de conteúdo em [README.md](README.md). Aqui só o que é específico de chat privado, com um exemplo de cada tipo de conteúdo.

`chat.type` é sempre `"private"`. `chat` traz `first_name`/`last_name`/`username`/`user_status` (dados do outro usuário), nunca `title`.

## Texto

```json
{
  "text": "Oi"
}
```

## `from.phone_number`

Só aparece quando o TDLib expõe o telefone do contato (não é garantido em todo `from`). Nunca aparece em `chat` — lá continua só `first_name`/`last_name`/`username`/`user_status`.

```json
{
  "from": {
    "id": 8989074661,
    "is_bot": false,
    "is_deleted": false,
    "first_name": "Alex Sm",
    "phone_number": "5511969082639",
    "is_premium": true,
    "user_status": "online"
  },
  "text": "Slv"
}
```

## Áudio de voz

```json
{
  "voice": { "duration": 2, "mime_type": "audio/ogg", "file_id": "AwACAgEAAxkBAAIFiGpN...", "file_unique_id": "AgADcgYAAkROaEY", "file_size": 49931 }
}
```

## Figurinha

```json
{
  "sticker": { "width": 512, "height": 512, "emoji": "👍", "set_name": "MrCat", "is_animated": true, "is_video": false, "type": "regular", "file_id": "CAACAgIAAxkBAAIFimpN...", "file_unique_id": "AgADQgADWbv8JQ", "file_size": 16441 }
}
```

## Foto (com e sem legenda)

```json
{
  "photo": [
    { "file_id": "AgACAgEAAxk...", "file_unique_id": "AQADzAxrG0ROaEZy", "file_size": 4004, "width": 320, "height": 160 },
    { "file_id": "AgACAgEAAxk...", "file_unique_id": "AQADzAxrG0ROaEZ-", "file_size": 17005, "width": 1179, "height": 590 }
  ],
  "caption": "Com caption"
}
```

## Vídeo

```json
{
  "video": { "duration": 7, "width": 720, "height": 1280, "mime_type": "video/mp4", "file_id": "BAACAgEAAxkBAAIFjGpN...", "file_unique_id": "AgADcwYAAkROaEY", "file_size": 2099833 }
}
```

## Documento

```json
{
  "document": { "file_name": "CamScanner 03-07-2026 07.37.pdf", "mime_type": "application/pdf", "file_id": "BQACAgEAAxkBAAIFjWpN...", "file_unique_id": "AgADdQYAAkROaEY", "file_size": 411373 }
}
```

## Localização fixa

```json
{ "location": { "latitude": -23.492922, "longitude": -46.642205 } }
```

## Localização em tempo real (início, atualização e revogação)

Início (`message`), `live_period` em segundos:

```json
{ "location": { "latitude": -23.492922, "longitude": -46.642205, "live_period": 900 } }
```

Atualização — chega como `edited_message` (mesmo `message_id`, com `edit_date`), com `horizontal_accuracy`:

```json
{ "location": { "latitude": -23.492909, "longitude": -46.642194, "live_period": 29700, "horizontal_accuracy": 3 } }
```

Revogação de permissão — outro `edited_message`, `live_period` desaparece (localização volta a ser estática):

```json
{ "location": { "latitude": -23.492909, "longitude": -46.642194, "horizontal_accuracy": 3 } }
```

## Contato (vCard)

```json
{
  "contact": {
    "phone_number": "944446538",
    "first_name": "cabeça de penes",
    "last_name": "🖤",
    "vcard": "BEGIN:VCARD VERSION: 2.1 N;..."
  }
}
```

## Áudio (música)

```json
{
  "audio": { "duration": 200, "file_name": "Over_the_Horizon.m4a", "mime_type": "audio/m4a", "title": "Over the Horizon", "performer": "Samsung", "file_id": "CQACAgEAAxkBAAIFkmpN...", "file_unique_id": "AgADeQYAAkROaEY", "file_size": 20145407 }
}
```

## GIF

Vem com `animation` **e** `document` juntos, mesmo arquivo:

```json
{
  "animation": { "mime_type": "video/mp4", "duration": 2, "width": 736, "height": 640, "file_id": "CgACAgIAAxkBAAIFlWpN...", "file_unique_id": "AgADWxYAAv9DSUg", "file_size": 55143 },
  "document": { "mime_type": "video/mp4", "file_id": "CgACAgIAAxkBAAIFlWpN...", "file_unique_id": "AgADWxYAAv9DSUg", "file_size": 55143 }
}
```

## Nota de vídeo (círculo)

```json
{
  "video_note": { "duration": 4, "length": 384, "file_id": "DQACAgEAAxkBAAMRalT...", "file_unique_id": "AgADMAcAAkTCqEY", "file_size": 343055 }
}
```

## Checklist (lista de tarefas)

Criação:

```json
{
  "checklist": {
    "title": "Teste hook lista",
    "tasks": [
      { "id": 1, "text": "Testar" },
      { "id": 2, "text": "Lista😄", "text_entities": [{ "offset": 5, "length": 2, "type": "custom_emoji", "custom_emoji_id": "5411174771620585784" }] }
    ],
    "others_can_add_tasks": true,
    "others_can_mark_tasks_as_done": true
  }
}
```

Tarefa marcada como concluída — `checklist_tasks_done.checklist_message` traz a mensagem original inteira, com a tarefa concluída ganhando `completed_by_user` e `completion_date`; `marked_as_done_task_ids` lista os IDs marcados nesse evento:

```json
{
  "checklist_tasks_done": {
    "checklist_message": { "message_id": 1436, "checklist": { "tasks": [ { "id": 1, "text": "Testar", "completed_by_user": { "id": 8989074661, "first_name": "Alex Sm" }, "completion_date": 1783707874 }, { "id": 2, "text": "Lista😄" } ] } },
    "marked_as_done_task_ids": [1]
  }
}
```

## Mensagem apagada

Ver estrutura em [README.md](README.md#mensagens-apagadas-deleted_messages).

## Mensagem citando outra (reply)

Citação simples (responde a mensagem toda):

```json
{
  "reply_to_message": { "message_id": 18, "from": { "id": 8989074661, "first_name": "SM CLICK" }, "text": "Teste" },
  "text": "Opaaa"
}
```

Citação de um trecho específico (seleção manual) — ganha o campo `quote`:

```json
{
  "reply_to_message": { "message_id": 18, "from": { "id": 8989074661, "first_name": "SM CLICK" }, "text": "Teste" },
  "quote": { "text": "te", "position": 3, "is_manual": true },
  "text": "Testeeee citação"
}
```
</content>
