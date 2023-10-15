import requests
from requests.exceptions import RequestException
from podcast_summary import podcast_summary
from airflow.models import DagBag, TaskInstance
from airflow.decorators import dag, task
import pendulum
import pytest
import requests_mock
from unittest.mock import patch, Mock



def test_get_episodes():
    dags = podcast_summary()
    task_get_episodes = dags.get_task('get_episodes')
    assert task_get_episodes is not None

@pytest.fixture
def requests_mock_fixture():
    with requests_mock.Mocker() as mock:
        # Configure o comportamento do mock aqui
        yield mock

def test_get_episodes_():
    dags = podcast_summary()
    task = dags.get_task('get_episodes')
    ti = TaskInstance(task)
    mock = Mock()
    # Mock a execução bem-sucedida da tarefa
    mock.patch('airflow.models.TaskInstance.get_state', return_value='success')
    # Execute a tarefa
    ti.run()

    # Verifique se a tarefa foi bem-sucedida
    assert ti.state == 'success'



def test_get_episodes_success(requests_mock):
    # Configure o mock para retornar dados simulados
    mock_data = """
    <rss>
        <channel>
            <item>
                <title>Episode 1</title>
                <link>https://example.com/episode1</link>
                <description>Episode 1 description</description>
                <pubDate>2023-01-01</pubDate>
            </item>
            <item>
                <title>Episode 2</title>
                <link>https://example.com/episode2</link>
                <description>Episode 2 description</description>
                <pubDate>2023-02-01</pubDate>
            </item>
        </channel>
    </rss>
    """
    requests_mock.get("https://www.marketplace.org/feed/podcast/marketplace/", text=mock_data)

    # Chame a função e verifique o resultado
    dag = podcast_summary()
    episodes = dag.get_task('get_episodes')
    ti = TaskInstance(episodes)
    ti.run()

    # Acesse os resultados da execução da tarefa
    result = ti.xcom_pull()

    # Verifique se a propriedade 'title' do primeiro episódio está correta
    assert result[0]['title'] == "Episode 1"
   
    #assert len(episodes) == 2
    assert episodes[0]['title'] == "Episode 1"
    assert episodes[1]['title'] == "Episode 2"

def test_task_load_episodes():
    dag = podcast_summary()
    task_load_episodes = dag.get_task('load_episodes')
    assert task_load_episodes is not None

    # Simule dados de episódios para testar a tarefa
    episodes_data = [{'link': 'episode_link', 'title': 'Episode 1', 'pubDate': '2023-10-13', 'description': 'Description', 'filename': 'episode1.mp3'}]

    ti = TaskInstance(task_load_episodes, execution_date=pendulum.now())
    ti.xcom_push(key=None, value=episodes_data)  # Define os dados simulados como XCom

    # Execute a tarefa
    result = task_load_episodes.execute(ti.get_template_context())

    # Verifique se a tarefa retornou o número esperado de novos episódios
    assert len(result) == 1
