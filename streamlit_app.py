import plotly.express as px
import streamlit as st
from auxiliar.process_data import prepared_data


st.set_page_config(layout="wide")

model_names = list(set( prepared_data["model_name"] ))
model_names.sort()

question_types = list(set( prepared_data["question_type"] ))
question_types.sort()

with st.sidebar:
    st.image("imgs/Logo_full_color.png", width=200)
    st.write("Filters")
    selected_model_names = st.multiselect(
        label="Models",
        options=model_names
    )
    if len(selected_model_names) > 0:
        prepared_data = prepared_data[prepared_data['model_name'].isin(selected_model_names)]

    selected_question_types = st.multiselect(
        label="Question Types",
        options=question_types
    )
    if len(selected_question_types) > 0:
        prepared_data = prepared_data[prepared_data['question_type'].isin(selected_question_types)]


# Pivoting the data, so it's easier to plot.
prepared_data_pivoted = prepared_data.pivot(
    index="question_type", columns="model_name", values="accuracy"
)

# Generating two columns, a wider one and a smaller one.
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Chart")
    fig = (
        px.bar(
            prepared_data_pivoted.groupby("question_type").mean(),
            barmode='group',
            title="Which model performs better based on  question type",
        )
        .update_layout(
            xaxis_title="Question Type",
            yaxis_title="Accuracy",
            yaxis=dict(range=[0, 1]),
            legend_title_text="",
            legend=dict(x=0, y=1.15),
            legend_orientation='h'
        )
    )
    fig.update_xaxes(tickangle=-30)
    st.write(fig)

with col2:
    st.title("Findings")
    st.write("The model A performs better in Anatomy, Clinical Knowledge, College Biology and College Medicine.")
    st.write("The model D performs better in Medical Genetics, Profesional Medicine.")
    st.write("Combining these two models would result in a better overal accuracy.")

st.title("Data")
st.dataframe(prepared_data_pivoted)
