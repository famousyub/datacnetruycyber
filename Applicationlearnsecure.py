import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Load CSV file
data = pd.read_csv('Test_data.csv')

# Create a dummy target column (replace with your actual target column if available)
data['target'] = [0, 1, 0, 1, 0] * (len(data) // 5) + [0] * (len(data) % 5)

# Print column names to confirm
print(data.columns)

# Define numerical and categorical features
numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
categorical_features = data.select_dtypes(include=['object', 'bool']).columns

# Remove the target column from the features list
numerical_features = numerical_features.drop('target', errors='ignore')
categorical_features = categorical_features.drop('target', errors='ignore')

# Preprocessing steps
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Define model

try : 
    model = RandomForestClassifier()

    # Create preprocessing and modeling pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                            ('model', model)])

    # Split data
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training with GridSearchCV for hyperparameter tuning
    param_grid = { 'model__n_estimators': [100, 200],
                'model__max_features': ['auto', 'sqrt', 'log2']}
    CV = GridSearchCV(pipeline, param_grid, cv=5)
    CV.fit(X_train, y_train)

    # Best model parameters
    print('Best parameters:', CV.best_params_)

    # Evaluate the model
    best_model = CV.best_estimator_
    accuracy = best_model.score(X_test, y_test)
    print(f"Test set accuracy: {accuracy * 100:.2f}%")
except Exception  as ex :
    error  = str(ex)
    with open('error.txt' , "a+") as f :
        f.write(error +"\n")