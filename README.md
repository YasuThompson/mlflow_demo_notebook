# mlflow_demo_notebook


![Alt text](static/tracking-setup-overview.png?raw=true "Overview")

# Scenario 1: Localhost (default)

Setting up an environment
```commandline
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run a local tracking server
```commandline
mlflow server --host 127.0.0.1 --port 8081
```
Open `http://127.0.0.1:8081` in a browser

In another terminal window
```commandline
source venv/bin/activate
cd 1_localhost
python local_deployment_demo.py
```
In the UI, register a model like in the figure below. 
```commandline
mlflow models serve -m models:/sample_model/1 --port 5001 
```
Note: you might need to handle the issues like in [this link](https://stackoverflow.com/questions/75534090/mlflow-model-serve-cant-find-pyenv).

In another terminal window, curl the endpoint just made 
```commandline
curl -d '{"dataframe_split": {                                                                           
"columns": ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol"],
"data": [[7,0.27,0.36,20.7,0.045,45,170,1.001,3,0.45,8.8]]}}' \
-H 'Content-Type: application/json' -X POST localhost:5001/invocations
```