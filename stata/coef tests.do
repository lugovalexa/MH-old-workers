* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_country.csv", clear

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

keep if gender==0

quietly su jqi_sum , d
scalar per25=r(p25)
scalar per75=r(p75)


* Step 1: Run individual regressions
qui regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects jqi_sum i.cell1_encoded [aweight=cciw] if jqi_sum <= per25

*qui regress eurod i.did i.treated i.post i.cell1_encoded [aweight=cciw] if jqi_prospects <= per25

est sto below

qui regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects jqi_sum i.cell1_encoded [aweight=cciw] if jqi_sum >= per75

*qui regress eurod i.did i.treated i.post i.cell1_encoded [aweight=cciw] if jqi_prospects >= per75

est sto above

suest below above, vce(cluster cell1)

test [above_mean]1.did = [below_mean]1.did
