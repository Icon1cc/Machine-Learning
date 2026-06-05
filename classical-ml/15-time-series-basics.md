# Time Series Basics

## Beginner-Friendly Intuition

Time series data has order. Yesterday's value influences today's, and today's
influences tomorrow's. That single property breaks most assumptions of
ordinary ML: rows are not independent, splits cannot be random, and a model
that performs well on a shuffled validation set will collapse in production.

The intuition is straightforward: a time series is not just a column of
numbers. It is a column of numbers plus the structure of when each one
happened. If you ignore the structure, you train on the future and test on
the past, get unrealistically good metrics, and ship a broken model. If you
respect the structure, you discover that classical statistical models often
beat fancy ones, that decomposing trend and seasonality before modeling pays
off, and that the right metric depends entirely on what you are forecasting.

## Formal Explanation

A time series `{y_t}` is a sequence indexed by time. The classical
decomposition is

```
y_t = trend_t + seasonality_t + residual_t      (additive)
y_t = trend_t · seasonality_t · residual_t      (multiplicative)
```

Choose multiplicative when seasonal swings grow with the level (sales).
Additive when they do not (temperature).

### Stationarity

A series is **stationary** if its mean, variance, and autocorrelation
structure do not change over time. Stationarity is the central assumption of
ARIMA and many other classical models. Most real series are non-stationary;
we make them stationary by **differencing** (`y_t - y_{t-1}`), log-transforming,
or removing trend and seasonality.

Tests:

- **Augmented Dickey-Fuller (ADF).** Null hypothesis: non-stationary. If
  p-value is small, the series is stationary.
- **KPSS.** Null hypothesis: stationary. Use both in combination; agreement is
  more convincing than either alone.

### Autocorrelation

The **ACF** (autocorrelation function) measures correlation between `y_t` and
`y_{t-k}` for various lags `k`. The **PACF** (partial autocorrelation
function) is the correlation after controlling for shorter lags. ACF and PACF
plots reveal seasonality (regular spikes at lag 7, 12, 24, etc.) and tell you
where to start with ARIMA orders.

### ARIMA(p, d, q)

The classical workhorse. Three parameters:

- **p:** number of autoregressive (AR) lags. `y_t` depends on `y_{t-1}, ..., y_{t-p}`.
- **d:** number of differences to make the series stationary.
- **q:** number of moving-average (MA) lags. The model includes lagged
  forecast errors.

With seasonality, **SARIMA(p, d, q)(P, D, Q)_m** adds seasonal AR, differencing,
and MA terms at period `m` (12 for monthly with annual seasonality, 7 for
daily with weekly seasonality).

Choose `d` from differencing tests, then pick `p, q` from ACF and PACF or by
AIC/BIC search. `auto_arima` automates this and is often a strong baseline.

### Exponential smoothing (ETS)

A weighted moving average where weights decay exponentially with age.
**Holt-Winters** extends this to trend and seasonality. ETS is fast,
interpretable, often competitive with ARIMA, and the default for forecasting
at scale.

### Prophet

Facebook's library models the series as `y_t = trend_t + seasonality_t +
holidays_t + residual_t` with a piecewise-linear trend. Designed for business
time series with seasonality, holiday effects, and missing data. Easy to use,
robust defaults, but less flexible than full ARIMA or modern methods.

### Modern methods

Gradient boosted trees on engineered lag features (lag-1, lag-7, rolling
mean, day-of-week, holiday flag) often beat classical methods on
medium-to-large datasets. Deep models (DeepAR, N-BEATS, Temporal Fusion
Transformer) win on large datasets with many related series.

### Train/test split

Always **time-ordered**: train on the past, test on the most recent window.
For cross-validation, use **expanding window** or **rolling origin**: train on
[1..T], test on T+1; train on [1..T+1], test on T+2; and so on. Random
shuffling on time series is a leakage bug.

### Forecast metrics

Pick by what the business is sensing.

- **MAE.** Mean absolute error. Robust to outliers; in original units.
- **RMSE.** Root mean squared error. Penalizes large errors heavily.
- **MAPE.** Mean absolute percentage error. Scale-free but blows up when
  actuals are near zero, and is asymmetric (over-forecasts and
  under-forecasts are penalized differently).
- **sMAPE.** Symmetric MAPE. Mitigates one of MAPE's issues but is still
  unstable near zero.
- **MASE.** Mean absolute scaled error. The error relative to a naive
  one-step forecast. Robust, scale-free, and the recommended default for
  cross-series benchmarks.
- **Quantile loss.** When the deliverable is a prediction interval (inventory
  bounds, capacity planning).

## Why It Matters in Real Jobs

Forecasting drives demand planning, inventory, capacity, ad budget pacing,
financial reporting, and any system that has to commit to a number tomorrow
based on what happened yesterday. The classical methods are still used because
they are interpretable (a forecast plus a confidence interval, with named
trend and seasonality components), they handle small data well, and they are
fast to retrain. Modern methods take over when you have many related series
or when you can afford to train deep models.

## How It Works Step by Step

1. **Plot the series.** Trend, seasonality, level shifts, missing data, and
   outliers should all be visible. Without this plot you cannot model.
2. **Decompose.** Use STL or seasonal_decompose to separate trend, seasonality,
   and residual. The residual should look like noise; if it does not, you
   missed structure.
3. **Test stationarity.** ADF and KPSS. If non-stationary, difference until
   stationary.
4. **Pick a model class.** ETS for fast and interpretable. SARIMA when ACF and
   PACF show clear structure. Prophet for business series with holidays and
   missing data. Tree-based with lag features for medium-to-large data. Deep
   models for many related series.
5. **Train with time-ordered splits.** Expanding or rolling origin
   cross-validation. Random splits leak.
6. **Pick a metric matched to the use case.** MASE as a default, quantile loss
   when intervals matter.
7. **Generate prediction intervals.** Point forecasts hide uncertainty; for
   any decision (order quantities, capacity), a CI is required.
8. **Monitor for drift.** Time series distributions shift; retrain weekly or
   monthly.

## Real-World Example

A retail team forecasts daily demand per SKU per store, 60 days ahead. They
have 5 years of history, 120K SKU-store combinations. ETS per series is fast
(2 minutes) and gives MASE 1.18. SARIMA is slow and gives 1.12. Prophet is
1.10 with built-in holiday handling. A LightGBM model with lag-1, lag-7,
lag-30, rolling-7 mean, day-of-week, holiday flag, and store-SKU embeddings
gets MASE 0.91. They ship LightGBM with quantile loss at `τ ∈ {0.1, 0.5, 0.9}`
to give inventory bounds. The fallback is Prophet for new SKUs without
enough history.

## Common Mistakes

- Random train/test split. The model trains on the future, scores look great,
  production fails.
- Forecasting without a baseline. Always compare to naive (`y_t = y_{t-1}`)
  and seasonal naive (`y_t = y_{t-m}`); your fancy model should beat both.
- Reporting MAPE on series that include zeros or near-zero values. Switch to
  MASE.
- Ignoring stationarity. Fitting ARIMA on a clearly trending series without
  differencing produces noise.
- Forgetting holiday and special-event effects. They blow up forecast errors
  and are easy to encode.
- Treating prediction intervals as guarantees. They are calibrated under
  model assumptions; check empirically.
- Using deep models on a single short series with no covariates. Classical
  methods almost always win.
- Forecasting one step ahead and reporting metrics, then shipping a model
  that is asked to forecast 30 steps. Errors compound; evaluate at the
  horizon you ship.

## Interview Angle

**Question:** Why must you use a time-ordered train/test split for time
series, and what specifically goes wrong with a random split?

**Strong answer:** Time series observations are not independent. `y_t` depends
on `y_{t-1}`, on long-range autocorrelations, on seasonality, and on slow
non-stationary drift. A random shuffle puts some observations from later in
the series into the training set and some from earlier into the test set.
The model learns to interpolate between known surrounding points, which is
trivial for autocorrelated data, and reports near-perfect metrics. In
production, the model is asked to extrapolate forward in time without
neighboring future data; performance collapses. A time-ordered split (train
on [1..T], test on T+1..T+h) reproduces the production task: forecast the
future from the past. Within the training set, expanding-window or
rolling-origin cross-validation evaluates how the model behaves as more data
becomes available, which mirrors how it will be retrained over time. Random
splits also leak seasonality (training on Sundays around the test Sunday
means the model knows the local seasonal level), trend (training on
neighboring points means the model interpolates between them), and any
holiday effect. The bug is silent in offline metrics and obvious only at
deployment.

**Weak answer:** "Time matters" without explaining autocorrelation, leakage,
or how the production task differs from random scoring.

**Follow-up questions:**

- What is stationarity and how do you achieve it?
- When would you choose ETS over ARIMA?
- Why is MAPE a bad default metric?
- How do you forecast a series with no history (cold start)?

## Mini Exercise

Take a public daily time series (sales, electricity, weather). Plot it. Run
ADF and KPSS. Difference if needed. Fit a naive baseline, ETS, SARIMA, and
LightGBM with engineered features. Compare MASE on a held-out last-90-days
window.

## Diagram

```mermaid
flowchart LR
    Y[Series y_t] --> P[Plot and decompose]
    P --> S[Test stationarity]
    S --> M[Choose model: ETS / SARIMA / Prophet / GBM]
    M --> CV[Time-ordered CV]
    CV --> F[Forecast + intervals]
    F --> O[Monitor and retrain]
```

---
## Navigation

[⬅ Previous](14-anomaly-detection.md) | [🏠 Home](../README.md) | [➡ Next](16-model-selection.md)
