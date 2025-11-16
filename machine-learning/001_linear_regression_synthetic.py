import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def generate_synthetic_data(num_samples: int = 200, slope: float = 2.5, intercept: float = -1.0, noise_std: float = 1.0):
	np.random.seed(42)
	X = np.linspace(0, 10, num_samples).reshape(-1, 1)
	y = slope * X[:, 0] + intercept + np.random.normal(0, noise_std, size=num_samples)
	return X, y


def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> tuple[LinearRegression, np.ndarray, float, float]:
	model = LinearRegression()
	model.fit(X, y)
	predictions = model.predict(X)
	mse = mean_squared_error(y, predictions)
	r2 = r2_score(y, predictions)
	return model, predictions, mse, r2


def plot_results(X: np.ndarray, y: np.ndarray, predictions: np.ndarray, r2: float, mse: float) -> None:
	plt.style.use("dark_background")
	title = f"Linear Regression (R^2={r2:.3f}, MSE={mse:.3f})"
	plt.figure(figsize=(8, 5))
	plt.scatter(X, y, s=12, alpha=0.7, label="Data")
	plt.plot(X, predictions, color="orange", linewidth=2.5, label="Fit")
	plt.title(title)
	plt.xlabel("X")
	plt.ylabel("y")
	plt.legend()
	plt.tight_layout()
	plt.show()


def main() -> None:
	X, y = generate_synthetic_data()
	model, preds, mse, r2 = fit_linear_regression(X, y)
	print({
		"estimated_slope": float(model.coef_[0]),
		"estimated_intercept": float(model.intercept_),
		"r2": float(r2),
		"mse": float(mse),
	})
	plot_results(X, y, preds, r2, mse)


if __name__ == "__main__":
	main()


