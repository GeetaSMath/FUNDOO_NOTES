import redis
import json


class RedisCrud:
    r = redis.Redis(decode_responses=True)
    dict_name = None
    key_template = None
    pk = 'user_id'

    @classmethod
    def save(cls, payload: dict, dict_name: str = None):
        if not isinstance(payload, dict):
            raise Exception('input need to be a type of dict')
        pk = payload.get(cls.pk)
        if not pk:
            raise ValueError('primary key is not found')
        return cls.r.hset(dict_name or cls.dict_name, cls.key_template.format(pk), json.dumps(payload))

    @classmethod
    def get(cls, key, dict_name=None):
        return cls.r.hget(dict_name or cls.dict_name, cls.key_template.format(key))

    @classmethod
    def delete(cls, key, dict_name=None):
        return cls.r.hdel(dict_name or cls.dict_name, cls.key_template.format(key))


class RedisNote(RedisCrud):
    key_template = 'notes_{}'
    dict_name = 'notes_dict'
    pk = 'user'
