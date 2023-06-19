## Simulations

This section will conduct a series of simulations to better understand fukkatsu's potential capabilities. To achieve this, multiple error types will be tested. Each error type and scenario will consist of a total of 50 runs under the same conditions. We will test the following hypotheses:

### Hypotheses testing

- H<sub>0</sub>: `The proportion of errors solved is not significantly greater than 0.5.`
- H<sub>1</sub>: `The proportion of errors solved is significantly greater than 0.5.`

We will consider a confidence interval of 0.05 and utilize a binomial distribution.

```python
import scipy.stats as stats

successes = # number of successful repairs

alpha = 0.05

p_value = stats.binom_test(successes, n=50, p=0.5, alternative='greater')

print(f"p_value: {p_value}")

if p_value < alpha:
    print("Reject the null hypothesis")
    print("The proportion of errors solved is significantly greater than 0.5.")
else:
    print("Fail to reject the null hypothesis")
    print("The proportion of errors solved is not significantly greater than 0.5.")
```


fukkatsu will utilize the `gpt-3.5-turbo` model in all simulations. For each simulation, 3 lives will be allocated. The functions will also be provided with sufficient context. 

After conducting all the tests, we will finally apply a `chi-square test`. This test will help determine whether there is a statistically significant difference in the fukkatsu's performance across the error types. If the test results indicate a significant association, it suggests that the effectiveness of fukkatsu varies depending on the error type.

```python
import numpy as np
from scipy.stats import chi2_contingency

observed_counts = np.array([[,], [,], [,]])

chi2, p_value, dof, expected = chi2_contingency(observed_counts)

print("Chi-square statistic:", chi2)
print("P-value:", p_value)
print("Degrees of freedom:", dof)
print("Expected counts:", expected)
```

You can see each simulation recored in the different jupyter notebooks contained within the `research` directory.


| Error Type | Error Name | Success | Failure |    Date    |   Version  | Commit ID | p-value | alpha |Rejected H<sub>0</sub> |
|------------|------------|---------|---------|------------|------------|-----------|---------|--------|-------|
|UnicodeDecodeError |  [Parser Error](https://github.com/maxmekiska/fukkatsu/blob/main/research/siumlationNotebooks/fukkatsuParserError.ipynb) |   45    |   5     | 19/06/23 |   0.0.7  | 9d3ec24   | 2.104926011270436e-09 |0.05| Yes    |        
| Type B     |   Type Error  |   -     |   -    | - |   -     |   -  |        -       |   -       |   -  | 
