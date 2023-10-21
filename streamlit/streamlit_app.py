import plotly.express as px
import streamlit as st
from auxiliar.process_data import (
    mean_accuracy_by_model_and_question_type,
    counts_data,
    mean_accuracy_by_model,
    add_columns,
)


st.set_page_config(layout="wide")

model_names = list(set(mean_accuracy_by_model_and_question_type["model_name"]))
model_names.sort()

question_types = list(set(mean_accuracy_by_model_and_question_type["question_type"]))
question_types.sort()

with st.sidebar:
    st.image("streamlit/imgs/Logo_full_color.png", width=200)
    genre = st.radio("Metric",["accuracy","relative_accuracy"])
    st.write("Filters")
    selected_model_names = st.multiselect(label="Models", options=model_names)
    if len(selected_model_names) > 0:
        mean_accuracy_by_model_and_question_type = (
            mean_accuracy_by_model_and_question_type[
                mean_accuracy_by_model_and_question_type["model_name"].isin(
                    selected_model_names
                )
            ]
        )

    selected_question_types = st.multiselect(
        label="Question Types", options=question_types
    )
    if len(selected_question_types) > 0:
        mean_accuracy_by_model_and_question_type = (
            mean_accuracy_by_model_and_question_type[
                mean_accuracy_by_model_and_question_type["question_type"].isin(
                    selected_question_types
                )
            ]
        )

# Pivoting the data, so it's easier to plot.
mean_accuracy_by_model_and_question_type_pivoted = (
    mean_accuracy_by_model_and_question_type.pivot(
        index="question_type", columns="model_name", values=genre
    )
)
counts_data_pivoted = counts_data.pivot(
    index="question_type", columns="model_name", values=genre
)

st.title("Chart")

# Overal performance by model.
model_data = mean_accuracy_by_model[["model_name", genre]]
grouped_model_data = model_data.groupby("model_name").mean().sort_values(by=genre)
grouped_model_data[genre] = grouped_model_data[genre].round(2)
model_chart = px.bar(
    grouped_model_data,
    barmode="group",
    title="Accuracy by model.",
    x=genre,
).update_layout(
    yaxis_title="Model Name",
    xaxis_title="",
    xaxis=dict(showticklabels=False),
)
model_chart.update_xaxes(tickangle=0)
model_chart.update_traces(
    text=grouped_model_data[genre],
    textposition="inside",
    showlegend=False,
    marker=dict(color=grouped_model_data[genre]),
)
st.write(model_chart)
st.write(
    "At a first look, the models C and E have the best accuracy, but since the number of tested models based on question type is not uniform, it's not conclusive. Check table 1 in the section 'Data'."
)

# Accuracy by question Type.
question_type_data = mean_accuracy_by_model_and_question_type[
    ["question_type", genre]
]
grouped_question_type_data = (
    question_type_data.groupby("question_type").mean().sort_values(by=genre)
)
grouped_question_type_data[genre] = grouped_question_type_data[genre].round(2)
question_chart = px.bar(
    grouped_question_type_data,
    barmode="group",
    title="Accuracy by question type.",
    x=genre,
).update_layout(
    yaxis_title="Question Type",
    xaxis_title="",
    xaxis=dict(showticklabels=False),
)
question_chart.update_xaxes(tickangle=-30)
question_chart.update_traces(
    text=grouped_question_type_data[genre],
    textposition="inside",
    showlegend=False,
    marker=dict(color=grouped_question_type_data[genre]),
)
st.write(question_chart)
st.write(
    "We can see a better accuracy in College Biology questions, and a lower performance in Professional Medicine questions, the posible reason is the subject complexity."
)

# Which model performs better based on  question type?
model_vs_question_type_chart = px.bar(
    mean_accuracy_by_model_and_question_type_pivoted.groupby("question_type").mean(),
    barmode="group",
    title="Which model performs better based on  question type?",
).update_layout(
    xaxis_title="Question Type",
    yaxis_title=genre,
    yaxis=dict(range=[0, 1]),
    legend_title_text="",
    legend=dict(x=0, y=1.15),
    legend_orientation="h",
)
model_vs_question_type_chart.update_xaxes(tickangle=-30)
st.write(model_vs_question_type_chart)
st.write("But if we pay attention to Accuracy by Model vs Question Types...")
st.write(
    "The model A has the best accuracy in Anatomy, Clinical Knowledge, College Biology and College Medicine while model D has the best accuracy in Medical Genetics, Professional Medicine. Although these last two questions types were not tested as much as Anatomy, Clinical Knowledge, College Biology and College Medicine."
)
st.write(
    "Combining the models based on question type would result in a better overal accuracy. Check table 2 in the section 'Data'."
)

st.title("Data")
st.write("Table 1 - Number of questions by question type.")
st.dataframe(counts_data_pivoted)

st.write("Table 2 - Number of questions by question type.")
mean_accuracy_by_model_and_question_type_pivoted[
    "best model accuracy"
] = mean_accuracy_by_model_and_question_type_pivoted[
    ["model_a", "model_b", "model_c", "model_d", "model_e"]
].max(
    axis=1
)
st.dataframe(
    mean_accuracy_by_model_and_question_type_pivoted.style.highlight_max(axis=1)
)
