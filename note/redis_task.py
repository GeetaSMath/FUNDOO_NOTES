import redis
import json

# redis connnection
redis_instance = redis.Redis(host='localhost', port=6379, db=0)


class RedisNote:
    def get_key(self, user_id):
        return f"notes:{user_id}"

    def save(self, note, user_id):
        key = self.get_key(user_id)
        note_id = note.get('id')
        if note_id is None:
            raise ValueError("Note id is required")
        note_dict = self.get(user_id)
        note_dict[str(note_id)] = note
        redis_instance.hset(key, str(note_id), json.dumps(note))

    def get(self, user_id):
        key = self.get_key(user_id)
        notes_dict = {}
        for note_id, note_json in redis_instance.hgetall(key).items():
            notes_dict[note_id.decode('utf-8')] = json.loads(note_json)
        return notes_dict

    def delete(self, note_id, user_id):
        key = self.get_key(user_id)
        redis_instance.hdel(key, str(note_id))
