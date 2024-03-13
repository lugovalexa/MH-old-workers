* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/3digits_year_country.csv", clear

* Create variables for DID
gen post = (year == 2015)
gen treated = (work_horizon_change_minimum > 0)
*gen treated = work_horizon_change_minimum
gen did = post * treated

gen cell1 = country + "_" + string(gender)
gen cell2 = country + "_" + string(work_horizon_change)

sort cell1
by cell1: gen dupcount = _N
keep if dupcount >= 2
drop dupcount

encode cell1, generate(cell1_encoded)
encode cell2, generate(cell2_encoded)

encode industry, generate(industry_encoded)

gen agesq = age^2
gen thinclog = log(thinc)

*keep if gender==1

egen mean_jqi = mean(jqi_prospects)
egen sd_jqi = sd(jqi_prospects)


* Step 1: Run individual regressions
qui regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.isco1 i.industry_encoded i.cell1_encoded [aweight=cciw] if jqi_prospects <= mean_jqi-sd_jqi

est sto below

qui regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects  i.isco1 i.industry_encoded i.cell1_encoded [aweight=cciw] if jqi_prospects >= mean_jqi+sd_jqi

est sto above

suest below above, vce(cluster cell1)

test [above_mean]1.did = [below_mean]1.did
