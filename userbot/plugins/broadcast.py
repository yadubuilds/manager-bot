import asyncio
import csv
import os
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

DEFAULT_DELAY = 0.8
LOG_DIR = "userbot/plugins/logs"

os.makedirs(LOG_DIR, exist_ok=True)

def parse_delay(cmd):
    try:
        return float(cmd[1])
    except Exception:
        return DEFAULT_DELAY


async def save_log(rows, ts):
    log_file = f"{LOG_DIR}/broadcast_{ts}.csv"
    with open(log_file, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    return log_file


@Client.on_message(filters.me & filters.reply & filters.command("broadcast", prefixes=[".", "/"]))
async def broadcast_all(client, message):
    reply = message.reply_to_message
    delay = parse_delay(message.command)

    start_time = time.time()
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    sent = failed = total = 0
    rows = [("chat_id", "status")]

    status = await message.reply(f"📢 Broadcast started\n⏱ Delay: `{delay}s`")

    async for dialog in client.get_dialogs():
        chat = dialog.chat
        from pyrogram.enums import ChatType

if chat.type not in (
    ChatType.PRIVATE,
    ChatType.GROUP,
    ChatType.SUPERGROUP
):
    continue

        total += 1
        try:
            await reply.copy(chat.id)
            sent += 1
            rows.append((chat.id, "sent"))
            await asyncio.sleep(delay)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1
            rows.append((chat.id, "failed"))

        if total % 25 == 0:
            await status.edit(
                f"📢 Broadcasting...\n\n"
                f"📨 Total: `{total}`\n"
                f"✅ Sent: `{sent}`\n"
                f"❌ Failed: `{failed}`"
            )

    log_file = await save_log(rows, ts)
    duration = int(time.time() - start_time)
    success_rate = round((sent / total) * 100, 2) if total else 0

    await status.edit(
        f"✅ **Broadcast Completed**\n\n"
        f"📨 Total: `{total}`\n"
        f"📤 Sent: `{sent}`\n"
        f"⚠️ Failed: `{failed}`\n"
        f"📈 Success: `{success_rate}%`\n"
        f"⏱ Duration: `{duration}s`\n\n"
        f"🗂 Log:\n`{log_file}`"
    )


@Client.on_message(filters.me & filters.reply & filters.command("broadcast_contacts", prefixes=[".", "/"]))
async def broadcast_mutual_contacts(client, message):
    reply = message.reply_to_message
    delay = parse_delay(message.command)

    start_time = time.time()
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    sent = failed = total = 0
    rows = [("user_id", "status")]

    status = await message.reply(
        f"📇 **Broadcasting to Mutual Contacts Only**\n⏱ Delay: `{delay}s`"
    )

    async for user in client.get_contacts():
        if not user.is_mutual_contact:
            continue

        total += 1
        try:
            await reply.copy(user.id)
            sent += 1
            rows.append((user.id, "sent"))
            await asyncio.sleep(delay)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1
            rows.append((user.id, "failed"))

        if total % 20 == 0:
            await status.edit(
                f"📇 Broadcasting...\n\n"
                f"👥 Contacts: `{total}`\n"
                f"✅ Sent: `{sent}`\n"
                f"❌ Failed: `{failed}`"
            )

    log_file = await save_log(rows, ts)
    duration = int(time.time() - start_time)
    success_rate = round((sent / total) * 100, 2) if total else 0

    await status.edit(
        f"✅ **Contacts Broadcast Completed**\n\n"
        f"👥 Total Contacts: `{total}`\n"
        f"📤 Sent: `{sent}`\n"
        f"⚠️ Failed: `{failed}`\n"
        f"📈 Success: `{success_rate}%`\n"
        f"⏱ Duration: `{duration}s`\n\n"
        f"🗂 Log:\n`{log_file}`"
    )
