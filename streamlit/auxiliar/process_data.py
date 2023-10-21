import pandas as pd


def get_text_between_delimiters(text, left_del, right_del):
    if left_del not in text:
        return 'Unknown'
    if right_del not in text:
        return 'Unknown'
    partial_result = text.split(left_del)[1]
    partial_result = partial_result.split(right_del)[0]
    return partial_result.title()


raw_data = pd.read_csv('streamlit/data/data_science_prog_assigment.csv')

left_delimiter = 'The following are multiple choice questions (with answers) about '
right_delimiter = '.'
add_columns = raw_data
add_columns['question_type'] = add_columns['question_text'].apply(lambda x: get_text_between_delimiters(x, left_delimiter, right_delimiter))

summarised_by_model_and_question_data = add_columns[['model_name','question_type','accuracy']]

mean_accuracy_by_model_and_question_type = summarised_by_model_and_question_data.groupby(by=['model_name','question_type']).mean()
mean_accuracy_by_model_and_question_type = mean_accuracy_by_model_and_question_type.reset_index()

counts_data = summarised_by_model_and_question_data.groupby(by=['model_name','question_type']).count()
counts_data = counts_data.reset_index()

summarised_by_model_data = add_columns[['model_name','accuracy']]
mean_accuracy_by_model = summarised_by_model_data.groupby(by=['model_name']).mean()
mean_accuracy_by_model = mean_accuracy_by_model.reset_index()

summarised_by_question_data = add_columns[['question_type','accuracy']]
mean_accuracy_by_question = summarised_by_question_data.groupby(by=['question_type']).mean()
mean_accuracy_by_question = mean_accuracy_by_question.reset_index()
