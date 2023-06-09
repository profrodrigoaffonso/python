import mysql.connector
import requests
import json

# cria a conexão
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database="site"
)

# cria um cursor
mycursor = mydb.cursor()

# executa um SELECT na tabela e exibe os resultados usando um for loop
mycursor.execute("SELECT distinct(ip) FROM contagens WHERE pais IS NULL")

resultados = mycursor.fetchall()

sql = ""

for registro in resultados:
    # print(registro[0])  

    # Faz uma requisição GET para uma URL
    response = requests.get('http://ip-api.com/json/'  + registro[0])

    # Exibe o código de status da resposta
    # print(response.status_code)

    # Exibe o conteúdo da resposta
    # print(response.text)

    dados = json.loads(response.text)
    # print(dados['city'])

    sql = sql + "UPDATE contagens SET cidade = '" + dados['city'] + "', pais = '" + dados['country'] + "' \
                     WHERE ip = '" + registro[0] + "';"
    
    # print(sql)
    # exit()

    # mycursor.execute(sql)
    print(registro[0]) 
    # exit()

file = open('atualiza.sql', 'w')
file.write(sql)
file.close()

