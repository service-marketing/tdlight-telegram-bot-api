# Mensagens enviadas x recebidas

Exemplo completo: [exemplos/mensagens-enviadas-recebidas.jsonc](exemplos/mensagens-enviadas-recebidas.jsonc) (mensagens **enviadas** pela conta conectada). Pra mensagens **recebidas**, ver [chats-individuais.md](chats-individuais.md) e [grupos.md](grupos.md).

Campos comuns em [README.md](README.md).

## Como diferenciar

O único campo que importa é `is_outgoing`:

| `is_outgoing` | Significado | `from` |
|---|---|---|
| `false` | Mensagem **recebida** de outra pessoa | A outra pessoa |
| `true` | Mensagem **enviada** pela conta conectada ao bot/userbot | A própria conta |

Em ambos os casos, `chat` é sempre o chat onde a mensagem está (não muda conforme direção) — em conversa privada, `chat` continua sendo os dados da outra pessoa mesmo quando é a própria conta que enviou.

```json
{
  "message_id": 24,
  "from": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true },
  "chat": { "id": 5425710484, "first_name": "Leo Cel", "last_name": "Novo", "username": "leoaraujo98", "type": "private" },
  "date": 1783955050,
  "is_outgoing": true,
  "text": "Textooo"
}
```

Todos os tipos de conteúdo (`text`, `voice`, `sticker`, `photo`, `video`, `document`, `contact`, `audio`, GIF, `video_note`, `checklist`, `checklist_tasks_done`, `poll`) seguem a mesma estrutura documentada em [chats-individuais.md](chats-individuais.md), só com `is_outgoing: true`. Não repetido aqui.

Enquete enviada gera o mesmo update `poll` de nível superior (voto/estado) quando alguém responde, mesmo com a enquete tendo sido criada com `is_outgoing: true` — ver [README.md](README.md#atualização-de-estado-de-enquete-poll-no-nível-superior).

## Localização em tempo real enviada — ciclo completo

Início (`message`, `live_period` em segundos — pode vir como número muito alto, ex. `2147483647`, quando configurado "até desativar manualmente"):

```json
{ "location": { "latitude": -23.492954, "longitude": -46.642029 } }
```

Atualização — `edited_message`, mesmo `message_id`, `heading` e `horizontal_accuracy` presentes:

```json
{
  "edit_date": 1783955740,
  "location": { "latitude": -23.492953, "longitude": -46.642033, "live_period": 2147483647, "heading": 223, "horizontal_accuracy": 16 }
}
```

Revogação — outro `edited_message`, `live_period` some (volta a ser localização estática):

```json
{
  "edit_date": 1783955758,
  "location": { "latitude": -23.492954, "longitude": -46.642029 }
}
```

## Mensagens apagadas (pela própria conta)

Mesma estrutura de [README.md](README.md#mensagens-apagadas-deleted_messages). `message_ids` pode vir com vários IDs de uma vez:

```json
{
  "deleted_messages": {
    "chat": { "id": 5425710484, "first_name": "Leo Cel", "last_name": "Novo", "username": "leoaraujo98", "type": "private" },
    "message_ids": [42, 44, 43]
  }
}
```

## Citação em mensagem enviada

Mesma estrutura de `reply_to_message`/`quote` de [chats-individuais.md](chats-individuais.md#mensagem-citando-outra-reply), só com `is_outgoing: true` na mensagem que cita.

## Mensagem encaminhada (forward)

Encaminhar mensagem soma três campos no nível da `message`: `forward_origin`, `forward_from` (legado, espelha `forward_origin.sender_user`) e `forward_date` (timestamp do envio original, não confundir com `date`, que é quando o encaminhamento aconteceu).

```json
{
  "date": 1784634833,
  "is_outgoing": true,
  "forward_origin": {
    "type": "user",
    "sender_user": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true },
    "date": 1784634778
  },
  "forward_from": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true },
  "forward_date": 1784634778,
  "text": "Teste"
}
```

`forward_origin.type` varia conforme origem: `user` (`sender_user` presente, como acima), `chat`/`channel` (`sender_chat`/`chat` no lugar de `sender_user`) ou `hidden_user` (`sender_user_name` como texto, sem `id` — remetente escondeu conta). Conteúdo (texto, mídia etc.) segue o mesmo formato normal do tipo, sem mudança.
</content>
