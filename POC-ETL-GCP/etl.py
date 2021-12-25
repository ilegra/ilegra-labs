import datetime
import json
import os
import shutil
import pandas as pd
import requests
from gcloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound


def read_spotify_secret(json_file_path: str) -> dict:
    """
    Esta função realiza a leitura do arquivo JSON contendo o token da API e armazena-o em um dicionário
    
    :param str json_file_path: Caminho local para o arquivo JSON.

    :return: Retorna um dicionário contendo o token da API do Spotify.
    :rtype: dict
    """
    
    with open(json_file_path) as jf:
        secrets = json.load(jf)

    return secrets

def upload_object_to_bucket(bucket_name: str, object_path: str, object_key=None) -> bool:
    """
    Esta função é responsável por fazer upload de um arquivo/objeto a um determinado bucket no GCS.

    :param str bucket_name: Nome do bucket que receberá o arquivo/objeto.
    :param str object_path: Caminho local para o arquivo/objeto que será enviado ao bucket.
    :param str object_key: O caminho final do objeto dentro do bucket. Este parametro é opcional e caso não seja informado o valor do parametro object_path será assumido.

    :returns: True se o upload for bem sucedido. False caso contrário.
    :rtype: bool
    """

    file_name = (object_path if (object_key==None) else object_key)
        
    try:
        # Criando uma variável de ambiente contendo o caminho para o arquivo "key_file.json" da conta de serviço
        pk_path = os.getcwd()+"\\key_file.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = pk_path

        # Instanciando um novo cliente da API gcloud
        client = storage.Client()
        # Recuperando um objeto referente ao nosso Bucket
        bucket = client.get_bucket(bucket_name)
        if bucket==None:
            return False
        # Fazendo upload do objeto (arquivo) desejado
        blob = bucket.blob(file_name)
        blob.upload_from_filename(object_path)
    except Exception as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False
        
    return True

def extract_spotify_data(spotify_secret_file_path='', bucket_name='') -> str:
    """
    Esta função é responsável pela extração dos dados do Spotify através de uma requisição à API.

    :param str spotify_secret_file_path: Caminho local para o arquivo JSON contendo o token do Spotify.
    :param str bucket_name: Nome do bucket que receberá o arquivo/objeto com os dados.

    :return: Retorna o object_key (caminho para o objeto JSON dentro do bucket)
    :rtype: str

    """

    # Fazendo a leitura do token da API do Spotify e armazenando-o em uma variável
    secrets = read_spotify_secret(spotify_secret_file_path)
    token = secrets["token"]
    
    # Definindo os headers para a requisição à API
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Definindo um limite de 24 horas antes do momento que a função for executada
    # Com isso, conseguimos recuperar as últimas 50 músicas reproduzidas nas últimas  24 horas
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1) # Ontem = Hoje - 1 Dia
    # Convertendo a data para o formato Unix Timestamp, que é o formato utilizado pela API
    yesterdays_timestamp = int(yesterday.timestamp())*1000

    # Realizando a requisição: 
    # O parâmetro "after" serve para indicarmos a partir de quando devemos fazer a busca
    # O parâmetro "limit" define o limite de músicas retornadas (o valor máximo é 50)
    request = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?after={yesterdays_timestamp}&limit=50", headers = headers)

    # Transformando o resultado da requisição em um objeto JSON
    data = request.json()

    # Recuperando a data e hora da execução
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Checando a existência do diretório local para armazenar o JSON
    if not os.path.exists('spotify_data\\raw\\'):
        os.makedirs('spotify_data\\raw\\')

    # Salvando o resultado da requisição em um arquivo JSON 
    file_name = f'spotify_data\\raw\\{date}_spotify_data.json'
    with open(file_name, 'w+') as f:
        json.dump(data, f, indent=4)

    # Fazendo upload do arquivo JSON para o bucket
    object_key = f"raw/{date}_spotify_data.json"
    upload_object_to_bucket(bucket_name=bucket_name, object_path=file_name, object_key=object_key)

    # Retorna o object key do objeto gerado (JSON com as músicas) dentro do bucket
    full_object_key = f"{bucket_name}/{object_key}"
    return full_object_key

def transform(json_object_key="") -> str:
    """
    Esta função é responsavel pela transformação do arquivo JSON gerado pela função extract_spotify_data() em um arquivo .csv contendo apenas as informações desejadas.

    :param str json_object_key: Caminho para o objeto dentro do bucket.

    :return: Retorna o object_key (caminho para o objeto .csv dentro do bucket).
    :rtype: str
    """

    # Fazendo download do JSON do bucket, para iniciar as transformações
    try:
        # Criando uma variável de ambiente contendo o caminho para o arquivo "key_file.json" da conta de serviço
        pk_path = os.getcwd()+"\\key_file.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = pk_path
        
        # Instanciando um novo cliente da API gcloud
        client = storage.Client()

        # Variáveis auxiliares
        full_object_key_splited = json_object_key.split('/')
        bucket_name = full_object_key_splited[0]
        object_key = json_object_key.replace(f"{bucket_name}/", "")
        local_path = f"spotify_data//raw//{full_object_key_splited[-1]}"
        
        # Criando um objeto para o Bucket
        bucket = client.get_bucket(bucket_name)
        # Criando um objeto BLOB para o caminho do arquivo
        blob = bucket.blob(object_key)
        # Fazendo download local do arquivo
        blob.download_to_filename(local_path)
    except Exception as e:
        print(e)
        exit()

    # Abrindo o JSON que foi baixado
    file = open(local_path)
    data = json.load(file)
    file.close()
    
    # Definindo as listas que vão armazenar as informações que desejamos. 
    # Elas irão nos auxiliar a compor o Dataframe final que vai resultar num .csv.
    song_names = []
    album_names = []
    artist_names = []
    songs_duration_ms = []
    songs_popularity = []
    played_at_list = []

    # Percorrendo todos os itens presentes no JSON e capturando as informações que
    # queremos armazenar no .csv final
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        album_names.append(song["track"]["album"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        songs_duration_ms.append(song["track"]["duration_ms"])
        songs_popularity.append(song["track"]["popularity"])
        played_at_list.append(song["played_at"])

    # Criando um dicionário com os resultados obtidos nas listas
    song_dict = {
        "song_name": song_names,
        "album_name": album_names,
        "artist_name": artist_names,
        "duration_ms": songs_duration_ms,
        "popularity": songs_popularity,
        "played_at": played_at_list
    }

    # Transformando nosso dicionário em um dataframe
    song_df = pd.DataFrame(song_dict, columns=["song_name", "album_name", "artist_name", "duration_ms", "popularity", "played_at"])
    
    # Checando a existência do diretório local para armazenar o .csv
    if not os.path.exists('spotify_data\\transformed\\'):
        os.makedirs('spotify_data\\transformed\\')
    
    # Convertendo nosso dataframe para um .csv
    file_name = ((full_object_key_splited[-1]).rsplit('.',1)[0])+'.csv'
    local_path = f"spotify_data\\transformed\\{file_name}"
    song_df.to_csv(local_path, index=False)

    # Fazendo upload do arquivo JSON para o bucket
    object_key = f"transformed/{file_name}"
    upload_object_to_bucket(bucket_name=bucket_name, object_path=local_path, object_key=object_key)
    
    # Removendo os arquivos locais gerados
    shutil.rmtree("spotify_data\\")

    # Retorna o object key do objeto gerado (JSON com as músicas) dentro do bucket
    full_object_key = f"{bucket_name}/{object_key}"
    return full_object_key

def load(csv_object_key="") -> bool:
    """
    Esta é a função responsável por inserir todos os dados extraídos pela requisição à API do Spotify em uma tabela no Big Query.

    :param str csv_object_key: Caminho para o objeto gerado pela função transform() dentro do bucket.

    :return: True se a inserção tiver ocorrido com sucesso. False caso contrário.
    :rtype: bool
    """
    # Criando uma variável de ambiente contendo o caminho para o arquivo "key_file.json" da conta de serviço
    pk_path = os.getcwd()+"\\key_file.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = pk_path

    # Instanciando um novo cliente da API gcloud
    client = bigquery.Client()

    # Checa se o dataset existe. Se não existe, cria um novo dataset
    dataset_id = "Spotify_Data"
    try:
        client.get_dataset(dataset_id)
        print(f"O dataset {dataset_id} já existe!")
    except NotFound:
        try:
            dataset = bigquery.Dataset(f"{client.project}.Spotify_Data")
            client.create_dataset(dataset, timeout=30)
            print(f"Dataset '{dataset_id}' criado com sucesso!")
        except Exception as e:
            print(e)
            return False
    
    try:
    
        # Definindo nova tabela
        table_id = f"{client.project}.{dataset_id}.recently_played"

        destination_table = client.get_table(table_id)
        
        # Definindo a configuração do Job
        job_config = bigquery.LoadJobConfig(
            # Definições do nosso schema (estrutura da tabela)
            schema=[
                bigquery.SchemaField("song_name", "STRING"),
                bigquery.SchemaField("album_name", "STRING"),
                bigquery.SchemaField("artist_name", "STRING"),
                bigquery.SchemaField("duration_ms", "INTEGER"),
                bigquery.SchemaField("popularity", "INTEGER"),
                bigquery.SchemaField("played_at", "TIMESTAMP")
            ],
            # Aqui definimos o número de linhas que queremos pular.
            # Como a primeira linha do nosso csv contém o nome das colunas, queremos pular sempre 1 linha
            skip_leading_rows = 1,
            # Aqui definimos o formato do arquivo fonte (o nosso é um .csv)
            source_format=bigquery.SourceFormat.CSV,
        )

        # Capturando o número de registros na tabela antes de iniciar o load
        query_count = f"SELECT COUNT(*) FROM {table_id}"
        query_count_job = client.query(query_count)
        start_count = 0
        for row in query_count_job:
            start_count=start_count+row[0]

        # Definimos a URI do nosso objeto .csv transformado dentro do bucket
        uri = f"gs://{csv_object_key}"

        # Iniciamos o job que vai carregar os dados para dentro da nossa tabela no BigQuery
        load_job = client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )

        load_job.result()

        # Removendo duplicatas
        remove_duplicates_query = ( f"CREATE OR REPLACE TABLE {table_id}"
                                    f" AS (SELECT DISTINCT * FROM {table_id})")
        remove_duplicates_job = client.query(remove_duplicates_query)
        remove_duplicates_job.result()
        # Capturando o número de registros na tabela depois de realizar o load
        query_count = f"SELECT COUNT(*) FROM {table_id}"
        query_count_job = client.query(query_count)
        end_count = 0
        for row in query_count_job:
            end_count=end_count+row[0]   

        print(f"{end_count-start_count} novos registros em {table_id}!")
    except Exception as e:
        print(e)
        return False
    
    return True
