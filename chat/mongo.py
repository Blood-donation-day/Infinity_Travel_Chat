from pymongo import MongoClient, InsertOne
from bson import ObjectId
import datetime, os, time
from dotenv import load_dotenv

load_dotenv()
env = os.environ.get

# MongoDB 연결
client = MongoClient(env("MONGO_DB_HOST"), int(env("MONGO_DB_PORT")))
db = client.chatserver

# collection 생성
chat_collection = db.chat


def test():
    chats = []
    for _ in range(10000):
        chat = {
            # "_id": ObjectId(),
            "user": "test1",
            "room": "chatroom1",
            "content": "MongoDB채팅 저장 테스트입니다.",
            "read_count": "2",
            "is_delete": "0",
            "created_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }
        chats.append(InsertOne(chat))

    # inserted_id >> sqlite3처럼 자동으로 부여되는 id

    start = time.time()
    chat_ids = chat_collection.bulk_write(chats)
    end = time.time()
    print(f"{end-start}.sec")
