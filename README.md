## IRProject

This is the personal assignment of zhiyuan hu on his Information Retrieval Class. The aim is to develop an IR system which can build index and conduct query effectively



#### How to use

----------

Step1. Download dataset to the *data* directory

> Please contact our teaching assistant since the dataset is not released.

Step2. Index construction

First, make sure you have started the Elasticsearch server, run the following command in the terminal

```bash
$ elasticsearch
```

Then construct the index.

```python
python preprocess/index.py --docs <path_to_your_crops>
```

This process will be time-consuming, I am trying to accelerate it.

The program will print the document num of your crop, **you need to manually fill this number to the 6ht line of frontend/util.py.**

Step3. Start frontend and begin query!

```python
python main.py
```

Access 127.0.0.1:5000 to begin your query.

