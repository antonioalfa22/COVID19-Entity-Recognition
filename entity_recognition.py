import argparse

import spacy
from elasticsearch import Elasticsearch


# ========  Search Entities  ========
def search_entities(index_name, es):
    """Searchs entities in indexed texts in ElasticSearch

    :param index_name: ElasticSearch index file
    :param es: ElasticSearch object
    :return: Dict<name:str, count:int>
    """
    entities = {}
    total_docs = get_number_docs(index_name, es)
    for i in range(1, total_docs):
        text = get_text(index_name, es, i)
        print("Searching entities in text: " + str(i))
        nlp = spacy.load("en_core_sci_sm")
        doc = nlp(text)
        for entity in doc.ents:
            entity = str(entity).lower()
            entity = clean_text(entity)
            if entity not in entities and len(entity) > 3:
                entities[entity] = get_term_apparitions(index_name, es, entity)
    return entities


def clean_text(texto):
    text = texto
    text = text.replace(" ", "").replace("(", "").replace(")", "").replace("{", "").replace("}",
        "").replace("*","").replace(",", "").replace(".", "").replace(">", "").replace("<", "")
    return text


def get_text(index_name, es, text_id):
    """ Return a text in ElasticSearch with the param id

    :param index_name: ElasticSearch index file
    :param es: ElasticSearch object
    :param text_id: Text id
    :return: str
    """
    res = es.get(index=index_name, id=text_id)
    return res['_source']['text']


def get_term_apparitions(index_name, es, term):
    """ Return a text in ElasticSearch with the param id

    :param index_name: ElasticSearch index file
    :param es: ElasticSearch object
    :param term: Term (Entity) to search
    :return: str
    """
    res = es.count(index=index_name, body={
        "query": {
            "match": {
                "text": {
                    "query": term,
                    "operator": "and"
                }
            }
        }
    })
    return res['count']


def get_number_docs(index_name, es):
    """ Return the number of indexed documents in ElasticSearch

    :param index_name: ElasticSearch index file
    :param es: ElasticSearch object
    :return: int
    """
    res = es.count(index=index_name)
    return res['count']


# ========  Main  ===================

def parse_args():
    parser = argparse.ArgumentParser(description='COVID 19 Entity Recognition')
    parser.add_argument("-n", "--name", help="Index name")
    parser.add_argument("--host", help="ElasticSearch Adress", required=True)
    args = parser.parse_args()
    return args


def main(args) -> None:
    name = args.name if args.name is not None else "covid19-index"
    es = Elasticsearch(hosts=[args.host])
    entities = search_entities(name, es)
    with open('entities.txt', 'w', encoding="utf8") as f:
        for entity in sorted(entities, key=lambda x: entities[x], reverse=True):
            f.write("{},{}\n".format(entity, entities[entity]))


if __name__ == '__main__':
    main(parse_args())
