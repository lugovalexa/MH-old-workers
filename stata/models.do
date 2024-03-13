* Working directory
cd "/Users/alexandralugova/Documents/GitHub/MH-old-workers/stata"

* Data
import delimited "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/3digits_year_country.csv", clear

* Leave a balanced panel
*sort mergeid
*by mergeid: gen dupcount = _N
*keep if dupcount == 2
*drop dupcount

* Leave only countries present in both waves
*keep if !inlist(country, "Greece", "Hungary", "Luxembourg","Netherlands","Poland","Portugal")

* Filter by gender
keep if gender == 1

* Filter by working conditions
egen mean_jqi = mean(jqi_prospects)
egen sd_jqi = sd(jqi_prospects)
*keep if jqi_prospects <= mean_jqi - sd_jqi
keep if jqi_prospects >= mean_jqi + sd_jqi
*egen median_jqi = median(jqi_social_environment)
*keep if jqi_social_environment < median_jqi

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

* DID regression
*regress eurod i.did i.treated i.post [aweight=cciw], vce(cluster cell1)
*regress eurod did treated i.post [aweight=cciw], vce(cluster cell1)

regress eurod i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.isco1 i.industry_encoded i.cell1_encoded [aweight=cciw], vce(cluster cell1)

*regress eurod did treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity_slim jqi_prospects [aweight=cciw], vce(cluster cell1)

*regress eurod i.treated i.post i.did i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.cell1_encoded i.isco1 i.industry_encoded [aweight=cciw], vce(cluster cell1)

*regress eurodcat i.did i.treated i.post [aweight=cciw], vce(cluster cell1)
*regress eurodcat did treated i.post [aweight=cciw], vce(cluster cell1)

*regress eurodcat i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects [aweight=cciw], vce(cluster cell1)
*regress eurodcat did treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity_slim jqi_prospects [aweight=cciw], vce(cluster cell1)

*regress eurodcat i.treated i.post i.did i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.cell1_encoded i.isco1 i.industry_encoded [aweight=cciw], vce(cluster cell1)

*logit eurodcat i.treated i.post i.did, vce(cluster cell1)

*regress eurodcat i.did i.treated i.post i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects, vce(cluster cell1)

*logit eurodcat i.treated i.post i.did i.gender age agesq nb_children nb_grandchildren i.partnerinhh yrseducation thinclog  i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.cell1_encoded i.isco1 i.industry_encoded, vce(cluster cell1)

* Panel model
*egen panel_id = group(mergeid)
*sort panel_id year

*xtset panel_id
*xtreg eurod i.did i.post age agesq nb_children nb_grandchildren i.partnerinhh thinclog i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.isco1 [aweight=my_wgt], fe vce(cluster cell1)

*xtset panel_id
*xtreg eurod i.did i.post age agesq nb_children nb_grandchildren i.partnerinhh thinclog i.life_insurance sphus chronic work_horizon jqi_skills_discretion jqi_physical_environment jqi_social_environment jqi_working_time_quality jqi_intensity jqi_prospects i.isco1 [aweight=cciw_w6], fe vce(cluster cell1)
