"""Topic-specific content for statistics/, classical-ml/, deep-learning/."""

CONTENT = {
    # ============================================================
    # STATISTICS
    # ============================================================
    "statistics/01-probability-basics.md": {
        "title": "Probability Basics",
        "intuition": (
            "Probability is the language for reasoning about uncertainty. Every ML prediction is a guess; probability tells you how to attach a "
            "confidence to it, how to combine evidence, and how often you should be right in the long run."
        ),
        "formal": (
            "A sample space `Ω` lists all possible outcomes. An event is a subset of `Ω`. A probability assigns each event a number in `[0,1]` such that "
            "`P(Ω) = 1` and disjoint events add. Joint probability `P(A,B)`, conditional `P(A|B) = P(A,B)/P(B)`, and independence (`P(A,B)=P(A)P(B)`) are "
            "the building blocks. The chain rule `P(x_1,...,x_n) = Π P(x_i | x_<i)` is the foundation of language models and many graphical models."
        ),
        "why": (
            "Classifiers output probabilities; calibration says whether those probabilities match observed frequencies. Bayesian reasoning combines prior "
            "belief with evidence. A/B tests use probability to decide whether a difference is real. Retrieval and recommenders rank by probability of relevance."
        ),
        "steps": [
            "Define the sample space and the event of interest.",
            "Write the probabilities of the simple events from data or assumption.",
            "Combine using the rules: complement, sum (disjoint), product (independent), conditional.",
            "Sanity-check: do probabilities sum to 1? Are conditionals between 0 and 1?",
            "Translate the answer back into a decision (accept, reject, route to review).",
        ],
        "example": (
            "A spam filter outputs `P(spam | message) = 0.92`. The product rule and prior data say a 0.92 model probability corresponds to actual spam in "
            "88 percent of cases (the model is slightly overconfident). Calibration analysis catches this; uncalibrated probabilities make downstream "
            "thresholds wrong."
        ),
        "mistakes": [
            "Confusing `P(A|B)` with `P(B|A)` (the prosecutor's fallacy).",
            "Assuming independence when events are correlated.",
            "Using model output as a probability without calibrating.",
            "Treating a low-probability event as impossible after observing it once.",
        ],
        "iq": "Explain conditional probability, the chain rule, and how language models use them.",
        "is_strong": (
            "`P(A|B)` is the probability of `A` given `B` happened, equal to `P(A,B)/P(B)`. The chain rule decomposes a joint distribution into a product "
            "of conditionals: `P(x_1, x_2, x_3) = P(x_1) P(x_2|x_1) P(x_3|x_1, x_2)`. Language models predict the next token conditional on the previous "
            "ones, training to maximize the chain-rule likelihood of training text."
        ),
        "is_weak": (
            "Confuse joint and conditional, or claim language models predict joint distributions directly."
        ),
        "follow_ups": [
            "Why are calibrated probabilities important for thresholding?",
            "What does `P(B) = 0` imply for `P(A|B)`?",
            "How would you check independence between two features?",
            "What is the difference between marginal and joint probabilities?",
        ],
        "exercise": (
            "Take any classifier you have used. Bin its predicted probabilities into deciles and plot empirical accuracy per bin. Note where the model is "
            "overconfident or underconfident."
        ),
        "diagram": (
            "flowchart LR\n"
            "    Ev[Evidence E] --> C[P(H | E)]\n"
            "    H[Hypothesis H] --> Pr[Prior P(H)]\n"
            "    Pr --> C\n"
            "    Ev --> L[Likelihood P(E | H)]\n"
            "    L --> C"
        ),
    },
    "statistics/02-random-variables.md": {
        "title": "Random Variables",
        "intuition": (
            "A random variable is a function that maps outcomes to numbers. The roll of a die is a random variable. The latency of an API call is a "
            "random variable. Most ML quantities (predictions, losses, errors) are random variables, which means they have distributions you can describe "
            "and reason about, not single fixed values."
        ),
        "formal": (
            "Discrete random variables take countable values, characterized by a probability mass function `p(x) = P(X = x)`. Continuous random variables "
            "take a continuum, described by a probability density function `f(x)`, with `P(a < X < b) = ∫_a^b f(x) dx`. The CDF `F(x) = P(X ≤ x)` works "
            "for both. Two random variables can be independent or dependent; their joint distribution captures the relationship."
        ),
        "why": (
            "Latency, accuracy on a holdout, and revenue per user are all random variables. Reporting a single number without a distribution hides risk. "
            "Confidence intervals, A/B tests, and uncertainty estimation all assume you can describe the random variable behind the number."
        ),
        "steps": [
            "Decide whether the quantity is discrete or continuous.",
            "Pick a parametric family that matches (Bernoulli, Binomial, Gaussian, Poisson).",
            "Estimate parameters from data (MLE, method of moments).",
            "Validate with a histogram or QQ plot before using the assumption.",
            "Report a distribution or interval, not just a point estimate.",
        ],
        "example": (
            "A team reports p95 latency as 280 ms. They look at the latency distribution and find a heavy right tail with rare 2-second outliers. The 95th "
            "percentile is fine, but the p99 is 1900 ms. Reporting only p95 hid the worst-case experience for a small but important group."
        ),
        "mistakes": [
            "Reporting only the mean for highly skewed data.",
            "Treating a sample of size 5 as the true distribution.",
            "Confusing sample statistics with population parameters.",
            "Picking a Gaussian model for clearly heavy-tailed data.",
        ],
        "iq": "What does it mean to say the model's accuracy is a random variable, and how would you report it?",
        "is_strong": (
            "Accuracy on a held-out set is one realization of a random variable: another set would yield a different number. Report a confidence interval, "
            "not just the point estimate. For small samples, use bootstrap. For large samples, use a normal approximation."
        ),
        "is_weak": (
            "Quote a single accuracy number with no uncertainty."
        ),
        "follow_ups": [
            "What is the difference between PMF, PDF, and CDF?",
            "Why does the law of large numbers matter for evaluation?",
            "How do you bootstrap a confidence interval?",
            "How do you handle heavy-tailed metrics like latency?",
        ],
        "exercise": (
            "Take any metric you compute. Bootstrap-resample it 1000 times to get a 95 percent CI. Note how wide the interval is and what would shrink it."
        ),
        "diagram": (
            "flowchart LR\n"
            "    Ω[Sample space] --> X[Random variable X]\n"
            "    X --> D[Distribution PMF or PDF]\n"
            "    D --> M[Mean, variance, percentiles]\n"
            "    D --> CI[Confidence interval]"
        ),
    },
    "statistics/03-common-distributions.md": {
        "title": "Common Distributions",
        "intuition": (
            "A handful of distributions cover most ML use cases. Bernoulli for yes/no, Binomial for counts of yeses out of n, Categorical for multiclass, "
            "Gaussian (normal) for noise and many real-valued quantities, Poisson for rates of rare events, Exponential for waiting times, and Beta/Dirichlet "
            "for probabilities about probabilities. Recognizing the right one shortcuts a lot of modeling decisions."
        ),
        "formal": (
            "- **Bernoulli(p):** 1 with probability `p`, 0 otherwise.\n"
            "- **Binomial(n, p):** sum of `n` independent Bernoulli(p) trials.\n"
            "- **Categorical:** generalization of Bernoulli to `K` classes; the softmax output of a classifier.\n"
            "- **Gaussian(μ, σ²):** continuous, symmetric, defined by mean and variance; central limit theorem makes it ubiquitous.\n"
            "- **Poisson(λ):** count of events in a fixed interval at rate `λ`; mean equals variance.\n"
            "- **Exponential(λ):** waiting time between Poisson events; memoryless.\n"
            "- **Beta(α, β):** distribution over probabilities, conjugate prior to Bernoulli.\n"
            "- **Dirichlet:** multivariate Beta, conjugate to categorical."
        ),
        "why": (
            "Picking the right distribution gives you the right loss (Bernoulli -> binary cross-entropy, Gaussian -> MSE, Poisson -> Poisson regression), "
            "the right confidence interval, and the right A/B test. Misusing a Gaussian assumption on count data is one of the most common analysis errors."
        ),
        "steps": [
            "Look at the data type: binary, count, real, time, set of probabilities.",
            "Pick the distribution family that matches the data type.",
            "Estimate parameters (MLE for most; conjugate priors for Bayesian).",
            "Validate the fit (QQ plots for Gaussian; mean vs variance for Poisson).",
            "Use the fitted distribution to compute the quantity you actually need.",
        ],
        "example": (
            "A product team reports daily signups with a Gaussian-style mean ± stddev. Signups are counts so a Poisson is more appropriate. Switching to "
            "Poisson reveals that the variance is much higher than the mean (overdispersion), which suggests the right model is negative binomial. The "
            "alert thresholds change because heavy-tailed counts deserve looser bounds."
        ),
        "mistakes": [
            "Modeling counts with a Gaussian (it allows negatives).",
            "Treating mean of Poisson as a tight estimate when variance equals mean.",
            "Forgetting that the central limit theorem requires enough samples and finite variance.",
            "Using Beta with wrong priors and getting overly tight posterior intervals.",
        ],
        "iq": "When would you use Poisson regression instead of linear regression?",
        "is_strong": (
            "When the target is a non-negative count and the variance grows with the mean. Linear regression assumes constant variance and continuous "
            "values; Poisson naturally models counts with variance equal to mean. If you see overdispersion, switch to negative binomial."
        ),
        "is_weak": (
            "Default to Gaussian assumptions for count data."
        ),
        "follow_ups": [
            "Why is the Gaussian so common in ML losses?",
            "What is conjugate prior and why is Beta-Bernoulli so popular?",
            "How would you detect overdispersion in count data?",
            "What is the relationship between exponential and Poisson?",
        ],
        "exercise": (
            "Pick a quantity in your data (clicks per day, signups per hour). Plot a histogram and compare with a fitted Poisson. Decide whether the fit "
            "is acceptable."
        ),
        "diagram": (
            "flowchart LR\n"
            "    Type{Data type} --> Bin[Binary -> Bernoulli]\n"
            "    Type --> Cnt[Count -> Poisson / NB]\n"
            "    Type --> Real[Real -> Gaussian]\n"
            "    Type --> Time[Waiting -> Exponential]\n"
            "    Type --> Probs[Probability -> Beta / Dirichlet]"
        ),
    },
    "statistics/04-expectation-variance-covariance.md": {
        "title": "Expectation, Variance, and Covariance",
        "intuition": (
            "Expectation is the long-run average. Variance is how spread out the values are. Covariance is how two variables move together. These three "
            "summaries appear in nearly every ML formula: loss is an expectation, regularization controls variance, PCA decomposes covariance."
        ),
        "formal": (
            "`E[X] = Σ x p(x)` (or `∫ x f(x) dx`). Linearity: `E[aX + bY] = aE[X] + bE[Y]`. `Var(X) = E[(X - E[X])²] = E[X²] - E[X]²`. `Var(aX + b) = a² Var(X)`. "
            "Covariance `Cov(X, Y) = E[(X - E[X])(Y - E[Y])]`; correlation `ρ = Cov(X, Y) / (σ_X σ_Y)`, in `[-1, 1]`. For independent variables, "
            "`Var(X + Y) = Var(X) + Var(Y)`."
        ),
        "why": (
            "Empirical loss is a sample estimate of expectation; bias-variance decomposition is in the same language. Feature correlation explains why models "
            "do not improve when you add a near-duplicate feature. Risk dashboards report variance and covariance to capture portfolio behavior."
        ),
        "steps": [
            "Pick the quantity whose expectation you care about.",
            "Compute or estimate it from data.",
            "Compute variance to know how reliable that estimate is.",
            "Compute covariance/correlation between features to spot redundancy.",
            "Decide whether dependencies require modeling adjustments (multivariate distributions, decorrelation).",
        ],
        "example": (
            "A model uses two features that are 0.95 correlated. Performance does not improve over using one. Removing the duplicate keeps performance the "
            "same and simplifies the model. Inspecting covariance saved time and complexity."
        ),
        "mistakes": [
            "Confusing correlation 0 with independence (it implies independence only for joint Gaussians).",
            "Reporting mean without variance for noisy metrics.",
            "Treating high correlation as causation.",
            "Ignoring covariance when combining models or features.",
        ],
        "iq": "What is the difference between correlation and causation, and when does correlation imply independence?",
        "is_strong": (
            "Correlation measures linear association; causation requires a directional, mechanistic link. Zero correlation does not imply independence in "
            "general (a quadratic relationship has zero linear correlation). It does imply independence for joint Gaussian variables. To establish causation, "
            "you need controlled experiments or careful causal inference."
        ),
        "is_weak": (
            "Treat correlation and independence as the same."
        ),
        "follow_ups": [
            "Why does adding correlated features rarely help a linear model?",
            "How do you compute the covariance matrix from a data matrix?",
            "What is conditional expectation and where does it appear in ML?",
            "How does Jensen's inequality relate `E[f(X)]` and `f(E[X])`?",
        ],
        "exercise": (
            "Take any feature matrix. Compute the correlation matrix. List the top three highly correlated pairs and decide whether to drop or transform them."
        ),
        "diagram": (
            "flowchart LR\n"
            "    X[Random variable] --> E[Mean E[X]]\n"
            "    X --> V[Variance Var(X)]\n"
            "    Y[Other variable] --> C[Cov(X,Y)]\n"
            "    X --> C\n"
            "    C --> Cor[Correlation ρ]"
        ),
    },
    "statistics/05-bayes-theorem.md": {
        "title": "Bayes' Theorem",
        "intuition": (
            "Bayes' theorem updates a belief in light of evidence. You start with a prior probability of a hypothesis, observe evidence, and end with a "
            "posterior probability. The same machinery underlies medical tests, spam classifiers, and Bayesian inference."
        ),
        "formal": (
            "`P(H | E) = P(E | H) P(H) / P(E)`. The posterior is proportional to likelihood times prior. The denominator is a normalization. For multiple "
            "hypotheses, the posterior is a categorical distribution over them. Updating with new evidence `E2` (independent given `H`) just multiplies in "
            "another likelihood."
        ),
        "why": (
            "Naive Bayes classifiers, Bayesian A/B tests, and many uncertainty estimates use Bayes' rule directly. Even non-Bayesian engineers should "
            "understand it for diagnostic problems: a positive medical test does not mean the disease is likely if the prior is small."
        ),
        "steps": [
            "Write the prior `P(H)` from base rates or domain knowledge.",
            "Write the likelihood `P(E | H)` from data or model.",
            "Multiply, normalize, and read the posterior.",
            "Update with new evidence by multiplying in more likelihoods.",
            "Communicate the result with both the posterior and the underlying assumptions.",
        ],
        "example": (
            "A medical test has 99 percent sensitivity and 99 percent specificity for a disease that has 1 in 1000 prevalence. A positive result yields a "
            "posterior probability of disease around 9 percent, not 99 percent. Without applying Bayes, the test result is dangerously misinterpreted."
        ),
        "mistakes": [
            "Ignoring the prior when interpreting test results.",
            "Treating a posterior as a frequency (interpretation depends on Bayesian vs frequentist).",
            "Picking a flat prior when a real prior exists.",
            "Forgetting that likelihoods must integrate to 1 over evidence, not over hypotheses.",
        ],
        "iq": "Explain Bayes' theorem and apply it to a diagnostic test problem.",
        "is_strong": (
            "Posterior = likelihood times prior over evidence. Apply: with prevalence 0.001, sensitivity 0.99, specificity 0.99, the false-positive rate "
            "is 0.01 across 999 healthy people, producing about 10 false positives for every true positive. The posterior probability of disease given "
            "a positive test is roughly 9 percent."
        ),
        "is_weak": (
            "Quote the formula without explaining how the prior changes the answer."
        ),
        "follow_ups": [
            "What is the difference between prior and posterior?",
            "How does naive Bayes use this rule?",
            "When would you use a Bayesian A/B test?",
            "How do you pick a prior when you do not have data?",
        ],
        "exercise": (
            "Pick a binary classification problem. Estimate base rate, sensitivity, and specificity from data. Compute the posterior probability of the "
            "positive class given a positive prediction."
        ),
        "diagram": (
            "flowchart LR\n"
            "    Pr[Prior P(H)] --> Po[Posterior P(H|E)]\n"
            "    L[Likelihood P(E|H)] --> Po\n"
            "    Po --> D[Decision]\n"
            "    E2[New evidence E2] --> Po"
        ),
    },
    "statistics/06-maximum-likelihood-estimation.md": {
        "title": "Maximum Likelihood Estimation",
        "intuition": (
            "MLE picks the parameters that make the observed data most likely under the assumed model. It is the workhorse of training: classification "
            "with cross-entropy is MLE, regression with MSE is MLE under Gaussian noise, and many other losses are MLEs of specific likelihoods."
        ),
        "formal": (
            "Given a parametric model `p(x; θ)` and i.i.d. data `x_1, ..., x_n`, the likelihood is `L(θ) = Π p(x_i; θ)`. The log-likelihood "
            "`ℓ(θ) = Σ log p(x_i; θ)` is easier to optimize. MLE is `θ_hat = argmax ℓ(θ)`, often by setting the gradient to zero or running gradient descent. "
            "Under regularity conditions, MLE is consistent and asymptotically efficient."
        ),
        "why": (
            "Most ML losses are negative log-likelihoods. Knowing the underlying likelihood tells you which loss to use, what the model assumes about "
            "the noise, and what the maximum-likelihood asymptotics imply about confidence intervals."
        ),
        "steps": [
            "Choose a probabilistic model that matches the data.",
            "Write the log-likelihood as a sum over data points.",
            "Take the derivative with respect to parameters.",
            "Set to zero (closed form) or run gradient descent (general case).",
            "Validate that the assumed distribution actually fits the data.",
        ],
        "example": (
            "Linear regression with squared error is MLE under the assumption that residuals are i.i.d. Gaussian. If residuals are heavy-tailed, MLE under "
            "a Laplace distribution gives least absolute deviations, which is more robust. Choosing the right likelihood is choosing the right loss."
        ),
        "mistakes": [
            "Using MSE on classification (wrong likelihood).",
            "Forgetting that MLE can overfit small data; regularization or MAP is safer.",
            "Quoting MLE confidence intervals without checking the model fits.",
            "Believing MLE is always unbiased; it can be biased for small samples.",
        ],
        "iq": "Explain MLE and connect it to the cross-entropy loss in classification.",
        "is_strong": (
            "MLE picks parameters that maximize `Σ log p(y_i | x_i; θ)`. For categorical `y` with model probability `q(y | x)`, the negative log-likelihood "
            "is `-Σ log q(y_i | x_i)`, which is exactly cross-entropy with a one-hot target. So minimizing cross-entropy is MLE for the categorical model."
        ),
        "is_weak": (
            "Treat MLE as an unrelated theoretical concept."
        ),
        "follow_ups": [
            "What is MAP and how does it differ from MLE?",
            "When is MLE biased?",
            "What is the connection between MLE and KL divergence?",
            "Why is regularization equivalent to a Bayesian prior?",
        ],
        "exercise": (
            "Pick a small dataset. Derive the MLE for a Bernoulli model by hand and confirm it equals the sample mean."
        ),
        "diagram": (
            "flowchart LR\n"
            "    M[Model p(x;θ)] --> L[Likelihood Π p(x_i;θ)]\n"
            "    D[Data] --> L\n"
            "    L --> LL[Log-likelihood]\n"
            "    LL --> O[argmax θ]\n"
            "    O --> P[θ_hat]"
        ),
    },
    "statistics/07-hypothesis-testing.md": {
        "title": "Hypothesis Testing",
        "intuition": (
            "Hypothesis testing asks whether an observed effect is real or could be noise. You set up a null (no effect) and an alternative, compute a test "
            "statistic, and ask how likely the data would be if the null were true. If unlikely (small p-value), you reject the null."
        ),
        "formal": (
            "Two-sample tests (t-test, z-test, Mann-Whitney) compare distributions. Categorical data uses chi-square. The p-value is `P(observed or more extreme | H0)`. "
            "A significance level `α` (often 0.05) sets the type-I error rate. Power is `1 - P(type-II error)`; sample size, effect size, and variance set "
            "achievable power. Multiple testing inflates false positives; correct with Bonferroni, BH, or sequential methods."
        ),
        "why": (
            "Every A/B test, every claim of a model improvement, every experiment in the wild lives or dies by hypothesis testing. Misusing it produces "
            "fake wins, wasted resources, and embarrassing rollbacks."
        ),
        "steps": [
            "State `H0` and `H1` precisely.",
            "Pick the right test based on the data (continuous, categorical, paired, sample size).",
            "Estimate sample size for desired power before running.",
            "Compute the test statistic and p-value.",
            "Decide using both p-value and effect size; report a confidence interval.",
        ],
        "example": (
            "A team A/B tests a UI change with 500 users per arm. p-value is 0.03 with a 0.5 percent lift. The change is statistically significant but the "
            "effect is tiny and the CI nearly includes zero. Shipping it provides almost no business value and adds maintenance burden. Statistical "
            "significance is necessary, not sufficient."
        ),
        "mistakes": [
            "Confusing p-value with `P(H0 is true)`.",
            "Peeking at results and stopping early (inflates false positives).",
            "Ignoring power; small samples cannot detect small effects.",
            "Multiple testing without correction.",
            "Running a one-sided test to chase significance.",
        ],
        "iq": "What is a p-value and what are its common misinterpretations?",
        "is_strong": (
            "A p-value is the probability of observing data at least as extreme as ours, assuming the null hypothesis. It is not the probability the null is "
            "true, not the probability the effect is real, and not the magnitude of the effect. Pair it with a confidence interval and a practical "
            "significance threshold."
        ),
        "is_weak": (
            "Define a p-value as the probability the null is true."
        ),
        "follow_ups": [
            "What is the difference between type-I and type-II error?",
            "Why is `p < 0.05` a convention rather than a law?",
            "How do you correct for multiple comparisons?",
            "What is the difference between statistical and practical significance?",
        ],
        "exercise": (
            "Take any A/B test result you have. Recompute the test, the CI, and the practical effect size. Decide whether the win is worth shipping."
        ),
        "diagram": (
            "flowchart LR\n"
            "    H0[Null H0] --> T[Test stat]\n"
            "    H1[Alternative H1] --> T\n"
            "    D[Data] --> T\n"
            "    T --> P[p-value]\n"
            "    P --> Dec{p < α and<br/>effect meaningful?}"
        ),
    },
    "statistics/08-confidence-intervals.md": {
        "title": "Confidence Intervals",
        "intuition": (
            "A confidence interval is a range of plausible values for a quantity. A 95 percent CI says: if we repeated the experiment many times, the "
            "interval would contain the true value 95 percent of the time. It is not a probability statement about a single interval, but a long-run "
            "frequency property. CIs are how you communicate uncertainty without pretending you have a point estimate."
        ),
        "formal": (
            "For a sample mean with known variance, `CI = x_bar ± z (σ / sqrt(n))`. With unknown variance and small `n`, use the t-distribution. For "
            "binomials, Wilson or Clopper-Pearson are better than the normal approximation, especially near 0 or 1. For arbitrary statistics, bootstrap "
            "by resampling the data and computing the statistic many times."
        ),
        "why": (
            "Reporting only a point estimate is a common cause of bad decisions. A 'lift of 5 percent' that has a CI of [-2 percent, 12 percent] is "
            "different from one with [4 percent, 6 percent]. CIs let stakeholders see the risk."
        ),
        "steps": [
            "Decide the statistic of interest (mean, proportion, ratio, AUC).",
            "Pick a CI method matched to the statistic and sample size.",
            "Compute or bootstrap the interval.",
            "Communicate both the point estimate and the interval.",
            "Check that the interval is narrow enough for the decision; if not, collect more data.",
        ],
        "example": (
            "A model evaluation reports AUC 0.84 with a 95 percent CI of [0.79, 0.89]. The wide interval signals that the holdout is too small to be confident "
            "in fine model differences. Adding data narrows the CI; the comparison between two models becomes meaningful only after."
        ),
        "mistakes": [
            "Reporting a point estimate with no interval.",
            "Treating a single 95 percent CI as 'the truth is 95 percent inside this'.",
            "Using a normal-approximation CI for a proportion near 0 or 1.",
            "Bootstrapping incorrectly (e.g., not preserving the sampling unit).",
            "Confusing CI with prediction interval.",
        ],
        "iq": "Explain a 95 percent confidence interval and how you would compute one for AUC.",
        "is_strong": (
            "A 95 percent CI is constructed so that, in repeated sampling, 95 percent of intervals contain the true value. For AUC, bootstrap by resampling "
            "the holdout (with replacement, preserving the unit of analysis), recompute AUC each time, and take the 2.5th and 97.5th percentiles. Or use "
            "the DeLong method for a parametric estimate."
        ),
        "is_weak": (
            "Say the true value is 95 percent inside the interval (incorrect frequentist interpretation)."
        ),
        "follow_ups": [
            "What is the difference between a CI and a prediction interval?",
            "How does sample size affect CI width?",
            "When is bootstrap inappropriate?",
            "What is a credible interval and how does it differ?",
        ],
        "exercise": (
            "Take any metric. Bootstrap a 95 percent CI from 1000 resamples. Note how the CI changes with sample size by subsampling 10 percent of the data."
        ),
        "diagram": (
            "flowchart LR\n"
            "    D[Data] --> B[Bootstrap resamples]\n"
            "    B --> S[Statistic per sample]\n"
            "    S --> P[2.5% and 97.5% percentiles]\n"
            "    P --> CI[95% CI]"
        ),
    },
    "statistics/09-correlation-vs-causation.md": {
        "title": "Correlation vs Causation",
        "intuition": (
            "Two things move together does not mean one causes the other. Lurking variables (a third factor causing both), reverse causation, and selection "
            "bias all create correlation without causation. Real ML systems are full of correlated features that look causal but break under intervention."
        ),
        "formal": (
            "Causal inference asks `P(Y | do(X))`, the distribution of Y when we intervene on X, not just observe it. Randomized experiments break the "
            "lurking-variable problem because they assign X independently of confounders. Observational methods (instrumental variables, propensity scores, "
            "difference-in-differences, regression discontinuity) attempt to recover causal effects without random assignment, with assumptions."
        ),
        "why": (
            "Models trained on observational data learn correlations. When deployed in a setting that changes the upstream cause, predictions break. "
            "Engineers who confuse correlation with causation ship models that work until they do not, often during the most important moments."
        ),
        "steps": [
            "Decide whether you need to predict or to understand what would happen under intervention.",
            "If interventional, run an experiment (A/B test) when possible.",
            "If not, identify confounders and use methods to adjust for them.",
            "Be explicit about assumptions: which lurking variables you assume away.",
            "Report effect sizes and uncertainty, with caveats about causal interpretation.",
        ],
        "example": (
            "A team finds that customers who use feature X churn less. They make X mandatory and churn worsens. The original correlation came from highly "
            "engaged users self-selecting into X, not from X causing retention. An A/B test would have caught this; the observational analysis did not."
        ),
        "mistakes": [
            "Treating regression coefficients as causal effects.",
            "Adjusting for variables that are downstream of the treatment (post-treatment bias).",
            "Forgetting that selection bias makes observational data unrepresentative.",
            "Using ML models to claim causal insight from purely observational data.",
        ],
        "iq": "How do you tell whether a model is learning a correlation or a causal effect, and why does it matter?",
        "is_strong": (
            "Pure ML models learn correlations. To establish causation, you need an intervention (A/B test) or strong assumptions plus a causal method "
            "(propensity scoring, instrumental variables, DiD). It matters because predictions about what will happen under a new policy require causal "
            "knowledge; observational correlations can flip when the upstream world changes."
        ),
        "is_weak": (
            "Claim a model identifies causes simply because it predicts well."
        ),
        "follow_ups": [
            "What is Simpson's paradox?",
            "Why are randomized experiments the gold standard?",
            "When can observational data give causal insight?",
            "What is a confounder and how do you adjust for it?",
        ],
        "exercise": (
            "Take an observational claim from your data. Sketch a causal diagram. Identify at least one possible confounder and propose an experiment to "
            "test whether the relationship is causal."
        ),
        "diagram": (
            "flowchart LR\n"
            "    X[Observed X] -. correlation .- Y[Observed Y]\n"
            "    Z[Confounder Z] --> X\n"
            "    Z --> Y\n"
            "    A[A/B test] -- breaks confound --> Cause[True effect of X on Y]"
        ),
    },
    "statistics/10-ab-testing.md": {
        "title": "A/B Testing",
        "intuition": (
            "An A/B test is a randomized experiment that splits users into a control and a treatment group, applies a change to the treatment, and measures "
            "the difference in a chosen metric. Randomization makes the groups comparable; the only systematic difference should be the treatment."
        ),
        "formal": (
            "Define the primary metric, the unit of randomization, and the duration. Compute sample size using `n ≈ 2 σ² (z_{α/2} + z_β)² / Δ²` where `Δ` "
            "is the minimum detectable effect. Run the test long enough to reach the planned size before peeking. Use stratified or blocked randomization "
            "to reduce variance. Analyze with a t-test for continuous metrics or a proportion test for binary; correct for multiple comparisons across "
            "secondary metrics. Watch for SUTVA violations (treatment effect spilling between users) and novelty/seasonality effects."
        ),
        "why": (
            "Most product changes that look good in dashboards are noise; A/B tests filter the real wins. Big tech runs thousands of experiments per quarter. "
            "Engineers who can design and analyze them rigorously protect the company from shipping changes that hurt users."
        ),
        "steps": [
            "Define the user, the metric, and the minimum effect that matters.",
            "Compute required sample size for desired power.",
            "Randomize at the right unit (user, account, session) so spillover does not contaminate.",
            "Pre-register hypotheses, sample size, and stopping rules.",
            "Run for the planned duration; do not peek and stop early.",
            "Analyze with confidence intervals and a check on guardrail metrics (latency, errors, revenue).",
        ],
        "example": (
            "A search team A/B tests a new ranker. Click-through rate rises 1 percent (significant) but revenue drops 2 percent (significant). Looking only "
            "at the primary metric would have shipped a clearly bad change. Tracking guardrails saved the team from a regression."
        ),
        "mistakes": [
            "Stopping early when results look good (peeking inflates false positives).",
            "Randomizing at the wrong unit (treating sessions when users straddle treatments).",
            "Ignoring power and chasing tiny effects with too-small samples.",
            "Skipping pre-registration and trying many metrics until one is significant.",
            "Forgetting novelty effects: the first week may not represent steady state.",
        ],
        "iq": "Walk through how you would design an A/B test for a new recommendation algorithm.",
        "is_strong": (
            "Define the metric (e.g., long-term watch time per user) and minimum lift that matters. Compute sample size for 80 percent power. Randomize at "
            "user level to avoid contamination. Run a pre-launch sanity check on a small percentage of traffic. Pre-register hypotheses. Run for at least "
            "a week to capture day-of-week effects. Analyze with CI plus guardrails (latency, ad revenue, complaints). Decide based on practical and "
            "statistical significance."
        ),
        "is_weak": (
            "Quote 'p < 0.05 ship it' without effect size, sample size, or guardrails."
        ),
        "follow_ups": [
            "What is the difference between SUTVA and SUTPA?",
            "When do you need a switchback test instead of a parallel A/B?",
            "How do you handle long-term metrics that take weeks to mature?",
            "What is a guardrail metric and why does it matter?",
        ],
        "exercise": (
            "Pick a feature you ship. Design the A/B test: metric, randomization unit, sample size, duration, guardrails, decision rule. One page."
        ),
        "diagram": (
            "flowchart LR\n"
            "    U[Users] --> R[Randomize]\n"
            "    R --> A[Control]\n"
            "    R --> B[Treatment]\n"
            "    A --> M[Metric]\n"
            "    B --> M\n"
            "    M --> St[Stat test + CI]\n"
            "    St --> Dec[Ship / kill / iterate]"
        ),
    },
    "statistics/11-sampling-bias-and-data-leakage.md": {
        "title": "Sampling Bias and Data Leakage",
        "intuition": (
            "Sampling bias means the data does not represent the population you care about. Data leakage means features carry information that would not "
            "be available at prediction time. Both produce models that look great offline and fail in production. They are the two most common causes of "
            "ML disasters."
        ),
        "formal": (
            "Selection bias: samples are not random with respect to the target (only loan acceptees, only past customers, only users who completed a flow). "
            "Survivorship bias: missing entities skew the analysis. Temporal leakage: a feature uses information from after the prediction time. Target "
            "leakage: a feature is a near-copy of the label. Train-test leakage: identical or near-duplicate items appear in both splits."
        ),
        "why": (
            "These problems are silent. Validation looks great because the same bias contaminates the holdout. They surface only after deployment when "
            "real traffic exposes the gap. Engineers who learn to detect leakage early save weeks of cleanup."
        ),
        "steps": [
            "Map the timeline: when is each feature created relative to the prediction?",
            "Identify the data-generating process. Who is in the dataset and who is not?",
            "Run a 'leakage check' by training on shuffled labels; if performance is high, you have leakage.",
            "Compare segment performance to global performance; gaps may indicate selection bias.",
            "When deploying, log inputs to verify they match training distribution.",
        ],
        "example": (
            "A loan default model includes 'amount of late payments to date' as a feature. In production, that field is updated continuously; when fed "
            "current values, the feature already contains the answer. AUC drops from 0.95 (offline) to 0.6 (online). Removing the leaky feature gives the "
            "real number."
        ),
        "mistakes": [
            "Using post-event data as a feature.",
            "Random splits when grouping or time matters.",
            "Computing scaling or imputation parameters on the full dataset.",
            "Treating dropout from the funnel as random.",
            "Training only on positive cases (only past defaults), then evaluating on all loans.",
        ],
        "iq": "How would you audit a new dataset for sampling bias and leakage before training?",
        "is_strong": (
            "Map who is in the dataset and how they got there; ask which users are missing. Examine each feature for temporal validity and write down the "
            "exact moment it is computed. Run a sanity training on shuffled labels; high performance there is a red flag. Compare distributions of features "
            "across train, validation, and a fresh production sample."
        ),
        "is_weak": (
            "Trust the data because it came from an internal warehouse."
        ),
        "follow_ups": [
            "What is the difference between selection bias and confounding?",
            "How would you detect train-test contamination?",
            "What logging would you add to verify training distribution matches production?",
            "How do you handle missing data without leaking?",
        ],
        "exercise": (
            "Pick a recent dataset. List every feature with the time it is computed. Circle any feature that might exist after the prediction time."
        ),
        "diagram": (
            "flowchart LR\n"
            "    R[Raw data] --> S{Check sampling}\n"
            "    R --> L{Check leakage}\n"
            "    S --> Pop[Does it represent prod?]\n"
            "    L --> Time[Features only from past?]\n"
            "    Pop --> Tr[Train safely]\n"
            "    Time --> Tr"
        ),
    },
}
