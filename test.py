from utils.redis import conn

r = conn.pool()
r.hset('account','ak','abc')
r.hset('account','sk','def')
mm = r.hget('account', 'sk')
print(mm)
print(type(mm))
