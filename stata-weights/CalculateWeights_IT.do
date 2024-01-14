* Set Stata
*-----------------------------------------------------------------------------
clear
set linesize 100
cd "/Users/dimaf/Documents/Sasha/"
adopath ++ "/Users/dimaf/Documents/Sasha/"
local data "/Users/dimaf/Documents/Sasha/data/"
*-----------------------------------------------------------------------------
global wi 4
global wf 6
global cc "IT"
global cc_num "16"
global pop_time 2011
global mort_time 2014
global w "l_`wi'_`wf'"
global age_groups 4
global age_thr_low "80 70 60 50"
global age_thr_upp "89 79 69 59"

local wi ${wi}
local wf ${wf}
local cc ${cc}
local cc_num ${cc_num}
local w ${w}
*-----------------------------------------------------------------------------
* Run CalMar_long.do
*-----------------------------------------------------------------------------
noi run CalMar_long_custom.do
*-----------------------------------------------------------------------------
* Number of calibration equations
*-----------------------------------------------------------------------------
* No NUTS1 for longitudinal weights
matrix ${cc}_w${w}_P_MARG = ${cc}_w${w}_P_SA
noi mat li ${cc}_w${w}_P_MARG

mata: st_matrix("C1",rows(st_matrix("${cc}_w${w}_P_SA")))
local C1 = C1[1,1]
mata: st_matrix("C",rows(st_matrix("${cc}_w${w}_P_MARG")))
local C = C[1,1]
local C2 = `C' - `C1'
local nag = `C1' / 2
assert `C1'==8
//assert `C2'==0
*-----------------------------------------------------------------------------
* Load my SHARE dataset and select the country-data
*-----------------------------------------------------------------------------
qui use "data/mydata_long_ind", clear
qui keep if country==`cc_num'
*-----------------------------------------------------------------------------
* Calibration variables
*-----------------------------------------------------------------------------
sum age gender dw_w`wi'
qui gen str3 nuts1=nuts1_2010
qui gen region = .
qui replace region=0 if nuts1=="ITC"
qui replace region=1 if nuts1=="ITF"
qui replace region=2 if nuts1=="ITG"
qui replace region=3 if nuts1=="ITH"
qui replace region=4 if nuts1=="ITI"

*-----------------------------------------------------------------------------


*-----------------------------------------------------------------------------
* Binary indicator for missing weights
*-----------------------------------------------------------------------------
//qui gen nowi=(dw_w`wi'==.|gender==.|age==.|region==.|age<50)
qui gen nowi = (dw_w`wi'==.|gender==.|age==.|age<50)
noi tab nowi, mis
*-----------------------------------------------------------------------------


*-----------------------------------------------------------------------------
* Binary indicators for calibration groups
*-----------------------------------------------------------------------------
local t = 1
forvalues ss=1(1)2 {
  forvalues aa=1(1)`nag' {
    local lb = ${cc}_w${w}_P_AGE_THR[`aa',1]
    local ub = ${cc}_w${w}_P_AGE_THR[`aa',2]
    if `aa'==1 qui gen xi_`t'=(age_w`wi'>=`lb')*(age_w`wi'!=.   )*(gender==`ss') if nowi!=1
    else       qui gen xi_`t'=(age_w`wi'>=`lb')*(age_w`wi'<=`ub')*(gender==`ss') if nowi!=1
    local t = `t' + 1
  }
}
forvalues i=1(1)`C2' {
  local i2 = `C1' + `i'
  qui gen xi_`i2' = (region==`i' & age_w`wi'>=50 & age_w`wi'!=. & gender!=.) if nowi!=1
}
// list mergeid gender age_w4 xi_1-xi_8 if _n<=5, noobs
// list mergeid region xi_9-xi_10 if _n<=5, noobs
*-----------------------------------------------------------------------------



*-----------------------------------------------------------------------------
* Compute calibrated weights (distance function: DS - case 6)
*-----------------------------------------------------------------------------
local list_CVar ""
forvalues i=1(1)`C' {
  local list_CVar `list_CVar' xi_`i'
}
sreweight `list_CVar' if nowi!=1 & dw_w`wi'!=.,   ///
	nweight(my_wgt) sweight(dw_w`wi')             ///
	total(${cc}_w${w}_P_MARG)                  ///
	dfunction(chi2) upbound(10) lowbound(.01) ///
	niter(200) ntries(50)
*-----------------------------------------------------------------------------

save "data/mydata_long_ind_IT.dta", replace
