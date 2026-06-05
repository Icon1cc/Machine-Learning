"""Topic-specific content for math/, statistics/, and classical-ml/."""

CONTENT = {
    # ============================================================
    # MATH (12 files)
    # ============================================================
    "math/01-why-math-matters-for-ml.md": {
        "title": "Why Math Matters for ML",
        "intuition": (
            "You can use ML libraries without deep math, but you cannot debug them or design new methods without it. "
            "Three branches do almost all the work: linear algebra moves data through models (a layer is a matrix multiply), "
            "calculus tells you which way to nudge parameters to reduce error (the gradient), and probability lets you reason about "
            "uncertainty and write losses as likelihoods."
        ),
        "formal": (
            "The minimum useful math for ML practice covers vectors and matrices, eigen-decomposition, partial derivatives and the chain "
            "rule, gradient descent, basic probability, expectation, common distributions (Gaussian, Bernoulli, multinomial), Bayes' rule, "
            "and information-theoretic quantities (entropy, cross-entropy, KL divergence). You do not need every proof, but you should know "
            "what each tool computes and when it applies."
        ),
        "why": (
            "When a model fails, math tells you why. A loss that does not decrease points to a vanishing gradient or wrong learning rate. "
            "A retrieval system with bad recall points to a distance metric that does not match how embeddings were trained. A regression that "
            "cannot extrapolate points to a basis that is too narrow. Engineers who know the math diagnose these in minutes."
        ),
        "steps": [
            "Read code with math in mind: spot the matrix shapes, the loss, the gradient flow.",
            "When a model misbehaves, write the equation for what it should be doing and compare.",
            "Use small numerical experiments to confirm your math intuition before scaling up.",
            "Keep a one-page cheat sheet for the formulas you re-derive most often.",
        ],
        "example": (
            "A team's deep model trains fine on small data but loss explodes on full data. Doing the math, batch norm statistics differ between "
            "modes; gradients through the normalization explode at high LR. The fix is gradient clipping plus warmup. Without the math nobody "
            "would know which knob to turn."
        ),
        "mistakes": [
            "Treating ML as plug-and-play; you cannot debug what you cannot describe with math.",
            "Memorizing formulas without intuition for what each piece does.",
            "Skipping linear algebra in favor of code, then getting stuck on shape mismatches.",
            "Avoiding probability and so writing classification metrics that do not handle calibration.",
        ],
        "iq": "Which areas of math do you actually use day to day in ML, and where has math helped you debug a real problem?",
        "is_strong": (
            "Name linear algebra (shapes, projections, decompositions), calculus (gradients, chain rule), and probability (likelihoods, Bayes). "
            "Give one debugging story: a vanishing gradient, a metric mismatch, an embedding similarity issue, a calibration fix."
        ),
        "is_weak": (
            "Claim the libraries handle the math, with no example of using math to debug or design."
        ),
        "follow_ups": [
            "What is the gradient of softmax cross-entropy with respect to logits?",
            "Why does cosine similarity behave differently from dot product on normalized vectors?",
            "What does the Hessian tell you that the gradient does not?",
            "Why is KL divergence asymmetric and what does that imply?",
        ],
        "exercise": (
            "Take a recent training failure or weird metric. Write down in math what should be happening and where the actual run diverges. "
            "If you cannot, that is the gap to close."
        ),
        "diagram": (
            "flowchart LR\n"
            "    LA[Linear algebra] --> M[Model forward pass]\n"
            "    C[Calculus] --> Bp[Backprop and gradients]\n"
            "    P[Probability] --> L[Loss + uncertainty]\n"
            "    M --> R[Predictions]\n"
            "    Bp --> R\n"
            "    L --> R"
        ),
    },
    "math/02-linear-algebra-vectors.md": {
        "title": "Linear Algebra: Vectors",
        "intuition": (
            "A vector is an arrow with a length and a direction; in ML, it is also a list of numbers that represents an example, a feature, "
            "or a hidden state. Operations on vectors (add, scale, dot product) are how models combine information. If you can picture two "
            "vectors and their angle, you can picture most of what early ML layers do."
        ),
        "formal": (
            "A vector in `R^n` is an n-tuple of real numbers. Key operations: addition (`u + v`), scalar multiplication (`αv`), dot product "
            "(`u · v = Σ u_i v_i`), L2 norm (`||v||₂ = sqrt(v · v)`), cosine similarity (`u · v / (||u|| ||v||)`). The dot product equals "
            "`||u|| ||v|| cos θ`, so it measures alignment. Normalization (`v / ||v||`) puts vectors on the unit sphere, which is what most "
            "embedding models do before similarity search."
        ),
        "why": (
            "Embeddings are vectors. Tokens are vectors. Hidden layers are vectors. Searching by meaning is dot product or cosine on vectors. "
            "Almost every modern ML system reduces to: turn things into vectors, compare them, combine them, transform them. You cannot "
            "reason about embedding quality, retrieval, or attention without the vector picture."
        ),
        "steps": [
            "Confirm the dimension and norm of vectors you handle.",
            "Decide whether to use dot product, cosine, or Euclidean (match how the model was trained).",
            "Normalize when comparing direction, not magnitude.",
            "Use orthogonality to think about independence: orthogonal directions carry independent information.",
            "Visualize in 2D or 3D first; the intuition usually transfers to higher dimensions.",
        ],
        "example": (
            "A retrieval system stores 1024-dim embeddings of documents. A query is encoded into the same space. Top-k is found by largest "
            "dot product. Recall drops on long documents because the embedding norm grows with length and biases the score. Normalizing both "
            "query and documents (cosine similarity) fixes the bias and improves recall."
        ),
        "mistakes": [
            "Using Euclidean distance when the embedding model was trained for cosine.",
            "Forgetting to normalize when length should not matter.",
            "Confusing the dot product (a scalar) with element-wise multiplication.",
            "Treating vectors of different dimensions as comparable.",
            "Ignoring that high dimensions distort distances (curse of dimensionality).",
        ],
        "iq": "Explain dot product, cosine similarity, and L2 distance, and when you would use each.",
        "is_strong": (
            "Dot product captures alignment scaled by lengths. Cosine ignores lengths and measures direction. L2 measures geometric distance. "
            "Use cosine when length is meaningless (text embeddings); dot product when training defined it; L2 when geometric distance is "
            "meaningful (image features in some setups)."
        ),
        "is_weak": (
            "Treat them as interchangeable or quote definitions without saying when to pick which."
        ),
        "follow_ups": [
            "Why do high-dimensional random vectors tend to be near orthogonal?",
            "What is the relationship between cosine similarity and L2 on normalized vectors?",
            "How would you index vectors for fast nearest-neighbor search at scale?",
            "Why is dot product faster than cosine in practice for normalized vectors?",
        ],
        "exercise": (
            "Take 5 random unit vectors in 2D. Compute dot products. Repeat in 100D using random sampling. Note how often the dot product is "
            "close to zero in 100D and explain why."
        ),
        "diagram": (
            "flowchart LR\n"
            "    A[Item to compare] --> E1[Encode to vector]\n"
            "    B[Query] --> E2[Encode to vector]\n"
            "    E1 --> S[Similarity: dot, cosine, or L2]\n"
            "    E2 --> S\n"
            "    S --> R[Rank top-k]"
        ),
    },
    "math/03-matrices-and-matrix-multiplication.md": {
        "title": "Matrices and Matrix Multiplication",
        "intuition": (
            "A matrix is a stack of vectors arranged in a grid. Multiplying a matrix by a vector applies a linear transformation: rotate, scale, "
            "project, or mix. A neural network layer is exactly this operation followed by a non-linearity. If you can read shapes and trace "
            "where each row and column goes, you can read most ML code."
        ),
        "formal": (
            "If `A` is `m x n` and `B` is `n x p`, then `C = A B` is `m x p` with `C[i,j] = Σ_k A[i,k] B[k,j]`. Cost is roughly `m n p`. "
            "Matrix multiplication is associative but not commutative. Special matrices: identity `I`, diagonal `D`, orthogonal (`Q^T Q = I`), "
            "symmetric (`A = A^T`), positive definite. Transpose flips rows and columns. The inverse `A^{-1}` exists only for square non-singular matrices."
        ),
        "why": (
            "Every dense layer, attention head, and embedding lookup is a matrix multiplication. Optimized matmul on GPUs is what makes deep learning "
            "practical. Reading shapes and choosing batch dimensions decide whether your model fits in memory and how fast it runs."
        ),
        "steps": [
            "Always check the shape sequence in a forward pass: `(B, T, d) @ (d, h) -> (B, T, h)`.",
            "Pick the batch dimension that maximizes GPU utilization without OOM.",
            "Use einsum or einops for clarity when shapes get hairy.",
            "Watch for transposes; a single missing `.T` wrecks accuracy and you may not notice.",
            "Profile matmul time: it usually dominates training and inference.",
        ],
        "example": (
            "Attention does `Q K^T` (scores) then `softmax(scores) V`. With sequence length `T` and head dim `d`, the cost is `O(T^2 d)`. "
            "Doubling sequence quadruples compute. Engineers who track these shapes know exactly why long context is expensive and where "
            "tricks like flash attention save time."
        ),
        "mistakes": [
            "Confusing element-wise multiply with matrix multiply.",
            "Wrong order in chained multiplications: `A B != B A` in general.",
            "Forgetting that batch dim is implicit; broadcasting hides shape errors.",
            "Computing `A^T A` when `A A^T` is what you needed (different shapes, different meaning).",
            "Storing dense matrices that should be sparse or factored.",
        ],
        "iq": "Walk through the shapes of a transformer attention block.",
        "is_strong": (
            "`X` is `(B, T, d)`. Three projections produce `Q, K, V` each `(B, T, h, d_h)`. Scores are `Q K^T / sqrt(d_h)` of shape `(B, h, T, T)`. "
            "Softmax over last axis, then `attn @ V` gives `(B, T, h, d_h)`, reshaped back to `(B, T, d)`. A residual and feed-forward follow. "
            "Cost is `O(T^2 d)`; that quadratic is why context length is expensive."
        ),
        "is_weak": (
            "Hand-wave the shapes or skip the `T^2` cost discussion."
        ),
        "follow_ups": [
            "How does flash attention reduce memory cost?",
            "Why do we divide by `sqrt(d_k)` in attention?",
            "What is the cost difference between dense and low-rank matrix multiply?",
            "Why are GPUs much faster than CPUs at matmul?",
        ],
        "exercise": (
            "Pick any transformer layer. Trace shapes for batch 8, sequence 1024, hidden 768, 12 heads. Estimate FLOPs for one forward pass."
        ),
        "diagram": (
            "flowchart LR\n"
            "    X[X: B x T x d] --> Q[X Wq]\n"
            "    X --> K[X Wk]\n"
            "    X --> V[X Wv]\n"
            "    Q --> S[Q K^T / sqrt d]\n"
            "    K --> S\n"
            "    S --> P[softmax]\n"
            "    P --> O[P V]\n"
            "    V --> O"
        ),
    },
    "math/04-dot-products-projections-and-similarity.md": {
        "title": "Dot Products, Projections, and Similarity",
        "intuition": (
            "The dot product measures how much two vectors point in the same direction, weighted by their lengths. Project a vector onto another "
            "and you keep only the component aligned with that direction. Similarity scores in ML are almost always built from this idea: "
            "alignment in some learned vector space."
        ),
        "formal": (
            "`u · v = Σ u_i v_i = ||u|| ||v|| cos θ`. The projection of `v` onto `u` is `(v · u / u · u) u`. Cosine similarity is `u · v / (||u|| ||v||)`. "
            "On normalized vectors, dot product equals cosine. The dot product is linear in each argument, which is why it composes well with linear models."
        ),
        "why": (
            "Retrieval, attention, recommender scoring, and contrastive losses are all dot products in disguise. Whether to normalize, what dimension "
            "to use, and whether to scale by `sqrt(d)` change quality and stability. These are not exotic choices; they show up in every embedding system."
        ),
        "steps": [
            "Normalize when length should not matter.",
            "Scale by `sqrt(d)` when dimensions differ to keep variance comparable.",
            "Use dot product (faster) when vectors are already normalized.",
            "Project to remove a direction you do not want (debiasing embeddings).",
            "Confirm the metric matches how the model was trained.",
        ],
        "example": (
            "An image embedding model returns 512-dim vectors with average norm 5. A new model trained with cosine has unit norms. Mixing them "
            "in one index without re-normalizing produces wildly biased scores. Re-encoding everything with the same normalization fixes recall."
        ),
        "mistakes": [
            "Forgetting that dot product favors longer vectors when lengths vary.",
            "Comparing vectors from different models without sanity-checking norms.",
            "Computing cosine on already-normalized vectors and paying for the extra divisions.",
            "Using projection without checking the projector is unit-norm.",
        ],
        "iq": "Why might a retrieval system using dot product perform worse than one using cosine on the same embeddings?",
        "is_strong": (
            "Dot product is sensitive to vector length. If embedding norm correlates with frequency or length, longer items dominate. Cosine removes "
            "length and ranks by direction. The fix is to normalize, or to switch to cosine. Either way, match the metric the model was trained for."
        ),
        "is_weak": (
            "Claim they are always equivalent."
        ),
        "follow_ups": [
            "When is dot product preferred to cosine for performance?",
            "How do you debias an embedding by projecting out a direction?",
            "What does Cauchy-Schwarz tell you about dot products?",
            "Why do attention scores divide by `sqrt(d_k)`?",
        ],
        "exercise": (
            "Take 100 random vectors with varying norms. Rank them by dot product to a query and by cosine. Show the top-10 lists differ and explain why."
        ),
        "diagram": (
            "flowchart LR\n"
            "    U[u] --> D[u . v]\n"
            "    V[v] --> D\n"
            "    D --> S{Lengths matter?}\n"
            "    S -- No --> Cos[Normalize then dot = cosine]\n"
            "    S -- Yes --> Dot[Use raw dot product]"
        ),
    },
    "math/05-eigenvalues-eigenvectors-and-pca-intuition.md": {
        "title": "Eigenvalues, Eigenvectors, and the Intuition Behind PCA",
        "intuition": (
            "An eigenvector of a matrix is a direction that does not get rotated by the matrix; only stretched. The stretch factor is the eigenvalue. "
            "PCA finds the directions in which data varies most. Those are the eigenvectors of the covariance matrix, and the variance along each is "
            "the eigenvalue. Compressing a dataset to its top eigenvectors keeps the information you care about with fewer dimensions."
        ),
        "formal": (
            "If `A v = λ v` for nonzero `v`, then `v` is an eigenvector of `A` with eigenvalue `λ`. For a real symmetric matrix (like a covariance matrix), "
            "eigenvectors are orthogonal and eigenvalues are real. PCA centers data, computes covariance `Σ = X^T X / n`, and decomposes it. The principal "
            "components are the eigenvectors sorted by eigenvalue. Equivalently, SVD of the centered data matrix gives the same components."
        ),
        "why": (
            "PCA is the simplest, fastest dimensionality reduction. It is used to visualize, denoise, compress, decorrelate features, and as a starting "
            "point before training. Eigen-decomposition also underlies spectral clustering, PageRank, and many graph methods. It is one of the most "
            "transferable mental models in math for ML."
        ),
        "steps": [
            "Center the data (subtract the mean per feature).",
            "Compute the covariance matrix (or SVD on the centered data).",
            "Sort eigenvalues from largest to smallest.",
            "Keep the top k components that explain enough variance (often 90 or 95 percent).",
            "Project data onto those components for the reduced representation.",
        ],
        "example": (
            "A model has 200 highly correlated features. Training is slow and unstable. Running PCA reveals 95 percent of variance in the top 30 "
            "components. Training on those is faster, more stable, and only loses a tiny fraction of accuracy. Storage and inference also drop."
        ),
        "mistakes": [
            "Forgetting to center the data; PCA without centering captures the mean direction.",
            "Using PCA on highly nonlinear structure (consider kernel PCA or autoencoders).",
            "Treating principal components as interpretable features without checking.",
            "Applying PCA before splitting train/validation, leaking statistics.",
            "Keeping too few components and losing important variance.",
        ],
        "iq": "Explain PCA in terms of eigenvalues and how you would choose the number of components.",
        "is_strong": (
            "PCA finds orthogonal directions that maximize variance. They are the top eigenvectors of the (centered) covariance matrix. Pick `k` by "
            "the cumulative explained variance, e.g. 90 or 95 percent, or by an elbow in the variance curve. Always fit PCA on training data only and "
            "apply it to validation."
        ),
        "is_weak": (
            "Confuse PCA with feature selection or apply it without centering."
        ),
        "follow_ups": [
            "When is PCA a bad fit?",
            "How does SVD relate to eigen-decomposition?",
            "What is whitening and when do you want it?",
            "How does kernel PCA differ from PCA?",
        ],
        "exercise": (
            "Take a tabular dataset. Run PCA, plot the cumulative explained variance, pick the elbow, and report how much variance the top components "
            "capture. Then train any model on the reduced set and compare to the full features."
        ),
        "diagram": (
            "flowchart LR\n"
            "    X[Centered data X] --> C[Covariance Σ]\n"
            "    C --> E[Eigen-decompose]\n"
            "    E --> V[Top-k eigenvectors]\n"
            "    X --> P[Project to V]\n"
            "    V --> P\n"
            "    P --> R[Reduced representation]"
        ),
    },
    "math/06-calculus-derivatives.md": {
        "title": "Calculus and Derivatives",
        "intuition": (
            "A derivative tells you how a function changes when you nudge its input a little. In ML, that nudge is a small change to a parameter, and "
            "the function is the loss. If the derivative is positive, raising the parameter raises the loss; you should lower it. Gradient descent is "
            "this idea, repeated."
        ),
        "formal": (
            "For `f: R -> R`, the derivative is `f'(x) = lim h->0 (f(x+h) - f(x)) / h`. It is the slope of the tangent line. For composite functions, "
            "the chain rule gives `(f ∘ g)'(x) = f'(g(x)) g'(x)`. Common derivatives: `(x^n)' = n x^{n-1}`, `(e^x)' = e^x`, `(log x)' = 1/x`, "
            "`(sin x)' = cos x`. The second derivative tells you about curvature: positive means convex, negative means concave."
        ),
        "why": (
            "Every learning algorithm uses derivatives, directly or through autograd. Understanding them lets you read training logs, design custom "
            "losses, and reason about why a particular step blows up or stalls. The chain rule is the spine of backpropagation."
        ),
        "steps": [
            "Identify the function whose value you want to minimize (the loss).",
            "Compute or autograd the derivative with respect to each parameter.",
            "Move each parameter in the direction that lowers the loss.",
            "Pick a step size small enough not to overshoot.",
            "Watch the loss curve to confirm you are decreasing.",
        ],
        "example": (
            "Linear regression with squared error has a closed-form solution because its loss is a quadratic with a derivative we can solve directly. "
            "Logistic regression has no closed form because its derivative is nonlinear in parameters. Both use the same idea: set the derivative to "
            "zero or follow it down."
        ),
        "mistakes": [
            "Confusing the gradient (a vector) with a single derivative.",
            "Forgetting the chain rule when composing functions.",
            "Trusting numerical derivatives without checking step size.",
            "Computing gradients by hand for a function autograd already handles.",
        ],
        "iq": "Derive the gradient of the binary cross-entropy loss with respect to the logits.",
        "is_strong": (
            "With logit `z`, prediction `p = σ(z)`, label `y in {0,1}`, the loss is `-y log p - (1-y) log(1-p)`. Using `dσ/dz = σ(1-σ)`, the gradient "
            "simplifies to `p - y`. That clean form is why logistic regression and softmax classification have such simple gradient updates."
        ),
        "is_weak": (
            "Confuse cross-entropy with squared error or skip the chain rule."
        ),
        "follow_ups": [
            "What does the second derivative tell you about convergence?",
            "What happens at points where the derivative is zero?",
            "How is automatic differentiation different from numerical differentiation?",
            "Why do ReLU networks have non-differentiable points and is that a problem?",
        ],
        "exercise": (
            "Pick any loss function in your code. Compute its derivative by hand for one parameter. Compare to what autograd produces."
        ),
        "diagram": (
            "flowchart LR\n"
            "    L[Loss L] --> D[Derivative dL/dθ]\n"
            "    D --> S[Step: θ <- θ - α dL/dθ]\n"
            "    S --> L"
        ),
    },
    "math/07-gradients-and-partial-derivatives.md": {
        "title": "Gradients and Partial Derivatives",
        "intuition": (
            "When the input is a vector (every parameter in your model is one slot of a big vector), the derivative becomes a vector too: the gradient. "
            "The gradient points in the direction of steepest increase. Stepping in the opposite direction is gradient descent, the workhorse of ML training."
        ),
        "formal": (
            "For `f: R^n -> R`, the partial derivative `∂f/∂x_i` measures change in `f` when only `x_i` moves. The gradient `∇f = (∂f/∂x_1, ..., ∂f/∂x_n)` "
            "stacks them into a vector. The directional derivative in unit direction `u` is `∇f · u`, maximized when `u = ∇f / ||∇f||`. "
            "For matrix-valued parameters, gradients are matrices of the same shape."
        ),
        "why": (
            "Every backward pass is a gradient. Training stability, learning rate choice, and gradient clipping all depend on gradient magnitude. "
            "Vanishing or exploding gradients explain a huge fraction of training failures in deep learning."
        ),
        "steps": [
            "Confirm the loss is a scalar; gradients are taken with respect to it.",
            "Use autograd to compute gradients for each parameter.",
            "Inspect gradient norms across layers; large or zero norms point to problems.",
            "Clip gradients when norms blow up.",
            "Scale the learning rate to gradient magnitude (LR finder, warmup).",
        ],
        "example": (
            "An RNN training run shows training loss not decreasing. Plotting gradient norms shows the deepest time-step gradients are near zero: "
            "vanishing gradient. Switching to LSTM with gating, or to a transformer, fixes the problem because both let gradient flow more directly."
        ),
        "mistakes": [
            "Computing the gradient of the wrong scalar (e.g., sum vs mean changes scale).",
            "Not zeroing gradients between batches (PyTorch accumulates by default).",
            "Confusing parameter gradients with input gradients.",
            "Ignoring gradient norm when debugging training failures.",
            "Forgetting that some operations are non-differentiable; you may need a surrogate.",
        ],
        "iq": "What is the gradient and how would you debug a model that has training loss not decreasing?",
        "is_strong": (
            "The gradient is the vector of partial derivatives of the loss with respect to each parameter. To debug a stuck loss, check learning rate, "
            "gradient norms, layer-by-layer activations, and whether gradients flow back through every layer. Look for vanishing or exploding gradients, "
            "wrong loss formulation, or data issues."
        ),
        "is_weak": (
            "Just lower the learning rate without checking the symptoms."
        ),
        "follow_ups": [
            "What is gradient clipping and when do you use it?",
            "Why does ReLU help with vanishing gradients?",
            "How is the Jacobian related to the gradient?",
            "What is the gradient with respect to the input used for?",
        ],
        "exercise": (
            "Train any deep model and log gradient norms per layer. Identify which layer has the smallest norm and explain why."
        ),
        "diagram": (
            "flowchart LR\n"
            "    L[Scalar loss] --> G[Gradient ∇L]\n"
            "    G --> N[Per-layer norm]\n"
            "    N --> C{Vanishing?<br/>Exploding?}\n"
            "    C -- Yes --> F[Fix: arch, init, clip, LR]\n"
            "    C -- No --> S[Step]"
        ),
    },
    "math/08-chain-rule-and-backpropagation-intuition.md": {
        "title": "Chain Rule and the Intuition Behind Backpropagation",
        "intuition": (
            "Backpropagation is the chain rule applied to a computational graph. Each operation in the forward pass has a known local derivative; "
            "the backward pass multiplies these together from the loss back to each parameter. You do not need to derive the whole gradient by hand; "
            "you just need to know the local derivative of each piece and let the chain rule combine them."
        ),
        "formal": (
            "For composed functions `y = f(g(x))`, `dy/dx = f'(g(x)) g'(x)`. For computational graphs, each node has a local Jacobian; the gradient with "
            "respect to any input is the product of local Jacobians along the path from output to input, summed over all paths. Reverse-mode automatic "
            "differentiation computes this in time roughly equal to the forward pass, which is why deep networks are trainable."
        ),
        "why": (
            "Every modern model trains by backprop. Knowing how it works tells you why some architectures train easily (residuals keep gradients alive), "
            "why others fail (long product chains lose signal), and what to change when training stalls."
        ),
        "steps": [
            "Trace the computational graph from inputs and parameters to the loss.",
            "For each op, know the local derivative (autograd handles standard ones).",
            "Compute the loss in the forward pass.",
            "Run the backward pass, multiplying local derivatives along edges.",
            "Aggregate gradients at parameters and step.",
        ],
        "example": (
            "A residual block computes `y = x + f(x)`. The gradient flowing back is `dy/dx = I + df/dx`. The identity term ensures gradient does not "
            "vanish even if `df/dx` is small. That is why ResNets train deeper than plain stacks."
        ),
        "mistakes": [
            "Believing autograd is magic; it is just the chain rule applied carefully.",
            "Forgetting that any non-differentiable op breaks the chain at that point.",
            "Computing gradients through a detached tensor and getting zeros.",
            "Implementing custom ops without testing the backward against numerical gradients.",
        ],
        "iq": "Explain how backpropagation works and why residual connections help with deep networks.",
        "is_strong": (
            "Backprop applies the chain rule on the computational graph: each node has a local derivative, and gradients of inputs are products of local "
            "derivatives along paths to the output. Residual connections add an identity path, so the gradient has an `I + ...` form. The identity keeps "
            "the gradient from vanishing even if the rest is small, which lets very deep networks train."
        ),
        "is_weak": (
            "Recite that backprop computes gradients without explaining how."
        ),
        "follow_ups": [
            "What is reverse-mode versus forward-mode autodiff?",
            "Why is checkpointing useful for memory in long backward passes?",
            "How does layer normalization help gradient flow?",
            "What happens if a non-differentiable op (argmax) sits in the middle of the graph?",
        ],
        "exercise": (
            "Pick a small two-layer MLP. Derive the gradient of the loss with respect to the first layer weight by hand. Confirm it matches autograd."
        ),
        "diagram": (
            "flowchart RL\n"
            "    L[Loss] --> D1[dL/dz3]\n"
            "    D1 --> D2[dL/dz2 via chain rule]\n"
            "    D2 --> D3[dL/dz1]\n"
            "    D3 --> P[Parameter gradients]"
        ),
    },
    "math/09-optimization-gradient-descent.md": {
        "title": "Optimization and Gradient Descent",
        "intuition": (
            "Gradient descent is a simple loop: compute the gradient of the loss, take a small step in the opposite direction, repeat. The size of the "
            "step (learning rate) is the most important knob. Too small and you wait forever; too large and you bounce around or diverge."
        ),
        "formal": (
            "Update rule: `θ_{t+1} = θ_t - α ∇L(θ_t)`. Stochastic variants estimate `∇L` from minibatches. Momentum accumulates a velocity "
            "(`v_{t+1} = μ v_t + ∇L`, then `θ <- θ - α v`) to dampen oscillations. Adam scales each parameter by an estimate of the gradient's "
            "second moment, giving an effective adaptive learning rate per parameter. AdamW decouples weight decay from the adaptive update."
        ),
        "why": (
            "Optimization choice affects whether training converges, how fast, and how well. The learning rate, schedule, batch size, optimizer, and "
            "weight decay are levers an engineer must understand. The default is rarely optimal; the LR especially needs care."
        ),
        "steps": [
            "Pick the optimizer that fits the model (Adam/AdamW for deep, SGD for some convex or large-batch regimes).",
            "Find a learning rate (LR finder, warmup-then-decay schedules).",
            "Tune weight decay separately from L2.",
            "Watch the loss curve and gradient norms; adjust LR or schedule based on what you see.",
            "Use early stopping to avoid wasting compute and overfitting.",
        ],
        "example": (
            "A team trains a transformer with Adam at LR 1e-3 and the loss explodes. Lowering to 1e-4 with linear warmup over 1000 steps and cosine decay "
            "trains stably. The model architecture did not change; only the optimizer schedule did."
        ),
        "mistakes": [
            "Using a single LR for the whole training without warmup.",
            "Treating Adam as 'best by default' without reasoning about generalization or memory.",
            "Forgetting that batch size and LR interact (large batch usually wants higher LR).",
            "Not clipping gradients in models prone to spikes (RNNs, transformers without normalization).",
            "Confusing decreasing training loss with successful learning when validation is flat.",
        ],
        "iq": "Compare SGD, Adam, and AdamW and when you would pick each.",
        "is_strong": (
            "SGD with momentum is simple and often generalizes well, but is sensitive to LR and batch size. Adam adapts per-parameter LR via gradient "
            "second moments and trains fast, sometimes generalizing slightly worse. AdamW separates weight decay from the adaptive update and tends to "
            "be the strongest default for transformers. Pick by training stability and what generalizes best on validation."
        ),
        "is_weak": (
            "Default to Adam without comment, or claim one optimizer dominates always."
        ),
        "follow_ups": [
            "Why does Adam sometimes generalize worse than SGD?",
            "What is a learning rate schedule and why do warmup + cosine decay help?",
            "What is gradient accumulation and when do you need it?",
            "What is the relationship between batch size, LR, and training noise?",
        ],
        "exercise": (
            "Train a small model with three different LRs (1e-2, 1e-3, 1e-4). Plot training and validation loss. Identify which LR is too high, too low, "
            "and good, and explain why."
        ),
        "diagram": (
            "flowchart LR\n"
            "    G[Gradient] --> O[Optimizer state]\n"
            "    O --> Up[Update θ <- θ - α step]\n"
            "    Up --> N[New parameters]\n"
            "    N --> G"
        ),
    },
    "math/10-convex-vs-non-convex-optimization.md": {
        "title": "Convex vs Non-Convex Optimization",
        "intuition": (
            "A convex loss surface is a bowl: any local minimum is the global minimum. A non-convex surface has hills, valleys, and saddle points; "
            "different starts lead to different solutions. Linear and logistic regression are convex; neural networks are not. Knowing which regime you "
            "are in changes how you optimize and how you trust the result."
        ),
        "formal": (
            "A function is convex if its second derivative (Hessian) is positive semi-definite everywhere. Convex problems have a unique minimum; "
            "first-order methods provably converge. Non-convex problems can have many minima, saddle points, and flat regions. Deep network losses are "
            "non-convex but in practice SGD finds solutions that generalize well, partly because of implicit regularization."
        ),
        "why": (
            "If the problem is convex, you can guarantee convergence and trust the solution. If non-convex, you must rely on multiple seeds, careful "
            "initialization, and good heuristics. This affects how you scope projects, how you debug, and how confident you can be in 'best' models."
        ),
        "steps": [
            "Check whether your loss is convex (linear/logistic regression with convex loss is yes; neural nets are no).",
            "If convex, use deterministic optimizers (L-BFGS) on small data, SGD on large.",
            "If non-convex, use SGD/Adam, multiple seeds, and good initialization (Xavier, He).",
            "For non-convex, evaluate by validation and treat the optimum as approximate.",
            "Use techniques like batch norm and residuals to smooth the loss landscape.",
        ],
        "example": (
            "Two teams train the same neural network with different random seeds and get models with the same training loss but very different predictions "
            "on hard cases. That is non-convexity in action. Ensembling reduces variance from this; reporting only one seed hides it."
        ),
        "mistakes": [
            "Trusting a single non-convex run as the 'best' model.",
            "Using convex optimization theory to reason about deep network training.",
            "Confusing convergence to a local minimum with finding the truth.",
            "Forgetting that initialization strongly biases where non-convex training lands.",
        ],
        "iq": "Why can deep networks train despite being non-convex, and what does that mean for reproducibility?",
        "is_strong": (
            "Despite the loss being non-convex, SGD finds solutions that generalize because of architectural choices (residuals, normalization), data scale, "
            "and implicit regularization from noisy gradients. For reproducibility, fix random seeds, data shuffling, and library versions, and report "
            "results across multiple seeds because two runs may differ."
        ),
        "is_weak": (
            "Treat the local minimum as 'the' minimum or assume non-convex training is hopeless."
        ),
        "follow_ups": [
            "What is a saddle point and why is it less of a problem in high dimensions than minima?",
            "How does initialization affect non-convex optimization?",
            "Why does SGD often beat second-order methods for deep models?",
            "What does it mean that loss landscapes have many equally good minima?",
        ],
        "exercise": (
            "Train the same network with three different seeds. Compare training and validation loss. Then ensemble the three. Note the gap between best "
            "single run and ensemble."
        ),
        "diagram": (
            "flowchart LR\n"
            "    P[Problem] --> C{Convex?}\n"
            "    C -- Yes --> Det[Unique minimum,<br/>guaranteed convergence]\n"
            "    C -- No --> NC[Many minima,<br/>seed-dependent, validate empirically]"
        ),
    },
    "math/11-information-theory-entropy-cross-entropy-kl-divergence.md": {
        "title": "Information Theory: Entropy, Cross-Entropy, and KL Divergence",
        "intuition": (
            "Entropy measures how uncertain a distribution is. Cross-entropy measures how badly one distribution predicts another. KL divergence measures "
            "the extra cost of using the wrong distribution to encode the right one. Most classification losses are cross-entropy; many regularizers and "
            "alignment losses are KL divergences."
        ),
        "formal": (
            "For a distribution `p`, entropy is `H(p) = -Σ p(x) log p(x)`. Cross-entropy of `q` relative to `p` is `H(p, q) = -Σ p(x) log q(x)`. "
            "KL divergence is `KL(p || q) = Σ p(x) log(p(x) / q(x)) = H(p, q) - H(p)`. KL is non-negative and zero iff `p = q`. It is asymmetric: "
            "`KL(p || q) != KL(q || p)`. In ML, `p` is the target (one-hot or soft label), `q` is the model's predicted distribution."
        ),
        "why": (
            "Cross-entropy is the standard loss for classification because it directly penalizes confident wrong predictions. KL divergence underlies "
            "label smoothing, knowledge distillation (student predicts teacher), variational autoencoders, and policy regularization in RLHF. Calibration "
            "metrics are entropy-based."
        ),
        "steps": [
            "For a hard-labeled classification, cross-entropy reduces to `-log p(true class)`.",
            "Use softmax to map logits to a distribution before computing cross-entropy.",
            "Use KL when both target and prediction are full distributions (distillation, RLHF).",
            "Use label smoothing to soften targets and improve calibration.",
            "Track per-class cross-entropy to see which classes the model is bad at.",
        ],
        "example": (
            "A model is overconfident on training data and miscalibrated. Adding label smoothing (target becomes `(1-ε) one_hot + ε/K uniform`) is "
            "equivalent to training against a softer KL target. The model becomes less confident, generalizes better on validation, and produces "
            "probabilities that match observed frequencies."
        ),
        "mistakes": [
            "Confusing entropy (a property of one distribution) with cross-entropy (between two).",
            "Treating KL as a distance even though it is not symmetric and does not satisfy the triangle inequality.",
            "Forgetting that cross-entropy with one-hot targets equals `-log p(true)`.",
            "Using KL when forward and reverse give different answers without thinking about which to pick.",
        ],
        "iq": "Explain entropy, cross-entropy, and KL divergence and how each shows up in an ML loss.",
        "is_strong": (
            "Entropy is the average information needed to encode samples from a distribution. Cross-entropy is the cost of encoding samples from `p` "
            "using a code optimized for `q`. KL is the difference: how much extra you pay using `q` instead of the true `p`. In ML, classification loss is "
            "cross-entropy with the model's predicted distribution; distillation uses KL of student to teacher; label smoothing softens the target; "
            "VAEs penalize KL of approximate posterior to prior."
        ),
        "is_weak": (
            "Quote formulas without explaining what each measures or how it is used."
        ),
        "follow_ups": [
            "Why is forward KL `KL(p || q)` mode-covering and reverse KL mode-seeking?",
            "How does temperature in softmax affect entropy?",
            "How is KL related to maximum likelihood estimation?",
            "What is mutual information and how is it related?",
        ],
        "exercise": (
            "Compute entropy, cross-entropy, and KL for two simple discrete distributions by hand. Verify `KL(p || q) = H(p, q) - H(p)`."
        ),
        "diagram": (
            "flowchart LR\n"
            "    P[True dist p] --> CE[Cross-entropy H(p,q)]\n"
            "    Q[Pred dist q] --> CE\n"
            "    P --> H[Entropy H(p)]\n"
            "    CE --> KL[KL = H(p,q) - H(p)]\n"
            "    H --> KL"
        ),
    },
    "math/12-distance-metrics.md": {
        "title": "Distance Metrics",
        "intuition": (
            "A distance metric is a way to say how different two things are. The choice changes which neighbors look closest, which clusters form, and "
            "which retrieval results win. Different geometries match different data: Euclidean for continuous features, cosine for normalized embeddings, "
            "Hamming for binary, edit distance for strings."
        ),
        "formal": (
            "Common metrics:\n\n"
            "- **Euclidean (L2):** `||u - v||₂`.\n"
            "- **Manhattan (L1):** `Σ |u_i - v_i|`.\n"
            "- **Cosine distance:** `1 - cos θ = 1 - u·v / (||u|| ||v||)`.\n"
            "- **Dot product (similarity):** `u · v`. Larger is closer.\n"
            "- **Hamming:** number of positions where two binary strings differ.\n"
            "- **Jaccard:** `|A ∩ B| / |A ∪ B|` for sets.\n"
            "- **Edit distance:** minimum edits to convert one string to another.\n\n"
            "A formal metric must be non-negative, zero iff identical, symmetric, and obey the triangle inequality. Cosine similarity is not a metric; "
            "cosine distance often almost is."
        ),
        "why": (
            "Retrieval, clustering, recommenders, and many ML systems hinge on distance choice. The metric must match how features were trained or scaled, "
            "or results are misleading. Mixing metrics across models is a common production bug."
        ),
        "steps": [
            "Identify the data type: dense numeric, binary, set, sequence, embedding.",
            "Pick a metric that matches that type and how the model was trained.",
            "Normalize features so no single dimension dominates (or use a metric robust to scale).",
            "Index for fast nearest-neighbor lookup if the data is large (HNSW, IVF-PQ).",
            "Validate by spot-checking nearest neighbors on real queries.",
        ],
        "example": (
            "A team builds a duplicate-detection system on text. Switching from edit distance to cosine on transformer embeddings catches paraphrases that "
            "edit distance misses. They use both: cosine for semantic similarity and edit distance for near-exact duplicates. Combining both gives the best "
            "precision and recall."
        ),
        "mistakes": [
            "Using Euclidean on raw text or one-hot data without justification.",
            "Comparing cosine similarity scores across embedding spaces from different models.",
            "Forgetting that distance changes meaning when features are not scaled.",
            "Using a non-metric in algorithms that require triangle inequality.",
            "Not matching the metric to how the embedding model was trained.",
        ],
        "iq": "How would you choose a distance metric for a new retrieval problem?",
        "is_strong": (
            "Look at the data type and how the embedding (if any) was trained. Use cosine for normalized text embeddings, dot product when training "
            "specified it, Euclidean when geometric distance is meaningful, Hamming or Jaccard for set-like data. Validate empirically on a small holdout: "
            "are the top neighbors actually similar?"
        ),
        "is_weak": (
            "Default to Euclidean without considering the embedding training or feature scaling."
        ),
        "follow_ups": [
            "Why is L2 sensitive to feature scale and L1 less so?",
            "What is Mahalanobis distance and when do you want it?",
            "How does distance behave in high dimensions?",
            "When is the triangle inequality important for retrieval data structures?",
        ],
        "exercise": (
            "Take a small text dataset. Compute pairwise similarities with cosine on TF-IDF and on transformer embeddings. Compare the top-5 neighbors of "
            "5 queries. Discuss the differences."
        ),
        "diagram": (
            "flowchart LR\n"
            "    D[Data type] --> C{Choose metric}\n"
            "    C -- Dense vectors --> E[Euclidean / Cosine / Dot]\n"
            "    C -- Sets --> J[Jaccard]\n"
            "    C -- Strings --> Ed[Edit distance]\n"
            "    C -- Binary --> H[Hamming]\n"
            "    E --> Idx[Index for fast NN]\n"
            "    J --> Idx\n"
            "    Ed --> Idx\n"
            "    H --> Idx"
        ),
    },
}
