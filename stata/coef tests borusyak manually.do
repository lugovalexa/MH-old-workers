* Given coefficients and standard errors
local coef1 = 0.589
local se1 = 0.237

local coef2 = -0.074
local se2 = 0.398

* Calculate the difference between the coefficients
local diff_coef = `coef1' - `coef2'

* Calculate the standard error of the difference
local se_diff = sqrt(`se1'^2 + `se2'^2)

* Compute the t-statistic
local t_stat = `diff_coef' / `se_diff'

* Compute the p-value
local p_value = 2 * (1 - normal(abs(`t_stat')))

* Display results
di "t-statistic: " `t_stat'
di "p-value: " `p_value'
