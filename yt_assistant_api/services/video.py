# from sqlalchemy.ext.asyncio import AsyncSession

# from core import logger
# from crud.video import *


# class VideoService:

#     async def fetch_video(self, db: AsyncSession, video_id: str):
#         logger.info("Fetching video from all videos...")
#         video = await get_video(db, video_id)
#         return video

#     async def fetch_user_video(self, db: AsyncSession, account_id: str, video_id: str):
#         logger.info("Fetching video from account videos...")
#         video = await get_account_video(db, account_id, video_id)
#         return video

#     async def link_video(self, db: AsyncSession, account_id: str, video_id: str):
#         logger.info("Linking video to the user account")

#     async def create_and_link_video(
#         self, db: AsyncSession, account_id: str, video_id: str
#     ):
#         logger.info("Creating video...")
#         video = await create_video(db, account_id, video)
