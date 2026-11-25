# 🧠 ECOSPHERE AI — Artificial Intelligence & Optimization Architecture
**Machine Learning Mathematical Formulations**

---

## 1. Environmental Time-Series Regressor Forecasting

### Mathematical Formulation
To forecast continuous environmental variables without overfitting non-stationary time series, ECOSPHERE AI employs **L2-Regularized Ridge Regression** combined with polynomial lag transformations:

$$\min_{w} \left( \sum_{i=1}^n \left( y_i - w^T \phi(x_i) \right)^2 + \alpha \|w\|_2^2 \right)$$

Where:
* $y_i$: Target environmental variable (e.g., AQI, Ambient Temperature, Energy Consumption)
* $\phi(x_i)$: Feature extraction vector composed of:
  * Autoregressive lag values: $y_{t-1}, y_{t-2}, y_{t-24}$
  * Diurnal cyclical features: $\sin(2\pi \cdot \text{hour} / 24)$, $\cos(2\pi \cdot \text{hour} / 24)$
  * Day of week cyclical features: $\sin(2\pi \cdot \text{dow} / 7)$, $\cos(2\pi \cdot \text{dow} / 7)$
  * Meteorological covariates (temperature, humidity, wind velocity)
* $\alpha$: Regularization penalty parameter ($\alpha = 1.0$)

### Quantitative Model Evaluation Metrics
Every forecast execution reports three empirical metrics calculated over validation folds:
1. **Mean Absolute Error (MAE)**:
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
2. **Root Mean Square Error (RMSE)**:
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}$$
3. **Coefficient of Determination ($R^2$)**:
   $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

---

## 2. Unsupervised Anomaly & Hazard Detection

### Isolation Forest Engine
ECOSPHERE AI utilizes `sklearn.ensemble.IsolationForest` to isolate outliers in continuous multidimensional environmental streams without requiring labeled anomalies.

* **Partitioning Principle**: Anomalies are few and topologically distinct, requiring fewer random recursive hyper-plane splits to isolate in feature trees.
* **Path Length Score**:
  $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
  Where $h(x)$ is tree depth, $E(h(x))$ is average path length, and $c(n)$ is average path length of unsuccessful search in a Binary Search Tree.
* **Contamination Rate**: $c = 0.08$ (8% expected anomaly density).

### Parametric 3-Sigma ($3\sigma$) Z-Score Verification
As an orthogonal validation layer for single-stream sensor metrics (e.g. pH spikes or sudden AQI surges):

$$Z = \frac{|x_t - \mu_{window}|}{\sigma_{window}}$$

A reading is flagged as an acute environmental hazard if $Z > 2.5$.

---

## 3. Graph-Theoretic Waste Collection Routing (Dijkstra)

Municipal solid waste collection dispatch is modeled as a directed weighted graph $G = (V, E)$, where $V$ represents smart-bin sensor nodes and central transit depot, and $E$ represents street segments weighted by Haversine spherical distance:

$$d = 2R \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$

### Algorithmic Execution:
1. **Priority Filter**: Nodes where ultrasonic fill percentage $F_i \ge 70\%$ are added to the active collection set $V_{active}$.
2. **Priority Heap**: Nodes where $F_i \ge 85\%$ receive critical weighting $w_{priority} = 0.6 \cdot d_{ij}$.
3. **Min-Priority Queue Dijkstra**: Computes the optimal Hamiltonian tour originating and terminating at the Hanamkonda Central Depot.
4. **Impact Metrics**:
   * Distance Saved ($km$): $D_{baseline} - D_{optimized}$
   * Fuel Saved ($L$): $\Delta D \times 0.28\text{ L/km}$ (Euro-VI diesel fleet average)
   * Carbon Abatement ($kg\text{ CO}_2$): $\Delta \text{Fuel} \times 2.68\text{ kg CO}_2/\text{L}$

---

## 4. Multi-Criteria Decision Analysis (MCDA) Resource Allocation

To equitably deploy limited emergency teams and environmental field inspectors across competing municipal zones, the engine executes a **Weighted Sum Multi-Criteria Decision Model**:

$$S_k = \sum_{j=1}^m w_j \cdot r_{kj}$$

### Criteria & Weight Vector:
| Criterion $j$ | Dimension | Assigned Weight $w_j$ | Normalization |
|---|---|---|---|
| $C_1$: Air Quality Hazard | Peak AQI / PM2.5 | $0.45$ | $\min(1.0, \text{AQI} / 300)$ |
| $C_2$: Hydrological Risk | WQI Deficit & BOD | $0.35$ | $(100 - \text{WQI}) / 100$ |
| $C_3$: Incident Severity | Open Violations | $0.20$ | Normalized incident count & severity |

The zones are ranked by descending $S_k$, and available emergency response teams and inspection personnel are allocated proportionally to minimize total civic exposure risk.
