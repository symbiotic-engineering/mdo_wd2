from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import matplotlib.pyplot as plt

def randomtrees(df):
    # Drop NaNs
    df_clean = df.dropna()

    # Train a simple random forest model
    X = df_clean.drop(columns=["LCOW"])
    y = df_clean["LCOW"]
    model = RandomForestRegressor()
    model.fit(X, y)

    # Get feature importances
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

    print(importances)

    importances.plot(kind='bar', figsize=(10,6))
    plt.xlabel("Design Variables")
    plt.ylabel("Importance")
    plt.title("Feature Importance from Random Forest")
    plt.xticks(rotation=45)
    plt.show()