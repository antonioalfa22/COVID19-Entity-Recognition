# COVID19-Entity-Recognition

COVID19-Entity-Recognition uses [scispaCy](https://allenai.github.io/scispacy/) to locate entities in the
[COVID-19 Open Research Dataset (CORD-19)](https://www.semanticscholar.org/cord19) corpus and 
then searches these entities on [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) to recognize whether 
it is a possible symptom or a medication.


## 1. Install

### 1.1. Run ElasticSearch & Kibana

```docker
docker-compose -f docker-compose.yml up -d
```

### 1.2. Index CORD-19 Dataset in ElasticSearch

To create an ElasticSearch index and index the documents in the dataset
you can use the **index_manager.py** script.

```
python index_manager.py [-n NAME] [-d DATASET] [-r] [-c] --host HOST
```

#### 1.2.1. Example 1: Create index and index documents

```commandline
python index_manager.py -n covid19-index -d covid19_dataset -c --host localhost
```

#### 1.2.2. Example 2: Remove index

```commandline
python index_manager.py -n covid19-index -r --host localhost
```


## 2. Stop containers

### 2.1. Stop ELasticSearch & Kibana

```docker
docker-compose -f docker-compose.yml down
```

## 3. Search Entities

To search the entities of the CORD-19 corpus we can use the script **entity_recognition.py**.

```commandline
python entity_recognition.py -n INDEX_NAME --host HOST
```

The output of this script is a file called **entities.txt** with the list of entities ordered by 
number of occurrences in the paragraphs.


## 4. Search Symptoms and Medications

Using the script search.py we can search, once obtained the terms, 
which of those terms are a symptom or are a medication.

```bash
python search.py ENTITIES_FILE [-s] [-m] 
```

### 4.1 Search symptoms

```commandline
python search.py entities.txt -s
```


### 4.1 Search medications

```commandline
python search.py entities.txt -m
```


## 5. Example outputs

### 5.1. Entities

```
time,1046
data,971
model,917
model-the',901
number,893
time-and,876
infected,746
covid,724
covid-,724
covid',724
covid-19,666
infection,588
cases,583
case,558
different,550
population,545
disease,500
epidemic,490
rate,463
individuals,456
```


### 5.2. Symptoms

[Original entity, Wikidata entity, Relevance]

```
cough,cough,19
confusion,mental confusion,18
fever,fever,15
coughing,cough,12
collapse,collapse,7
intermittent,intermittent claudication,4
inflammation,inflammation,3
fatigue,fatigue,3
nostrils,nostrils distended,3
contraction,uterine contraction,2
burnin,heartburn,1
```


### 5.3. Medications

[Original entity, Wikidata entity, Relevance]

```
veneto,venetoclax,10
serine,L-serine,4
arginine,L-Arginine,4
nitrogen,nitrous oxide,3
phyton,(E)-phytonadione,2
antibacterial,antibiotic,1
hydroxychloroquine,hydroxychloroquine,1
methionine,L-methionine,1
betax,betaxolol,0
```