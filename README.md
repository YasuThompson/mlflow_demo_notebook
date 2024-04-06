# mlflow_demo_notebook


![Alt text](static/tracking-setup-overview.png?raw=true "Three scenarios")

# Scenario 1: Localhost (default)
Note: based on this [tutorial](https://mlflow.org/docs/latest/getting-started/quickstart-2/index.html).

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
export MLFLOW_TRACKING_URI=http://127.0.0.1:8081 
cd 1_localhost
python local_deployment_demo.py
```

In the UI choose a model based on a metric
![Alt text](static/model_selection.png?raw=true "Modle selection")

And deploy the selected model, setting a name
![Alt text](static/model_registry.png?raw=true "Modle registry")

And deploy the model, spefifying the
```commandline
mlflow models serve -m models:/sample_model/1 --port 5001 
```
Note 1: you might need to handle the issues like in [this link](https://stackoverflow.com/questions/75534090/mlflow-model-serve-cant-find-pyenv), running the commands below. <br>
```commandline
curl https://pyenv.run | bash
python -m  pip install virtualenv
PATH="$HOME/.pyenv/bin:$PATH"
```
Note 2: If the deployment command above does not work, you can deploy the model also by specifying the model path like `-m <path-of-a-model>` instead of `models:/<model-name>/<model-version>`

In another terminal window, curl the endpoint just made 
```commandline
curl -d '{"dataframe_split": {                                                                           
"columns": ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol"],
"data": [[7,0.27,0.36,20.7,0.045,45,170,1.001,3,0.45,8.8]]}}' \
-H 'Content-Type: application/json' -X POST localhost:5001/invocations
```

If you get a output like below, it is a success

```commandline
{"predictions": [[5.719637393951416]]}%  
```