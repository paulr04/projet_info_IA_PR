from datetime import *
import re
import csv
import os
import random
from objects import *
import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime
from collections import defaultdict
from collections import Counter

fichier_vehicules='vehicules.csv'
fichier_reservations='reservations.csv'

print('chemin_repertoire')
print(os.path.dirname(os.path.realpath(__file__)))
chemin_repertoire=os.path.dirname(os.path.realpath(__file__))
print('chemin_data')
print(os.path.join(chemin_repertoire, 'data'))
chemin_data=os.path.join(chemin_repertoire, 'data')
print('chemin_vehicules')
print(os.path.join(chemin_data, fichier_vehicules))
