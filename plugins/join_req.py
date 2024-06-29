from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
import logging
from info import ADMINS, AUTH_CHANNEL, AUTH_CHANNEL_2

# Event handler for chat join requests
@Client.on_chat_join_request(filters.chat(AUTH_CHANNEL) | filters.chat(AUTH_CHANNEL_2))
async def join_reqs(client, message: ChatJoinRequest):
    try:
        if not await db.find_join_req(message.from_user.id):
            await db.add_join_req(message.from_user.id)
            logging.info(f"Added join request for user {message.from_user.id}")
    except Exception as e:
        logging.error(f"Error handling join request: {e}")

# Command to delete join requests
@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    try:
        await db.del_join_req()
        await message.reply("<b>⚙ Successfully deleted users who left the channel</b>", parse_mode=enums.ParseMode.HTML)
        logging.info("Deleted all join requests from the database")
    except Exception as e:
        await message.reply("<b>⚠ An error occurred while deleting the requests</b>", parse_mode=enums.ParseMode.HTML)
        logging.error(f"Error deleting join requests: {e}")
