*-----------------------------------------------------------------------------
* Set Stata
*-----------------------------------------------------------------------------
set linesize 100
cd "/Users/dimaf/Documents/Sasha/"
adopath ++ "/Users/dimaf/Documents/Sasha/"
local data "/Users/dimaf/Documents/Sasha/data/"
*-----------------------------------------------------------------------------
* Extract individual data for longitudinal sample
*-----------------------------------------------------------------------------
local wi = 4
local wf = 6
global w = "l_`wi'_`wf'"
* Identify longitudinal (balanced) sample
forvalues wj=`wi'(1)`wf' {
  qui use "`data'sharew`wj'_rel8-0-0_cv_r", clear
  qui keep if interview==1
  qui keep mergeid
  if `wj'>`wi' qui merge 1:1 mergeid using temp_balanced_ii,keep(3) nogen
  sort mergeid
  qui save temp_balanced_ii,replace
  }
* Merge longitudinal sample
qui use "`data'sharew`wi'_rel8-0-0_cv_r", clear
keep mergeid hhid4 country gender yrbirth interview
qui gen age_w4 = 2011 - yrbirth if yrbirth>0
qui keep if interview==1
drop interview
qui merge 1:1 mergeid using "data\sharew`wi'_rel8-0-0_gv_weights",  	///
 			keepus(dw_w4) assert(3) nogen
// qui merge 1:1 mergeid using "data/sharewX_rel8-0-0_gv_longitudinal_weights_w4w5",  	///
//	keepus(dw_w4 cliw_e) assert(1 3) nogen
qui merge 1:1 mergeid using "data/sharew`wi'_rel8-0-0_gv_housing", 	///
	keepus(nuts1_2010) assert(3) nogen
qui merge 1:1 mergeid using temp_balanced_ii
gen balanced = _merge==3
cap lab drop balanced
lab define balanced 0 "not all waves" 1 "all waves"
lab value balanced balanced
noi tab country balanced,m
drop if balanced==0
drop _merge balanced
* Save data
qui compress
sort mergeid
qui saveold "`data'mydata_long_ind.dta", replace
erase temp_balanced_ii.dta
