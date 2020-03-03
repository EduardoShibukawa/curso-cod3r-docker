import psycopg2
import redis
import json
import os
from bottle import Bottle, request



class Sender(Bottle):
    def __init__(self):
        super().__init__()        
        
        redis_host = os.getenv('REDIS_HOST', 'queue')
        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'sender')
        db_password = os.getenv('DB_PASSWORD', 'password')
        dsn = f'dbname={db_name} user={db_user} host={db_host} password={db_password}'

        self.route('/', method='POST', callback=self.send)        
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)
        self.conn = psycopg2.connect(dsn)


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