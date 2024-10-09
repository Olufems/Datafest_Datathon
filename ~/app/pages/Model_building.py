import streamlit as st
from kmodes.kmodes import KModes
import  base64
import pickle

st.header("WAEC & JAMB Exam Challenges Prediction")

trained_model = pickle.load(open(
    'kmodes_model.pkl', 'rb'))

# Image For Page
file_ = open("image.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


import streamlit as st

# Define a function to generate predictions and recommendations
def generate_prediction_and_recommendation(data):
    prediction = trained_model.predict(data)
    cluster_label = prediction[0]
    
    if cluster_label == 0:
        return "The student is predicted to succeed in the exam. Recommendation: Needs foundational support in exam preparation, increased access to exam resources, and stress management strategies."
    elif cluster_label == 1:
        return "The student is predicted to face challenges in the exam. Recommendation: Requires stress management and more advanced tools for exam preparation to maintain high performance and confidence levels."
    elif cluster_label == 2:
        return "The student is predicted to excel in the exam. Recommendation: Benefits from personalized preparation plans and confidence-building programs, with an emphasis on consistent study routines and leveraging family support."
    else:
        return "No specific prediction or recommendation."

# Apply the prediction and recommendation function
df_selected['Prediction_and_Recommendation'] = df_selected.apply(generate_prediction_and_recommendation, axis=1)


# Main app interface
st.title('WAEC & JAMB Exam Challenges Prediction')

# Input fields for prediction variables
try:
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.selectbox('Age Group', ['15-17 years', '18-20 years', '21-23 years', '24 years or older'])
    school = st.selectbox('School Type', ['Private School', 'Public School'])
    exam = st.selectbox('Exam Type', ['WAEC', 'JAMB', 'Both WAEC and JAMB'])
    location = st.selectbox('Location', ['Urban area', 'Rural area', 'Semi-urban area'])
    guardians_education = st.selectbox("Guardian's Education Level", ['Primary education', 'Secondary education', 'Tertiary education (e.g., university, polytechnic)', 'No formal education'])
    exam_readiness = st.selectbox('Exam Readiness', ['Very well prepared', 'Somewhat prepared', 'Not well prepared', 'Not prepared at all'])
    exam_preparation = st.selectbox('Exam Preparation Level', ['Extremely stressful', 'Moderately stressful', 'Not stressful'])
    after_school_study = st.selectbox('After School Study', ['Every day', 'A few times a week', 'Occasionally', 'Rarely or never'])
    exam_guidance = st.selectbox('Exam Guidance Availability', ['Very easy to access', 'Somewhat easy to access', 'Difficult to access', 'Not available at all'])
    exam_confidence = st.selectbox('Exam Confidence Level', ['Very confident', 'Somewhat confident', 'Not confident', 'Unsure'])
    health_issues = st.selectbox('Health Issues', ['Yes', 'No'])
    family_support = st.selectbox('Family Support', ['Very supportive', 'Somewhat supportive', 'Not supportive', 'Indifferent'])

    prediction_result = ""

    # Prediction code
    if st.button('Predict'):
        prediction_result = generate_prediction([[gender, age, school, exam, location, guardians_education, 
                                                  exam_readiness, cbt_technical_issues, exam_preparation, 
                                                  after_school_study, exam_guidance, exam_confidence, 
                                                  health_issues, family_support]])
except Exception as e:
    st.error(f"Error: {e}")

st.success(prediction_result)
