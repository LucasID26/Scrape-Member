from pyrogram import Client,filters,idle

import pyromod.listen

import os

from pyrogram.errors import PhoneNumberInvalid,PhoneCodeInvalid, SessionPasswordNeeded,UserPrivacyRestricted,FloodWait, UserNotMutualContact, PeerFlood

from pyrogram.enums import UserStatus

import asyncio



import random

ID = os.environ['API_ID']

HASH = os.environ['API_HASH']

TOKEN = os.environ['TOKEN']

bot = Client('BOT_ADD', api_id=ID, api_hash=HASH, bot_token=TOKEN, in_memory=True)

@bot.on_message(filters.command('start'))

async def start(_, m):

  await m.reply_text(f'HALLO {m.from_user.first_name}\nSilahkan jalankan perintah /add untuk melakukan scrape')

@bot.on_message(filters.command('add'))

async def add(_, m):

  phone_number_msg = await m.chat.ask("» Silakan kirim **PHONE_NUMBER** Anda dengan kode negara yang ingin Anda buat sesinya. \nContoh : `+6286356837789`'", filters=filters.text)

  phone_number = phone_number_msg.text

  otp = await m.reply("» Mencoba mengirim OTP ke nomor yang diberikan...")

  

  client = Client(name="user", api_id=ID, api_hash=HASH, in_memory=True)

  await client.connect()

  

  try:

    code = await client.send_code(phone_number)

  except (PhoneNumberInvalid):

    await m.reply("» **PHONE_NUMBER** yang Anda miliki bukan milik akun mana pun di Telegram.\n\nMulai buat sesi Anda lagi.")

    return

  try:

    phone_code_msg = await m.chat.ask("» Silakan kirim **OTP** yang Anda terima dari Telegram di akun Anda.\nJika OTP adalah `12345`, **silakan kirimkan sebagai** `1 2 3 4 5`.", filters=filters.text, timeout=600)

  except TimeoutError:

    await m.reply("» Batas waktu mencapai 10 menit.\n\nSilakan mulai membuat sesi Anda lagi.")

    return

  

  phone_code = phone_code_msg.text.replace(" ", "")

  try:

    await client.sign_in(phone_number, code.phone_code_hash, phone_code)

  except (PhoneCodeInvalid):

    await m.reply("» kode OTP yang Anda kirim **salah.**\n\nSilakan mulai membuat sesi Anda lagi.")

    return

  except (SessionPasswordNeeded):

    await m.reply("Pastikan anda sudah mematikan **Verifikasi Dua Langkah**!!")

    return 

  await client.send_message('me','LOGIN✅')

  await add_member(m,client)

  try:

    await client.log_out()

  except:

    return True

async def add_member(m, user):

  from_chatid = await m.chat.ask("Masukan username group yang mau diculik membernya!!\n\nContoh : @username")

  to_chatid = await m.chat.ask("Masukan username group tujuan memasukan member!!\n\nContoh : @username")

  

  pesan = f"Dalam prosess menambahkan member dari {from_chatid.text} ke {to_chatid.text}\nSelang waktu penambahan member yaitu 20 detik"

  stt = await m.reply(pesan)

  async for member in user.get_chat_members(from_chatid.text):

    target = member.user

    zxb = [

            UserStatus.ONLINE,

            UserStatus.OFFLINE,

            UserStatus.RECENTLY,

            UserStatus.LAST_WEEK,

        ]

    if target.status in zxb:

      try:
        await user.join_chat(to_chatid.text)
        await user.add_chat_members(to_chatid.text, target.id)

        await asyncio.sleep(20)

      except UserPrivacyRestricted:

        await bot.send_message(m.chat.id,"Gagal memasukkan user karena privasi!!\nMenjalankan tugas selanjutnya!!")
        await asyncio.sleep(20)
      except UserNotMutualContact:

        await bot.send_message(m.chat.id,"Gagal memasukkan user karena bukan mutual kontak!!\nMenjalankan tugas selanjutnya!!")
        await asyncio.sleep(20)
      except PeerFlood:
        await stt.delete()
        return await bot.send_message(m.chat.id,"Akun anda dibatasi atau limit silahkan coba dengan akun lain!!")

      except FloodWait:
        await stt.delete()
        return await bot.send_message(m.chat.id,"Akun anda mengalami **FLOODWAIT**\nSilahkan coba dengan akun lain!!")

      except Exception as e:
        
        await stt.delete()
        await bot.send_message(m.chat.id,f"**ERROR:** `{e}`")

        await asyncio.sleep(0.3)

        return 
  await stt.delete()
  await bot.send_message(m.chat.id,"**BERHASIL**✅")

      

   


bot.start()

idle()

bot.stop()
