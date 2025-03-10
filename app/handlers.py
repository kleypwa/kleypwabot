from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import app.database as db
import requests
import re

from api import DEEPINFRA_API_KEY, CAPS_ID

router = Router()

import re

def process_text(text):

    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    cleaned_text = re.sub(r'^[^A-Za-zА-Яа-я]+', '', cleaned_text)

    if cleaned_text and not cleaned_text[0].isupper():
        cleaned_text = cleaned_text[1:].strip() 
    
    if cleaned_text and cleaned_text[-1] != '.':
        cleaned_text += '.' 
    return cleaned_text


def clever_answer(prompt: str) -> str:
    url = "https://api.deepinfra.com/v1/openai/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1", 
        "prompt": f"Сделай краткое и осмысленное резюме текста:\n\n{prompt}",
        "max_tokens": 300,
        "temperature": 0.3  
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["text"].strip()



def get_gpt_summary(prompt: str) -> str:
    url = "https://api.deepinfra.com/v1/openai/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 200
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return re.sub(r'__.*?__', '', response.json()["choices"][0]["text"])
    else:
        return "Я сломался, чините меня, идиоты."

def get_gpt_answer(prompt: str, tokens: int) -> str:
    url = "https://api.deepinfra.com/v1/openai/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": tokens
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        text = response.json()["choices"][0]["text"]
        return process_text(text)  
    else:
        return "Я сломался, чините меня, идиоты."


@router.message(F.text.startswith('/s'))
async def summarize_messages(message: Message):
    print(f'Обращение: {message.text}')
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Не выебывайся, окда?")
        return

    limit = int(args[1])
    messages = db.get_messages_from_db(message.chat.id, limit)

    if not messages:
        await message.answer("Пошли вы нахуй, я работать не буду.")
        return

    text_to_summarize = "\n".join([f"{user}: {text}" for user, text in messages])

    summary = get_gpt_summary(
        f"{text_to_summarize} \n\n\n Только напиши ЧЕЛОВЕЧНО. Суммируй все это в небольшой рассказ. Добавь немного черного юмора. Повестование должно быть складным и иметь примерную величину в 50 слов."
    )

    summary = process_text(summary)

    await message.answer(hbold("ГОЛОС ИЗ БЕЗДНЫ:") + f"\n{summary}")



@router.message(F.text.startswith('ашк '))
async def request_messages(message: Message):
    print(f'Обращение: {message.text}')
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Не выебывайся, окда?")
        return
    
    text = " ".join(args[1:]) + "\n\n ответ запиши текстом начинающимся с большой буквы, в исключительно текстовом формате, и заканчивающимся точкой"

    await message.answer(f"{get_gpt_answer(text, 1000)}")

@router.message(F.text.startswith('капс '))
async def handle_caps_command(message: Message, bot: Bot):
    print(f'Капс-команда в канале: {message.text}')

    text_of_request = message.text[5:].strip()
    if not text_of_request:
        return

    generated_text = process_text(get_gpt_summary(text_of_request)).upper()

    await bot.send_message(CAPS_ID, generated_text)

@router.message(F.text.startswith('/n'))
async def summarize_messages_new(message: Message):
    print(f'Обращение: {message.text}')
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Не выебывайся, окда?")
        return

    limit = int(args[1])
    messages = db.get_messages_from_db(message.chat.id, limit)

    print(messages)

    if not messages:
        await message.answer("Пошли вы нахуй, я работать не буду.")
        return

    text_to_summarize = "\n".join([f"{user}: {text}" for user, text in messages])

    print(text_to_summarize)

    summary = clever_answer(
        f"{text_to_summarize}"
    )

    print(summary)

    #summary = process_text(summary)

    await message.answer(hbold("ГОЛОС ИЗ РАЯ:") + f"\n{summary}")

@router.message()
async def std_message(message: Message):
    print(f'Message: {message.text}')
    if message.text and not message.text.startswith("/sum"):
        db.save_message_to_db(message.chat.id, message.from_user.full_name, message.text)
    if message.text and message.text.lower() in {"нет ты", "нет, ты"}:
        await message.reply("Нет, ты.")
