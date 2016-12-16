import json
import sys




"""
File to Generate tab delimited data files for different subsets of film/data
Pipe output to txt file for further use
"""

#Command line for what attrs you want
attrs = sys.argv[1]
attrs = attrs.split(',')



 
  
with open('master_dataset.txt') as dataset_file:
   dataset_movie_list = dataset_file.readlines()

s = 'Title'
for attr in attrs:
	s = s+ '\t' + attr 
print (s)
   
#   For each movie in the dataset...
for movie in dataset_movie_list:
        #   Initialize the json for this particular movie.
        zero = False
        movie_json = json.loads(movie)
        s = movie_json['Title']
        for attr in attrs:
                #if (float(movie_json[attr]) == 0):
                #        zero = True
                #        break
		s = s+'\t' + movie_json[attr]
	if not zero:
		print(s)
