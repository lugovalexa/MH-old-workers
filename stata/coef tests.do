* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/3digits_country.csv", clear

* Create variables for DID
gen post = (year == 2015) | (year == 2013 & wblock56 == 0)
gen treated = (work_horizon_change_minimum > 0)
*gen treated = work_horizon_change_minimum
gen did = post * treated

gen cell1 = country + "_" + string(gender) + "_" + string(wblock56)
*gen cell2 = country + "_" + string(work_horizon_change)

*sort cell1
*by cell1: gen dupcount = _N
*keep if dupcount >= 2
*drop dupcount

encode cell1, generate(cell1_encoded)
*encode cell2, generate(cell2_encoded)

encode industry, generate(industry_encoded)

gen agesq = age^2
gen thinclog = log(thinc)

*egen mean_jqi = mean(jqi_prospects)
*egen sd_jqi = sd(jqi_prospects)

quietly su jqi_sum_w , d
scalar per25=r(p25)
scalar per75=r(p75)

keep if gender==0

* Step 1: Run individual regressions
qui regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion_w jqi_physical_environment_w jqi_social_environment_w jqi_working_time_quality_w jqi_intensity_w jqi_prospects_w jqi_sum_w i.cell1_encoded [aweight=cciw] if jqi_prospects_w <= per25

est sto below

qui regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion_w jqi_physical_environment_w jqi_social_environment_w jqi_working_time_quality_w jqi_intensity_w jqi_prospects_w jqi_sum_w i.cell1_encoded [aweight=cciw] if jqi_prospects_w >= per75

est sto above

suest below above, vce(cluster cell1)

test [above_mean]1.did = [below_mean]1.did
