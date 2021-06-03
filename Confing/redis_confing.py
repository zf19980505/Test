import redis


class Redis:
    def connect_redis(self, redis_data):
        POOL = redis.ConnectionPool(host='47.100.90.244', port=6379, max_connections=1000, decode_responses=True, db=3)
        conn = redis.Redis(connection_pool=POOL)
        access_token = conn.get(redis_data)
        print(access_token)
        # return access_token


if __name__ == '__main__':
    Redis().connect_redis('test_1_myUser_Id_82_token')
