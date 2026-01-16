import asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pyrogram.errors import FloodWait

DEFAULT_DELAY = 1.2

"""
Usage:
Reply to a photo or video

.vo_contacts
.vo_contacts 2        -> custom delay (seconds)
"""

def parse_delay(cmd):
    try:
        return float(cmd[1])
    except Exception:
        return DEFAULT_DELAY


@Client.on_message(filters.me & filters.reply & filters.command("vo_contacts", prefixes=[".", "/"]))
async def viewonce_mutual_contacts(client, message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("❌ Reply to a photo or video")

    delay = parse_delay(message.command)

    # Prepare media (view-once)
    if reply.photo:
        media = InputMediaPhoto(
            media=reply.photo.file_id,
            has_spoiler=True
        )
    elif reply.video:
        media = InputMediaVideo(
            media=reply.video.file_id,
            has_spoiler=True
        )
    else:
        return await message.reply("❌ Only photo or video supported")

    sent = failed = total = 0

    status = await message.reply(
        f"📇 **View Once → Mutual Contacts**\n\n"
        f"⏱ Delay: `{delay}s`"
    )

    async for user in client.get_contacts():
        # 🔐 MUTUAL CONTACTS ONLY
        if not user.is_mutual_contact:
            continue

        total += 1
        try:
            await client.send_media_group(
                chat_id=user.id,
                media=[media]
            )
            sent += 1
            await asyncio.sleep(delay)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1

        if total % 10 == 0:
            await status.edit(
                f"📇 Sending...\n\n"
                f"👥 Contacts: `{total}`\n"
                f"✅ Sent: `{sent}`\n"
                f"❌ Failed: `{failed}`"
            )

    await status.edit(
        f"✅ **View Once Contacts Broadcast Completed**\n\n"
        f"👥 Total Contacts: `{total}`\n"
        f"📤 Sent: `{sent}`\n"
        f"⚠️ Failed: `{failed}`"
    )

    try:
        await message.delete()
    except:
        pass
