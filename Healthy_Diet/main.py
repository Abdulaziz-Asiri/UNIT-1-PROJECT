from pprint import pprint
from art import *
from colorama import *
from functions import signup,calculateCaloric,calculateBMI,login
from model import model


def introDisplay():
    intro =Fore.GREEN + text2art("Smart Diet Planner" ) + Style.RESET_ALL
    return print(intro)

def get_user_input():
        print(Fore.LIGHTGREEN_EX+"\nEnter your personal data to calculate you BMI , Calories and generate diet plan: \n "+ Style.RESET_ALL)
        user_info = {
            'age': int(input("Enter your age: ")),
            'gender': input("Enter your gender (Male/Female): "),
            'weight': float(input("Enter your weight (kg): ")),
            'height': float(input("Enter your height (cm): ")),
            'activity_level': input("Enter your activity level (Sedentary, Lightly Active, Active, Very Active): "),
            'health_goal': input("Enter your health goal (Weight Loss, Muscle Gain, Maintenance): "),
    }
        return user_info



def main():

    introDisplay()

    print(Fore.BLUE + "\n--------- Welcome to the Smart Diet Planner! Please sign up or log in to continue. -------------\n" + Style.RESET_ALL)
    while True:
        choice = input('''\n
                       Choose option:
                       (1) Sign Up  
                       (2) Log In
                       (3) Exit
                        \n 
                       ''')
        if choice == '3':
            break
        if choice == '1':
            user = signup.register()
            if user:
                break
        elif choice == '2':
            user = login.login()
            user_info = get_user_input()
            bmi_Results = calculateBMI.calculate_bmi(user_info)
            displayBmi =calculateBMI.display_result(bmi_Results)
            caloric_needs = calculateCaloric.calculate_caloric_needs(user_info)

            print(f"\n ------ {displayBmi} ------- \n")
            print(Fore.GREEN + f"\n---- Recommended daily caloric intake: {caloric_needs:.2f} calories -------\n" + Style.RESET_ALL)

            diet = model.better_model(user_info['weight'], caloric_needs)

            day = 'Monday'
            print(Fore.BLUE+f"\n{day}:" + Style.RESET_ALL)
            for meal, df in diet[day].items():
                print(Fore.BLUE+f"\n  {meal}:" + Style.RESET_ALL)
                print(df.to_string(index=False))
            
            # Convert diet to a formatted string
            diet_str = f"User Info:\n"
            diet_str += f"Age: {user_info['age']}\n"
            diet_str += f"Gender: {user_info['gender']}\n"
            diet_str += f"Weight: {user_info['weight']} kg\n"
            diet_str += f"Height: {user_info['height']} cm\n"
            diet_str += f"Activity Level: {user_info['activity_level']}\n"
            diet_str += f"Health Goal: {user_info['health_goal']}\n"
            diet_str += f"\nBMI Result: {displayBmi}\n"
            diet_str += f"Recommended daily caloric intake: {caloric_needs:.2f} calories\n\n"

            for day, meals in diet.items():
                diet_str += f"{day}:\n"
                for meal, df in meals.items():
                    diet_str += f"  {meal}:\n"
                    diet_str += df.to_string(index=False)
                    diet_str += "\n\n"

            # Save the results to a text file
            with open('diet_plan.txt', 'w') as f:
                f.write(diet_str)

        else:
            print("Invalid choice. Please enter 1 or 2.")   


    
if __name__ == "__main__":
    main()
