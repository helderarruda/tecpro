import redis, json, os
from time import sleep
from random import randint

if __name__ == "__main__" :
	redis_host = os.getenv( "REDIS_HOST", "fila" )
	# r = redis.Redis( host = "fila", port = 6379, db = 0 )
	r = redis.Redis( host = redis_host, port = 6379, db = 0 )
	print( "Aguardando mensagens..." )
	while True :
		mensagem = json.loads( r.blpop( "envia" )[ 1 ] )
		print( "Enviando a mensagem: ", mensagem[ "nome" ] )
		sleep( randint( 10, 20 ) )
		print( "Mensagem", mensagem[ "nome" ], "enviada" )
