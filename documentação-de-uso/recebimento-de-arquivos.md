# Recebimento de arquivos (download de mídia recebida)

Contexto: `TELEGRAM_LOCAL=1` fica fixo no [docker-compose.yml](../docker-compose.yml) — sem endpoint HTTP `/file/` (ver `TELEGRAM_LOCAL` em [variaveis-de-ambiente.md](variaveis-de-ambiente.md)). `getFile` passa a devolver `file_path` **absoluto** do disco dentro do container `bot-api`, não um path relativo pra montar link direto. Pra baixar de fato, usa o container `file-server` (porta 8084), que compartilha o mesmo volume (`botdata`) e serve os bytes por HTTP.

## Fluxo

1. Webhook de mensagem chega com o conteúdo trazendo um `file_id` (`photo`, `video`, `document`, `voice`, `audio`, `video_note`, sticker...).
2. Chamar `getFile(file_id)` → retorna `{ file_path: "/var/lib/telegram-bot-api/<...>/photos/xyz.jpg" }` (path absoluto, por causa do `LOCAL=1`).
3. Montar a URL do `file-server`: `http://<host>:8084/<file_path>`. O [file-server.py](../file-server.py) aceita o path com ou sem o prefixo `var/lib/telegram-bot-api/` (remove antes de juntar com `ROOT=/data`, que aponta pro mesmo volume do `bot-api`).
4. `GET` nessa URL baixa o arquivo (Content-Type resolvido por extensão, com fallback pra assinatura binária/magic bytes).

## Link de uso único — por que "expira"

O `file-server` roda com `DELETE_AFTER_SERVE=1` ([docker-compose.yml:31](../docker-compose.yml)): depois de servir os bytes, apaga o arquivo do disco — mesmo volume que o `bot-api` usa. Ou seja, o link **não é reutilizável**: só serve uma vez.

Tentar baixar de novo o mesmo `file_path` → **404** (arquivo já foi removido, inclusive do lado do `bot-api`, já que é o mesmo volume).

**Repetir o fluxo**: chamar `getFile(file_id)` de novo. Como o arquivo local sumiu, o `bot-api` baixa de novo do Telegram e devolve o path (novo ou recriado) — daí dá pra repetir o download uma vez antes que o próximo `GET` apague de novo.

## Regras práticas

- Nunca cachear/guardar a URL do `file-server` pra uso posterior — trate como uso único.
- Fluxo correto: `getFile` → download imediato → subir pro storage próprio (S3, etc.) → descartar a URL. Não adiar o download.
- Se dois consumidores tentarem baixar o mesmo `file_id` em paralelo, só o primeiro `GET` tem sucesso; o segundo recebe 404 e precisa repetir `getFile` do zero.

## Diferença de `TELEGRAM_FILE_EXPIRATION_TIME`

Existe uma outra expiração, interna do `bot-api` (`--file-expiration-time`, ver [variaveis-de-ambiente.md](variaveis-de-ambiente.md)), que apaga arquivo do cache do `bot-api` após N segundos sem uso. É independente do delete-after-serve do `file-server` — na prática o `file-server` costuma apagar primeiro (a cada `GET`), então essa outra variável normalmente nem chega a agir nesse fluxo.
