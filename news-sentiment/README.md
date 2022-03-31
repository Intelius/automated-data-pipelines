## News sentiment 
In this repo, we define a news sentiment model API that recieves news description and  predicts a sentiment category based on pre-trained model. These categories are Negative, Positive and Neutral. 

##  Project organization

------------

├── README.md          <- The top-level README for developers using this project.
│
├── kubernetes-manifests
│   ├── newssentiment-deployment.yaml        <-  Kubernetes config for deployment
│   ├── newssentiment-service.yaml     <- Kubernetes config for the service
│
├── model_news         <- the directory for pretrained saved model
│       ├── news
│           └── newssentiment_artifacts
│               └── artifacts
│                   └── sentiment-prediction
│                       └── data_news
│                           └── model
│                               └──saved_model.pb   < - the pre-trained saved model
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    ├── .gitignore   <- determine ignored directories when we use version control
    │
    ├── Dockerfile    <-  script of instructions that is used to create a container image.
    │
    ├── input           <- the data needed for sentiment prediction
    │   └── glove.6B.100d.txt
    │
    ├── entrypoint.py  <- define the main function when we call the FAST API
    │
    ├── news_main.py  <- run the prediction model for sentimenting (categorizing) news 
    │
    ├── news_preprocess.py  <- the preprocessing step
    │
    └── news_util.py <- util functions to adopt the format of the news

------------