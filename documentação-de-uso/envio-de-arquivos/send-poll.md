# sendPoll

Envia lista/enquete (poll). Retorna a `Message` enviada em `result` no sucesso.

**Não é upload de arquivo** — não usa `file_id`/URL/`multipart/form-data`, não tem `caption`. As regras gerais do [README.md](README.md) sobre envio de arquivo não se aplicam aqui; só os campos de mensagem comuns (`chat_id`, `disable_notification`, `reply_to_message_id`, `allow_sending_without_reply`, `reply_markup`, `send_at`).

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `chat_id` | Integer ou String | Sim | ID do chat de destino ou @username do canal (formato `@channelusername`) |
| `question` | String | Sim | Pergunta da enquete, 1-300 caracteres |
| `options` | Array de String | Sim | Lista de opções de resposta, 2-10 strings de 1-100 caracteres cada |
| `is_anonymous` | Boolean | Não | Enquete anônima. Padrão `true` |
| `type` | String | Não | `"quiz"` ou `"regular"`. Padrão `"regular"` |
| `allows_multiple_answers` | Boolean | Não | Permite múltiplas respostas. Ignorado se `type` for `"quiz"`. Padrão `false` |
| `correct_option_id` | Integer | Só se `type: "quiz"` | Índice (base 0) da opção correta |
| `explanation` | String | Não | Texto mostrado quando o usuário erra ou toca no ícone de lâmpada, em enquete tipo quiz. 0-200 caracteres, até 2 quebras de linha, após parsing de entidades |
| `explanation_parse_mode` | String | Não | Modo de parsing de entidades em `explanation` |
| `explanation_entities` | Array de `MessageEntity` | Não | Entidades especiais em `explanation` — alternativa a `explanation_parse_mode` |
| `open_period` | Integer | Não | Segundos que a enquete fica ativa após criada, 5-600. Não pode ser usado junto com `close_date` |
| `close_date` | Integer | Não | Unix timestamp de fechamento automático, 5-600 segundos no futuro. Não pode ser usado junto com `open_period` |
| `is_closed` | Boolean | Não | `true` = enquete já fechada ao criar (útil pra preview) |
| `disable_notification` | Boolean | Não | Envia silenciosamente (notificação sem som) |
| `reply_to_message_id` | Integer | Não | ID da mensagem original, se for resposta |
| `allow_sending_without_reply` | Boolean | Não | `true` = envia mesmo se a mensagem respondida não existir |
| `reply_markup` | `InlineKeyboardMarkup` \| `ReplyKeyboardMarkup` \| `ReplyKeyboardRemove` \| `ForceReply` | Não | Teclado/interface adicional |
| `send_at` | Integer ou String | Não | **Só contas de usuário.** Agenda envio: unix timestamp (máx 365 dias no futuro) ou string `"online"`. Vazio = envia na hora |

**Regra de tratamento**:
- `chat_id`, `question`, `options` são os únicos obrigatórios.
- `correct_option_id` é obrigatório só quando `type == "quiz"`.
- `open_period` e `close_date` são mutuamente exclusivos — escolha um.
- `explanation_parse_mode` e `explanation_entities` são mutuamente exclusivos.

**JSON de exemplo**:

```json
{
  "chat_id": 123456789,
  "question": "Qual sua linguagem favorita?",
  "options": ["JavaScript", "Python", "C++"],
  "is_anonymous": true,
  "type": "quiz",
  "correct_option_id": 1,
  "explanation": "Python é a resposta certa aqui!",
  "open_period": 60
}
```
