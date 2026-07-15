# Webhooks recebidos — regras gerais

Cada webhook chega como um `Update` (objeto do Bot API). Sempre tem `update_id` mais **uma** destas chaves:

| Chave | Quando aparece |
|---|---|
| `message` | Mensagem nova (recebida ou enviada pela própria conta) |
| `edited_message` | Mensagem existente foi editada (inclui atualização/revogação de localização em tempo real) |
| `deleted_messages` | Uma ou mais mensagens foram apagadas |
| `poll` | Estado de uma enquete mudou (voto registrado, fechamento etc.) — não vem dentro de `message` |

Exemplos completos em [exemplos/](exemplos/): [criacao-de-chats.md](criacao-de-chats.md) · [chats-individuais.md](chats-individuais.md) · [grupos.md](grupos.md) · [mensagens-enviadas-recebidas.md](mensagens-enviadas-recebidas.md).

## Objeto `User` (campo `from`)

| Campo | Tipo | Sempre presente | Descrição |
|---|---|---|---|
| `id` | Integer | Sim | ID do usuário |
| `is_bot` | Boolean | Sim | Se é bot |
| `is_deleted` | Boolean | Sim | Conta deletada |
| `first_name` | String | Sim | |
| `last_name` | String | Não | |
| `username` | String | Não | |
| `user_status` | String | Sim | `online` ou `offline` |
| `last_seen` | Integer (unix) | Não | Só quando `user_status` é `offline` |
| `is_premium` | Boolean | Não | Só quando o usuário tem Telegram Premium |

## Objeto `Chat`

Igual em `message.chat` e `deleted_messages.chat`. Campos variam por `type`:

| Campo | Tipo | Chat privado (`private`) | Grupo (`group`) |
|---|---|---|---|
| `id` | Integer | Sim (positivo) | Sim (negativo) |
| `title` | String | — | Sim |
| `first_name` / `last_name` / `username` | String | Sim (dados do usuário) | — |
| `type` | String | `"private"` | `"group"` |
| `user_status` / `last_seen` | — | Sim (status do usuário) | — |
| `is_premium` | Boolean | Não (opcional) | — |
| `all_members_are_administrators` | Boolean | — | Sim |
| `accepted_gift_types` | Object | — | Sim — `{unlimited_gifts, limited_gifts, unique_gifts, premium_subscription, gifts_from_channels}` (todos Boolean) |

## Campos comuns de `message` / `edited_message`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `message_id` | Integer | Sim | |
| `from` | User | Sim | Quem enviou |
| `chat` | Chat | Sim | Onde foi enviada |
| `date` | Integer (unix) | Sim | Data de envio original |
| `is_outgoing` | Boolean | Sim | `true` = enviada pela conta conectada ao bot/userbot; `false` = recebida de outra pessoa |
| `edit_date` | Integer (unix) | Só em `edited_message` | Data da edição |

Cada `message` tem **um** campo de conteúdo (`text`, `voice`, `sticker`, `photo`, etc.) — ver tabela abaixo — e opcionalmente `reply_to_message` (citação) e `caption` (mídia com legenda).

## Tipos de conteúdo de mensagem

| Campo | Tipo de mensagem | Estrutura |
|---|---|---|
| `text` | Texto puro | String |
| `voice` | Áudio de voz (nota de voz) | `{duration, mime_type, file_id, file_unique_id, file_size}` |
| `sticker` | Figurinha | `{width, height, emoji, set_name, is_animated, is_video, type, thumbnail, thumb, file_id, file_unique_id, file_size}` |
| `photo` | Foto | Array de tamanhos: `[{file_id, file_unique_id, file_size, width, height}, ...]` — o **último** item é o de maior resolução. Aceita `caption` |
| `video` | Vídeo | `{duration, width, height, mime_type, thumbnail, thumb, file_id, file_unique_id, file_size, file_name?}`. Aceita `caption` |
| `document` | Arquivo genérico (ou GIF, quando `mime_type` é `image/gif` ou `video/mp4`) | `{file_name?, mime_type, thumbnail?, thumb?, file_id, file_unique_id, file_size}` |
| `animation` | GIF/vídeo curto sem som — enviado **junto** com `document` (mesmo arquivo nos dois formatos) | `{file_name?, mime_type, duration, width, height, thumbnail, thumb, file_id, file_unique_id, file_size}` |
| `audio` | Áudio de música (com metadados) | `{duration, file_name?, mime_type, title, performer, thumbnail?, thumb?, file_id, file_unique_id, file_size}` |
| `video_note` | Nota de vídeo circular | `{duration, length, thumbnail, thumb, file_id, file_unique_id, file_size}` |
| `location` (fixa) | Localização estática | `{latitude, longitude}` |
| `location` (tempo real) | Localização ao vivo | `{latitude, longitude, live_period}` — atualizações chegam como `edited_message` (ver [mensagens-enviadas-recebidas.md](mensagens-enviadas-recebidas.md)) |
| `contact` | Contato | `{phone_number, first_name, last_name?, vcard?, user_id?}` |
| `checklist` | Lista de tarefas | `{title, tasks: [{id, text, text_entities?}], others_can_add_tasks, others_can_mark_tasks_as_done}` |
| `checklist_tasks_done` | Tarefa(s) da lista marcada(s) como concluída(s) | `{checklist_message: Message, marked_as_done_task_ids: [Integer, ...]}` — `checklist_message` é a mensagem original do checklist, já com `completed_by_user` e `completion_date` preenchidos nas tarefas concluídas |
| `poll` | Enquete criada nessa mensagem | `{id, question, options: [{text, voter_count}, ...], total_voter_count, is_closed, is_anonymous, type, allows_multiple_answers}` |

`thumbnail` e `thumb` sempre vêm duplicados com o mesmo conteúdo (campo legado mantido por compatibilidade) — pode usar qualquer um dos dois.

## Citações (`reply_to_message` e `quote`)

Quando uma mensagem responde outra, ganha o campo `reply_to_message`: uma cópia da mensagem original (mesma estrutura de `message`).

Se a citação for de um **trecho específico** do texto (seleção manual), aparece também `quote`:

| Campo | Tipo | Descrição |
|---|---|---|
| `text` | String | Trecho citado |
| `position` | Integer | Posição (offset) do trecho dentro do texto original |
| `is_manual` | Boolean | `true` quando o usuário selecionou o trecho manualmente |

## Mensagens apagadas (`deleted_messages`)

Não é `message`, é update de nível superior:

```json
{
  "update_id": 993143514,
  "deleted_messages": {
    "chat": { "...": "objeto Chat" },
    "message_ids": [103]
  }
}
```

`message_ids` pode conter mais de um ID (apagou várias de uma vez).

## Atualização de estado de enquete (`poll` no nível superior)

Não é `message`, é update de nível superior — mesmo objeto `Poll` da criação (`message.poll`), sem `question`/`chat` associado direto no update, disparado a cada mudança de estado (voto novo, fechamento):

```json
{
  "update_id": 993143527,
  "poll": {
    "id": "5096030880556646862",
    "question": "Opa",
    "options": [
      { "text": "A", "voter_count": 0 },
      { "text": "A", "voter_count": 0 },
      { "text": "A", "voter_count": 0 },
      { "text": "A", "voter_count": 1 }
    ],
    "total_voter_count": 1,
    "is_closed": false,
    "is_anonymous": false,
    "type": "regular",
    "allows_multiple_answers": true
  }
}
```

Correlacionar com a enquete original pelo campo `id`. `total_voter_count` e os `voter_count` de cada opção refletem o estado acumulado (não é um diff).
</content>
