# Models

## GAB (Guggenheim-Anderson-de Boer)

$$m = \frac{m_0 \, C \, K \, a_w}{(1 - K a_w)(1 - K a_w + C K a_w)}$$

Three parameters: monolayer moisture content $m_0$, and the Guggenheim constant $C$ and correction factor $K$. Recommended by the European COST 90 project as the reference model for food isotherms across the full $a_w$ range (0–0.9+).

## BET (Brunauer-Emmett-Teller)

$$m = \frac{m_0 \, C \, a_w}{(1 - a_w)(1 - a_w + C a_w)}$$

Two parameters, classically valid only for $a_w < 0.5$. `isotherm-fit` therefore fits BET **only on the subset of data points with $a_w < 0.5$**, requiring at least 3 such points.

## Peleg

$$m = k_1 a_w^{n_1} + k_2 a_w^{n_2}$$

Four-parameter empirical model with no physical monolayer interpretation, but often gives the best pure curve fit across the full range, especially at high $a_w$.

## Model selection (AIC) and why BET is treated separately

AIC values are only statistically comparable across models fitted on the **same data**. Because BET is fitted on a restricted $a_w < 0.5$ subset while GAB and Peleg are fitted on the full dataset, `isotherm-fit` excludes BET from the "best model" AIC comparison (unless it is the only model that converged). BET's own R², RMSE, and AIC are still reported for reference.

## Monolayer moisture content (m₀) and the stability zone

$m_0$ is the key food-stability parameter: below it, chemical degradation reactions and microbial growth are strongly inhibited. Since Peleg has no $m_0$ parameter, `isotherm-fit` computes the reported $m_0$ and the shaded "stability zone" on the report plot from **GAB** (preferred, per COST 90) or **BET** as a fallback — independent of which model wins the AIC race for overall curve shape. This is handled by `get_monolayer_reference()` in `isotherm_fit.models`.
