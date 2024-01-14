qui {
//--------------------------------------------------------------------------------------------------
// Set macros
//--------------------------------------------------------------------------------------------------
local cc            ${cc}              // country
local cc_num        ${cc_num}          // country number //
local pop_time      ${pop_time}        // reference year
local mort_time     ${mort_time}       // final year
local w             ${w}
local age_groups    ${age_groups}      // number of age groups
local age_thr_low   ${age_thr_low}     // lower thresholds of age groups
local age_thr_upp   ${age_thr_upp}     // upper thresholds of age groups
//--------------------------------------------------------------------------------------------------


//--------------------------------------------------------------------------------------------------
	use "data/margins_nuts1", clear
	keep if country=="`cc'"

	gen age_mort = age - (year-`pop_time')
	local age_min: word `age_groups' of `age_thr_low'
	local age_max: word 1            of `age_thr_upp'
	drop if age<`age_min'
	assert age>=`age_min'&age<=`age_max'

	* Joint age-sex classification
	local rname ""
	local t=1
	matrix `cc'_w`w'_P=0
	cap matrix drop `cc'_w`w'_P_AGE_THR
	cap matrix drop `cc'_w`w'_P_SA
	forvalues ss=0(1)1 {
		if `ss'==0 local slab "M"
		if `ss'==1 local slab "F"
		forvalues aa=1(1)`age_groups' {
			local age_upp: word `aa' of `age_thr_upp'
			local age_low: word `aa' of `age_thr_low'
			sum pop 	if year==`pop_time' 									& (sex==`ss') & (age>=`age_low' & age<=`age_upp')
			local marg_`t'=r(sum)
			sum deaths 	if year>=`pop_time' & year<`mort_time' 	& (sex==`ss') & (age_mort>=`age_low' & age_mort<=`age_upp')
			local marg_`t'=`marg_`t''-r(sum)
			assert `marg_`t''>0
			matrix `cc'_w`w'_P = `cc'_w`w'_P + `marg_`t''
			matrix `cc'_w`w'_P_SA = nullmat(`cc'_w`w'_P_SA) \ (`marg_`t'')
			if `aa'==1 	local rname "`rname' `slab'-`age_low'+"
			else 			local rname "`rname' `slab'-`age_low'-`age_upp'"
			if `ss'==0	matrix `cc'_w`w'_P_AGE_THR = nullmat(`cc'_w`w'_P_AGE_THR) \ (`age_low',`age_upp')
			local t=`t'+1
		}
	}
	matrix coln 	`cc'_w`w'_P_SA		=POP
	matrix rown 	`cc'_w`w'_P_SA		=`rname'
	matrix coln 	`cc'_w`w'_P 	 	=POP
	matrix rown 	`cc'_w`w'_P 		=TOT
	matrix coln 	`cc'_w`w'_P_AGE_THR	= "age_thr_low age_thr_upp"
	noi matrix list `cc'_w`w'_P
	noi matrix list `cc'_w`w'_P_SA

	* NUTS1 classification
	tab nuts1
	local nreg=r(r)
	if `nreg'>1 {
		cap matrix drop `cc'_w`w'_P_NUTS1
		local rname ""
		local t=1
		encode nuts1, gen(REG)
		forvalue nn=1(1)`nreg' {
			local nn_lab: label REG `nn'
			sum pop 	if year==`pop_time' 					& sex==2 & nuts1=="`nn_lab'"
			local marg_`t'=r(sum)
			sum deaths 	if year>=`pop_time' & year<`mort_time' 	& sex==2 & (age_mort>=`age_min') & nuts1=="`nn_lab'"
			local marg_`t'=`marg_`t''-r(sum)
			assert `marg_`t''>0
			matrix `cc'_w`w'_P_NUTS1 = nullmat(`cc'_w`w'_P_NUTS1) \ (`marg_`t'')
			local rname "`rname' `nn_lab'"
			local t=`t'+1
		}
		matrix coln 	`cc'_w`w'_P_NUTS1	=POP
		matrix rown 	`cc'_w`w'_P_NUTS1	=`rname'
		matrix `cc'_w`w'_P_N = `cc'_w`w'_P_NUTS1[2..`nreg',1]
		* Margins
		matrix `cc'_w`w'_P_MARG=`cc'_w`w'_P_SA \ `cc'_w`w'_P_N
	}
	else {
		matrix 		`cc'_w`w'_P_NUTS1	=`cc'_w`w'_P
		matrix 		`cc'_w`w'_P_MARG	=`cc'_w`w'_P_SA
	}
	noi matrix list `cc'_w`w'_P_NUTS1
	noi matrix list `cc'_w`w'_P_MARG

//--------------------------------------------------------------------------------------------------
}
