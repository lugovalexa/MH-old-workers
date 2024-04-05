* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_country.csv", clear

* CS DID regression - Callaway and Sant’Anna

* Modifications for this model
drop if wblock56 == 1 & wave == 5
replace work_horizon_change_minimum = 0 if wave == 4
gen treated = (work_horizon_change_minimum > 0)

* Additional variables
gen cell1 = country + "_" + string(gender)
gen cell2 = country + "_" + string(wblock56) + "_" + string(work_horizon_change)

*sort cell1
*by cell1: gen dupcount = _N
*keep if dupcount >= 2
*drop dupcount

encode cell1, generate(cell1_encoded)
encode cell2, generate(cell2_encoded)

encode industry, generate(industry_encoded)
encode country, generate(country_encoded)
encode mergeid, generate(mergeid_encoded)

gen agesq = age^2
gen thinclog = log(thinc)

* Filter by gender
keep if gender == 0

* Filter by working conditions
quietly su jqi_working_time_quality , d
scalar per25=r(p25)
*scalar per75=r(p75)
keep if jqi_working_time_quality <= per25
*keep if jqi_prospects >= per75

*egen median_jqi = median(jqi_physical_environment)
*keep if jqi_physical_environment < median_jqi


* Regressions
*csdid  eurod , ivar(mergeid_encoded) time(year) gvar(first_treated) [notyet] cluster(cell1_encoded) method(dripw)

*csdid  eurod , time(year) gvar(first_treated) [notyet] cluster(cell2_encoded) method(dripw)

qui csdid  eurod [iw=my_wgt], ivar(mergeid_encoded) time(year) gvar(first_treated) [notyet] cluster(cell1_encoded) method(dripw)
estat simple

*csdid  eurod i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects jqi_sum , time(year) gvar(first_treated) [notyet] cluster(cell2_encoded) method(dripw)

qui csdid  eurod i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects jqi_sum [iw=my_wgt], ivar(mergeid_encoded) time(year) gvar(first_treated) [notyet] cluster(cell1_encoded) method(dripw)
estat simple
