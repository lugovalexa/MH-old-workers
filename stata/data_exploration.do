* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_year.csv", clear

* Leave a balanced panel
* sort mergeid
* by mergeid: gen dupcount = _N
* keep if dupcount == 2
* drop dupcount

* Leave only countries present in both waves
* keep if !inlist(country, "Greece", "Hungary", "Luxembourg","Netherlands","Poland","Portugal")

* Create variables for DID
gen post = (year == 2015)
gen treated = (work_horizon_change_minimum > 0)
gen did = post * treated

gen cell1 = country + "_" + string(gender)
gen cell2 = country + "_" + string(work_horizon_change_minimum)
sort cell2
by cell2: gen dupcount = _N
keep if dupcount >= 4
drop dupcount

gen agesq = age^2
gen thinclog = log(thinc)

* Number of observations
local num_obs `=r(N)'
di "Number of observations in the dataset: " `num_obs'

* Number of observations by year
di "Number of observations by year:"
tabulate year

*  Number of observations by country
di "Number of observations by country:"
tabulate country

* Number of individuals
quietly levelsof mergeid, local(unique_values)
local num_unique : word count `unique_values'
di "Number of unique individuals: " `num_unique'

* Demographic data description
summarize gender age partnerinhh nb_children nb_grandchildren yrseducation thinc investment life_insurance sphus chronic

* Mental health data description
summarize eurod eurodcat affective_suffering motivation_lack

* Work and retirement data description
summarize yrscontribution retirement_age retirement_age_minimum work_horizon work_horizon_change work_horizon_change_minimum

di "Number of observations by industry:"
tabulate industry

di "Number of observations by job status:"
tabulate job_status

quietly levelsof isco, local(unique_values)
local num_unique : word count `unique_values'
di "Number of unique ISCO: " `num_unique'

* Job quality data description
summarize jqi_skills_discretion_pure jqi_physical_environment_pure jqi_social_environment_pure jqi_intensity_pure  jqi_working_time_quality_pure  jqi_prospects_pure jqi_sum_pure


* Mann-Whitney U test (compares median when not normal distibution, H0: equal medians)
* Compare EuroD between 2011 and 2015
sort post
by post: summarize eurod

ranksum eurod, by(post)

* Compare EuroD between treated and not treated
sort treated
by treated: summarize eurod

ranksum eurod, by(treated)

* Compare EuroD between treated and not treated in 2011 and 2015
sort post treated
by post treated: summarize eurod

* Scalar DID estimation
summarize eurod if treated == 1 & post == 0, meanonly
scalar mean_treated_before = r(mean)
summarize eurod if treated == 1 & post == 1, meanonly
scalar mean_treated_after = r(mean)
summarize eurod if treated == 0 & post == 0, meanonly
scalar mean_control_before = r(mean)
summarize eurod if treated == 0 & post == 1, meanonly
scalar mean_control_after = r(mean)
scalar did_estimate = (mean_treated_after - mean_treated_before) - (mean_control_after - mean_control_before)
di "DID estimate: " did_estimate

* DID regression
regress eurod i.treated i.post i.did [aweight=cciw], vce(cluster cell2)

regress eurod i.treated i.post i.did i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects [aweight=cciw], vce(cluster cell2)

egen panel_id = group(mergeid)
xtreg eurod i.treated##i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects [aweight=my_wgt], fe robust

egen mean_jqi = mean(jqi_physical_environment)
egen sd_jqi = sd(jqi_physical_environment)
local threshold = mean_jqi - sd_jqi
drop if jqi_physical_environment > `threshold'
