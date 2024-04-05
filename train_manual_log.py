from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow

def conduct_single_experiment(n_estimators,
                              min_samples_split,
                              x_train,
                              x_test,
                              y_train,
                              y_test):
    with mlflow.start_run():
        # Create a Random Forest classifier
        rf_classifier = RandomForestClassifier(n_estimators=n_estimators, min_samples_split=min_samples_split)

        # Train the model
        rf_classifier.fit(x_train, y_train)

        # Make predictions
        y_pred = rf_classifier.predict(x_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)

        # Log parameters, metrics, and model
        mlflow.log_params({
            "n_estimators": n_estimators,
            "random_state": min_samples_split
        })
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(rf_classifier, "random_forest_model")

        # Print the results
        print("Random Forest Model Metrics:")
        print("Accuracy:", accuracy)

    # End the MLflow run
    mlflow.end_run()



def simple_grid_search(x_train, x_test, y_train, y_test):
    for n_estimators, min_samples_split in zip([80, 100], [2, 3]):
        conduct_single_experiment(n_estimators, min_samples_split, x_train, x_test, y_train, y_test)



if __name__ == '__main__':

    host = '127.0.0.1'
    port = 8081
    mlflow.set_tracking_uri(uri=f"http://{host}:{port}")

    # %% 手順3 エクスペリメントの作成
    # Experimentの生成 (artifact_locationはDockerfileのコマンドで指定しているので不要)
    EXPERIMENT_NAME = 'RandomForest_Iris_Classification'
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    if experiment is None:  # 当該Experiment存在しないとき、新たに作成
        experiment_id = mlflow.create_experiment(
            name=EXPERIMENT_NAME)
    else:  # 当該Experiment存在するとき、IDを取得
        experiment_id = experiment.experiment_id

    # Start MLflow experiment
    mlflow.set_experiment("")

    cancer = load_breast_cancer()
    X, y = cancer.data, cancer.target

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    simple_grid_search(x_train, x_test, y_train, y_test)

