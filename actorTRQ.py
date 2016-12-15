from pytrends.request import TrendReq

import json

import sys

import time


def main():

    sleepSecs = 12

    #linesToSkip = 18

    actor_2 = ''


    #   Initialize pytrends.

    pytrends = TrendReq('colin.corliss@gmail.com', 'Tr0ub4dor&8',

            custom_useragent=None)


    #   Initialize standard_actor.

    standard_actor = 'Leonardo Dicaprio'
	
	 with open('unique_actor_list.txt') as actor_list_file:
        actor_list = actor_list_file.readlines()


	sys.stdout.write('{')
	for actor in reverse(actor_list):

                time.sleep(sleepSecs)
				actor = actor.strip()
				sys.stdout.write( '"'+ actor + '":')

				#{'"actor_name":{"Value":[data,data,data], "Standard": [data,data,data]} }
                trend_parameters = {'q': standard_actor + ', ' + actor, 'date': '01/2008 37m'}

                current_trend = pytrends.trend(trend_parameters)


                month_list = []

                standard_actor_vals = []

                actor_vals = []


                for row in current_trend['table']['rows']:

                    month_list.append(row['c'][0]['v'])

                    standard_actor_vals.append(row['c'][1]['f'])

                    actor_vals.append(row['c'][2]['f'])


                #   Output the trends to stdout (or whatever we are piping them to).

                sys.stdout.write('{"Value":[')

                sys.stdout.write(', '.join(actor_vals))

                sys.stdout.write('],"Standard":[')

                sys.stdout.write(', '.join(standard_actor_vals))

                sys.stdout.write(']')


                if (actor_list.index(actor) != len(actor_list) - 1):

                    sys.stdout.write(',')


                sys.stdout.flush()
				
sys.stdout.write('}')
sys.stdout.flush()