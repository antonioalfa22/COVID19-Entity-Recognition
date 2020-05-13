import argparse
import json
import os

from elasticsearch import Elasticsearch


def create_index(name, es):
    """Create index
    Ignore 400 cause by IndexAlreadyExistsException when creating an index
    :param name: Index name
    :param es: Elastic search object
    """
    es.indices.create(index=name, ignore=400)


def remove_index(name, es):
    """
    :param name: Index name
    :param es: Elastic search object
    """
    es.indices.delete(index=name, ignore=[400, 404])
    indices = es.indices.get_alias().keys()
    print("Remove index: " + name)
    print("--> Existing indexes: " + indices)


def index_dataset(name, directory, es):
    """Indexa en Elastic todos los ficheros del directorio
    :param name: Index Name
    :param directory: Dataset folder
    :param es: ElasticSearch object
    """
    data_set = {"texts": []}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(directory + '/' + filename, "rb") as f:
                raw_json = json.load(f)
                body = raw_json['body_text']
                for x in body:
                    data_set["texts"].append(str(x['text']))
    i = 1
    for text in data_set["texts"]:
        # Send the data into ES
        value = {
            "text": text
        }
        es.index(index=name, ignore=400, doc_type='docket',
                 id=i, body=json.dumps(value))
        print("They've already been indexed " + i + " texts")
        i = i + 1


# ========  Main  ===================

def parse_args():
    parser = argparse.ArgumentParser(description='COVID 19 Symptom Search')
    parser.add_argument("-n", "--name", help="Index name")
    parser.add_argument("-d", "--dataset", help="COVID 19 Dataset folder location")
    parser.add_argument("-r", "--remove", help="Delete Index", action="store_true")
    parser.add_argument("-c", "--create", help="Create Index", action="store_true")
    parser.add_argument("--host", help="ElasticSearch Adress", required=True)
    args = parser.parse_args()
    return args


def main(args) -> None:
    name = args.name if args.name is not None else "covid19-index"
    dataset_folder = args.dataset
    remove = args.remove
    create = args.create
    es = Elasticsearch(hosts=[args.host])
    if create:
        create_index(name, es)
    if remove:
        remove_index(name, es)
    if dataset_folder is not None:
        index_dataset(name, dataset_folder, es)


if __name__ == '__main__':
    main(parse_args())
