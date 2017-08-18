from scipy import stats
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result_page():
    result = request.form['result']
    data_table = get_table_from_textarea(result)
    chi_test_results = calculate_chi(data_table)
    # print(chi_test_results)
    return render_template('result.html', result=chi_test_results)


def get_table_from_textarea(text):
    lines = text.split("\r\n")
    data_table = [row.split("\t") for row in lines if row != '']
    return data_table


def calculate_chi(data_table):
    number_of_cases = len(data_table[0]) - 1
    number_of_data_lines = len(data_table) - 1
    
    group_var_name = data_table[0][0]
    category_var_list = [data_table[0][i+1] for i in range(number_of_cases)]

    text_to_save = 'The p-values for the chi-square statistic are:\n'
    for category_id, category in enumerate(category_var_list):
        text_to_save += category + ", "
        category_list = []
        group_list = []
        for row in range(1, number_of_data_lines+1):
            category = data_table[row][0]
            group = data_table[row][category_id+1]
            if category not in category_list:
                category_list.append(category)
            if group not in group_list and group != '':
                group_list.append(group)
        list_to_analyze = [[0 for i in category_list] for j in group_list]
        for row in range(1, number_of_data_lines+1):
            cat_id = category_list.index(data_table[row][0])
            if data_table[row][category_id+1] != '':
                group_id = group_list.index(data_table[row][category_id+1])
                list_to_analyze[group_id][cat_id] += 1
        
        print(list_to_analyze)
        obs = np.array(list_to_analyze)
        chi2, p, dof, expected = stats.chi2_contingency(obs)
        print (p)
        text_to_save += str(p) + ";\n"
    return text_to_save
    
    """
    obs = np.array([[14452, 4287, 4073^p30864, 9887, 11439]])
    chi2, p, dof, expected = stats.chi2_contingency(obs)
    print (p)
    """


if __name__ == '__main__':
    app.run(debug=True)
