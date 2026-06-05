"""
Topic-specific content for every templated learning file.

Each entry is keyed by relative path. The fields below replace the templated
sections with real, topic-specific prose. When a field is missing, the rewriter
falls back to a generic but still topic-aware string built from the title.

Sections produced:
    intuition  -> Beginner-Friendly Intuition (1-2 paragraphs)
    formal     -> Formal Explanation (1-2 paragraphs, can include lists)
    why        -> Why It Matters in Real Jobs (1 paragraph)
    steps      -> How It Works Step by Step (numbered list, 5-7 steps)
    example    -> Real-World Example (1-2 paragraphs)
    mistakes   -> Common Mistakes (5-7 bullets)
    iq         -> Interview Angle question text after "Question:"
    is_strong  -> Strong answer
    is_weak    -> Weak answer
    follow_ups -> 4-5 follow-up bullets
    exercise   -> Mini Exercise (1 paragraph)
    diagram    -> Mermaid block (without the surrounding fence)
"""

CONTENT = {
    # --------------------------------------------------------------
    # FUNDAMENTALS
    # --------------------------------------------------------------
    "fundamentals/01-what-is-machine-learning.md": {
        "title": "What Is Machine Learning",
        "intuition": (
            "Machine learning is the practice of teaching a computer to do a task by showing it examples instead of writing the rules by hand. "
            "If you can describe a task as input goes in and an answer comes out, and you have many past inputs paired with the right answers, "
            "you can usually train a model that makes useful predictions on inputs it has never seen.\n\n"
            "A useful test for any beginner: name the input, the output, where the labels come from, the metric you would judge it by, "
            "and one mistake the model is likely to make. If you can answer those five things, you can talk about almost any ML problem."
        ),
        "formal": (
            "Machine learning fits a function `f(x) -> y` from data. You collect a dataset of input-output pairs, choose a model family "
            "(linear, tree-based, neural, etc.), pick a loss that measures how wrong the predictions are, and run an optimizer that adjusts "
            "the model's parameters to reduce the loss. The goal is not to memorize the training set but to generalize, which is checked on a held-out set.\n\n"
            "Three flavors cover most problems:\n\n"
            "- **Supervised learning** uses labeled examples to predict a target (classification, regression).\n"
            "- **Unsupervised learning** finds structure in unlabeled data (clustering, dimensionality reduction).\n"
            "- **Reinforcement learning** learns from rewards collected by acting in an environment.\n"
        ),
        "why": (
            "On the job, ML is judged by whether it improves a real decision: a click-through rate, a fraud loss, an answer that helps a user. "
            "Engineers who do well frame the task crisply, build a baseline first, evaluate honestly on data that looks like production, "
            "and watch the system after launch. Engineers who struggle skip framing and chase model complexity."
        ),
        "steps": [
            "**Frame the problem.** Write down the user, the decision, the cost of each kind of mistake, and the constraints (latency, privacy, cost).",
            "**Collect and inspect data.** Look at sources, missing fields, label noise, time ranges, and obvious leakage.",
            "**Build a baseline.** A rule, a logistic regression, or a small tree. The baseline is the bar every later model must beat.",
            "**Train and validate.** Split by time when relevant. Use cross-validation only when leakage cannot sneak across folds.",
            "**Evaluate.** Pick metrics that match the cost of errors (precision/recall, calibration, AUC, RMSE). Slice by segment.",
            "**Ship a small version.** Shadow mode or A/B test with monitoring for input drift, latency, and outcome quality.",
            "**Iterate.** Look at errors, feed them back into features, data, or model choice. Repeat.",
        ],
        "example": (
            "A streaming service wants to recommend movies. The input is a user's recent watch history; the output is a ranked list. "
            "A baseline could simply rank by global popularity. A learned model uses watch patterns to personalize the list. The team measures "
            "click-through rate and watch time on a held-out cohort, and watches for failure cases like a new user with no history.\n\n"
            "Notice how the model is one piece. The data pipeline, the metric, the cold-start fallback, and the monitoring all matter. "
            "ML projects fail more often because of those pieces than because of the model itself."
        ),
        "mistakes": [
            "Jumping to a deep model before defining the user, decision, and metric.",
            "Training on data that includes information not available at prediction time (leakage).",
            "Reporting a single average score instead of slicing by user, segment, or time.",
            "Confusing offline metric improvements with real product wins.",
            "Forgetting that production traffic drifts, so a model that was good last quarter may be bad now.",
        ],
        "iq": "Explain what machine learning is, when you would and would not use it, and how you would scope a new ML problem.",
        "is_strong": (
            "Define ML as learning a function from data, not from hand-written rules. Use it when you have many examples, a measurable outcome, "
            "and a problem where rules are hard to enumerate. Avoid it when the problem can be solved with a simple deterministic rule, when "
            "data is too sparse, or when the cost of a wrong answer is too high without a fallback. Scope by writing down the user, decision, "
            "data, baseline, metric, and one likely failure mode before any modeling."
        ),
        "is_weak": (
            "Recite a textbook definition and immediately propose a deep neural network without discussing data, baselines, evaluation, or constraints."
        ),
        "follow_ups": [
            "When would a rule-based system beat ML?",
            "What would make your offline metric misleading?",
            "How would you handle a model that performs well on average but badly on a key segment?",
            "What would you monitor in production and why?",
            "How does this answer change if the user's safety is at stake?",
        ],
        "exercise": (
            "Pick a feature you used today (a search bar, a recommendation, a fraud check). Write five bullets: input, output, baseline, primary metric, "
            "and one failure mode. Then describe one signal that would tell you the model has degraded after launch."
        ),
        "diagram": (
            "flowchart LR\n"
            "    A[User problem] --> B[Frame: input, output, metric]\n"
            "    B --> C[Data and baseline]\n"
            "    C --> D[Train model]\n"
            "    D --> E[Evaluate honestly]\n"
            "    E --> F[Ship + monitor]\n"
            "    F --> C"
        ),
    },
    "fundamentals/02-ai-vs-ml-vs-deep-learning-vs-data-science.md": {
        "title": "AI vs ML vs Deep Learning vs Data Science",
        "intuition": (
            "These terms overlap and people use them loosely, which causes confusion in interviews and at work. The cleanest mental picture is nested: "
            "AI is the broad goal of making machines act intelligently. ML is one approach to AI, where the system learns from data. Deep learning is "
            "a subfield of ML that uses many-layered neural networks. Data science is a job and a workflow that uses statistics and ML to answer questions about data."
        ),
        "formal": (
            "**AI** covers any technique that produces intelligent behavior, including hand-written rules, search, planning, and learning. "
            "**Machine learning** is the subset where behavior is learned from data via optimization of an objective. **Deep learning** is the subset of ML "
            "that uses neural networks with many layers, typically trained on GPUs with backpropagation. **Data science** is the practice of extracting "
            "insight from data and is usually a mix of statistics, ML, and communication, often producing reports or dashboards rather than production systems."
        ),
        "why": (
            "On the job, the term you use signals what kind of work you do. AI engineer roles focus on applied AI systems, ML engineers ship learned models, "
            "deep learning specialists work on neural architectures and training, and data scientists answer business questions and run experiments. "
            "Knowing the boundaries helps you scope the right team, the right tooling, and the right interview prep."
        ),
        "steps": [
            "Identify the user goal and decision.",
            "Decide whether learning from data is needed, or a rule will do.",
            "If learning is needed, decide whether tabular methods or deep models fit the data shape.",
            "If deep, decide whether to fine-tune, prompt, or train from scratch.",
            "Match the team and tooling to the choice (data scientist for analysis, ML engineer for shipping models, AI engineer for AI products).",
            "Plan evaluation, observability, and rollout that match the chosen path.",
        ],
        "example": (
            "A bank wants to reduce fraud. A data scientist analyzes recent fraud cases and reports patterns. An ML engineer turns those patterns into a "
            "real-time tabular classifier. A deep learning engineer adds a sequence model over transaction history. An AI engineer wraps the whole thing in a "
            "reviewer-facing tool that explains decisions. Each role uses different tools, but all are working on the same problem."
        ),
        "mistakes": [
            "Using AI as a buzzword for any data work, which hides the engineering tradeoffs.",
            "Reaching for deep learning on a small tabular dataset where boosted trees would beat it cheaply.",
            "Confusing data analysis projects with productionized ML systems.",
            "Treating LLMs as the only AI; classical ML still owns most of the value in industry.",
            "Asking for an ML engineer when you actually need a data scientist, or vice versa.",
        ],
        "iq": "Distinguish AI, ML, deep learning, and data science with a concrete example for each.",
        "is_strong": (
            "Use the nested mental model. Give one example each: a chess engine using search is AI but not ML. A logistic regression for churn is ML. "
            "A CNN for image classification is deep learning. An A/B-test analysis of a checkout flow is data science. Note that real teams often blend roles."
        ),
        "is_weak": (
            "Treat the terms as synonyms or describe deep learning as a type of data science."
        ),
        "follow_ups": [
            "When would you choose a classical ML model over a deep one?",
            "Where does an LLM application fit in this picture?",
            "Which role best fits an experimentation-heavy growth team?",
            "What does an ML engineer own that a data scientist usually does not?",
        ],
        "exercise": (
            "Take a system you have used (search, recommendations, voice assistant). Identify the parts that are clearly AI, ML, deep learning, and data analysis. "
            "Then propose which role would own each part."
        ),
        "diagram": (
            "flowchart LR\n"
            "    AI[Artificial Intelligence] --> ML[Machine Learning]\n"
            "    ML --> DL[Deep Learning]\n"
            "    DS[Data Science] -. uses .-> ML\n"
            "    DS -. uses .-> Stats[Statistics]\n"
        ),
    },
    "fundamentals/03-supervised-unsupervised-self-supervised-reinforcement-learning.md": {
        "title": "Supervised, Unsupervised, Self-Supervised, and Reinforcement Learning",
        "intuition": (
            "The four learning styles differ by where the supervision signal comes from. Supervised learning learns from labeled examples (input, target). "
            "Unsupervised learning finds structure in unlabeled data. Self-supervised learning creates labels from the data itself (predict the next word, "
            "fill in a masked token). Reinforcement learning learns from rewards earned by acting in an environment over time."
        ),
        "formal": (
            "Each style minimizes a different kind of objective:\n\n"
            "- **Supervised:** minimize loss between predicted `y_hat` and labeled `y` (cross-entropy, MSE).\n"
            "- **Unsupervised:** maximize a structural objective without labels (cluster compactness, reconstruction error, density).\n"
            "- **Self-supervised:** define a pretext task whose labels are derived from the data (next-token prediction, contrastive pairs). "
            "This is how LLMs and modern foundation models are pretrained.\n"
            "- **Reinforcement:** maximize expected reward `E[Σ γ^t r_t]` over a policy that chooses actions, using methods like policy gradients or Q-learning."
        ),
        "why": (
            "Most production ML systems are supervised, because labels carry the most direct signal about what we want. Self-supervised pretraining is "
            "what made foundation models possible: it removed the human-labeling bottleneck for the pretraining stage. Unsupervised methods help with "
            "exploration and segmentation. Reinforcement learning shines for sequential decision problems but is hard to deploy because reward shaping "
            "and safety are tricky."
        ),
        "steps": [
            "Look at what kind of signal you have. Labels? Use supervised. Only data? Try unsupervised or self-supervised.",
            "Define the objective explicitly: what would success look like with this signal?",
            "Pick the smallest method that uses that signal well (logistic regression before transformers).",
            "Evaluate against held-out data, even if the supervision is weak.",
            "Combine styles when needed: pretrain self-supervised, then fine-tune supervised, then RL with human feedback.",
        ],
        "example": (
            "An e-commerce team wants product search. They start with supervised learning: train a ranker on click data. They add unsupervised steps: "
            "cluster products to fill in cold-start and explore. For text understanding they use a self-supervised pretrained transformer. To improve a chatbot "
            "answering refund questions, they apply RLHF: collect human preferences over answers and train the model to prefer the better one."
        ),
        "mistakes": [
            "Calling unsupervised what is actually self-supervised (next-token prediction is supervised by the next token).",
            "Trying RL when you have no good simulator and the cost of bad actions is high.",
            "Using cluster IDs as features without checking that the clusters mean something to the user.",
            "Forgetting that even self-supervised models need supervised evaluation.",
            "Treating RLHF as the only way to align a model when SFT plus rule-based filters often does most of the work.",
        ],
        "iq": "Compare supervised, unsupervised, self-supervised, and reinforcement learning with a concrete use case for each.",
        "is_strong": (
            "Define each by the source of the supervision signal. Give an example: spam classification (supervised), customer segmentation (unsupervised), "
            "LLM pretraining (self-supervised), AlphaGo or RLHF (reinforcement). Note the modern stack often combines them."
        ),
        "is_weak": (
            "Confuse self-supervised with unsupervised, or claim RL is dominant in industry production systems."
        ),
        "follow_ups": [
            "Why is self-supervised pretraining so important for LLMs?",
            "When would you use clustering features in a supervised pipeline?",
            "What makes RL hard to deploy in real systems?",
            "How does RLHF combine supervised and reinforcement learning?",
        ],
        "exercise": (
            "Pick a single product (search, recs, fraud, support chat). For each of the four styles, describe one component of that product where it would "
            "be a reasonable choice and explain why."
        ),
        "diagram": (
            "flowchart TB\n"
            "    A[Data] --> B{Have labels?}\n"
            "    B -- Yes --> C[Supervised]\n"
            "    B -- No --> D{Can derive labels<br/>from data?}\n"
            "    D -- Yes --> E[Self-supervised]\n"
            "    D -- No --> F[Unsupervised]\n"
            "    G[Environment + reward] --> H[Reinforcement]"
        ),
    },
    "fundamentals/04-training-validation-test-splits.md": {
        "title": "Training, Validation, and Test Splits",
        "intuition": (
            "You cannot evaluate a model on the data it learned from, or you will only measure how well it memorized. So you keep some data hidden. "
            "The training set is what the model fits. The validation set is what you use to tune knobs (model choice, hyperparameters). The test set is "
            "the final, untouched holdout you only look at when you are done. Touching the test set repeatedly turns it into a second validation set, "
            "and your real generalization estimate disappears."
        ),
        "formal": (
            "The classic split is 60/20/20 or 70/15/15 of i.i.d. data. For time series, split chronologically so the validation and test sets are after the "
            "training window. For grouped data (multiple rows per user), split by group so a user does not appear in both train and test. "
            "If the dataset is small, use k-fold cross-validation to get a more stable validation estimate, but still keep a held-out test set for the final number.\n\n"
            "Two failure modes dominate: **leakage** (information from the future or from the label sneaks into features) and **distribution shift** "
            "(the test data is too easy or too different from production)."
        ),
        "why": (
            "Honest splits are the difference between a model that looks great offline and dies in production. Most ML disasters trace back to a leaky split, "
            "a too-easy holdout, or a test set that was peeked at so many times that it stopped representing new data."
        ),
        "steps": [
            "Decide whether the data is i.i.d., grouped, or temporal.",
            "Reserve a held-out test set first and lock it away.",
            "Split the rest into train and validation, by group or by time as needed.",
            "Engineer features only from the training window to avoid leakage.",
            "Tune on validation. Do not look at test until the model is final.",
            "Refresh splits when the data distribution shifts; old splits go stale.",
        ],
        "example": (
            "A team builds a churn model. They split rows i.i.d., reach AUC 0.95, and ship. In production, AUC drops to 0.7. The reason: a single user appeared in both "
            "train and test, and one of the features encoded the user's eventual churn. Splitting by user_id and excluding the leaky feature drops offline AUC "
            "to 0.78, which actually holds in production. The painful lesson is that the higher number was lying."
        ),
        "mistakes": [
            "Random row splits when the data is grouped or temporal.",
            "Computing scaling or imputation parameters on the full dataset before splitting (data leakage).",
            "Tuning on the test set, then quoting that number as generalization.",
            "Ignoring class balance: a 1% positive rate split randomly may produce a fold with no positives.",
            "Reusing the same test set for years until it no longer represents real traffic.",
        ],
        "iq": "How would you split a dataset for a churn model, and how would your answer change for a time-series forecasting problem?",
        "is_strong": (
            "For churn, split by user (group split) so the same person is not on both sides. Hold out a recent time window for the test set if churn behavior shifts. "
            "For forecasting, use a chronological split: train on the past, validate on the next window, test on the most recent. Also use rolling-origin "
            "evaluation if you want a more robust estimate. Always check leakage: any feature that encodes the future."
        ),
        "is_weak": (
            "Use a random shuffle, ignore time and groups, or compute features on the whole dataset before splitting."
        ),
        "follow_ups": [
            "When would you use k-fold CV instead of a single split?",
            "How do you detect leakage from a single feature?",
            "What if the test set is too small to trust?",
            "How do you refresh splits as the production distribution shifts?",
        ],
        "exercise": (
            "Take a tabular dataset you know. Write down the unit (row, user, session). Choose a split strategy and justify it in two sentences. "
            "Then list two ways leakage could sneak in if you used naive random splitting."
        ),
        "diagram": (
            "flowchart LR\n"
            "    D[Full dataset] --> T[Train]\n"
            "    D --> V[Validation]\n"
            "    D --> Te[Test held out]\n"
            "    T --> M[Fit model]\n"
            "    V --> H[Tune hyperparams]\n"
            "    Te --> F[Final estimate]"
        ),
    },
    "fundamentals/05-overfitting-underfitting-bias-variance.md": {
        "title": "Overfitting, Underfitting, and the Bias-Variance Tradeoff",
        "intuition": (
            "An underfit model misses the pattern (high bias). An overfit model memorizes the training set including its noise (high variance). The art is "
            "finding the sweet spot where the model captures the real structure without chasing noise. You diagnose this from the gap between training error "
            "and validation error: if both are high, you are underfitting; if training error is low but validation error is high, you are overfitting."
        ),
        "formal": (
            "The expected test error of a model can be decomposed as `error = bias^2 + variance + irreducible noise`. **Bias** is how far the average "
            "model is from the truth; high bias means the model is too rigid for the problem (too few parameters, wrong family). **Variance** is how much "
            "the model changes if the training data changes; high variance means the model is too flexible. Regularization, more data, simpler models, and "
            "ensembling all reduce variance. Adding capacity, better features, or better optimization reduces bias."
        ),
        "why": (
            "Bias-variance is the framework that turns vague phrases like the model is too simple into a fix. When you see the train-validation gap, you "
            "know which lever to pull. This is one of the most common interview tests for ML fundamentals because it shows whether you can debug a model, "
            "not just train one."
        ),
        "steps": [
            "Plot training and validation loss as functions of training set size (learning curves) and of model complexity.",
            "If both curves are high and close together: high bias. Increase capacity, add features, train longer.",
            "If training is low and validation is much higher: high variance. Add regularization, get more data, simplify the model, or ensemble.",
            "If both are low and close: you are at the sweet spot. Stop and ship.",
            "If validation gets worse with more data, you have a deeper problem (leakage, distribution shift, label noise).",
        ],
        "example": (
            "A team fits a 100-tree random forest to 1000 rows and gets 100% training accuracy and 65% validation accuracy. That is overfitting. "
            "Solutions: limit tree depth, lower the number of trees, set minimum samples per leaf, or get more data. After tuning, training drops to 80% "
            "and validation rises to 75%. The gap is smaller and the model generalizes better."
        ),
        "mistakes": [
            "Adding capacity to fix overfitting (it makes it worse).",
            "Adding regularization to a model that is already underfitting.",
            "Reading the gap from a small validation set where noise dominates.",
            "Using accuracy on imbalanced data and missing the real bias-variance picture.",
            "Confusing high test error with overfitting when the real cause is leakage or shift.",
        ],
        "iq": "Explain the bias-variance tradeoff and how you would diagnose underfitting versus overfitting in a real model.",
        "is_strong": (
            "Define bias as systematic error from a too-rigid model and variance as sensitivity to the training set. Diagnose by comparing training and "
            "validation error: high both = bias, big gap = variance. Use learning curves to confirm. Fix bias by adding capacity or features; fix variance "
            "with regularization, more data, simpler models, or ensembling."
        ),
        "is_weak": (
            "Recite the formula without describing how to spot the symptom in a real run."
        ),
        "follow_ups": [
            "How does adding more data change the bias-variance picture?",
            "When does early stopping help and when does it just hide the problem?",
            "How is bias-variance related to model capacity and regularization strength?",
            "Why can ensembling reduce variance without much bias cost?",
        ],
        "exercise": (
            "Train any model on a small dataset twice: once with high regularization, once with none. Compare training and validation error. "
            "Write three sentences explaining which run is underfit, which is overfit, and what you would change next."
        ),
        "diagram": (
            "flowchart LR\n"
            "    A[Train error high<br/>Val error high] --> B[Underfitting / High bias]\n"
            "    C[Train error low<br/>Val error high] --> D[Overfitting / High variance]\n"
            "    E[Train error low<br/>Val error low] --> F[Sweet spot]"
        ),
    },
    "fundamentals/06-features-labels-datasets.md": {
        "title": "Features, Labels, and Datasets",
        "intuition": (
            "A dataset is a table where each row is an example. The columns split into features (the inputs the model sees) and labels (the outputs we want "
            "to predict). Good features encode the signal cleanly; good labels reflect the actual decision the system supports. Most ML quality wins come from "
            "fixing features and labels, not from changing models."
        ),
        "formal": (
            "A feature can be numeric (price, age), categorical (country), ordinal (rating tier), text, image, or derived (rolling 7-day average). Labels can "
            "be ground truth (a confirmed fraud chargeback), a proxy (a click on a result), or human judgment. Each label kind brings different noise. "
            "A dataset is a snapshot of the world at a moment, with a schema, a sampling process, and a time range. Knowing the sampling process is what tells "
            "you whether the data covers the cases you care about."
        ),
        "why": (
            "Many production failures are mislabeled features or mismatched labels. A click-as-label optimizes engagement, not satisfaction. A 'fraud' label "
            "that includes only confirmed cases misses the long tail of unconfirmed fraud. Engineers who pause on the dataset definition save weeks of debugging."
        ),
        "steps": [
            "Write the feature schema: name, type, source, freshness, missing-rate.",
            "Write the label schema: source, delay, noise, coverage, who decides.",
            "Plot distributions and missingness for each feature; spot leakage and outliers.",
            "Check the join: are you sure the label belongs to this row?",
            "Decide which features are available at prediction time. Drop ones that leak the future.",
            "Document assumptions where the dataset will fail (new users, new merchants, new languages).",
        ],
        "example": (
            "A churn dataset uses 'cancelled within 30 days' as the label. The team finds that 'time since last login' is a strong feature. But this feature "
            "is computed at the moment of training, after some users already cancelled, so it leaks. They fix it by computing the feature as of the prediction "
            "time. Validation AUC drops from 0.94 to 0.82, which is the real number."
        ),
        "mistakes": [
            "Using post-event information as a feature (leakage).",
            "Treating missing values as zero without labeling missingness.",
            "Optimizing a proxy label that does not match the real decision (clicks vs satisfaction).",
            "Ignoring label noise and reviewer disagreement.",
            "Letting a single column secretly encode the user identity, which destroys generalization.",
        ],
        "iq": "How do you design features and labels for a new ML problem, and what failure modes do you watch for?",
        "is_strong": (
            "Define the user decision first, then choose a label that reflects that decision (not a convenient proxy). Build features that are available at "
            "prediction time, with explicit handling of missing values. Document data sources and freshness. Check leakage by training on shuffled labels "
            "and seeing if performance is too good."
        ),
        "is_weak": (
            "Pick whatever fields are available, treat them as features, and use the most convenient column as the label."
        ),
        "follow_ups": [
            "How would you detect label noise?",
            "What is the difference between a hard label and a soft label?",
            "How would you handle missing values in a high-stakes setting?",
            "When is a proxy label good enough and when is it dangerous?",
        ],
        "exercise": (
            "Pick a problem you understand. Write the feature schema (5+ features with type, source, freshness) and the label schema (source, delay, noise). "
            "Then circle any feature that might leak."
        ),
        "diagram": (
            "flowchart LR\n"
            "    R[Raw events] --> J[Join + filter]\n"
            "    J --> F[Features at prediction time]\n"
            "    J --> L[Labels with delay + noise]\n"
            "    F --> D[Dataset row]\n"
            "    L --> D"
        ),
    },
    "fundamentals/07-models-parameters-hyperparameters.md": {
        "title": "Models, Parameters, and Hyperparameters",
        "intuition": (
            "A model is a function with knobs. The knobs that learning adjusts based on data are parameters. The knobs you set before training are hyperparameters. "
            "Parameters are large in number and learned. Hyperparameters are few but sensitive: they control how learning happens (learning rate, regularization, "
            "tree depth). Wrong hyperparameters can sink a model that is otherwise correct."
        ),
        "formal": (
            "Formally, a model is a parametric family of functions `f_θ(x)`. Training picks `θ` to minimize a loss on the training data. Hyperparameters `λ` "
            "are not optimized by gradient descent but chosen by validation: you train multiple models with different `λ`, pick the one with the best validation "
            "loss, and refit. Common hyperparameters: learning rate, batch size, regularization strength, tree depth, number of layers, dropout rate."
        ),
        "why": (
            "On the job, hyperparameter tuning is half the work. A logistic regression with the wrong regularization can underperform a tuned tree by 10 points. "
            "Engineers who know which knobs matter and how to search efficiently save weeks of training time."
        ),
        "steps": [
            "List the hyperparameters and their plausible ranges (log scale for learning rate, regularization).",
            "Use a fast search first: grid for small spaces, random for medium, Bayesian or population-based for large.",
            "Always evaluate on the validation set, not the training set.",
            "Track each run: hyperparameters, data version, code version, validation metric.",
            "Refit the chosen configuration on train+validation, then evaluate once on the test set.",
        ],
        "example": (
            "A team runs a default XGBoost on a fraud dataset and gets 0.78 AUC. They run 50 random configurations of `max_depth`, `learning_rate`, `subsample`, "
            "`reg_lambda`, and `n_estimators` over 3-fold CV. The best configuration reaches 0.85 AUC. The improvement came not from a new model but from tuning."
        ),
        "mistakes": [
            "Tuning on the test set, then quoting that number as generalization.",
            "Searching too narrow a range and missing the optimum.",
            "Forgetting to fix the random seed or the data version, so runs are not reproducible.",
            "Tuning hyperparameters one at a time when they interact (learning rate and batch size).",
            "Pouring compute into tuning a weak model family instead of trying a stronger one.",
        ],
        "iq": "Explain the difference between parameters and hyperparameters and how you would tune a real model.",
        "is_strong": (
            "Parameters are learned; hyperparameters are configured. Tune by validation, not test. Use random search or Bayesian optimization for big spaces. "
            "Track every run. Refit the best configuration on train+validation before reporting on test."
        ),
        "is_weak": (
            "Treat all knobs as 'parameters', tune on the test set, or rely solely on default values."
        ),
        "follow_ups": [
            "Why is random search often better than grid search?",
            "When would you use Bayesian optimization?",
            "How do you handle hyperparameter tuning when training is expensive?",
            "What is early stopping doing in this picture?",
        ],
        "exercise": (
            "Pick a model you have used. List 5 hyperparameters, give plausible ranges, and rank them by sensitivity. Justify the ranking."
        ),
        "diagram": (
            "flowchart LR\n"
            "    H[Hyperparameters λ] --> Tr[Train: minimize loss over θ]\n"
            "    Tr --> P[Parameters θ]\n"
            "    P --> V[Validate]\n"
            "    V -->|adjust λ| H"
        ),
    },
    "fundamentals/08-loss-functions-and-optimization.md": {
        "title": "Loss Functions and Optimization",
        "intuition": (
            "A loss function tells the model how wrong it is on each example. Optimization is the process that changes the model to make the loss smaller. "
            "Pick the wrong loss and you optimize the wrong thing. Pick the wrong optimizer or learning rate and the model will not train at all. "
            "These two pieces, the loss and the optimizer, decide whether learning works."
        ),
        "formal": (
            "Common losses match common tasks:\n\n"
            "- **Regression:** mean squared error (sensitive to outliers), mean absolute error (robust), Huber (a smooth blend).\n"
            "- **Binary classification:** binary cross-entropy (log loss).\n"
            "- **Multiclass classification:** softmax cross-entropy.\n"
            "- **Ranking and retrieval:** pairwise hinge, listwise NDCG-based, contrastive loss.\n\n"
            "Optimization typically uses gradient descent variants: SGD with momentum, Adam, AdamW. The learning rate schedule, batch size, and weight decay "
            "are the most important knobs. For convex losses there is one global minimum; for deep networks there are many local minima but they are usually "
            "close in quality."
        ),
        "why": (
            "Loss design directly encodes what the system rewards. Cross-entropy for a calibrated classifier, MSE for a regressor that should care equally about "
            "all errors, weighted loss when one class is rarer or more costly. Engineers who match the loss to the cost of mistakes ship better systems than "
            "those who default to whatever the framework picks."
        ),
        "steps": [
            "State the cost of each kind of mistake from the product perspective.",
            "Pick a loss that aligns with that cost (asymmetric loss for asymmetric mistakes).",
            "Pick an optimizer: Adam/AdamW for most deep models, SGD with momentum when stability matters.",
            "Pick a learning rate via warmup and a schedule (cosine, step) when training large models.",
            "Watch the training loss curve: if it plateaus too early, lower the LR or change the schedule.",
            "Compare loss to a real metric on validation: a lower loss should mean a better metric.",
        ],
        "example": (
            "A team trains a fraud classifier with default cross-entropy. The class is 1% positive. The model learns to always predict negative and gets 99% "
            "accuracy with terrible recall. Switching to a class-weighted loss or using focal loss raises recall while keeping precision usable."
        ),
        "mistakes": [
            "Using MSE for a classification problem.",
            "Using accuracy as a loss (it is a metric, not a loss).",
            "Forgetting that the optimizer's default learning rate may be wrong for your model size.",
            "Ignoring the relationship between batch size and effective learning rate.",
            "Optimizing a loss that is far from the metric you actually care about.",
        ],
        "iq": "Walk through choosing a loss and optimizer for a new ML problem.",
        "is_strong": (
            "Start with the cost of mistakes. Map that cost to a differentiable loss. Pick an optimizer that suits the model family (Adam for deep, L-BFGS for "
            "small convex). Choose a learning rate via a short warmup or a learning rate finder. Validate that lower loss really does mean a better business metric."
        ),
        "is_weak": (
            "Default to cross-entropy and Adam without thinking about the cost of errors or the data shape."
        ),
        "follow_ups": [
            "When would you use focal loss or label smoothing?",
            "Why does learning rate often matter more than the optimizer choice?",
            "How does weight decay differ from L2 regularization in Adam vs AdamW?",
            "How do you debug a loss curve that is not decreasing?",
        ],
        "exercise": (
            "Pick a regression and a classification problem. For each, write the loss you would use and one alternative, with one sentence on when the "
            "alternative would be better."
        ),
        "diagram": (
            "flowchart LR\n"
            "    P[Prediction] --> L[Loss vs target]\n"
            "    L --> G[Gradient]\n"
            "    G --> O[Optimizer step]\n"
            "    O --> Pa[Updated parameters]\n"
            "    Pa --> P"
        ),
    },
    "fundamentals/09-generalization.md": {
        "title": "Generalization",
        "intuition": (
            "Generalization is the model's ability to perform on data it has not seen. Memorizing the training set is easy; doing well on new data is the whole "
            "point. Generalization comes from a combination of enough data, the right model capacity, regularization, and a training process that does not just "
            "chase the training loss."
        ),
        "formal": (
            "Statistical learning theory gives a bound on the gap between training error and true error that depends on the model's complexity (VC dimension, "
            "Rademacher complexity) and the size of the training set. In practice the bounds are loose for deep models, so we rely on empirical generalization: "
            "validation and test error. Modern deep learning generalizes despite huge capacity because of implicit regularization from SGD, large data, and "
            "architectural priors."
        ),
        "why": (
            "Every product decision rides on generalization. A model that is great offline and bad in production has a generalization problem, often caused by "
            "distribution shift, leakage, or overfitting. Building generalizable models is the core skill that separates research notebooks from shipped systems."
        ),
        "steps": [
            "Use a held-out test set that you do not touch during development.",
            "Match the validation set to production traffic in time, segment, and source.",
            "Use regularization sized to the data: more regularization for smaller datasets.",
            "Use ensembling to reduce variance when capacity is high and data is limited.",
            "Track production performance over time; generalization can fade as the world drifts.",
        ],
        "example": (
            "A vision team trains an object detector on daytime urban images and evaluates on the same kind of images. It hits 0.9 mAP. Deployed on a customer "
            "with night cameras, it drops to 0.55 mAP. The model generalized within its training distribution but not across it. The fix is to expand the "
            "training data to cover the deployment distribution and to monitor performance per camera and per time of day."
        ),
        "mistakes": [
            "Confusing low validation error with generalization to a different domain.",
            "Repeatedly tuning on the test set, which silently destroys the generalization estimate.",
            "Ignoring how production data differs from training data.",
            "Treating dataset size as the only fix for generalization (often features and labels matter more).",
            "Reporting one number instead of slicing by segment or time.",
        ],
        "iq": "How do you build models that generalize, and how do you detect when generalization is failing?",
        "is_strong": (
            "Build models with regularization and validation that mirrors production. Detect failure by slicing performance by segment, time, and source, and by "
            "monitoring drift in production. When generalization fails, look at distribution shift, leakage, and label drift before changing the model."
        ),
        "is_weak": (
            "Equate low test loss with generalization or assume more parameters always generalize better."
        ),
        "follow_ups": [
            "Why do deep networks generalize despite huge capacity?",
            "How does data augmentation help generalization?",
            "What is the difference between covariate shift and concept drift?",
            "How do you decide the size of the test set?",
        ],
        "exercise": (
            "Pick a model you trained. Identify three ways production data could differ from training data and which one you can monitor in production."
        ),
        "diagram": (
            "flowchart LR\n"
            "    Tr[Training distribution] --> M[Model]\n"
            "    M --> Vp[Performance on val]\n"
            "    Pr[Production distribution] --> M\n"
            "    M --> Pp[Performance in prod]\n"
            "    Vp -. should match .-> Pp"
        ),
    },
    "fundamentals/10-end-to-end-ml-workflow.md": {
        "title": "End-to-End ML Workflow",
        "intuition": (
            "An ML project is more than a model. It is framing, data, baselines, training, evaluation, deployment, monitoring, and iteration. The model itself "
            "is often the smallest piece. A solid end-to-end workflow is what separates a notebook from a system."
        ),
        "formal": (
            "A reasonable workflow:\n\n"
            "1. **Frame.** User, decision, cost of mistakes, constraints, success metric.\n"
            "2. **Data.** Source, schema, freshness, splits, labels, leakage check.\n"
            "3. **Baseline.** Rule or simple model that sets the bar.\n"
            "4. **Model.** Try a few candidates, tune, evaluate honestly.\n"
            "5. **Evaluate.** Metrics, slices, error analysis, calibration, robustness.\n"
            "6. **Deploy.** Shadow mode, then canary, then A/B test with rollback ready.\n"
            "7. **Monitor.** Inputs, outputs, latency, cost, business outcomes.\n"
            "8. **Iterate.** Feed errors back into data, features, or model.\n"
        ),
        "why": (
            "Senior engineers are paid for steps 1, 2, 5, 6, 7, 8. The model code is often the easy part. Whoever can drive the full loop is who ships value. "
            "Interviewers ask about the workflow to test whether you understand that ML is a system."
        ),
        "steps": [
            "Write a one-pager with the user, decision, data, baseline, metric, and risks.",
            "Build a baseline before any modeling. Lock its number.",
            "Iterate on a small model and a tiny dataset to debug fast.",
            "Scale up only when the small experiment beats the baseline.",
            "Plan deployment from day one: monitoring, fallback, rollback.",
            "Set up a feedback loop so production errors flow back into training data.",
        ],
        "example": (
            "A team building a search ranker spends one week framing, three weeks on data and labels, two weeks on a baseline (BM25), three weeks on a learned "
            "ranker, two weeks on evaluation and slicing, and two weeks on deployment with shadow + A/B. The model code is two hundred lines. The data, "
            "evaluation, and deployment code is many thousands. That ratio is normal."
        ),
        "mistakes": [
            "Skipping framing and jumping into code.",
            "Building no baseline, so improvements have nothing to compare against.",
            "Treating deployment as an afterthought.",
            "No monitoring, so silent regressions go undetected.",
            "No feedback loop, so the system never improves after launch.",
        ],
        "iq": "Walk me through how you would build an ML system end to end for a problem of your choice.",
        "is_strong": (
            "Pick a concrete problem. Walk through framing, data, baseline, modeling, evaluation, deployment, and monitoring. Mention the cost of errors, the "
            "metric, and the rollback plan. Keep the model story short and the system story long."
        ),
        "is_weak": (
            "Spend the whole answer on model architecture and ignore data, evaluation, and deployment."
        ),
        "follow_ups": [
            "What would the rollback plan look like?",
            "How would you evaluate before going live?",
            "What signals would tell you the model is degrading in production?",
            "Where would you instrument the system to debug a bad output?",
        ],
        "exercise": (
            "Pick a project you would build. Write a one-page workflow with all eight steps. Highlight which step is riskiest and how you would de-risk it."
        ),
        "diagram": (
            "flowchart LR\n"
            "    F[Frame] --> D[Data]\n"
            "    D --> B[Baseline]\n"
            "    B --> M[Model]\n"
            "    M --> E[Evaluate]\n"
            "    E --> Dp[Deploy]\n"
            "    Dp --> Mo[Monitor]\n"
            "    Mo --> F"
        ),
    },
}
