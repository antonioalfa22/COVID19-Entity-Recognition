import argparse
import requests
import csv

import pandas as pd
from multiprocessing import Pool


# ========  Entities  ===============
def get_entities(entities_file):
    """Returns an array of Medical Entities

    :param entities_file: Entities file csv
    :return: Array<[term:str, score:int]>
    """
    entities = []
    with open(entities_file, encoding='utf8') as ds1_file:
        csv_reader = csv.reader(ds1_file, delimiter=',')
        for row in csv_reader:
            entities.append([str(row[0]), int(row[1])])
    return entities


# ========  Symptoms  ===============
def search_symptoms(entities_file, clases):
    """Search symptoms in entities with Wikidata

    :param entities_file: Entities file
    :param clases: Symptoms SNOMED_CF
    """
    entities = get_entities(entities_file)
    symptoms = list(filter(lambda x: x[0] in clases, entities))
    with open('entities.txt', 'w') as f:
        for symptom in sorted(symptoms, key=lambda x: x[0], reverse=True):
            f.write("{},{}\n".format(symptom[0], symptom[1]))


# ========  Medications  ============
def search_medications(entities_file):
    """Search medications in entities with Wikidata

    :param entities_file: Entities file
    """
    medicamentos = []
    terminos = get_entities(entities_file)

    pool = Pool(4)
    len_terminos = len(terminos)
    i = 0

    for term in terminos:
        i += 1
        print(str((i / len_terminos) * 100) + '%')
        termino = term[0]
        apariciones = term[1]
        resultados = search_wikidata_results(termino)
        medications = pool.map(check_if_medication, resultados)
        for med in medications:
            if med is not None:
                medicamentos.append([termino, med, apariciones])
    print("=" * 80)
    with open('medications.csv', "w", encoding="utf8") as f:
        for medic in medicamentos:
            f.write("{},{},{}\n".format(medic[0], medic[1], medic[2]))


def search_wikidata_results(termino):
    """Devuelve un array con los IDs de Wikidata de los resultados de la busqueda
    :param termino: str
    :return: str[]
    """
    resultados = []
    url_search = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&language=en&format=json".format(
        termino)
    req = requests.get(url=url_search)
    if req.status_code == 200:
        response_terms = req.json()['search']
        for item in response_terms:
            resultados.append(item)
    return resultados


def check_if_medication(termino):
    term_id = termino['id']
    url_search = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&languages=en&format=json".format(
        term_id)
    req = requests.get(url=url_search)
    medication_id = 'Q12140'
    if req.status_code == 200:
        try:
            possible_med_id = \
                req.json()['entities'][term_id]['claims']['P31'][1]['mainsnak']['datavalue']['value']['id']
            if possible_med_id == medication_id:
                return termino['label']
            else:
                return None
        except:
            return None


# ========  SNOMED  =================

def get_snomed_classes(file):
    """Devuelve un array de terminos (clases)
    :param file: str
    :return: Array<str>
    """
    classes = []
    snomed_df = pd.read_csv(file, low_memory=False).astype(str)
    for clase in snomed_df.itertuples():
        classes.append(clase[2])
    return classes



# ========  Main  ===================
def parse_args():
    parser = argparse.ArgumentParser(description='COVID 19 Entity Recognition')
    parser.add_argument("entities", help="Entities")
    parser.add_argument("-s", "--symptoms", help="Search symptoms", action="store_true")
    parser.add_argument("-m", "--medications", help="Search medications", action="store_true")
    parser.add_argument("-o", "--ontology", help="SNOMED_CF Ontology csv")

    args = parser.parse_args()
    return args


def main(args) -> None:
    symptoms = args.symptoms
    medications = args.medications
    entities = args.entities
    snomed_file = args.ontology if args.ontology is not None else "SNOMED_CF.csv"
    clases = get_snomed_classes(snomed_file)
    if symptoms:
        search_symptoms(entities, clases)
    if medications:
        search_medications(entities)


if __name__ == '__main__':
    main(parse_args())
