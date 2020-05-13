import argparse

from elasticsearch import Elasticsearch


# ========  Search Entities  ========
def search_entities(index_name, es):
    """Searchs entities in indexed texts in ElasticSearch

    :param index_name: ElasticSearch index file
    :param es: ElasticSearch object
    :return: Array<str>
    """
    entities = []
    total_docs = get_number_docs(index_name, es)
    for i in range(1, total_docs):
        text = get_text(index_name, es, i)
        if i < 15:
            print(text)
    return entities


def get_text(index_name, es, id):
    """ Return a text in ElasticSearch with the param id

    :param index_name: ElasticSearch index file
    :param es: ElasticSearch object
    :param id: Text id
    :return: str
    """
    res = es.get(index=index_name, id=id)
    return res['_source']['text']


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
    parser = argparse.ArgumentParser(description='COVID 19 Symptom Search')
    parser.add_argument("-n", "--name", help="Index name")
    parser.add_argument("--host", help="ElasticSearch Adress", required=True)
    args = parser.parse_args()
    return args


def main(args) -> None:
    name = args.name if args.name is not None else "covid19-index"
    es = Elasticsearch(hosts=[args.host])
    entities = search_entities(name, es)
    print(entities)


if __name__ == '__main__':
    main(parse_args())
