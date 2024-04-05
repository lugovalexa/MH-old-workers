* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_country.csv", clear

* DID imputation regression - Borusyak

* Modifications for this model
drop if wblock56 == 1 & wave == 5
replace first_treated = . if first_treated == 0

* Additional variables
gen cell1 = country + "_" + string(gender)
gen cell2 = country + "_" + string(gender) + "_" + string(work_horizon_change_minimum)

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
*quietly su jqi_sum , d
*scalar per25=r(p25)
*scalar per75=r(p75)
*keep if jqi_sum <= per25
*keep if jqi_sum >= per75

*egen median_jqi = median(jqi_skills_discretion)
*keep if jqi_skills_discretion < median_jqi


* Regressions
did_imputation eurod mergeid year first_treated [aw=cciw], fe(cell1 year) autosample cluster(cell1)

did_imputation eurod mergeid year first_treated [aw=cciw], fe(cell1 year) controls(age nb_children nb_grandchildren partnerinhh thinclog life_insurance sphus chronic) autosample cluster(cell1)
