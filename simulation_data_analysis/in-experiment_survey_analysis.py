import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm

dass_ratings_mapping = {"不符合": 0,
                        "有时符合": 1,
                        "常常符合": 2,
                        "总是符合": 3}

wai_ratings_mapping = {"从来没有": 1,
                       "偶尔如此": 2,
                       "有时如此": 3,
                       "经常如此": 4,
                       "总是如此": 5}

def get_mental_health_state(filename):
    mental_health_state_df = pd.read_excel(filename)
    mental_health_survey_questions = [q for q in mental_health_state_df.columns[-23:] if
                                      not q.startswith("检查是否认真作答")]
    # convert option to rating
    for question in mental_health_survey_questions:
        mental_health_state_df[f"{question}_score"] = mental_health_state_df[question].apply(
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
        mental_health_state_df[f"{dimension}_score"] = mental_health_state_df[[f"{q}_score" for q in questions]].sum(
            axis=1)
    return mental_health_state_df

def get_wai_state(filename):
    wai_state_df = pd.read_excel(filename)
    wai_questions = [q for q in wai_state_df.columns[-14:] if
                                      not q.startswith("检查是否认真作答")]
    print(len(wai_questions))
    # convert option to rating
    for question in wai_questions:
        print(question)
        wai_state_df[f"{question}_score"] = wai_state_df[question].apply(
            lambda x: wai_ratings_mapping[x])
    # convert all questions to dimension score
    wai_question_type_mapping = {"goal": [], "task": [], "bond": []}
    for idx, q in enumerate(wai_questions):
        if idx + 1 in [4, 5, 10, 11]:
            wai_question_type_mapping["goal"].append(q)
        elif idx + 1 in [1, 2, 8, 12]:
            wai_question_type_mapping["task"].append(q)
        else:
            wai_question_type_mapping["bond"].append(q)
    for dimension, questions in wai_question_type_mapping.items():
        wai_state_df[f"{dimension}_score"] = wai_state_df[[f"{q}_score" for q in questions]].sum(
            axis=1)
    return wai_state_df

def get_goal_completion(filename):
    goal_completion_df = pd.read_excel(filename)
    return goal_completion_df


if __name__ == "__main__":
    # mental health state analysis
    mental_health_state_filename = "survey_data/mental_health_survey.xlsx"
    mental_health_state_df = get_mental_health_state(mental_health_state_filename)
    # mental_health_state_df.rename({'编号': 'Participant'}, inplace=True)
    mental_health_state_df['Group'] = pd.Categorical(mental_health_state_df['分组'], categories=['control', 'novice human', '50min AI', "24/7 AI"], ordered=False)

    for dimension in ["depression", "anxiety", "stress"]:
        print(dimension)
        md = mixedlm(f"{dimension}_score ~ Group * week", mental_health_state_df, groups=mental_health_state_df["编号"])
        mdf = md.fit()
        print(mdf.summary())

    goal_completion_filename = "survey_data/goal_completion.xlsx"
    goal_completion_df = get_goal_completion(goal_completion_filename)
    goal_completion_df['Group'] = pd.Categorical(goal_completion_df['分组'],
                                                     categories=['control', 'novice human', '50min AI', "24/7 AI"],
                                                     ordered=False)
    for goal in [1, 2, 3]:
        print(f"goal{goal}")
        md = mixedlm(f"goal{goal} ~ Group * week", goal_completion_df, groups=goal_completion_df["编号"])
        mdf = md.fit()
        print(mdf.summary())

    wai_filename = "survey_data/therapeutic_relationship.xlsx"
    wai_df = get_wai_state(wai_filename)
    wai_df['Group'] = pd.Categorical(wai_df['分组'],
                                     categories=['control', 'novice human', '50min AI', "24/7 AI"],
                                     ordered=False)
    for dimension in ["goal", "task", "bond"]:
        print(dimension)
        md = mixedlm(f"{dimension}_score ~ Group * week", wai_df, groups=wai_df["编号"])
        mdf = md.fit()
        print(mdf.summary())