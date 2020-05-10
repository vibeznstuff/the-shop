import pandas as pd 
import numpy as np

def get_record_count(df):
    return df.shape[0]


def get_numeric_features(df):
    return list(df.select_dtypes(include=np.number).columns)


def get_character_features(df):
    # To Do: Make this more robust
    all_feats = df.columns
    num_feats = get_numeric_features(df)
    char_feats = [x for x in all_feats if x not in num_feats]
    
    return char_feats


def get_feature_count(df):
    return len(df.columns)


def get_records_with_nulls(df):
    return df[df.isnull().any(axis=1)]


def get_missing_count_from_feature(series):
    return series.isnull().sum()

def get_feature_cardinality(df, feature_list=None):

    if feature_list == None:
        feature_list = df.columns
        
    card_list = []

    for feature in feature_list:
        cardinality = len(df[feature].unique())
        card_list.append((feature, cardinality))

    return card_list

def get_high_card_features(df, high_threshold=-1):
    
    high_card_feats = []

    if high_threshold == -1:
        record_count = get_record_count(df)
        high_threshold = record_count * (0.70)

    char_features = get_character_features(df)
    feat_cards = get_feature_cardinality(df, char_features)

    for feature in feat_cards:
        if feature[1] > high_threshold:
            high_card_feats.append(feature[0])

    return high_card_feats


def get_mostly_null_features(df, high_threshold=0.5):
    
    mostly_null_feats = []

    features = df.columns

    for feature in features:
        total_records = get_record_count(df)
        null_record_count = get_missing_count_from_feature(df[feature])

        missing_rate = float(null_record_count) / float(total_records)

        if missing_rate >= high_threshold:
            mostly_null_feats.append((feature, missing_rate))

    return mostly_null_feats


def get_unary_features(df, high_threshold=0.8):
    
    unary_feats = []

    features = df.columns

    for feature in features:
        top_levels = df[feature].value_counts(normalize=True).head()
        top_level_prevalence = top_levels.iloc[0]

        if top_level_prevalence >= high_threshold:
            unary_feats.append((feature, top_levels))

    return unary_feats


def get_likely_nominal_ordinal_features(df, low_threshold=50):
    #To Do: Make this whole function smarter

    nominal_ordinal_feats = []

    numeric_features = get_numeric_features(df)

    for feature in numeric_features:
        num_levels = len(df[feature].unique())

        if num_levels <= low_threshold:
            nominal_ordinal_feats.append(feature)

    return nominal_ordinal_feats


def get_clean_features(df, feature_list):
    high_card_feats = get_high_card_features(df)
    mostly_null_feats = get_mostly_null_features(df)
    unary_feats = get_unary_features(df)

    feature_list = [x for x in feature_list if x not in high_card_feats]
    feature_list = [x for x in feature_list if x not in mostly_null_feats]
    feature_list = [x for x in feature_list if x not in unary_feats]

    return feature_list


def get_diagnostic_summary(df):

    total_feat_count = get_feature_count(df)

    num_feats = get_numeric_features(df)
    num_feat_count = len(num_feats)

    char_feats = get_character_features(df)
    char_feat_count = len(char_feats)

    total_record_count = get_record_count(df)

    records_with_nulls = get_records_with_nulls(df)
    null_record_count = get_record_count(records_with_nulls)

    high_card_feats = get_high_card_features(df)
    num_high_card_feats = len(high_card_feats)

    mostly_null_feats = get_mostly_null_features(df)
    num_mostly_null_feats = len(mostly_null_feats)
    
    unary_feats = get_unary_features(df)
    num_unary_feats = len(unary_feats)

    nominal_ordinal_feats = get_likely_nominal_ordinal_features(df)
    num_nom_ord_feats = len(nominal_ordinal_feats)

    summary_text = """
                     Data Diagnostic Summary
        ================================================
        Total Feature Count: {0}
            Numeric Features: {1}
                Likely Nominal or Ordinal Features: {8}
            Character Features: {2}
                High-Cardinality Features: {5}
            Features w/ High Rate of Missing Values: {6}
            Features that are (almost) Unary: {7}
        Total Record Count: {3}
            Records with at least one NULL Value: {4}

        ================================================
        """.format(total_feat_count, num_feat_count, char_feat_count, 
        total_record_count, null_record_count, num_high_card_feats,
        num_mostly_null_feats, num_unary_feats, num_nom_ord_feats)

    print(summary_text)

    diagnostics = {
        "feature_diagnostics":{
            "total_feat_count": total_feat_count,
            "numeric_features": num_feats,
            "character_features": char_feats,
            "high_cardinality_features": high_card_feats,
            "mostly_null_features": mostly_null_feats,
            "unary_features": unary_feats,
            "likely_nominal_or_ordinal_features": nominal_ordinal_feats
        },
        "record_diagnostics": {
            "total_record_count": total_record_count,
            "null_record_count": null_record_count
        }
    }

    return diagnostics


