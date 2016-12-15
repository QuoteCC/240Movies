from pytrends.request import TrendReq

import json

import sys

import time


def main():

    sleepSecs = 18
    linesToSkip = 734


    #   Initialize pytrends.

    pytrends = TrendReq('colin.corliss@gmail.com', 'Fugi26441996', custom_useragent=None)


    #   Initialize standard_actor.

    standard_actor = 'Leonardo Dicaprio'


    #   Get movie_list_lines.

    with open('unique_actor_list.txt') as actor_list_file:

        actor_list = actor_list_file.readlines()


		
    for i in range(0, linesToSkip):

        actor_list.pop(0)


    sys.stdout.write('{')


    #   For each movie...

    for actor in actor_list:

        sys.stdout.flush()

        time.sleep(sleepSecs)


        current_trend = pytrends.trend({'q': standard_actor + ', ' + str.strip(actor), 'date': '01/2008 107m'})


        month_list = []

        standard_actor_vals = []

        actor_vals = []


        for row in current_trend['table']['rows']:

            month_list.append(row['c'][0]['v'])

            standard_actor_vals.append(row['c'][1]['f'])

            actor_vals.append(row['c'][2]['f'])


        #   Output the trends to stdout (or whatever we are piping them to).

        sys.stdout.write('"' + str.strip(actor) + '":')

        sys.stdout.write('{"Value":[')

        sys.stdout.write(', '.join(actor_vals))

        sys.stdout.write('],"Standard":[')

        sys.stdout.write(', '.join(standard_actor_vals))

        sys.stdout.write(']}')


        if (actor_list.index(actor) != len(actor_list) - 1):

            sys.stdout.write(',')

        else:

            sys.stdout.write('}')


        sys.stdout.flush()

main()
