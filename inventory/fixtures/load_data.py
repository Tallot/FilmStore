import os
import csv
import json
import gzip
import random
import requests
from tqdm import tqdm
from pprint import pprint

archs = ['name.basics.tsv',
         'title.akas.tsv',
         'title.basics.tsv',
         'title.crew.tsv',
         # 'title.principals.tsv',
         'title.ratings.tsv']


def download(archive_names):
    print('Downloading archives...')
    for archive_name in tqdm(archive_names):
        if os.path.exists(archive_name + '.gz'):
            print('{} already downloded!'.format(archive_name))
        else:
            archive = requests.get('https://datasets.imdbws.com/{}.gz'.format(archive_name))
            file = open(archive_name + '.gz', 'wb')
            file.write(archive.content)
            file.close()
    print('Finished')


def unpack(archive_names):
    print('Unpacking archives...')
    for archive_name in tqdm(archive_names):
        if os.path.exists(archive_name):
            print('{} already unpacked!'.format(archive_name))
        else:
            with gzip.open(archive_name + '.gz', 'rb') as f_in:
                with open(archive_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
    print('Finised')


def prepare_init_data(records_limit=10000):
    print('Preparing data...')
    films = []

    # open files
    basics = open('title.basics.tsv')
    crew = open('title.crew.tsv')
    ratings = open('title.ratings.tsv')

    # create iterators
    basics_reader = csv.reader(basics, delimiter='\t')
    crew_reader = csv.reader(crew, delimiter='\t')
    ratings_reader = csv.reader(ratings, delimiter='\t')

    # skip headers
    next(basics_reader)
    next(crew_reader)
    next(ratings_reader)

    names = open('name.basics.tsv')
    names_reader = csv.reader(names, delimiter='\t')
    names_list = list(names_reader)

    # iterarte throght each file and get only necessary data
    for i in tqdm(range(records_limit)):
        basics_row = next(basics_reader)
        crew_row = next(crew_reader)
        ratings_row = next(ratings_reader)

        if crew_row[1] == '\\N':
            continue

        # future db collection
        film_dict = {'title_alphanum': '', 'primary_title': '', 'is_adult': False,
                     'start_year': 0, 'runtime_minutes': 0, 'genres': [],
                     'directors': [], 'average_rating': 0.0, 'num_votes': 0}

        film_dict['title_alphanum'] = basics_row[0]
        film_dict['primary_title'] = basics_row[2]
        if int(basics_row[4]) == 0:
            film_dict['is_adult'] = False
        else:
            film_dict['is_adult'] = True
        film_dict['start_year'] = int(basics_row[5])
        if basics_row[7] == '\\N':
            film_dict['runtime_minutes'] = random.randint(1, 10)
        else:
            film_dict['runtime_minutes'] = int(basics_row[7])
        film_dict['genres'] = basics_row[8].split(',')

        film_dict['average_rating'] = float(ratings_row[1])
        film_dict['num_votes'] = int(ratings_row[2])

        directors = crew_row[1].split(',')

        for d in directors:
            film_dict['directors'].append(names_list[int(d[2:])][1])

        films.append(film_dict)

    basics.close()
    crew.close()
    ratings.close()
    names.close()

    with open('mongo_init_data.json', 'w') as fp:
        json.dump(films, fp)

    # command_file = open('mongo-init.js', 'w')
    # print('db.films.insertMany([', file=command_file)
    # for film in films:  # to prettify
    #     print(film, ',', sep='', file=command_file)
    # print('])', file=command_file)
    # command_file.close()


if __name__ == '__main__':
    download(archs)
    unpack(archs)
    prepare_init_data()
