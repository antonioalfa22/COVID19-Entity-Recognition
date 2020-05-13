import argparse

from elasticsearch import Elasticsearch


# ========  Entities  ===============
def get_entities(entities_file):
    """Returns an array of Medical Entities

    :param entities_file: Entities file csv
    :return: Array<str>
    """
    entities = []
    return entities


# ========  Symptoms  ===============
def search_symptoms(index_name, es, entities_file):
    """Search symptoms in entities with Wikidata

    :param index_name: ElasticSearch index name
    :param es: ElasticSearch object
    :param entities_file: Entities file
    """
    entities = get_entities(entities_file)


# ========  Medications  ============
def search_medications(index_name, es, entities_file):
    """Search medications in entities with Wikidata

    :param index_name: ElasticSearch index name
    :param es: ElasticSearch object
    :param entities_file: Entities file
    """
    entities = get_entities(entities_file)


# ========  Main  ===================
def parse_args():
    parser = argparse.ArgumentParser(description='COVID 19 Symptom Search')
    parser.add_argument("entities", help="Entities")
    parser.add_argument("-n", "--name", help="Index name")
    parser.add_argument("-s", "--symptoms", help="Search symptoms", action="store_true")
    parser.add_argument("-m", "--medications", help="Search medications", action="store_true")
    parser.add_argument("--host", help="ElasticSearch Adress", required=True)
    args = parser.parse_args()
    return args


def main(args) -> None:
    name = args.name if args.name is not None else "covid19-index"
    symptoms = args.symptoms
    medications = args.medications
    entities = args.entities
    es = Elasticsearch(hosts=[args.host])
    if symptoms:
        search_symptoms(name, es, entities)
    if medications:
        search_medications(name, es, entities)


if __name__ == '__main__':
    main(parse_args())
