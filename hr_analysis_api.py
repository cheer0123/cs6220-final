"""
To run this app, in your terminal:
> python hr_analysis_api.py
Navigate to:
> http://localhost:8080/ui/
"""
import pickle
from sklearn.compose import ColumnTransformer 
import numpy as np

import connexion
from joblib import load

# Instantiate our Flask app object
app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
app.debug = True
application = app.app


logreg = load('dt.joblib')


# Implement a simple health check function (GET)
def health():
    # Test to make sure our service is actually healthy
    try:
        predict( -0.5902481074083789, 'female', 'No relevent experience', 'no_enrollment', 'Graduate', 'STEM', '15', '50-99', 'Pvt Ltd', '>4', 47)
    except:
        return {"Message": "Service is unhealthy"}, 500

    return {"Message": "Service is OK"}


# Implement our predict function
def predict(city_development_index, gender, relevent_experience, enrolled_university, education_level, major_discipline, experience, company_size, company_type, 
            last_new_job, training_hours):
    input_list = [city_development_index, gender, relevent_experience, enrolled_university, education_level, major_discipline, experience, company_size, company_type, last_new_job, training_hours]

    features_list = parser_input(input_list)
    features = np.array(features_list)
    features = features.reshape(1, -1)
    prediction = logreg.predict(features)

    if prediction[0] == 0:
        predicted_class = "Tring for new job"
    else:
        predicted_class = "Not tring for new job"
    return {"prediction": predicted_class}


def parser_input(input_list):
    #0 city_development_index
    city_development_index = input_list[0]
    
    #1 gender
    if input_list[1] == 'male':
        gender = 0
    elif input_list[1] == 'female':
        gender = 1
    else: 
        gender = 2
    
    #2 relevent experience
    if input_list[2] == 'No relevent experience':
        relevent_experience = 0
    else: 
        relevent_experience = 1

    #3 enrolled_university 
    if input_list[3] == 'no_enrollment':
        enrolled_university = 0
    elif  input_list[3] == 'Part time course':
        enrolled_university = 1
    elif input_list[3] == 'Full time course':
        enrolled_university = 2
    else:
        print("please input correct enrolled_university type")

    #4 education_level
    if input_list[4] == 'Graduate':
        education_level = 0
    elif input_list[4] == 'Masters':
        education_level = 1
    elif input_list[4] == 'Phd':
        education_level = 2
    else:
        print("please input correct education level") 

    #5 major_discipline
    if input_list[5] == 'Arts':
        major_discipline = 0
    elif input_list[5] == 'Business Degree':
        major_discipline = 1
    elif input_list[5] == 'Humanities':
        major_discipline = 2
    elif input_list[5] == 'No Major':
        major_discipline = 3
    elif input_list[5] == 'Other':
        major_discipline = 4
    elif input_list[5] == 'STEM':
        major_discipline = 5
    else:
        print("please input correct major discipline") 

    #6 experience
    if input_list[6] == '>20':
        experience = 20
    elif input_list[6] == '<1':
        experience = 1
    else:
        experience = int(input_list[6])
    
    #7 company_size
    if input_list[7] == '<10':
        company_size = 0
    elif input_list[7] == '10/49':
        company_size = 1
    elif input_list[7] == '50-99':
        company_size = 2
    elif input_list[7] == '100-500':
        company_size = 3
    elif input_list[7] == '500-999':
        company_size = 4
    elif input_list[7] == '1000-4999':
        company_size = 5
    elif input_list[7] == '5000-9999':
        company_size = 6
    elif input_list[7] == '10000+':
        company_size = 7
    else:
       print("please input correct company size")  
    
    #8 company_type
    if input_list[8] == 'Early Stage Startup':
        company_type = 0
    elif input_list[8] == 'Funded Startup':
        company_type = 1
    elif input_list[8] == 'NGO':
        company_type = 2
    elif input_list[8] == 'Other':
        company_type = 3
    elif input_list[8] == 'Public Sector':
        company_type = 4
    elif input_list[8] == 'Pvt Ltd':
        company_type = 5
    else:
        print("please input correct company type")  

    #9 last new job
    if input_list[9] == '>4':
        last_new_job = 4
    elif input_list[9] ==  'never':
        last_new_job = 10000
    else:
        last_new_job = int(input_list[9])
    
    #10 training_hours
    training_hours = int(input_list[10])

    features = [city_development_index, gender, relevent_experience, enrolled_university, education_level, major_discipline, experience, company_size, company_type, last_new_job, training_hours]
    return features


app.add_api("hr_analysis_api.yaml")
    
if __name__ == '__main__':
    app.run()
