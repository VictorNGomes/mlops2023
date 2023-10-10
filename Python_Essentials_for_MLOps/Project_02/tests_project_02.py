import requests
from requests.exceptions import RequestException
#from podcast_summary import get_episodes
from airflow.decorators import dag, task

import pytest
import requests_mock

@pytest.fixture
def requests_mock_fixture():
    with requests_mock.Mocker() as mock:
        # Configure o comportamento do mock aqui
        yield mock

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
    episodes = get_episodes()
    assert len(episodes) == 2
    assert episodes[0]['title'] == "Episode 1"
    assert episodes[1]['title'] == "Episode 2"

def test_get_episodes_failure(requests_mock):
    # Configure o mock para simular uma falha na requisição
    requests_mock.get("https://www.marketplace.org/feed/podcast/marketplace/", exc=RequestException("Failed"))

    # Chame a função e verifique se ela lida com a exceção corretamente
    try:
        episodes = get_episodes()
    except RequestException as err:
        assert str(err) == "Failed"
    else:
        pytest.fail("Expected RequestException but got no exception")
