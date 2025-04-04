import pandas as pd
import numpy as np
import random
from datetime import date, timedelta


def generate_birthday(offset):    
        
        today = date.today()
        
        # start at the latest date in the range
        end_of_range = today.replace(year=today.year - int(offset))
        
        # grab a random day out of ~1826 days in 5 years
        dob = end_of_range - timedelta(days=random.randint(0,1825))
        
                                        #subtract 1 if the current date is past the birth date
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # must be is iso format
        birthday = dob.isoformat()

        return age, birthday


                        # Age demographic in 5 year intervals
def choose_random_age(filename='common_ages.csv'):
    
    #read data
    df = pd.read_csv(filename, header=None)

    age_ranges = df.iloc[0].tolist()        # Row 1
    weights = list(map(int, df.iloc[1]))    # Row 2 (Population of that age group)
    file_year = list(map(int, df.iloc[2]))  # Row 3


    probabilities = np.array(weights) / sum(weights)

    if not len(file_year) == len(probabilities):
        return f'Error: Invalid list length \n{len(file_year)} != {len(probabilities)}'

    random_i = random.choices(range(len(file_year)), weights=probabilities, k=1)[0]

    age_range = age_ranges[random_i].strip().split('-')
    nameslist = f'first_names/{file_year[random_i]}.csv'
    
    age, birthday = generate_birthday(age_range[0])
    
    return nameslist, age, birthday

### Define Values
nameslist, age, birthday = choose_random_age()
###

                                # Top 5000 by pop.
def choose_random_city(filename='US_cities.csv'):

    df = pd.read_csv(filename)
    
    # Combine city and state into a single locations list 
    locations = [(city, state) for city, state in zip(df['city'].tolist(), df['state_name'].tolist())] 
    
    # Determines probability of each city based on population
    weights = list(map(int, df['population']))
    probabilities = np.array(weights) / sum(weights)

    # Pick a random location
    rand_location = random.choices(locations, weights=probabilities, k=1)[0]
    
    state = rand_location[-1]

    return state, rand_location

###
state, location = choose_random_city()
###

## Pick a random college weighted to be in-state
def choose_random_college(education, state):
    
    #If they haven't been to college don't pick one
    if education == 'High School Diploma/GED' or education == 'Still in High School':
         return 'N/A'
    
    # read data
    df = pd.read_csv('colleges.csv')

    ## Sort by in-state colleges
    instate_colleges = [f'{name}; {city}, {state}' for name, city in 
                zip(df[df['state'] == state]['name'].tolist(), df[df['state'] == state]['city'].tolist())]
    
    all_colleges = [f'{name}; {city}, {state}' for name, city, state in 
                zip(df['name'], df['city'], df['state'])]

    # A bit over 70% chance they went to school in state
    if random.random() < 0.7:
        colleges = instate_colleges
        weights = list(map(int, df[df['state'] == state]['population']))
    else:
        colleges = all_colleges
        weights = list(map(int, df['population']))
    
    probabilities = np.array(weights) / sum(weights)

    rand_college = random.choices(colleges, weights=probabilities, k=1)[0]

    return rand_college

def choose_random_education(age, state):
        
        if age < 18:
            education = 'Still in High School'
        elif 18 <= age <= 22:
            education = random.choice(('High School Diploma/GED', 'Some College, No Degree'))
        else:
            education_levels = [
                "High School Diploma/GED",
                "Some College, No Degree",
                "Associate's Degree",
                "Bachelor's Degree",
                "Master's Degree",
                "Doctoral Degree (Ph.D., etc.)",
                "Professional Degree (JD, MD, etc.)",
            ]

            probabilities = [0.35, 0.25, 0.12, 0.20, 0.05, 0.01, 0.02]  # Percentages

            education_level = random.choices(education_levels, weights=probabilities, k=1)[0]
        
        college = choose_random_college(education_level, state)

        education = f"{education_level}; {college}"

        return education


###
education = choose_random_education(age, state)
###

def generate_email(first_name, last_name):
     
    domains = ['gmail',
            'outlook',
            'yahoo',
            'icloud',
            'protonmail',
            'zoho',
            'aol']
    
    rand_domain = random.choice(domains)

    email = f'{first_name[0]}{last_name}@{}.com'.lower()
    
    return email

def choose_random_name(filename=nameslist):

    #use pandas     # Most common names for approximate birthyear
    df = pd.read_csv(filename)

    # 50/50 chance
    gender = random.choice(('F', 'M'))

    # Only look at the half of the first_names file that holds the chosen gender
    if gender == 'F':
        section = slice(1, 501)
    elif gender == 'M':
        section = slice(501, 1001)

    first_names = df['name'][section].tolist()

    # grab name frequency and determine probability
    weights = df['frequency'][section].tolist()
    probabilities = np.array(weights) / sum(weights)

    # Randomly choose a first name
    first_name, middle_name = random.choices(first_names, weights=probabilities, k=2)[0:2]


## Repeat the process, but simplified, for last names

    df = pd.read_csv('last_names.csv')

    last_names = df['name'].tolist()

    weights = df['frequency'].tolist()
    probabilities = np.array(weights) / sum(weights)

    
    last_name = random.choices(last_names, weights=probabilities, k=1)[0]

## Full name
    name = f'{first_name} {middle_name} {last_name}'

    email = generate_email(first_name, last_name)

    return name, email

###
name, email = choose_random_name()
###


     


print(f'Age: {age}')
print(f'DOB: {birthday}')
print(f'Name: {name}')
print(f'Location: {location}')
print(f'Education: {education}')
print(f'Email: {email}')


# Choose a random first_name
### AI analyze the realness of the first_name
# Regenerate if not real


# Location
## Each City in each state, with population
### Use the population of each city as direct probability.
# Randomly choose city
# Log its ~ geo coordinates


# Age & Birthday
## United states age demographic
### Minimum 18
# Pick age based on real life probability of being that age
# Randomly select birthday based on that age


# Email
# First initial of first first_name, full last first_name, random number 00-99, random domain first_name,


# Interests
## Most common interests in the state
# ?


# Education
## US College database
## Use population of those colleges as probability
### Create weight on the in state colleges, and then a little less weight on surrounding state colleges.
# Pick random college


# First job must be at least 14 years after birth
# Randomize job duration and occupation
# Every year older, the chance they keep the job longer goes up.
# Make the next job start 0-1 year after the other job weighted around 1 month
# Continue looping until the gap catches up to today or the job overlaps with todays date meaning rpesent


