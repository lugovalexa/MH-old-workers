* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_country.csv", clear

* DID imputation regression - Borusyak

* Modifications for this model
drop if wblock56 == 1 & wave == 5
replace work_horizon_change_minimum = 0 if wave == 4
gen treated = (work_horizon_change_minimum > 0)

* Additional variables
gen cell1 = country + "_" + string(gender)
gen cell2 = country + "_" + string(gender) + "_" + string(work_horizon_change_minimum)

encode cell1, generate(cell1_encoded)
encode cell2, generate(cell2_encoded)

encode industry, generate(industry_encoded)
encode country, generate(country_encoded)
encode mergeid, generate(mergeid_encoded)

gen agesq = age^2
gen thinclog = log(thinc)

*sort cell1
*by cell1: gen dupcount = _N
*keep if dupcount >= 4
*drop dupcount

* Filter by gender
keep if gender == 1

* Filter by working conditions
quietly su jqi_physical_environment , d
scalar per25=r(p25)
scalar per75=r(p75)
*keep if jqi_physical_environment <= per25
keep if jqi_physical_environment >= per75

*egen median_jqi = median(jqi_skills_discretion)
*keep if jqi_skills_discretion < median_jqi

* Regressions
did_multiplegt eurod mergeid_encoded year treated, controls(age nb_children nb_grandchildren partnerinhh thinclog life_insurance sphus chronic) robust_dynamic weight(cciw) cluster(cell1_encoded)
