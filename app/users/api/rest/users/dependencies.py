import fastapi

from app.common.api.exceptions import HTTPNotFound
from app.users import database
from app.users.database.models import User

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load

"""
Create a Random Forest Classifier model to predict user activity in the next month.

The model is trained on user data that includes the user's registration date and last visit date.
The target variable is a binary label indicating if the user was active in the next month.

The trained model is saved to a file using joblib.
"""

# User data
data = {
    'user_id': [1, 2, 3, 4, 5],
    'username': ['user1', 'user2', 'user3', 'user4', 'user5'],
    'email': ['user1@example.com', 'user2@example.com', 'user3@example.com', 'user4@example.com',
              'user5@example.com'],
    'registration_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'last_visit_date': ['2024-01-15', '2024-01-10', '2024-01-20', '2024-01-18', '2024-01-25'],
    'active_next_month': [1, 0, 1, 1, 0]
}

df = pd.DataFrame(data)

# Предобработка данных
df['last_visit_date'] = pd.to_datetime(df['last_visit_date'])
df['registration_date'] = pd.to_datetime(df['registration_date'])
df['days_since_registration'] = (df['last_visit_date'] - df['registration_date']).dt.days

X = df.drop(['user_id', 'username', 'email', 'registration_date', 'last_visit_date', 'active_next_month'], axis=1)
y = df['active_next_month']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Сохранение модели в файл
filename = 'model.joblib'
dump(model, filename)


def load_model():
    """
    Load the trained model from a file.

    Returns:
        The trained model.
    """
    filename = 'model.joblib'
    model = load(filename)

    return model


def prepare_user_data(user: User):
    """
    Prepare user data for prediction.

    Args:
        user (User): The user object.

    Returns:
        A pandas DataFrame with user data.
    """
    # Prepare user data
    data = {
        'days_since_registration': [(user.updated_registration_date - user.registration_date).days]}

    df = pd.DataFrame(data)

    return df


async def predict_user_activity(user: User) -> float:
    """
    Predict the probability of user activity in the next month.

    Args:
        user (User): The user object.

    Returns:
        The probability of user activity in the next month.
    """
    # Prepare user data for prediction
    data = prepare_user_data(user)

    # Load the trained model
    model = load_model()

    # Make a prediction
    proba = model.predict_proba(data)[0][1]

    return proba


async def get_path_user(
        request: fastapi.Request,
        user_id: int = fastapi.Path(),
) -> User:
    """Get a user object from the database by ID.

    Args:
        request (fastapi.Request): The FastAPI request object.
        user_id (int): The ID of the user to retrieve.

    Returns:
        The user object with the specified ID, or raises an `HTTPNotFound` exception if the user is not found.
    """

    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_user = await database_service.get_user(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPNotFound()

    return db_user
