# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Linear Regression on Synthetic Data
#
# This notebook demonstrates a minimal, reproducible example of linear regression using synthetic data to showcase analysis structure.

# %%
# Dependencies
# !pip install --quiet numpy pandas matplotlib scikit-learn

# %%
# Imports and Setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

plt.style.use('dark_background')
np.random.seed(42)
print('1111111111111111111111111')

# %%
# Main Analysis
# Generate synthetic linear data with noise
n_samples = 200
X = np.linspace(0, 10, n_samples).reshape(-1, 1)
true_slope, true_intercept = 2.5, -1.0
y = true_slope * X[:, 0] + true_intercept + np.random.normal(0, 1.0, size=n_samples)

# Fit linear regression
model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

# Plot
title = f"Linear Regression (R^2={r2:.3f}, MSE={mse:.3f})"
plt.figure(figsize=(8, 5))
plt.scatter(X, y, s=12, alpha=0.7, label="Data")
plt.plot(X, y_pred, color="orange", linewidth=2.5, label="Fit")
plt.title(title)
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.show()

print({
    "estimated_slope": float(model.coef_[0]),
    "estimated_intercept": float(model.intercept_),
    "r2": float(r2),
    "mse": float(mse),
})

# %% [markdown]
# ## Results and Conclusions
#
# - The model recovers the underlying linear relationship with high R^2 on synthetic data.
# - The plot shows the fitted regression line over the noisy samples.
# - Replace this synthetic demo with your domain-specific dataset or API-powered data to fit the project's goals.
