"""
Classifying Heart Disease

Este script carrega dados de um conjunto de dados de doença cardíaca, pré-processa os dados,
treina um modelo de regressão logística e avalia o desempenho do modelo.

"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from ucimlrepo import fetch_ucirepo

def print_function_name(func):
    """Decorator para imprimir o nome da função.

    Args:
        func (function): A função a ser decorada.

    Returns:
        function: A função decorada.
    """
    def wrapper(*args, **kwargs):
        """Função de invólucro que imprime o nome da função antes de executá-la."""
        print(f"Executando função: {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper

def display_head(func):
    """Decorator para exibir as primeiras linhas do DataFrame.

    Args:
        func (function): A função a ser decorada.

    Returns:
        function: A função decorada.
    """
    def wrapper(*args, **kwargs):
        """Função de invólucro que exibe as primeiras
         linhas do DataFrame se o resultado for um DataFrame."""
        result = func(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            print(result.head())
        return result
    return wrapper

def calculate_performance_metrics(func):
    """Decorator para calcular métricas de desempenho.

    Args:
        func (function): A função a ser decorada.

    Returns:
        function: A função decorada.
    """
    def wrapper(model, x_test, y_test):
        """Função de invólucro que calcula métricas de desempenho do modelo e imprime os resultados.

        Args:
            model: O modelo treinado.
            x_test: Os dados de teste.
            y_test: As etiquetas de teste.

        Returns:
            model: O modelo treinado.
        """
        predictions = model.predict(x_test)
        tp = sum((predictions == 1) & (y_test == 1))
        fp = sum((predictions == 1) & (y_test == 0))
        tn = sum((predictions == 0) & (y_test == 0))
        fn = sum((predictions == 0) & (y_test == 1))
        sens = tp / (tp + fn)
        spec = tn / (tn + fp)

        acc = model.score(x_test, y_test)

        print("Test Accuracy:", acc)
        print("Test Sensitivity:", sens)
        print("Test Specificity:", spec)

        return model
    return wrapper

@print_function_name
def load_data(filename):
    """Carrega dados de um arquivo CSV.

    Args:
        filename (str): O nome do arquivo CSV a ser carregado.

    Returns:
        pandas.DataFrame: Um DataFrame contendo os dados do arquivo CSV.
    """
    return pd.read_csv(filename)

@display_head
def select_features_and_target(data):
    """Seleciona recursos (features) e o alvo (target) dos dados.

    Args:
        data (pandas.DataFrame): O DataFrame contendo os dados.

    Returns:
        tuple: Uma tupla contendo os recursos (x) e o alvo (y).
    """
    x = data[["age", "thalach", "restecg", "ca"]]
    y = data["present"]
    return x, y

@calculate_performance_metrics
def evaluate_model(model, x_test, y_test):
    """Avalia o desempenho do modelo.

    Args:
        model: O modelo treinado.
        x_test: Os dados de teste.
        y_test: As etiquetas de teste.

    Returns:
        model: O modelo treinado.
    """
    return model

def fetch_ucirepo_data(id):
    """Busca dados usando o pacote ucimlrepo.

    Args:
        id (int): O ID do conjunto de dados a ser buscado.

    Returns:
        tuple: Uma tupla contendo os recursos (x) e o alvo (y) do conjunto de dados.
    """
    heart_disease = fetch_ucirepo(id=id)
    x = heart_disease.data.features
    y = heart_disease.data.targets
    return x, y

def main():
    """Função principal para treinar e avaliar o modelo."""
    # Obtendo dados usando fetch_ucirepo
    x, y = fetch_ucirepo_data(id=45)

    # Criando um DataFrame a partir dos dados
    heart = pd.DataFrame(data=x, columns=["age", "thalach", "restecg", "ca"])
    heart["present"] = y

    # Removendo linhas com valores ausentes
    heart.dropna(inplace=True)

    # Dividindo o conjunto de dados em treinamento e teste
    x = heart[["age", "thalach", "restecg", "ca"]]
    y = heart["present"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

    # Criando e ajustando o modelo LogisticRegression
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # Avaliando o modelo
    evaluate_model(model, x_test, y_test)

if __name__ == "__main__":
    main()
   