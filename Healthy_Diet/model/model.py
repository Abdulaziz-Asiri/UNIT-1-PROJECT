import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pulp import *
from pprint import pprint

data = pd.read_csv('/Users/abdulaziz/Desktop/Python_Bootcamp/Repositories/UNIT-1-PROJECT/Healthy_Diet/model/nutrition.csv').drop('Unnamed: 0', axis=1)

# Select relevant columns
data = data[['name', 'serving_size', 'calories', 'carbohydrate', 'total_fat', 'protein']]

# Drop serving_size column
data = data.drop('serving_size', axis=1)

# Convert carbohydrate, protein, and total_fat columns to float
data['carbohydrate'] = data['carbohydrate'].str.split(' ').str[0].astype(float)
data['protein'] = data['protein'].str.split(' ').str[0].astype(float)
data['total_fat'] = data['total_fat'].str.split('g').str[0].astype(float)

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
split_values_day = np.linspace(0, len(data), 8).astype(int)
split_values_day[-1] = split_values_day[-1] - 1

def random_dataset_day():
    frac_data = data.sample(frac=1).reset_index(drop=True)
    day_data = [frac_data.loc[split_values_day[s]:split_values_day[s+1]] for s in range(len(split_values_day) - 1)]
    return dict(zip(week_days, day_data))

meals = ['Snack 1', 'Snack 2', 'Breakfast', 'Lunch', 'Dinner']
split_values_meal = np.linspace(0, split_values_day[1], len(meals) + 1).astype(int)
split_values_meal[-1] = split_values_meal[-1] - 1

def random_dataset_meal(data_day):
    frac_data = data_day.sample(frac=1).reset_index(drop=True)
    meal_data = [frac_data.loc[split_values_meal[s]:split_values_meal[s+1]] for s in range(len(split_values_meal) - 1)]
    return dict(zip(meals, meal_data))

# Calculate nutritional values
def build_nutritional_values(kg, calories):
    protein_calories = kg * 4
    carb_calories = calories / 2
    fat_calories = calories - carb_calories - protein_calories
    return {'Protein Calories': protein_calories, 'Carbohydrates Calories': carb_calories, 'Fat Calories': fat_calories}

# Extract grams from nutritional values
def extract_gram(table):
    protein_grams = table['Protein Calories'] / 4
    carbs_grams = table['Carbohydrates Calories'] / 4
    fat_grams = table['Fat Calories'] / 9
    return {'Protein Grams': protein_grams, 'Carbohydrates Grams': carbs_grams, 'Fat Grams': fat_grams}

days_data = random_dataset_day()

def model(prob, kg, calories, meal, data):
    G = extract_gram(build_nutritional_values(kg, calories))
    E = G['Carbohydrates Grams']
    F = G['Fat Grams']
    P = G['Protein Grams']
    day_data = data[data.calories != 0]
    food = day_data.name.tolist()
    c = day_data.calories.tolist()
    x = pulp.LpVariable.dicts("x", indices=food, lowBound=0, upBound=1.5, cat='Continuous')
    e = day_data.carbohydrate.tolist()
    f = day_data.total_fat.tolist()
    p = day_data.protein.tolist()
    div_meal = meal_split[meal]
    prob += pulp.lpSum([x[food[i]] * c[i] for i in range(len(food))])
    prob += pulp.lpSum([x[food[i]] * e[i] for i in range(len(x))]) >= E * div_meal
    prob += pulp.lpSum([x[food[i]] * f[i] for i in range(len(x))]) >= F * div_meal
    prob += pulp.lpSum([x[food[i]] * p[i] for i in range(len(x))]) >= P * div_meal
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    variables = [v.name for v in prob.variables()]
    values = [v.varValue for v in prob.variables()]
    sol = pd.DataFrame({'Food': food, 'Quantity': np.array(values).round(2)})
    sol = sol[sol['Quantity'] != 0.0]
    sol['Quantity'] = sol['Quantity'] * 100
    sol = sol.rename(columns={'Quantity': 'Quantity (g)'})
    return sol

def total_model(kg, calories):
    result = []
    for day in week_days:
        prob = pulp.LpProblem("Diet", LpMinimize)
        print(f'Building a model for {day}')
        result.append(model(prob, kg, calories, day))
    return dict(zip(week_days, result))

meal_split = {'Snack 1': 0.10, 'Snack 2': 0.10, 'Breakfast': 0.15, 'Lunch': 0.35, 'Dinner': 0.30}

def better_model(kg, calories):
    days_data = random_dataset_day()
    res_model = []
    for day in week_days:
        day_data = days_data[day]
        meals_data = random_dataset_meal(day_data)
        meal_model = []
        for meal in meals:
            meal_data = meals_data[meal]
            prob = pulp.LpProblem("Diet", LpMinimize)
            sol_model = model(prob, kg, calories, meal, meal_data)
            meal_model.append(sol_model)
        res_model.append(meal_model)
    unpacked = [dict(zip(meals, res_model[i])) for i in range(len(res_model))]
    return dict(zip(week_days, unpacked))

# diet = better_model(80, 2000)
#print plane for all days
# Pretty print the results
# for day, meals in diet:
#     print(f"\n{day}:")
#     for meal, df in meals.items():
#         print(f"\n  {meal}:")
#         print(df.to_string(index=False))

#Print plane for one day
# day = 'Monday'
# print(f"\n{day}:")
# for meal, df in diet[day].items():
#     print(f"\n  {meal}:")
#     print(df.to_string(index=False))
