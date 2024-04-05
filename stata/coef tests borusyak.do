* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/4digits_country.csv", clear

* Create variables for DID
gen post = (year == 2015) | (year == 2013 & wblock56 == 0)
gen treated = (work_horizon_change_minimum > 0)


gen cell1 = country + "_" + string(gender)
*gen cell2 = country + "_" + string(work_horizon_change)

*sort cell1
*by cell1: gen dupcount = _N
*keep if dupcount >= 2
*drop dupcount

encode cell1, generate(cell1_encoded)
*encode cell2, generate(cell2_encoded)

encode industry, generate(industry_encoded)
encode mergeid, generate(mergeid_encoded)

gen agesq = age^2
gen thinclog = log(thinc)

replace first_treated = . if first_treated == 0

keep if gender==1

quietly su jqi_prospects , d
local per25=r(p25)
local per75=r(p75)

generate level = ""
replace level = "low" if jqi_prospects <= `per25'
replace level = "mean" if jqi_prospects > `per25' & jqi_sum < `per75'
replace level = "high" if jqi_prospects >= `per75'

* Regressions and tests
did_imputation eurod mergeid year first_treated [aw=cciw], fe(cell1 year) controls(age nb_children nb_grandchildren partnerinhh thinclog life_insurance sphus chronic) autosample cluster(cell1) hetby(level)

lincom tau_high-tau_low
