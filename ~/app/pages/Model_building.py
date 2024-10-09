import streamlit as st
from kmodes.kmodes import KModes
import base64
import pickle

# Load the trained model
try:
    trained_model = pickle.load(open('kmodes_model.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model: {e}")

# Image For Page
file_ = open("image.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

# Encoding function to convert input data into numerical values
def encode_input(gender, age, school, exam, location, cbt_technical_issues, guardians_education, 
                 exam_readiness, exam_preparation, after_school_study, exam_guidance, 
                 exam_confidence, health_issues, family_support):
    gender_dict = {'Choose': None, 'Male': 0, 'Female': 1}
    age_dict = {'Choose': None, '15-17 years': 0, '18-20 years': 1, '21-23 years': 2, '24 years or older': 3}
    school_dict = {'Choose': None, 'Private School': 0, 'Public School': 1}
    exam_dict = {'Choose': None, 'WAEC': 0, 'JAMB': 1, 'Both WAEC and JAMB': 2}
    location_dict = {'Choose': None, 'Urban area': 0, 'Rural area': 1, 'Semi-urban area': 2}
    cbt_technical_issues_dict = {'Choose': None, 'Yes, frequently': 0, 'Yes, occasionally': 1, 'No, never': 2}
    guardians_education_dict = {'Choose': None, 'Primary education': 0, 'Secondary education': 1, 
                                 'Tertiary education': 2, 'No formal education': 3}
    exam_readiness_dict = {'Choose': None, 'Very well prepared': 0, 'Somewhat prepared': 1, 
                           'Not well prepared': 2, 'Not prepared at all': 3}
    exam_preparation_dict = {'Choose': None, 'Extremely stressful': 0, 'Moderately stressful': 1, 
                             'Not stressful': 2}
    after_school_study_dict = {'Choose': None, 'Every day': 0, 'A few times a week': 1, 
                                'Occasionally': 2, 'Rarely or never': 3}
    exam_guidance_dict = {'Choose': None, 'Very easy to access': 0, 'Somewhat easy to access': 1, 
                          'Difficult to access': 2, 'Not available at all': 3}
    exam_confidence_dict = {'Choose': None, 'Very confident': 0, 'Somewhat confident': 1, 
                            'Not confident': 2, 'Unsure': 3}
    health_issues_dict = {'Choose': None, 'Yes': 0, 'No': 1}
    family_support_dict = {'Choose': None, 'Very supportive': 0, 'Somewhat supportive': 1, 
                           'Not supportive': 2, 'Indifferent': 3}

    # Encode the inputs
    return [
        gender_dict[gender], age_dict[age], school_dict[school], exam_dict[exam],
        location_dict[location], cbt_technical_issues_dict[cbt_technical_issues], 
        guardians_education_dict[guardians_education], exam_readiness_dict[exam_readiness], 
        exam_preparation_dict[exam_preparation], after_school_study_dict[after_school_study], 
        exam_guidance_dict[exam_guidance], exam_confidence_dict[exam_confidence], 
        health_issues_dict[health_issues], family_support_dict[family_support]
    ]

# Define a function to generate recommendations based on cluster profiles
def generate_recommendations(cluster_label):
    if cluster_label == 0:
        return "Needs foundational support in exam preparation, increased access to exam resources, and stress management strategies."
    elif cluster_label == 1:
        return "Requires stress management and more advanced tools for exam preparation to maintain high performance and confidence levels."
    elif cluster_label == 2:
        return "Benefits from personalized preparation plans and confidence-building programs, with an emphasis on consistent study routines and leveraging family support."
    else:
        return "No specific recommendation."

# Function to predict cluster
def predict_cluster(data):
    try:
        cluster_label = trained_model.predict([data])
        return cluster_label[0]
    except Exception as e:
        st.error(f"Cluster prediction error: {e}")

# Function to make predictions and generate recommendations
def generate_prediction_and_recommendation(data):
    try:
        # Get prediction
        prediction = trained_model.predict([data])
        
        # Predict cluster label
        cluster_label = predict_cluster(data)

        # Generate recommendation based on the cluster
        recommendation = generate_recommendations(cluster_label)

        # Format result
        return {
            "prediction": prediction[0],
            "recommendation": recommendation,
            "cluster_label": cluster_label
        }
    except Exception as e:
        return f"Prediction error: {e}"

# Main app interface
st.title('WAEC & JAMB Exam Challenges Prediction')

# Input fields for prediction variables
try:
    gender = st.selectbox('Gender', ['Choose', 'Male', 'Female'])
    age = st.selectbox('Age Group', ['Choose', '15-17 years', '18-20 years', '21-23 years', '24 years or older'])
    school = st.selectbox('School Type', ['Choose', 'Private School', 'Public School'])
    exam = st.selectbox('Exam Type', ['Choose', 'WAEC', 'JAMB', 'Both WAEC and JAMB'])
    location = st.selectbox('Location', ['Choose', 'Urban area', 'Rural area', 'Semi-urban area'])
    cbt_technical_issues = st.selectbox('Issues With CBT', ['Choose', 'Yes, frequently', 'Yes, occasionally', 'No, never'])
    guardians_education = st.selectbox("Guardian's Education Level", ['Choose', 'Primary education', 
                                                                     'Secondary education', 'Tertiary education', 
                                                                     'No formal education'])
    exam_readiness = st.selectbox('Exam Readiness', ['Choose', 'Very well prepared', 'Somewhat prepared', 
                                                      'Not well prepared', 'Not prepared at all'])
    exam_preparation = st.selectbox('Exam Preparation Level', ['Choose', 'Extremely stressful', 
                                                               'Moderately stressful', 'Not stressful'])
    after_school_study = st.selectbox('After School Study', ['Choose', 'Every day', 'A few times a week', 
                                                              'Occasionally', 'Rarely or never'])
    exam_guidance = st.selectbox('Exam Guidance Availability', ['Choose', 'Very easy to access', 
                                                               'Somewhat easy to access', 'Difficult to access', 
                                                               'Not available at all'])
    exam_confidence = st.selectbox('Exam Confidence Level', ['Choose', 'Very confident', 'Somewhat confident', 
                                                             'Not confident', 'Unsure'])
    health_issues = st.selectbox('Health Issues', ['Choose', 'Yes', 'No'])
    family_support = st.selectbox('Family Support', ['Choose', 'Very supportive', 'Somewhat supportive', 
                                                     'Not supportive', 'Indifferent'])

    # Prediction code
    if st.button('Predict'):
        # Check if any options are left unselected
        if (gender == 'Choose' or age == 'Choose' or school == 'Choose' or exam == 'Choose' or 
            location == 'Choose' or cbt_technical_issues == 'Choose' or guardians_education == 'Choose' or 
            exam_readiness == 'Choose' or exam_preparation == 'Choose' or after_school_study == 'Choose' or 
            exam_guidance == 'Choose' or exam_confidence == 'Choose' or health_issues == 'Choose' or 
            family_support == 'Choose'):
            st.error("Please select all options before making a prediction.")
        else:
            input_data = encode_input(gender, age, school, exam, location, cbt_technical_issues, 
                                       guardians_education, exam_readiness, exam_preparation, 
                                       after_school_study, exam_guidance, exam_confidence, 
                                       health_issues, family_support)
            result = generate_prediction_and_recommendation(input_data)

            # Display recommendations based on cluster label
            cluster_label = result['cluster_label']
            recommendation = generate_recommendations(cluster_label)
            st.success(f"Recommendation: {recommendation}")
except Exception as e:
    st.error(f"Error: {e}")
