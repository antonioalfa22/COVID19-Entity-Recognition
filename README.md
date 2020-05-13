# COVID19-Entity-Recognition

COVID19-Entity-Recognition uses [scispaCy](https://allenai.github.io/scispacy/) to locate symptoms and medications in the
[COVID-19 Open Research Dataset (CORD-19)](https://www.semanticscholar.org/cord19).


## 1. Install

### 1.1. Run ElasticSearch & Kibana

```docker
docker-compose -f docker-compose.yml up -d
```

### 1.2. Index CORD-19 Dataset in ElasticSearch

To create an ElasticSearch index and index the documents in the dataset
you can use the **index_manager.py** script.

```bash
index_manager.py [-h] [-n NAME] [-d DATASET] [-r] [-c] --host HOST
```

#### 1.2.1. Example 1: Create index and index documents

```bash
index_manager.py -n covid19-index -d covid19_dataset -c --host localhost
```

#### 1.2.2. Example 2: Remove index

```bash
index_manager.py -n covid19-index -r --host localhost
```


## 2. Stop containers

### 2.1. Stop ELasticSearch & Kibana

```docker
docker-compose -f docker-compose.yml down
```