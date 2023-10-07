import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the trained model
model = joblib.load('model.pkl')

# Function to map categorical features back to their original values
def map_back(column, mapping):
    if isinstance(mapping, dict):
        reverse_mapping = {v: k for k, v in mapping.items()}
        return column.map(reverse_mapping)
    else:
        return column

# Custom CSS styles for the app
st.markdown(
    """
    <style>
    .header {
        background-color: #33adff;
        color: white;
        padding: 0.4rem;
        text-align: center;
        font-size: 1.75rem;
        border-radius: 0.25rem;
        margin-bottom: .75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .button {
        background-color: #33adff;
        color: white;
        padding: 1rem 1.5rem;
        font-size: 1.2rem;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .prediction {
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 1.5rem;
        text-align: center;
    }
    .branding {
        font-size: 1rem;
        font-weight: bold;
    }
    .sidebar-content {
        padding: 2rem;
    }
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #33adff;
        margin-bottom: 1rem;
    }
    .sidebar-link {
        font-size: 1.2rem;
        color: #33adff;
        text-decoration: none;
    }
    .sidebar-link:hover {
        text-decoration: underline;
    }
    .cover-image {
        max-width: 75%;
        margin: 0 auto;
        display: block;
        border-radius: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
def main():
    st.title('Customer Insurance Subscription Prediction')

    # Sidebar menu
    st.sidebar.title('About the App Developer')
    st.sidebar.markdown('<p class="branding">Mohammed Farooq basha S</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<p class="branding">Contact Information:</p>', unsafe_allow_html=True)
    st.sidebar.markdown('[LinkedIn Profile](https://www.linkedin.com/farooq-basha)', unsafe_allow_html=True)
    st.sidebar.markdown('GitHub Account: [Farooqbasha008](https://github.com/Farooqbasha008)')
    st.sidebar.markdown('Email: sfarooq8.fb@gmail.com')

    # App description and instructions
    st.markdown('<p class="sidebar-header">About the App</p>', unsafe_allow_html=True)
    st.markdown('This app predicts whether a customer is likely to subscribe to insurance based on their information.')

    st.markdown('<p class="sidebar-header">Instructions</p>', unsafe_allow_html=True)
    st.markdown('1. Use the dropdowns and sliders to enter the customer details.')
    st.markdown('2. Click on the "Predict" button to see the prediction result.')
    st.markdown('3. The prediction will appear below the "Prediction" section in green or red text.')


    # Read the dataset
    dataset = pd.read_csv('train.csv')
    dataset = dataset.dropna(axis=0)

    # Map categorical features to numeric values
    mapping = {
        'y': {'no': 0, 'yes': 1},
        'mon': {'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'oct': 10, 'nov': 11, 'dec': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'sep': 9},
        'education_qual': {'tertiary': 3, 'secondary': 2, 'unknown': 0, 'primary': 1},
        'marital': {'married': 24, 'single': 16, 'divorced': 32},
        'call_type': {'unknown': 0, 'cellular': 1, 'telephone': 2},
        'prev_outcome': {'unknown': 2, 'failure': 0, 'other': 3, 'success': 1}
    }
    dataset.replace(mapping, inplace=True)

    # Encode 'job' feature using LabelEncoder
    le = LabelEncoder()
    dataset['job'] = le.fit_transform(dataset['job'])

    # Inverse transform function to map numeric values back to job names
    def inverse_transform_job(code):
        return le.inverse_transform([code])[0]

    # Get user inputs for features

    col1, col2, col3 = st.columns(3)
    with col1:
        job = st.selectbox('Job', dataset['job'].unique(), format_func=inverse_transform_job)
    with col2:
        marital = st.selectbox('Marital Status', dataset['marital'].unique(), format_func=lambda x: map_back(pd.Series([x]), mapping['marital'])[0])
    with col3:
        education_qual = st.selectbox('Education Qualification', dataset['education_qual'].unique(), format_func=lambda x: map_back(pd.Series([x]), mapping['education_qual'])[0])

    col4, col5, col6 = st.columns(3)
    with col4:
        call_type = st.selectbox('Call Type', dataset['call_type'].unique(), format_func=lambda x: map_back(pd.Series([x]), mapping['call_type'])[0])
    with col5:
        prev_outcome = st.selectbox('Previous Outcome', dataset['prev_outcome'].unique(), format_func=lambda x: map_back(pd.Series([x]), mapping['prev_outcome'])[0])
    with col6:
        mon = st.selectbox('Month', dataset['mon'].unique(), format_func=lambda x: map_back(pd.Series([x]), mapping['mon'])[0])

    age = st.slider('Age', min_value=0, max_value=100, value=30)
    day = st.slider('Day', min_value=1, max_value=31, value=1)
    dur = st.slider('Duration (Seconds)', min_value=0, max_value=1000, value=200)
    num_calls = st.slider('Number of Calls', min_value=0, max_value=20, value=5)

    # Add a "Predict" button
    if st.button('Predict', key='predict_button'):
        # Prepare the input data for prediction
        data = pd.DataFrame({
            'job': [job],
            'marital': [marital],
            'education_qual': [education_qual],
            'call_type': [call_type],
            'prev_outcome': [prev_outcome],
            'mon': [mon],
            'age': [age],
            'day': [day],
            'dur': [dur],
            'num_calls': [num_calls]
        })

        # Make prediction using the loaded model
        prediction = model.predict(data)[0]

        st.markdown('<p class="header">Prediction</p>', unsafe_allow_html=True)

        # Display the prediction
        if prediction == 0:
            st.markdown('<p class="prediction" style="color: red;">No, The customer is highly unlikely to subscribe to the insurance.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="prediction" style="color: green;">Yes, The customer is highly likely to subscribe to the insurance.</p>', unsafe_allow_html=True)

# Run the app
if __name__ == '__main__':
    main()
