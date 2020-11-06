from math import floor, ceil, pow, sqrt
from numpy import loadtxt
from statistics import stdev, mean, variance
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm # Use the tqdm package to track how far your loop is
import pandas as pd 
import json

data = pd.read_csv('population.csv')
outHOUSE = open('house-seats.txt', 'w');
outEC = open('ec-seats.txt', 'w');

min_quotient = 30000;
tot_pop = int(data.at[51,'CurrPop'].replace(',',''))
totSeats = floor(tot_pop/min_quotient);
real_quotient = floor(tot_pop/totSeats);

seats = []
HHQuotient = []
sanitized_pop = []
currSeats = 0

for i in range(len(data)-1):
	sanitized_pop.append(int(data.at[i,'CurrPop'].replace(',','')))
	seats_state = floor(sanitized_pop[i]/min_quotient);
	seats.append(seats_state)
	currSeats += seats_state
	HHQuotient.append(sanitized_pop[i]/ sqrt(seats_state * (seats_state-1)))
	
while currSeats < totSeats:
	id = seats.index(max(seats))
	seats[id] += 1
	currSeats += 1
	HHQuotient[id] = sanitized_pop[i]/ sqrt(seats[id] * (seats[id]-1))

outEC.write("State\tPopulation\tSeats\n");
outHOUSE.write("State\tPopulation\tSeats\n");

for i in range(len(data)-1):
	outHOUSE.write("{0}\t{1}\t{2}\n".format(data.at[i,'State'],sanitized_pop[i],seats[i]))
	outEC.write("{0}\t{1}\t{2}\n".format(data.at[i,'State'],sanitized_pop[i],seats[i]+2))
	
	
outHOUSE.close()
outEC.close()

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

with open('president.json') as f:
	results = json.load(f)

candidates = []

for i in range(len(data)-1):
	currAbbrev = us_state_abbrev[data.at[i,'State']]
	for j in range(len(results['data'][currAbbrev]['cand'])):
		name = results['data'][currAbbrev]['cand'][j]['name']
		notThere = True
		for k in range(len(candidates)):
			if candidates[k] == name:
				notThere = False
		if notThere:
			candidates.append(name)
			
EC = [[]]

for i in range(len(data)-1):
	seatsAvailable = seats[i]+2
	currState = data.at[i,'State']
	currAbbrev = us_state_abbrev[currState]
	names = []
	votes = []
	totVotes = 0
	nCand = len(results['data'][currAbbrev]['cand'])
	for j in range(nCand):
		names.append(results['data'][currAbbrev]['cand'][j]['name'])
		votes.append(results['data'][currAbbrev]['cand'][j]['votes'])
		totVotes += results['data'][currAbbrev]['cand'][j]['votes']
	
	#print(totVotes)
	#print(seatsAvailable)
	nat_quotient = floor(totVotes / seatsAvailable)
	#print(nat_quotient)
	stateSeats = []
	remainder = []
	assignedSeats = 0
	print(seatsAvailable)
	for j in range(nCand):
		stateSeats.append(floor(votes[j]/nat_quotient))
		assignedSeats += floor(votes[j]/nat_quotient)
		remainder.append(floor(votes[j] - nat_quotient * stateSeats[j]))
		
	print(assignedSeats)
	
	while assignedSeats < seatsAvailable:
		id = stateSeats.index(max(stateSeats))
		stateSeats[id] += 1
		assignedSeats += 1
		remainder[id] = floor(votes[id] - nat_quotient * stateSeats[id])
	
	#print(assignedSeats - seatsAvailable)
	
	candId = []
	
	for j in range(nCand):
		for k in range(len(candidates)):
			if (names[j] == candidates[k]):
				candId.append(k)
	
	StateEC = []
	
	for j in range(len(candidates)):
		StateEC.append(0)
	
	for j in range(nCand):
		StateEC[candId[j]] = stateSeats[j]
	
	print(len(StateEC))
	EC.append(StateEC)
	

outProp = open('ec-seats.txt', 'w');
outProp.write("State\t")
for i in range(len(candidates)):
	outProp.write(str(candidates[i])+"\t")
	
outProp.write("\n")
for i in range(1,len(EC)):
	outProp.write(data.at[i-1,'State']+"\t")
	for j in range(len(candidates)):
		outProp.write(str(EC[i][j])+"\t")
	outProp.write("\n")
	