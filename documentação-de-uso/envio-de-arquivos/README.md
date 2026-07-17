# Envio de arquivos — regras gerais

Vale pra todos os métodos `send*` (sendPhoto, sendAudio, sendDocument, sendVideo, sendVoice, sendAnimation, sendVideoNote, sendSticker).

3 formas de enviar arquivo, passando no parâmetro correspondente (`photo`, `audio`, `document`...):

| Forma                 | Como                                                                                | Limite de tamanho                           |
| --------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------- |
| `file_id`             | Arquivo já armazenado nos servidores do Telegram — passe só o `file_id`, sem upload | Sem limite de quantidade                    |
| URL HTTP              | Telegram baixa e envia                                                              | 5 MB pra fotos, 20 MB pros outros tipos     |
| `multipart/form-data` | Upload direto, igual formulário de navegador                                        | 10 MB pra fotos, 50 MB pros outros arquivos |

## Reenviando por `file_id`

- Não pode mudar o tipo do arquivo ao reenviar: vídeo não pode virar foto, foto não pode virar documento, etc.
- Não é possível reenviar miniaturas (thumbnails).
- Reenviar uma foto por `file_id` reenvia **todos** os tamanhos dela.
- `file_id` é único por bot — não funciona transferido entre bots diferentes.
- Mesmo arquivo pode ter `file_id` diferentes e igualmente válidos, mesmo pro mesmo bot.

## Enviando por URL

- Arquivo de destino precisa ter o Content-Type/MIME correto (ex.: `audio/mpeg` pra `sendAudio`).
- `sendDocument` por URL só funciona pra `.pdf` e `.zip`.
- `sendVoice` por URL: precisa ser `audio/ogg` e no máx 1 MB. Voice de 1-20 MB é enviado como arquivo (`document`) em vez de nota de voz.
- Outros formatos/combinações podem funcionar, mas sem garantia.

## Campos comuns aos métodos `send*` de mídia

Presentes em praticamente todo endpoint (sendPhoto, sendAudio, sendDocument, sendVideo...), além do parâmetro de arquivo em si e do `caption`:

| Parâmetro                     | Tipo                                                                                     | Obrigatório | Descrição                                                                                                                                                                                                                    |
| ----------------------------- | ---------------------------------------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chat_id`                     | Integer ou String                                                                        | Sim         | ID do chat de destino ou @username do canal (formato `@channelusername`)                                                                                                                                                     |
| `caption`                     | String                                                                                   | Não         | Legenda do arquivo. 0-1024 caracteres após parsing de entidades                                                                                                                                                              |
| `parse_mode`                  | String                                                                                   | Não         | Modo de parsing de entidades na legenda (ver formatting options)                                                                                                                                                             |
| `caption_entities`            | Array de `MessageEntity`                                                                 | Não         | Entidades especiais na legenda — alternativa a `parse_mode`                                                                                                                                                                  |
| `disable_notification`        | Boolean                                                                                  | Não         | Envia silenciosamente (notificação sem som)                                                                                                                                                                                  |
| `reply_to_message_id`         | Integer                                                                                  | Não         | ID da mensagem original, se for resposta                                                                                                                                                                                     |
| `allow_sending_without_reply` | Boolean                                                                                  | Não         | `true` = envia mesmo se a mensagem respondida não existir                                                                                                                                                                    |
| `reply_markup`                | `InlineKeyboardMarkup` \| `ReplyKeyboardMarkup` \| `ReplyKeyboardRemove` \| `ForceReply` | Não         | Teclado/interface adicional                                                                                                                                                                                                  |
| `send_at`                     | Integer ou String                                                                        | Não         | **Só contas de usuário.** Agenda envio: unix timestamp (máx 365 dias no futuro) ou string `"online"` pra enviar quando o outro participante ficar online. Mensagem agendada tem `message_id` negativo. Vazio = envia na hora |

`parse_mode` e `caption_entities` são mutuamente exclusivos (escolha um). Cada doc de endpoint (`send-photos.md`, `send-audio.md`, `send-document.md`, `send-animation.md`, `send-voice.md`, `send-poll.md`, ...) documenta só o que é **específico** daquele tipo — os campos acima não se repetem.
