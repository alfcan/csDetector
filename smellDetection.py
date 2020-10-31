import csv
import os

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, libsvm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, auc, f1_score, r2_score, mean_squared_error
from sklearn.metrics import precision_score, precision_recall_curve, cohen_kappa_score, roc_curve
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
import warnings
import os
import pickle
from joblib import dump, load

from configuration import Configuration


warnings.filterwarnings("ignore")

def smellDetection(config: Configuration, batchIdx: int):

    # prepare results holder for easy mapping
    results = {}

    # open finalized results for reading
    project_csv_path = os.path.join(config.resultsPath, f"results_{batchIdx}.csv")
    with open(project_csv_path, newline="") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")

        # parse into a dictionary
        for row in rows:
            results[row[0]] = row[1]

    # map results to a list suitable for model classification
    metrics = buildMetricsList(results)

    # load all models
    smells = ["OSE", "BCE", "PDE", "SV", "OS", "SD", "RS", "TF", "UI", "UO", "VS"]
    all_models = {}
    for smell in smells:
        modelPath = os.path.abspath("./models/{}.joblib".format(smell))
        all_models[smell] = load(modelPath)

    # detect smells
    rawSmells = {smell: all_models[smell].predict(metrics) for smell in all_models}
    detectedSmells = [smell for smell in smells if rawSmells[smell][0] == 1]

    # add last commit date as first output param
    detectedSmells.insert(0, results["LastCommitDate"])

    # display results
    print("Detected smells:")
    print(detectedSmells)


def buildMetricsList(results: dict):

    # declare names to extract from the results file in the right order
    names = [
        "CommitCount",
        "DaysActive",
        "AuthorCount",
        "SponsoredAuthorCount",
        "PercentageSponsoredAuthors",
        "TimezoneCount",
        "AuthorActiveDays_mean",
        "AuthorActiveDays_stdev",
        "AuthorCommitCount_stdev",
        "TimezoneAuthorCount_stdev",
        "TimezoneCommitCount_stdev",
        "CommitMessageSentiment_mean",
        "CommitMessageSentiment_stdev",
        "CommitMessageSentimentsPositive_count",
        "CommitMessageSentimentsPositive_mean",
        "CommitMessageSentimentsPositive_stdev",
        "CommitMessageSentimentsNegative_count",
        "CommitMessageSentimentsNegative_mean",
        "Tag Count",
        "TagCommitCount_stdev",
        "commitCentrality_Density",
        "commitCentrality_Community Count",
        "commitCentrality_NumberHighCentralityAuthors",
        "commitCentrality_PercentageHighCentralityAuthors",
        "commitCentrality_Closeness_stdev",
        "commitCentrality_Betweenness_stdev",
        "commitCentrality_Centrality_stdev",
        "commitCentrality_CommunityAuthorCount_stdev",
        "commitCentrality_CommunityAuthorItemCount_stdev",
        "NumberReleases",
        "ReleaseAuthorCount_stdev",
        "ReleaseCommitCount_stdev",
        "NumberPRs",
        "NumberPRComments",
        "PRCommentsCount_mean",
        "PRCommitsCount_stdev",
        "PRCommentSentiments_stdev",
        "PRParticipantsCount_mean",
        "PRParticipantsCount_stdev",
        "PRCountPositiveComments_count",
        "PRCountPositiveComments_mean",
        "PRCountNegativeComments_count",
        "PRCountNegativeComments_mean",
        "NumberIssues",
        "NumberIssueComments",
        "IssueCommentsPositive",
        "IssueCommentsCount_mean",
        "IssueCommentsCount_stdev",
        "IssueCommentSentiments_stdev",
        "IssueParticipantCount_mean",
        "IssueParticipantCount_stdev",
        "IssueCountPositiveComments_mean",
        "IssueCountNegativeComments_count",
        "IssueCountNegativeComments_mean",
        "issuesAndPRsCentrality_Density",
        "issuesAndPRsCentrality_Community Count",
        "issuesAndPRsCentrality_NumberHighCentralityAuthors",
        "issuesAndPRsCentrality_PercentageHighCentralityAuthors",
        "issuesAndPRsCentrality_Closeness_stdev",
        "issuesAndPRsCentrality_Betweenness_stdev",
        "issuesAndPRsCentrality_Centrality_stdev",
        "issuesAndPRsCentrality_CommunityAuthorCount_stdev",
        "issuesAndPRsCentrality_CommunityAuthorItemCount_stdev",
    ]

    # build key/value list
    metrics = []
    for name in names:
        metrics.append(results.get(name, 0))

    # return as a 2D array
    return [metrics]