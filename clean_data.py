import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

def clean_data(df : pd.DataFrame):
    # Replace "?" with NaN
    df = df.replace('?', np.nan)

    for column in df.columns :
        cl = df[column]
        if len(set(cl)) == df.shape[0] :
            df = df.drop(columns=[column])
    df = df.dropna()
    # cl = df.columns
    # imputer = SimpleImputer(strategy="median")
    # df = imputer.fit_transform(df)
    # df = pd.DataFrame(df,columns=cl)
    # df = OneHotEncoder().fit_transform(df)
    return df


def get_pipeline(X,model ):
    numeric_features = X.select_dtypes(include=['number']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder())
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Create the final pipeline, including preprocessing
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    # X = pipeline.fit_transform(X)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size)
    return pipeline