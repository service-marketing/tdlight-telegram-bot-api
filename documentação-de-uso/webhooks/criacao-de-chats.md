# Criação de chats

Exemplo completo: [exemplos/criacao-de-chats.jsonc](exemplos/criacao-de-chats.jsonc).

Campos comuns em [README.md](README.md).

## Chat privado

Não existe um evento explícito de "chat criado". O primeiro contato com um novo chat privado chega como uma `message` normal (o próprio conteúdo, ex.: `text`) — se é a primeira mensagem daquele `chat.id`, trate como novo chat no seu sistema.

```json
{
  "update_id": 993143483,
  "message": {
    "message_id": 83,
    "from": { "id": 5425710484, "is_bot": false, "is_deleted": false, "first_name": "Leo Cel", "username": "leoaraujo98", "user_status": "online" },
    "chat": { "id": 5425710484, "first_name": "Leo Cel", "username": "leoaraujo98", "type": "private", "user_status": "online" },
    "date": 1784035091,
    "is_outgoing": false,
    "text": "Eaeee"
  }
}
```

## Grupo

Grupo tem evento explícito: `message.group_chat_created: true`. É o gatilho pra saber que o grupo acabou de ser criado (nesse caso, com a conta conectada como membro).

```json
{
  "update_id": 993143484,
  "message": {
    "message_id": 84,
    "from": { "id": 5425710484, "is_bot": false, "is_deleted": false, "first_name": "Leo Cel", "username": "leoaraujo98", "user_status": "online" },
    "chat": {
      "id": -5558416090,
      "title": "Teste criação",
      "type": "group",
      "all_members_are_administrators": false,
      "accepted_gift_types": { "unlimited_gifts": false, "limited_gifts": false, "unique_gifts": false, "premium_subscription": false, "gifts_from_channels": false }
    },
    "date": 1784035212,
    "is_outgoing": false,
    "group_chat_created": true
  }
}
```

**Regra de tratamento**: cheque `group_chat_created` pra detectar criação de grupo; pra chat privado, cheque se `chat.id` já existe na sua base — se não existir, é chat novo.
</content>
