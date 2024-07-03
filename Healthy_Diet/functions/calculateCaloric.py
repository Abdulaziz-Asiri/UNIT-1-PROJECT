

def calculate_caloric_needs(user_info):
    # Using Mifflin-St Jeor Equation
    if user_info['gender'].lower() == 'Male':
        bmr = 10 * user_info['weight'] + 6.25 * user_info['height'] - 5 * user_info['age'] + 5
    else:
        bmr = 10 * user_info['weight'] + 6.25 * user_info['height'] - 5 * user_info['age'] - 161

    activity_multiplier = {
        'sedentary': 1.2,
        'sightly active': 1.375,
        'active': 1.55,
        'very active': 1.725
    }

    caloric_needs = bmr * activity_multiplier[user_info['activity_level'].lower()]

    # Adjust based on health goal
    if user_info['health_goal'].lower() == 'weight loss':
        caloric_needs -= 500  # Example: Reduce 500 calories for weight loss
    elif user_info['health_goal'].lower() == 'muscle gain':
        caloric_needs += 500  # Example: Add 500 calories for muscle gain

    return int(caloric_needs)

# user_info = get_user_input()
# caloric_needs = calculate_caloric_needs(user_info)
# print(caloric_needs)