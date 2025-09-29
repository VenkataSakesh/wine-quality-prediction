import joblib
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def train_and_save_model():
    # Load wine dataset
    data = load_wine()
    X, y = data.data, data.target

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model trained. Accuracy: {acc:.4f}")

    # Save model
    joblib.dump(model, "wine_model.pkl")
    print("Model saved as wine_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
