from aiogram import types, Dispatcher
import hashlib


async def inline_wikipedia_handler(query: types.InlineQuery):
    text = query.query or "echo"
    link = f"https://ru.wikipedia.org/wiki/{text}"
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id,
            title="Wiki: ",
            url=link,
            input_message_content=types.InputMessageContent(
                message_text=link
            )
        )
    ]
    await query.answer(articles, cache_time=60, is_personal=True)


def register_handler_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_wikipedia_handler)