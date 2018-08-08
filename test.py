from utils.redis import conn

r = conn.pool()
r.lpush('namaesi', 'a', 'b', 'c')
mm = r.lrange('namaesi', 0, 2)
print(mm)
print(type(mm))
