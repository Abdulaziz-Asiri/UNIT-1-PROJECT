from colorama import * 


def calculate_bmi(user_info):
    """ Calculate Body Mass Index (BMI). """
    if user_info['height'] <= 0:
        raise ValueError("Height must be greater than zero.")
    if user_info['weight'] <= 0:
        raise ValueError("Weight must be greater than zero.")
    height_m = user_info['height'] / 100  # Convert height from cm to meters
    bmi = user_info['weight'] / (height_m ** 2)
    return bmi

def display_result(bmi):

        if bmi<18.5:
            category= Fore.RED +'Underweight' + Style.RESET_ALL
        elif 18.5<=bmi<25:
            category=Fore.GREEN + 'Normal' + Style.RESET_ALL
        elif 25<=bmi<30:
            category=Fore.YELLOW + 'Overweight' + Style.RESET_ALL
        else:
            category=Fore.RED + 'Obesity' + Style.RESET_ALL

        return Fore.CYAN + f"\n Your BMI is {bmi:.2f}kg/m², {category}\n "+ Style.RESET_ALL
