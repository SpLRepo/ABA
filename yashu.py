from pyrogram import Client, filters, idle
from config import *

yvi = Client(":AntiBanAll:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@yvi.on_chat_member_updated()
async def cmu_(_, cmu):
    if not cmu.chat.id in GROUPS:
        return
    if (not cmu.old_chat_member and not cmu.new_chat_member):
        return
    if (not cmu.old_chat_member.restricted_by and not cmu.new_chat_member.restricted_by):
        return
    x = cmu.old_chat_member.restricted_by or cmu.new_chat_member.restricted_by
    user_id = x.id
    tar_id = cmu.old_chat_member.user.id or cmu.new_chat_member.user.id
    if user_id in ADMINS:
        return
    try:
        await _.promote_chat_member(cmu.chat.id, user_id, cp())
        await _.send_message(cmu.chat.id)
        men = ""
        for x in ADMINS:
            men += (await _.get_users(x)).mention
            men += " "
        um = (await _.get_users(user_id)).mention
        tm = (await _.get_users(tar_id)).mention
        txt = f"{um}, all of your admin rights have been taken back due to restriction of {tm}.\n\nKindly inform {men}to get your rights back !"
    except:
        txt = f"{tm} is restricted by {um}.\n\n{men}I can't demote them !"
    await _.send_message(cmu.chat.id, txt)

yvi.start()
print("Bot started !")
idle()
    
        
