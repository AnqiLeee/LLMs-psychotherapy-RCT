import os
import pandas as pd
import numpy as np
from collections import Counter
from scipy.stats import f_oneway

dass_ratings_mapping = {"不符合": 0,
                        "有时符合": 1,
                        "常常符合": 2,
                        "总是符合": 3}


def get_demographic_info(filename):
    demographics = pd.read_excel(filename)
    sex_mapping = {"男": 0, "女": 1}
    demographics["sex_dummy"] = demographics["生理性别"].apply(lambda x: sex_mapping[x])
    sex_dist = dict(Counter(demographics["生理性别"]))
    occupation_dist = dict(Counter(demographics["职业"]))
    print("")
    print("the physical sex of all participants = ", sex_dist)
    print("the occupation distribution of all participants = ", occupation_dist)
    return demographics

def get_base_mental_health_state(filename):
    mental_health_state_df = pd.read_excel(filename)
    # select the first week state of each participant
    base_mental_health_state = mental_health_state_df.loc[mental_health_state_df["week"] == 1]
    mental_health_survey_questions = [q for q in mental_health_state_df.columns[-23:] if
                                      not q.startswith("检查是否认真作答")]
    # convert option to rating
    for question in mental_health_survey_questions:
        base_mental_health_state[f"{question}_score"] = base_mental_health_state[question].apply(
            lambda x: dass_ratings_mapping[x])
    # convert all questions to dimension score
    dass_question_type_mapping = {"depression": [], "anxiety": [], "stress": []}
    for idx, q in enumerate(mental_health_survey_questions):
        if idx + 1 in [3, 5, 10, 13, 16, 17, 21]:
            dass_question_type_mapping["depression"].append(q)
        elif idx + 1 in [2, 4, 7, 9, 15, 19, 20]:
            dass_question_type_mapping["anxiety"].append(q)
        else:
            dass_question_type_mapping["stress"].append(q)
    for dimension, questions in dass_question_type_mapping.items():
        base_mental_health_state[f"{dimension}_score"] = base_mental_health_state[[f"{q}_score" for q in questions]].sum(
            axis=1)
    return base_mental_health_state

def statistic_base_mental_health_state(df):
    dimension_base_mt = {}
    for dimension in ["depression", "anxiety", "stress"]:
        avg, std = np.average(df[f"{dimension}_score"]), np.std(df[f"{dimension}_score"])
        dimension_base_mt[dimension] = f"{'%0.2f'%avg}({'%0.2f'%std})"
    return dimension_base_mt

def one_way_anova(df, column):
    groups = []
    for group_id, group_df in df.groupby("分组"):
        groups.append(group_df[column])
    f_value, p_value = f_oneway(groups[0], groups[1], groups[2], groups[3])
    return f_value, p_value


if __name__ == '__main__':
    datapath = "survey_data"

    filename = "participants_register_form.xlsx"
    demographics = get_demographic_info(os.path.join(datapath, filename))
    sex_f, sex_p = one_way_anova(demographics, "sex_dummy")
    print("sex distribution among groups:", "%0.2f"%sex_f, "%0.2f"%sex_p)

    mt_filename = "mental_health_survey.xlsx"
    base_mt_df = get_base_mental_health_state(os.path.join(datapath, mt_filename))
    dimension_base_mt = statistic_base_mental_health_state(base_mt_df)
    print("DASS", dimension_base_mt)
    for dimension in ["depression", "anxiety", "stress"]:
        dimension_f, dimension_p = one_way_anova(base_mt_df, f"{dimension}_score")
        print(f"{dimension} anova:", "%0.2f"%dimension_f, "%0.2f"%dimension_p)








