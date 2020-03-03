import psycopg2
import redis
import json
from bottle import Bottle, request



class Sender(Bottle):
    def __init__(self):
        super().__init__()        
        self.route('/', method='POST', callback=self.send)
        self.fila = redis.StrictRedis(host='queue', port=6379, db=0)
        DSN = 'dbname=email_sender host=db user=postgres password=password'
        self.conn = psycopg2.connect(DSN)


    def register_message(self, assunto, mensagem):    
        SQL = 'INSERT INTO emails (assunto, mensagem) values (%s, %s)'
        cur = self.conn.cursor()
        cur.execute(SQL, (assunto, mensagem))
        self.conn.commit()

        msg = {'assunto': assunto, 'mensagem': mensagem}
        self.fila.rpush('sender', json.dumps(msg))

        print('Mensagem registrada!')
    
    def send(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')

        self.register_message(assunto, mensagem)
        return 'mensagem enfileirada! Assunto: {} mensagem: {}'.format(
            assunto, mensagem
        )

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)