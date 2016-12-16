from pytrends.request import TrendReq

import json

import sys

import time


def main():

    sleepSecs = 12
    linesToSkip = 330


    #   Initialize pytrends.

    pytrends = TrendReq('surprisefish14@gmail.com', 'Fugi26441996', custom_useragent=None)


    #   Initialize standard_actor.

    standard_actor = 'Leonardo Dicaprio'


    #   Get movie_list_lines.

    with open('unique_movie_list.txt') as movie_list_file:

        movie_list = movie_list_file.readlines()



    for i in range(0, linesToSkip):

        movie_list.pop()


    sys.stdout.write('{')


    #   For each movie...

    for movie in reversed(movie_list):

        sys.stdout.flush()

        time.sleep(sleepSecs)

        movieQ = movie.replace(',', '')


        current_trend = pytrends.trend({'q': standard_actor + ', ' + str.strip(movieQ), 'date': '01/2008 107m'})


        month_list = []

        standard_actor_vals = []

        movie_vals = []


        for row in current_trend['table']['rows']:

            month_list.append(row['c'][0]['v'])

            standard_actor_vals.append(row['c'][1]['f'])

            movie_vals.append(row['c'][2]['f'])


        #   Output the trends to stdout (or whatever we are piping them to).

        sys.stdout.write('"' + str.strip(movie) + '":')

        sys.stdout.write('{"Value":[')

        sys.stdout.write(', '.join(movie_vals))

        sys.stdout.write('],"Standard":[')

        sys.stdout.write(', '.join(standard_actor_vals))

        sys.stdout.write(']}')


        if (movie_list.index(movie) != len(movie_list) - 1):

            sys.stdout.write(',')

        else:

            sys.stdout.write('}')


        sys.stdout.flush()

main()
