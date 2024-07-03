import pandas as pd

# Load data
df = pd.read_csv('/Users/abdulaziz/Desktop/Python_Bootcamp/Repositories/UNIT-1-PROJECT/nutrition1.csv')

def calculate_bmr(age, gender, weight, height):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_daily_caloric_needs(bmr, activity_level):
    activity_factors = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'super_active': 1.9
    }
    return bmr * activity_factors[activity_level]

def get_user_input():
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ")
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))
    activity_level = input("Enter your activity level (sedentary, lightly_active, moderately_active, very_active, super_active): ")
    goal = input("Enter your goal (weight_loss, muscle_gain, general_health): ")
    
    return age, gender, weight, height, activity_level, goal

def recommend_meals(daily_caloric_needs, goal):
    if goal == 'weight_loss':
        target_calories = daily_caloric_needs * 0.8  # Reduce caloric intake by 20%
    elif goal == 'muscle_gain':
        target_calories = daily_caloric_needs * 1.2  # Increase caloric intake by 20%
    else:
        target_calories = daily_caloric_needs  # Maintain caloric intake for general health

    # Filter meals based on the target calories
    recommendations = df[df['calories'] <= target_calories / 3]  # Assume 3 meals a day
    
    return recommendations[['name', 'calories', 'protein', 'carbs', 'fats']]

def main():
    age, gender, weight, height, activity_level, goal = get_user_input()
    
    bmr = calculate_bmr(age, gender, weight, height)
    daily_caloric_needs = calculate_daily_caloric_needs(bmr, activity_level)
    
    recommendations = recommend_meals(daily_caloric_needs, goal)
    
    print(f"\nDaily Caloric Needs: {daily_caloric_needs:.2f} calories")
    print("\nRecommended meals for your goal:")
    print(recommendations)

if __name__ == "__main__":
    main()

