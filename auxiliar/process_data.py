import pandas as pd


def get_text_between_delimiters(text, left_del, right_del):
    if left_del not in text:
        return 'Unknown'
    if right_del not in text:
        return 'Unknown'
    partial_result = text.split(left_del)[1]
    partial_result = partial_result.split(right_del)[0]
    return partial_result.title()


raw_data = pd.read_csv('data/data_science_prog_assigment.csv')

left_delimiter = 'The following are multiple choice questions (with answers) about '
right_delimiter = '.'
add_question_type = raw_data
add_question_type['question_type'] = add_question_type['question_text'].apply(lambda x: get_text_between_delimiters(x, left_delimiter, right_delimiter))

remove_columns = add_question_type[['model_name','question_type','accuracy']]
summary = remove_columns.groupby(by=['model_name','question_type']).mean()
prepared_data = summary.reset_index()
