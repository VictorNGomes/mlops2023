import pytest
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from classifying_heart_disease import load_data, select_features_and_target, evaluate_model, fetch_ucirepo_data



# Teste para a função select_features_and_target
def test_select_features_and_target():
    data = pd.DataFrame({"age": [45, 50, 55], "thalach": [160, 170, 180], "restecg": [0, 1, 0], "ca": [1, 2, 0], "present": [0, 1, 1]})
    x, y = select_features_and_target(data)
    assert isinstance(x, pd.DataFrame)
    assert isinstance(y, pd.Series)
    assert "age" in x.columns
    assert "present" not in x.columns

# Teste para a função fetch_ucirepo_data
def test_fetch_ucirepo_data():
    x, y = fetch_ucirepo_data(id=45)
    heart = pd.DataFrame(data=x, columns=["age", "thalach", "restecg", "ca"])
    heart["present"] = y
    heart.dropna(inplace=True)

    x = heart[["age", "thalach", "restecg", "ca"]]
    y = heart["present"]
    assert isinstance(x, pd.DataFrame)
    assert isinstance(y, pd.Series)
    assert x.shape[0] == y.shape[0]


# Execute os testes
if __name__ == "__main__":
    pytest.main()
