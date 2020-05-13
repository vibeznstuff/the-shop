import data_diagnostics as dd

def remove_id_features(df, feature_list=None):
    if feature_list == None:
        feature_list = df.columns
    
    non_id_feats = [x for x in feature_list if 'id' not in x]

    return non_id_feats


def remove_junk_features(df, remove_ids=True):
    valid_char_feats = dd.get_character_features(df)
    valid_numeric_feats = dd.get_numeric_features(df)

    valid_char_feats = dd.get_clean_features(df, valid_char_feats)
    valid_numeric_feats = dd.get_clean_features(df, valid_numeric_feats)

    if remove_ids:
        valid_char_feats = remove_id_features(df, valid_char_feats)
        valid_numeric_feats = remove_id_features(df, valid_numeric_feats)

    return {'character': valid_char_feats, 'numeric': valid_numeric_feats}
