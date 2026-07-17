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

## Entrada de membro no grupo

Vem como `message` normal (com `message_id` próprio, tipo evento de sistema), trazendo o mesmo usuário duplicado em três campos — `new_chat_participant`/`new_chat_member` (legado, sempre só o **primeiro** adicionado) e `new_chat_members` (array, todos os adicionados nesse evento):

```json
{
  "update_id": 993143548,
  "message": {
    "message_id": 140,
    "from": { "id": 5425710484, "first_name": "Leo Cel", "username": "leoaraujo98", "user_status": "online" },
    "chat": { "id": -5558416090, "title": "Teste criação", "type": "group" },
    "date": 1784235732,
    "is_outgoing": false,
    "new_chat_participant": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true, "user_status": "online" },
    "new_chat_member": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true, "user_status": "online" },
    "new_chat_members": [
      { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true, "user_status": "online" }
    ]
  }
}
```

Usar `new_chat_members` como fonte da verdade (cobre adição em lote); os outros dois campos existem só por compatibilidade com versões antigas da Bot API.

## Saída de membro do grupo

Mesmo padrão, só que sem versão em array — sempre **um** membro por evento, duplicado em `left_chat_participant` (legado) e `left_chat_member` (atual):

```json
{
  "update_id": 993143549,
  "message": {
    "message_id": 141,
    "from": { "id": 5425710484, "first_name": "Leo Cel", "username": "leoaraujo98", "user_status": "online" },
    "chat": { "id": -5558416090, "title": "Teste criação", "type": "group" },
    "date": 1784235780,
    "is_outgoing": false,
    "left_chat_participant": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true, "user_status": "online" },
    "left_chat_member": { "id": 8989074661, "first_name": "SM CLICK", "is_premium": true, "user_status": "online" }
  }
}
```

`from` é quem removeu (ou o próprio usuário, se saiu sozinho); `left_chat_member` é quem saiu/foi removido.
</content>
