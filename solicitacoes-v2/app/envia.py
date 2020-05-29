import psycopg2
from bottle import route, run, request

DSN = "dbname=solicitacoes user=postgres host=db"
SQL = "insert into pedidos( nome, assunto, mensagem ) values ( %s, %s, %s )"

def registro_pedido( nome, assunto, mensagem ) :
	conecta = psycopg2.connect( DSN )
	cursorsql = conecta.cursor()
	cursorsql.execute( SQL, ( nome, assunto, mensagem ) )
	conecta.commit()
	cursorsql.close()

	print( "Mensagem registrada!!!" )

@route( "/", method = "POST" )
def send() :
	nome = request.forms.get( "nome" )
	assunto = request.forms.get( "assunto" )
	mensagem = request.forms.get( "mensagem" )

	registro_pedido( nome, assunto, mensagem )

	return "Mensagem enviada: Nome: {} Assunto: {} Mensagem: {}".format(
		nome, assunto, mensagem
	)

if __name__ == "__main__" :
	run( host = "0.0.0.0", port = 8080, debug = True )
