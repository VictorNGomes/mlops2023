"""
Este módulo faz parte da biblioteca padrão do Python e 
fornece funcionalidades relacionadas ao sistema operacional.
Você pode usá-lo para interagir com o sistema operacional, 
como criar, excluir, listar e manipular arquivos e diretórios, 
obter informações sobre o ambiente de execução e muito mais.
"""
import os
import json
import logging
import requests
import xmltodict
import pendulum

from airflow.decorators import dag, task
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

# Configuração do logging
LOG_FILE = 'podcast_summary.log'
log_handler = logging.FileHandler(LOG_FILE)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
EPISODE_FOLDER = "episodes"
FRAME_RATE = 16000

@dag(
    dag_id='podcast_summary',
    schedule_interval="@daily",
    start_date=pendulum.now(),
    catchup=False,
    auto_register=False
)
def podcast_summary():
    """
    This DAG (Directed Acyclic Graph) downloads podcast episodes from a given URL,
    transcribes the audio content, and stores the data in a SQLite database.

    It consists of several tasks:
    - create_table_sqlite: Creates a SQLite table if it doesn't exist.
    - get_episodes: Fetches podcast episode data from the specified URL.
    - load_episodes: Loads new podcast episodes into the database.
    - download_episodes: Downloads podcast audio files.
    - speech_to_text: Transcribes audio content to text using Vosk.

    Args:
        None

    Returns:
        None
    """
    create_database = SqliteOperator(
        task_id='create_table_sqlite',
        sql=r"""
        CREATE TABLE IF NOT EXISTS episodes (
            link TEXT PRIMARY KEY,
            title TEXT,
            filename TEXT,
            published TEXT,
            description TEXT,
            transcript TEXT
        );
        """,
        sqlite_conn_id="podcasts"
    )

    @task()
    def get_episodes():
        """
        Fetches podcast episode data from the specified URL.

        Args:
            None

        Returns:
            episodes: List of podcast episode data.
        """
        try:
            data = requests.get(PODCAST_URL, timeout=10)
            data.raise_for_status()  # Verifica se houve erro na requisição HTTP
            feed = xmltodict.parse(data.text)
            episodes = feed["rss"]["channel"]["item"]
            logger.info("Found %s episodes.",len(episodes))
            return episodes
        except requests.exceptions.RequestException as err:
            logger.error("Error fetching podcast data: %s",err)
            raise

    podcast_episodes = get_episodes()
    create_database.set_downstream(podcast_episodes)

    @task()
    def load_episodes(episodes):
        """
        Loads new podcast episodes into the database.

        Args:
            episodes: List of podcast episode data.

        Returns:
            new_episodes: List of newly loaded episode data.
        """
        hook = SqliteHook(sqlite_conn_id="podcasts")
        stored_episodes = hook.get_pandas_df("SELECT * from episodes;")
        new_episodes = []
        try:
            for episode in episodes:
                if episode["link"] not in stored_episodes["link"].values:
                    filename = f"{episode['link'].split('/')[-1]}.mp3"
                    new_episodes.append([episode["link"],
                                          episode["title"],
                                          episode["pubDate"],
                                          episode["description"],
                                          filename]
                                        )

            hook.insert_rows(table='episodes',
                            rows=new_episodes,
                            target_fields=["link",
                                            "title",
                                            "published",
                                            "description",
                                            "filename"])
            logger.info("Loaded %s new episodes.",len(new_episodes))
            return new_episodes
        except Exception as err:
            logger.error("Error loading episodes into the database: %s",err)
            raise

    new_episodes = load_episodes(podcast_episodes)

    @task()
    def download_episodes(episodes):
        """
        Downloads podcast audio files.

        Args:
            episodes: List of podcast episode data.

        Returns:
            audio_files: List of downloaded audio file data.
        """
        audio_files = []
        try:
            for episode in episodes:
                name_end = episode["link"].split('/')[-1]
                filename = f"{name_end}.mp3"
                audio_path = os.path.join(EPISODE_FOLDER, filename)
                if not os.path.exists(audio_path):
                    logger.info("Downloading %s",filename)
                    audio = requests.get(episode["enclosure"]["@url"], timeout=10)
                    audio.raise_for_status()  # Verifica se houve erro no download
                    with open(audio_path, "wb+") as file:
                        file.write(audio.content)
                audio_files.append({
                    "link": episode["link"],
                    "filename": filename
                })
            logger.info("Downloaded %s audio files.",len(audio_files))
            return audio_files
        except (requests.exceptions.RequestException, IOError) as err:
            logger.error("Error downloading audio files: %s}",err)
            raise

    audio_files = download_episodes(podcast_episodes)

    @task()
    def speech_to_text():
        """
        Transcribes audio content to text using Vosk.

        Args:
            None

        Returns:
            None
        """
        hook = SqliteHook(sqlite_conn_id="podcasts")
        untranscribed_episodes = hook.get_pandas_df(
            "SELECT * from episodes WHERE transcript IS NULL;"
        )

        model = Model(model_name="vosk-model-en-us-0.22-lgraph")
        rec = KaldiRecognizer(model, FRAME_RATE)
        rec.SetWords(True)

        try:
            for _, row in untranscribed_episodes.iterrows():
                logger.info("Transcribing %s",row['filename'])
                filepath = os.path.join(EPISODE_FOLDER, row["filename"])
                mp3 = AudioSegment.from_mp3(filepath)
                mp3 = mp3.set_channels(1)
                mp3 = mp3.set_frame_rate(FRAME_RATE)

                step = 20000
                transcript = ""
                for i in range(0, len(mp3), step):
                    logger.debug("Transcription progress: %s",i/len(mp3))
                    segment = mp3[i:i+step]
                    rec.AcceptWaveform(segment.raw_data)
                    result = rec.Result()
                    text = json.loads(result)["text"]
                    transcript += text
                hook.insert_rows(
                    table='episodes',
                    rows=[[row["link"], transcript]],
                    target_fields=["link", "transcript"],
                    replace=True
                )
                logger.info("Transcription completed for %s",row['filename'])
        except Exception as err:
            logger.error("Error transcribing audio content: %s",err)
            raise

    # Uncomment this to try speech to text (may not work)
    speech_to_text()

SUMMARY = podcast_summary()
