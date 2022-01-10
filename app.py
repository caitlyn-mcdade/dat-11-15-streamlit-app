import pandas as pd
import numpy as np
import streamlit as st
import plotly as px
import pickle
st.title("My First Dashboard!")

url = "https://raw.githubusercontent.com/JonathanBechtel/dat-11-15/main/ClassMaterial/Unit1/data/master.csv"

num_rows = st.sidebar.number_input('Select Number of Rows to Load', 
                                    min_value = 1000, 
                                    max_value = 5000, 
                                    step = 1000)


section = st.sidebar.radio('choose application section', ['data explorer', 'model explorer'])

print(section)

@st.cache #this decorater means that if the function is called once, it wont be called again. i.e. we are cache-ing our data. good for any function thats laoding large data
def load_data(num_rows):
    df = pd.read_csv(url, parse_dates = ['visit_date'], nrows = num_rows)
    return df

@st.cache
def create_grouping(x_axis, y_axis):
     grouping = df.groupby(x_axis)[y_axis].mean()
     return grouping

def load_model():
    with open('pipe.pkl', 'rb') as pickled_mod:
        model = pickle.load(pickled_mod)
    return model

df = load_data(num_rows)

#creating and saving side bar selections into varianles, using that to create different types of charts
if section == 'data explorer':

    df = load_data(num_rows)

    x_axis = st.sidebar.selectbox('choose column for x-axis', 
                                    df.select_dtypes(include= np.object).columns.tolist())
    
    y_axis = st.sidebar.selectbox('choose column for y-axis', ['visitors', 
                                                                'reserve_visitors'])

    chart_type = st.sidebar.selectbox('choose chart type', ['line', 
                                                            'bar', 
                                                            'area'])

    if chart_type == 'line':
        grouping = create_grouping(x_axis, y_axis)
        st.line_chart(grouping)
    elif chart_type == 'bar': 
        grouping = create_grouping(x_axis, y_axis)
        st.bar_chart(grouping)
    elif chart_type == 'area':
        fig = px.strip(df[[x_axis, y_axis]], x=x_axis, y=y_axis)
        st.plotly_chart(fig)

    st.write(df)

else:
    st.text('choose option on side of explorer')

    model = load_model()
    
    id_val = st.sidebar.selectbox('choose id', 
                                    df['id'].unique().tolist())

    yesterday = st.sidebar.number_input('visitors yest', min_value = 0, max_value = 100, step = 1, value = 20)

    day_of_week = st.sidebar.selectbox('day of week', df['day_of_week'].unique().tolist())

    sample = {
        'id': id_val,
        'yesterday': yesterday,
        'day_of_week': day_of_week
    }

    sample = pd.DataFrame(sample, index = [0])
    prediction = model.predict(sample)[0]

    st.title(f'predicted attendence: {int(prediction)}')

#print(num_rows) #num rows variable changes based on what is selected in the streamlit app sidebar

