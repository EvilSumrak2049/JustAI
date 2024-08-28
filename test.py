import requests, zipfile, io
import argparse
import os
import re
from model import chain

r = requests.get('http://www.labinform.ru/pub/named_entities/collection5.zip')
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./")


parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, help='count of files to test')
args = parser.parse_args()

def precision(pers_true, pers_pred):
    TP = 0
    FP = 0
    for per_true, per_pred in zip(pers_true, pers_pred):
        for i, name in enumerate(per_pred):
            if per_true[i] == name:
                TP += 1
            else:
                FP += 1
    return TP / (TP + FP)


def recall(pers_true, pers_pred):
    TP = 0
    FN = 0
    for per_true, per_pred in zip(pers_true, pers_pred):
        for i, name in enumerate(per_true):
            if per_pred[i] == name:
                TP += 1
            else:
                FN += 1
    return TP / (TP + FN)


def f1_score(pers_true, pers_pred):
    return 2 * precision(pers_true, pers_pred) * recall(pers_true, pers_pred) / (
                precision(pers_true, pers_pred) + recall(pers_true, pers_pred))


PERS = []
PERS_pred = []
pattern = r'\bPER\b\s+\d+\s+\d+\s+((?:[А-ЯЁ]\.\s*)?[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?)'
listdirs = os.listdir('/content/Collection5')

for i, path in enumerate(listdirs):
    fullpath = os.path.join('./Collection5', path)
    if fullpath.endswith('.ann'):
        with open(fullpath, 'r') as f_teg:
            text_teg = f_teg.read()
            PERS.append(re.findall(pattern, text_teg))
        with open(fullpath.replace('.ann', '.txt'), 'r') as f:
            text = f.read()

            PERS_pred.append(list(map(lambda x: str.strip(x), chain.invoke(text).split(','))))
    if i == args.count * 2:
        break

print(f'precision: {precision(PERS, PERS_pred)}')
print(f'recall: {recall(PERS, PERS_pred)}')
print(f' f1 score: {f1_score(PERS, PERS_pred)}')
