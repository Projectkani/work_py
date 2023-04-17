# **WORK BOT**

Этот бот создан для подсчёта кол-ва отработаных смен пользователем. 
Бот работает на БД sqlite 
Бот написан на Python система Aiogram.

```python
@dp.message_handler()
async def messages_hand(msg: types.Message):
    words = msg.text
    if words == 'Ворк':
        await work(msg)
    elif words == 'ворк':
        await work(msg)
    else:
        return
@dp.message_handler(commands=['work','работать'], commands_prefix='.!/')
```
Пот отвечает на слова "Ворк" и "ворк" Другие можно добавить через `elif words == 'слово'`

При использовании кода, просьба оставлять ссылку на телеграм канал https://pskbots.t.me
