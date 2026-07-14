# Grupos

Exemplo completo: [exemplos/grupos.jsonc](exemplos/grupos.jsonc).

Estrutura idêntica a [chats-individuais.md](chats-individuais.md) — mesmos tipos de conteúdo, mesma tabela de campos em [README.md](README.md). Aqui só o que muda por ser grupo.

## Diferenças no objeto `chat`

`chat.type` é `"group"` e `chat.id` é **negativo**. Em vez dos dados do usuário, traz:

```json
{
  "id": -5558416090,
  "title": "Teste criação",
  "type": "group",
  "all_members_are_administrators": false,
  "accepted_gift_types": { "unlimited_gifts": false, "limited_gifts": false, "unique_gifts": false, "premium_subscription": false, "gifts_from_channels": false }
}
```

Não tem `first_name`/`last_name`/`username`/`user_status` no nível do chat (isso fica em `message.from`, que continua sendo o usuário que enviou).

## Tipos de conteúdo

Todos os tipos (`text`, `voice`, `sticker`, `photo`, `video`, `document`, `location` fixa/tempo real, `contact`, `audio`, GIF, `video_note`, `checklist`, `checklist_tasks_done`, `deleted_messages`, `reply_to_message`/`quote`) seguem exatamente a mesma estrutura documentada em [chats-individuais.md](chats-individuais.md) — só troca o `chat` pelo objeto de grupo acima. Não repetido aqui.

Uma diferença observada no exemplo de grupo: o GIF chegou só com `document` (sem o campo `animation` junto) — ao contrário do exemplo privado/enviado, onde vêm os dois. Trate `animation` como opcional; a mídia de vídeo mudo curto pode chegar só como `document` com `mime_type: "image/gif"`.

## Criação do grupo

Ver [criacao-de-chats.md](criacao-de-chats.md#grupo) (`group_chat_created: true`).
</content>
