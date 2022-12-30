import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.preprocessing import MinMaxScaler
import feature_extractor as fe_ext

def get_phishing_percentage(url: str):
    df = fe_ext.extract_features(url)
    selected_features = df.columns.copy()

    # minmax scaling
    scaler: MinMaxScaler = pickle.load(open('models/min_max_scaler.sav', 'rb'))
    df_raw = pd.DataFrame(columns=scaler.feature_names_in_)
    df = pd.concat([df_raw, df])
    df = df.fillna(0)

    df_new = pd.DataFrame(columns=df_raw.columns, index=[0])
    df_new.iloc[0] = scaler.transform(df)

    # load model
    model: RandomForestClassifier = pickle.load(open("models/random_forest_model.sav", "rb"))
    y_pred = model.predict_proba(df_new[selected_features])
    
    return y_pred[0, 1]

if __name__ == '__main__':
    print(get_phishing_percentage('https://office-crack.com/'))