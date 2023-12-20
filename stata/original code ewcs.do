*  .-.    .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.    .-.   *
* /   \  /   \   /   \   /   JOB QUALITY INDEX 2015  \   /   \   /   \  /   \  *
*'     `'     `-'     `-'     `-'     `-'     `-'     `-'     `-'     `'     `'*

clear
capture log close
set more off

local today = c(current_date)
local input = "R:\SpssStata\Mathijn\EWCS\Data\Step 2 - after_recodes_2703.dta"
local output = "R:\SpssStata\Mathijn\EWCS\output\"
local work = "R:\SpssStata\Mathijn\EWCS\work\"

log using "`output'\log`today'.txt", replace

* Uses the recoded version of the EWCS2015 data, including all countries and
* all years.
use "`input'", clear
compress
save "`work'\workdata.dta", replace
use "`work'\workdata.dta", clear

********************************************************************************
*GENERATE WELL-BEING OUTPUTS

*(mvdecode replaces numeric 8 (DK) and 9 (REFUSAL) to missing)
mvdecode y15_Q87* y15_Q78* y15_Q73 y15_Q88 y15_Q73 y15_Q74, mv(8,9)
bysort wave: alpha y15_Q87*, item
* (called like this compute the (row) mean of nonmissing and save it in swb)
qui alpha y15_Q87*, g(swb)
by wave, sort : sum swb

*msp y15_Q87*
*alpha comparale to last year


*(5 questions on wellbeing: 1=all of the time .... 6=at no time)
* (reverse and rescale swb from 1 to 6 to 0-100)
replace swb=20*(6-swb)
label var swb "WHO (Five) Well-Being Index"

*@ A score is created for every observation for which there is a response to at
*   least one item (one variable in varlist is not missing). Makes sense from
*	the perspective of a set of indicators for a latent variable.

g hp=0
g hpm=0
foreach x of varlist y15_Q78* {
	replace hp=hp+2-`x' if `x'~=.
	replace hpm=hpm+1 if `x'==.
}
label var hp "Number of Health Problems"
*a negative well-being indicator
label var hpm "Number of Health Problem Missing Values"

by wave, sort : sum hp hpm

*@ We don't do anything with the missing symptoms. We could correct the variable
*  for this, though thats assuming the missing symptoms are proportional to the
*  non-missing.

g hsrisk=y15_Q73
recode hsrisk 2=0
label var hsrisk "Subjective Health & Safety Risk"
by wave, sort : sum hsrisk

*can also use Q67 and Q72 as health output measures

* (Q88. On the whole, are you very satisfied, satisfied, not very satisfied or not at all satisfied with working conditions in your main paid job?
* (1=very satisfied ... 4=not at all)
* (reverse and rescale in range 0,1)
g jobsat=(4-y15_Q88)/3
label var jobsat "Satisfaction with working conditions"
by wave, sort : sum jobsat

g heff=0 if y15_Q74==2
replace heff=1 if y15_Q74==3
replace heff=2 if y15_Q74==1

ta y15_Q73 y15_Q74, col nofr
*we see that some people say that their health is not at risk, but that their
*work affects their health mainly negatively;
*i.e. this is inconsistent; the opposite: some people say their health is at
*risk, but their work affects their health mainly positively; could be rational,
* but...

*@ the last one seems possible to me: your work generally affects your health
*  positively, but could at the same time be at risk.
*  e.g. a bus driver could be happy with his job and that might have a positive
*  effect on his health, but at the same time he runs the risk of getting into
*  a traffic accident.


mvdecode y15_Q44, mv(8,9)
tab y15_Q44 if wave==6
g wlb_outcome=sqrt((y15_Q44-4)^2)

********************************************************************************
****************************GENERATE MISC VARIABLES*****************************

* Unemployment rates for each of the countries, source of the data: Eurostat ***

*@ Needs to be updated
generate unemp=.
replace unemp=8.3  	 if countid==1
replace unemp=10.2   if countid==2
replace unemp=7.3  	 if countid==3
replace unemp=7.4  	 if countid==4
replace unemp=7.1  	 if countid==5
replace unemp=16.9   if countid==6
replace unemp=12.6   if countid==7
replace unemp=20.1   if countid==8
replace unemp=9.8  	 if countid==9
replace unemp=13.7   if countid==10
replace unemp=8.4  	 if countid==11
replace unemp=6.3  	 if countid==12
replace unemp=18.7   if countid==13
replace unemp=17.8   if countid==14
replace unemp=4.5    if countid==15
replace unemp=11.2   if countid==16
replace unemp=6.9  	 if countid==17
replace unemp=4.5  	 if countid==18
replace unemp=4.4  	 if countid==19
replace unemp=9.6  	 if countid==20
replace unemp=12   	 if countid==21
replace unemp=7.3  	 if countid==22
replace unemp=7.3    if countid==23
replace unemp=24  	 if countid==24
replace unemp=8.4  	 if countid==25
replace unemp=8.4    if countid==26
replace unemp=7.8    if countid==27
replace unemp=11.8   if countid==28
replace unemp=33.8   if countid==29
replace unemp=10.7   if countid==30
replace unemp=3.5    if countid==31
replace unemp=13.5   if countid==32
replace unemp=44     if countid==33
replace unemp=14.7   if countid==34


*Number of dependent individuals in the household under 16 and above 75 of age

g numdep=0
foreach x in y15_Q3b_2 y15_Q3b_3 y15_Q3b_4 y15_Q3b_5 y15_Q3b_6 ///
			 y15_Q3b_7 y15_Q3b_8 y15_Q3b_9 y15_Q3b_10 {
	mvdecode `x', mv(888,999)
	replace numdep=numdep+1 if (`x'>=75 | `x'<=16) & `x'~=.
	}
by wave, sort : sum numdep

*@ What is the definition here? why is a dependent somebody below 16 or
*  above 75? An unemployed partner or a studying child is not a dependent?

*next, some needed background variables
mvdecode y15_Q2a, mv(8,9)
g male=y15_Q2a==1

label var male "Gender"
label def male 0 "Female" 1 "Male"
label val male male

*Different than in 2010.
tab emp_stat, gen(emp_stat_)

********************************************************************************
********************************1. WAGE INDEX***********************************
* (not to be considered, only present in w6)

g income_mth=inc_euro
mvdecode y15_Q24, mv(888)

g hours_mth=y15_Q24*4.33
g income_hr=income_mth/hours_mth
by wave, sort : sum  hours_mth income_hr
*@this is not the contractual hours, but the actual hours (which is good)

*** adjust to PPP, Source of PPP data is Eurostat ***
* Actually not PPP because everything is in Euro already.
* its the price level indices in 2014, for actual individual consumption.
* taken from Eurostat at 3 feb 2016

generate ppp=.


/*       Belgium */ replace ppp=111.1   if countid==1  & wave==6
/*      Bulgaria */ replace ppp=42.9    if countid==2  & wave==6
/*Czech Republic */ replace ppp=59.4    if countid==3  & wave==6
/*       Denmark */ replace ppp=139.6   if countid==4  & wave==6
/*       Germany */ replace ppp=101.3   if countid==5  & wave==6
/*       Estonia */ replace ppp=70.9    if countid==6  & wave==6
/*        Greece */ replace ppp=81.8    if countid==7  & wave==6
/*         Spain */ replace ppp=92.5    if countid==8  & wave==6
/*        France */ replace ppp=107.3   if countid==9  & wave==6
/*       Ireland */ replace ppp=125.1   if countid==10 & wave==6
/*         Italy */ replace ppp=102.7   if countid==11 & wave==6
/*        Cyprus */ replace ppp=90.7    if countid==12 & wave==6
/*        Latvia */ replace ppp=65.7    if countid==13 & wave==6
/*     Lithuania */ replace ppp=57.6    if countid==14 & wave==6
/*    Luxembourg */ replace ppp=135.2   if countid==15 & wave==6
/*       Hungary */ replace ppp=53.2    if countid==16 & wave==6
/*         Malta */ replace ppp=80.8    if countid==17 & wave==6
/*   Netherlands */ replace ppp=112.7   if countid==18 & wave==6
/*       Austria */ replace ppp=109.4   if countid==19 & wave==6
/*        Poland */ replace ppp=52.6    if countid==20 & wave==6
/*      Portugal */ replace ppp=79.7    if countid==21 & wave==6
/*       Romania */ replace ppp=48      if countid==22 & wave==6
/*      Slovenia */ replace ppp=81.1    if countid==23 & wave==6
/*      Slovakia */ replace ppp=63.4    if countid==24 & wave==6
/*       Finland */ replace ppp=123.9   if countid==25 & wave==6
/*        Sweden */ replace ppp=135.9   if countid==26 & wave==6
/*United Kingdom */ replace ppp=121.8   if countid==27 & wave==6
/*       Croatia */ replace ppp=62.6    if countid==28 & wave==6

/*         Swiss */ replace ppp=156.3   if countid==35 & wave==6
/*        Norway */ replace ppp=158     if countid==31 & wave==6
/*    Montenegro */ replace ppp=50.1    if countid==34 & wave==6
/*         FYROM */ replace ppp=41.6    if countid==29 & wave==6
/*       Albania */ replace ppp=41.4    if countid==32 & wave==6
/*        Serbia */ replace ppp=45.4    if countid==36 & wave==6
/*        Turkey */ replace ppp=54.1    if countid==30 & wave==6

/*       Belgium */ replace ppp=113.5   if countid==1  & wave==5
/*      Bulgaria */ replace ppp=44.1    if countid==2  & wave==5
/*Czech Republic */ replace ppp=69.4    if countid==3  & wave==5
/*       Denmark */ replace ppp=144.6   if countid==4  & wave==5
/*       Germany */ replace ppp=102.4   if countid==5  & wave==5
/*       Estonia */ replace ppp=68.5    if countid==6  & wave==5
/*        Greece */ replace ppp=92.3    if countid==7  & wave==5
/*         Spain */ replace ppp=96.9    if countid==8  & wave==5
/*        France */ replace ppp=111.1   if countid==9  & wave==5
/*       Ireland */ replace ppp=121.6   if countid==10 & wave==5
/*         Italy */ replace ppp=102.1   if countid==11 & wave==5
/*        Cyprus */ replace ppp=90.3    if countid==12 & wave==5
/*        Latvia */ replace ppp=63.7    if countid==13 & wave==5
/*     Lithuania */ replace ppp=58.3    if countid==14 & wave==5
/*    Luxembourg */ replace ppp=135.8   if countid==15 & wave==5
/*       Hungary */ replace ppp=57.1    if countid==16 & wave==5
/*         Malta */ replace ppp=74.2    if countid==17 & wave==5
/*   Netherlands */ replace ppp=111.8   if countid==18 & wave==5
/*       Austria */ replace ppp=109.4   if countid==19 & wave==5
/*        Poland */ replace ppp=55.9    if countid==20 & wave==5
/*      Portugal */ replace ppp=86.2    if countid==21 & wave==5
/*       Romania */ replace ppp=50.1    if countid==22 & wave==5
/*      Slovenia */ replace ppp=85.3    if countid==23 & wave==5
/*      Slovakia */ replace ppp=64.4    if countid==24 & wave==5
/*       Finland */ replace ppp=122.5   if countid==25 & wave==5
/*        Sweden */ replace ppp=125.6   if countid==26 & wave==5
/*United Kingdom */ replace ppp=108.6   if countid==27 & wave==5
/*       Croatia */ replace ppp=71.3    if countid==28 & wave==5

/*         Swiss */ replace ppp=152.5   if countid==35 & wave==5
/*        Norway */ replace ppp=157.5   if countid==31 & wave==5
/*    Montenegro */ replace ppp=50.8    if countid==34 & wave==5
/*         FYROM */ replace ppp=39.6    if countid==29 & wave==5
/*       Albania */ replace ppp=44.3    if countid==32 & wave==5
/*        Serbia */ replace ppp=46.9    if countid==36 & wave==5
/*        Turkey */ replace ppp=62.6    if countid==30 & wave==5

replace ppp=ppp/100

g inf=.

/*       Belgium */ replace inf=92.9    if countid==1  & wave==5
/*      Bulgaria */ replace inf=96.6    if countid==2  & wave==5
/*Czech Republic */ replace inf=92.6    if countid==3  & wave==5
/*       Denmark */ replace inf=94.1    if countid==4  & wave==5
/*       Germany */ replace inf=93.2    if countid==5  & wave==5
/*       Estonia */ replace inf=87.96   if countid==6  & wave==5
/*        Greece */ replace inf=99.27   if countid==7  & wave==5
/*         Spain */ replace inf=94.08   if countid==8  & wave==5
/*        France */ replace inf=94.05   if countid==9  & wave==5
/*       Ireland */ replace inf=96.2    if countid==10 & wave==5
/*         Italy */ replace inf=92.6    if countid==11 & wave==5
/*        Cyprus */ replace inf=95.09   if countid==12 & wave==5
/*        Latvia */ replace inf=92.96   if countid==13 & wave==5
/*     Lithuania */ replace inf=92.43   if countid==14 & wave==5
/*    Luxembourg */ replace inf=91.44   if countid==15 & wave==5
/*       Hungary */ replace inf=89.47   if countid==16 & wave==5
/*         Malta */ replace inf=91.79   if countid==17 & wave==5
/*   Netherlands */ replace inf=92.05   if countid==18 & wave==5
/*       Austria */ replace inf=90.14   if countid==19 & wave==5
/*        Poland */ replace inf=92.7    if countid==20 & wave==5
/*      Portugal */ replace inf=93.22   if countid==21 & wave==5
/*       Romania */ replace inf=87.73   if countid==22 & wave==5
/*      Slovenia */ replace inf=93.85   if countid==23 & wave==5
/*      Slovakia */ replace inf=91.69   if countid==24 & wave==5
/*       Finland */ replace inf=90.83   if countid==25 & wave==5
/*        Sweden */ replace inf=96.43   if countid==26 & wave==5
/*United Kingdom */ replace inf=89.4    if countid==27 & wave==5
/*       Croatia */ replace inf=92.55   if countid==28 & wave==5

/*         Swiss */ replace inf=101.4   if countid==35 & wave==5
/*        Norway */ replace inf=98.8    if countid==31 & wave==5
/*    Montenegro */ replace inf=90.46   if countid==34 & wave==5
/*         FYROM */ replace inf=79.11   if countid==29 & wave==5
/*       Albania */ replace inf=89.7    if countid==32 & wave==5
/*        Serbia */ replace inf=75.2    if countid==36 & wave==5
/*        Turkey */ replace inf=68.37   if countid==30 & wave==5

replace inf=100 if wave==6

*g ln_income_mth = ln(income_mth)
*reg ln_income_mth male i.agecat_5 i.countid i.wave i.education i.supervisor i.nace10 i.emp_stat_lt [pweight=w4], robust
*predict pred_income_mth
*gen pred_income_mth_conv=2.718281^(pred_income_mth)
*g remove = (income_mth/pred_income_mth_conv)>4

*** adjusted hourly income***
g adincome_mth=(income_mth*(100/inf))/ppp
g adincome_hr= (income_hr *(100/inf))/ppp
by wave, sort : sum  adincome_mth adincome_hr
**** removing outliers *********
*removing top and bottom quarter percentiles

*@ quite arbitary
*@ If we were to remove incomes, I would base this on HOURLY incomes rather than
*  monthly. That is used below.

xtile income_perc_2015 = adincome_hr if wave==6, nq(400)
xtile income_perc_2010 = adincome_hr if wave==5, nq(400)
replace adincome_mth=. if wave==6 & (income_perc_2015==1 |  income_perc_2015==400)
replace adincome_hr=. if wave==6 & (income_perc_2015==1 |  income_perc_2015==400)
replace adincome_mth=. if wave==5 & (income_perc_2010==1 |  income_perc_2010==400)
replace adincome_hr=. if wave==5 & (income_perc_2010==1 |  income_perc_2010==400)

label var adincome_mth "Monthly Earnings at PPP (euros)"
label var adincome_hr  "Hourly Earnings at PPP (euros)"
*hist adincome_mth if wave==6, percent xlabel(#10)
*hist adincome_mth if wave==5, percent xlabel(#10)

by wave, sort : sum adincome_mth

********************************************************************************
************************2. INTRINSIC JOB QUALITY********************************

*-------------------------------------------------------------------------------
*A) THE WORK ITSELF: SKILL AND AUTONOMY

*@Changes 2015:
*  ISCED has more levels now.
*  mean isced is calculated with weights

*@ Only real difference is more ISCED levels: scale still comparable to 2010

mvdecode y15_isco_08_2, mv(-1)
mvdecode y15_ISCED, mv(88,99)
mvdecode y15_ISCED_lt, mv(9)

*@isced variable has changed, now 9 categories
* (2015: 9 levels, from 1 to 9; 2010: 7 levels from 0 to 6, gen unique var isced)
g isced=y15_ISCED-1 /* (rescaled 0 to 8) */
replace isced=y15_ISCED_lt if wave==5 /* (scale 0 to 6, master and doctorate not present) */

*@ this needs to be weighted, done below
*(compute the mean of education by isco, rescaled 0-1 to make it comparable waves 5-6)
g aved2=.
qui sum y15_isco_08_2
qui forvalues i = 1/`r(max)' {
	sum isced [aweight=w4] if y15_isco_08_2 == `i' & wave==6, detail
    replace aved2 = r(mean)/8 if y15_isco_08_2 == `i' & wave==6
	sum isced [aweight=w4] if y15_isco_08_2 == `i' & wave==5, detail
	replace aved2 = r(mean)/6 if y15_isco_08_2 == `i' & wave==5
}

label var aved2 "Average Education Level in 2-Digit Occupation"

mvdecode y15_Q65c y15_Q53b y15_Q53c y15_Q53d y15_Q53e y15_Q53f y15_Q54a ///
y15_Q54b y15_Q54c y15_Q18c y15_Q30i, mv(8,9)
mvdecode y15_Q63e y15_Q63a y15_Q63b y15_Q63c y15_Q63d y15_Q63f y15_Q61c ///
y15_Q61d y15_Q61e y15_Q61h  y15_Q61i y15_Q61j  y15_Q61n, mv(7,8,9)

*(the following vars are answers yes=1 and no=2 and are recoded as yes=1 and no=0)
foreach x of varlist training y15_Q65c y15_Q53b y15_Q53c y15_Q53d y15_Q53e ///
y15_Q53f y15_Q54a y15_Q54b y15_Q54c   {
	g `x'p=`x'
	recode `x'p 2=0
	}

*(the following vars are answers from 1=strongly agree to 5=strongly disagree)
*(the are reversed and standardized as from 0 (stronglhy disagree) to 1 (strongly agree)
foreach y of varlist y15_Q63e y15_Q63a y15_Q61c y15_Q61d y15_Q61e y15_Q61h ///
y15_Q61i y15_Q61j y15_Q61n y15_Q63b y15_Q63c y15_Q63d y15_Q63f y15_Q18c {
	g `y'p=(5-`y')/4
	}

mvdecode y15_Q60* y15_Q55 y15_Q56 y15_Q64, mv(8,9)

g meaning = y15_Q61hp+y15_Q61jp

* For the team in which you work mostly, do the members decide by themselvesâ€¦?
* A - â€¦ on the division of tasks (yes=1 2=no)
g teamaut=0
foreach x of varlist y15_Q60*	{
	replace teamaut = teamaut + 2-`x' if `x'~=. /* (increases by if "yes") */
	replace teamaut=0.25*teamaut
	}
*sum over 4 items and then ?????
replace teamaut=teamaut/3
label var teamaut "Team discretion"

g jobrot=0 if y15_Q55~=.
replace jobrot=1 if y15_Q56==1
label var jobrot "Job rotation with different skills"
g skmatch=0 if y15_Q64~=.
replace skmatch=1 if y15_Q64==2
label var skmatch "Skills Match"
*@ this assumes that either under or overuse of skills is negative.
*  Is that really the case?

mvdecode y15_isco_08_1, mv(-1)

g manprof= 0 if y15_isco_08_1~=.
replace manprof =1 if y15_isco_08_1>=1 & y15_isco_08_1<=3

g comp= (7-y15_Q30i)/6

*@Replication of 2010
*alpha trainingp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
*y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np, item ///
*g(wq)

*msp trainingp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
*y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np

*@Alternative (new)
*alpha trainingp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
*y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np      ///
*y15_Q61dp y15_Q18cp, item g(wq_a)
*@ y15_Q61dp works very well, and y15_Q18cp less so

by wave, sort : sum trainingp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
	y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np      ///
	y15_Q61dp

*@Alternative (new) (item=check the constructed vars)
forvalues i=5/6 {
	alpha trainingp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
	y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np      ///
	y15_Q61dp if wave==`i', item
}
qui alpha trainingp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
	y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np      ///
	y15_Q61dp if wave>4,  item g(wq)

*msp y15_Q65cp y15_Q53cp y15_Q53ep y15_Q53fp aved2 manprof comp ///
*y15_Q54ap y15_Q54bp y15_Q54cp y15_Q61cp y15_Q61ep y15_Q61ip y15_Q61np      ///
*y15_Q61dp y15_Q18cp

*(scale from 0-1 to 0-100)
replace wq = 100*wq
label var wq "Skills and Discretion"

by wave, sort : sum  trainingp y15_Q54ap y15_Q54bp y15_Q54cp y15_Q53cp y15_Q53ep y15_Q53fp
*Skills and discretion slim
forvalues i=2/6 {
	alpha trainingp y15_Q54ap y15_Q54bp y15_Q54cp y15_Q53cp y15_Q53ep y15_Q53fp if wave==`i', item
	}

qui alpha trainingp y15_Q54ap y15_Q54bp y15_Q54cp y15_Q53cp y15_Q53ep y15_Q53fp if wave>1, item g(wq_slim)

replace wq_slim = 100*wq_slim
label var wq_slim "Skills and Discretion slim"

by wave, sort : sum wq wq_slim
*-------------------------------------------------------------------------------
*B)GOOD SOCIAL ENVIRONMENT

*@ INCLUDED
*  Wording and scale of Q69=3 (manager quality) has changed.

*@ NOT INCLUDED:
*  Q58C: Is good at resolving conflicts: discontinued
*  Q58D: Is good at planning and organising the work: discontinued
*  Q58E: Encourages you to participate in important decisions: discontinued
*  Q77E: friends at work: discontinued

*@ Conclusion: not comparable to 2010

mvdecode y15_Q61a y15_Q61b, mv(7,8,9)

g collsup=(5-y15_Q61a)/4

*only includes managers support from employees; if self-employed, not recorded
g mansup=(5-y15_Q61b)/4

*alpha y15_Q63ap y15_Q63ep, item g(manqual)
*label var manqual "Manager Quality"

*@Alternative
alpha y15_Q63*p , item g(manqual)
*@works perfectly

*alpha collsup  mansup manqual ,  item g(support)
*msp collsup  mansup manqual
*@still works quite well without the friends
*@Alternative
alpha collsup  mansup manqual ,  item g(support)
*@works well
*msp collsup  mansup manqual_a

mvdecode y15_Q80a y15_Q80b y15_Q80c y15_Q80d y15_Q81a y15_Q81b y15_Q81c, mv(8,9)

*next, absence of any type of abuse
g noabuse=1
replace noab=0 if y15_Q80a==1 | y15_Q80b==1 | y15_Q80c==1 | y15_Q80d==1 | ///
				  y15_Q81a==1 | y15_Q81b==1 | y15_Q81c==1

*msp	  y15_Q80a y15_Q80b y15_Q80c y15_Q80d y15_Q81a y15_Q81b y15_Q81c

g goodsoc = support + noabuse
*this weights social support, and lack of abuse, equally; seems reasonable
replace goodsoc=goodsoc*50

*scales to 100

label var goodsoc "Good Social Environment"
replace goodsoc=. if wave!=6
sum goodsoc
*hist goodsoc, percent xlabel(#10) yscale(range(0 20))


*--------------------
*C) GOOD PHYSICAL ENVIRONMENT
*i.e. the obverse of environmental risk; i.e. the extent to which the work envir
*onment is free from potential sources of harm to health and well-being
*omits computer use and internet

mvdecode y15_Q29* y15_Q30*, mv(8,9)

forvalues i=5/6 {
	alpha y15_Q29* y15_Q30a y15_Q30b y15_Q30c y15_Q30e if wave==`i', item
}

qui alpha y15_Q29* y15_Q30a y15_Q30b y15_Q30c y15_Q30e if wave>=4, item g(z)

*msp y15_Q29* y15_Q30a y15_Q30b y15_Q30c y15_Q30e

g envsec=0 if z~=.
foreach x of varlist y15_Q29* y15_Q30a y15_Q30b y15_Q30c y15_Q30e {
	replace envsec=envsec+6 if `x'==. & z~=.
	replace envsec=envsec+`x'-1 if `x'~=. & z~=.
}

replace envsec=100*envsec/78
g envinsec=100-envsec

label var envsec "Good Physical Environment"
label var envinsec "Environmental Risk"

*hist envsec, percent xlabel(#10)

*Physical risk slim

by wave, sort : sum  y15_Q29* y15_Q30a y15_Q30b y15_Q30c y15_Q30e

alpha y15_Q29a y15_Q29b y15_Q29c y15_Q29d y15_Q29e y15_Q29g  y15_Q30a  y15_Q30c  y15_Q30e if wave>1, item g(z_slim)

g envsec_slim=0 if z_slim~=.
foreach x of varlist y15_Q29a y15_Q29b y15_Q29c y15_Q29d y15_Q29e y15_Q29g  y15_Q30a  y15_Q30c  y15_Q30e {
	replace envsec_slim=envsec_slim+6 if `x'==. & z_slim~=.
	replace envsec_slim=envsec_slim+`x'-1 if `x'~=. & z_slim~=.
}

replace envsec_slim=100*envsec_slim/54
g envinsec_slim=100-envsec_slim
label var envsec_slim "Good Physical Environment slim"

by wave, sort : sum envsec envsec_slim

*--------------------------------------
*D)WORK INTENSITY

*Emotionally disturbing situations is new: cannot produce work intensity for 2010

*we use three item sets: the speed/tight deadlines; number of work pressure
*sources; demands from emotional and value conflicts

mvdecode y15_Q49* y15_Q30g y15_Q30h, mv(8,9)
mvdecode y15_Q61* y15_Q50*, mv(7,8,9)

foreach y of varlist y15_Q49* y15_Q30g y15_Q30h {
	g `y'p=(7-`y')/6 if `y'~=.
	}


	foreach y of varlist y15_Q61o y15_Q61g {
	g `y'p=(5-`y')/4 if `y'~=.
	}

g wp=0
g wpm=0
foreach x of varlist y15_Q50* {
	replace wp=wp+2-`x' if `x'~=.
	replace wpm=wpm+1 if `x'==.
}
label var wp "Number of Work Pressure Sources"
label var wpm "Number of Work Pressure Missing Values"

replace wp=wp/5


*alpha y15_Q61op y15_Q30gp, casewise item g(vconfl)
*msp y15_Q61op y15_Q30gp
alpha y15_Q61op y15_Q30gp y15_Q30hp, casewise item g(vconfl)
*msp y15_Q61op y15_Q30gp y15_Q30hp

label var vconfl "Emotional or Value Conflict"
label var y15_Q61gp "Time Pressure During Worktime"

replace y15_Q61gp=1-y15_Q61gp

*alpha y15_Q49ap y15_Q49bp wp y15_Q61gp vconfl, item g(intens)
*msp y15_Q49ap y15_Q49bp wp y15_Q61gp vconfl
*answer 0.68, just about acceptable

*@alternative
alpha y15_Q49ap y15_Q49bp wp y15_Q61gp vconfl freq_dis_int if wave==6, item g(intens)
*msp y15_Q49ap y15_Q49bp wp y15_Q61gp vconfl_a disrupt

*cut those few with missing on both Q45 items, so not wholly dependent on the
*work pressure items
replace intens=. if y15_Q49ap==. & y15_Q49bp==.
replace intens=100*intens

g effabs=100-intens

*hist intens, percent xlabel(#10) yscale(range(0 4.5))

*Intensity slim

by wave, sort : sum  y15_Q49ap y15_Q49bp y15_Q50* wp freq_dis_int y15_Q61gp

alpha y15_Q49ap y15_Q49bp wp if wave>1, item g(intens_slim)
replace intens_slim=. if y15_Q49ap==. & y15_Q49bp==.
replace intens_slim=100*intens_slim
label var intens "Intensity (more is worse)"
label var intens_slim "Intensity_slim (more is worse)"
by wave, sort : sum  intens intens_slim


*-----------------------------------------

g ijq=0.25*(wq+effabs+goodsoc+envsec)

g ijqp=0.3*wq + 0.3*goodsoc +0.3*envsec + 0.1*effabs if wave==6
label var ijq "Intrinsic Job Quality"

sum ijq
*hist ijq, percent xlabel(#10) yscale(range(0 7))


*------------------------------------

*3. EMPLOYMENT QUALITY

*@ change in employment is new question: only 2015. Also emp_stat has changed.

*g esec=Q77F*(6-Q77A)
*combines employability with the obverse of "chance of job loss"
*label var esec "Employment Security"

mvdecode y15_Q89g y15_Q89h y15_Q89b, mv(7,8,9)

g einsec=(y15_Q89g-1)/4 + (5-y15_Q89h)/4 + (y15_Q89g-1)*(5-y15_Q89h)/16
label var einsec "Employment Insecurity"
*combines chance of job loss with difficulty of re-employment
g esec = 3-einsec
replace esec=100*esec/3
label var esec "Employment Security"

g indef=0 if emp_stat==.
replace indef = 1 if emp_stat<=3
label var indef "Indefinite contract or self-employed"

g js =(y15_Q89g-1)/4
label var js "Job Security"
g cp = (5-y15_Q89b)/4
label var cp "Career Progression"

*g templong=0 if Q6==3
*replace templong=1 if (Q7==2|Q7==3) & (Q8A>1&Q8A<50)
*g tempshort=0 if Q6==3
*replace tempshort=1 if (Q7==2|Q7==3) & (Q8A<=1|Q8A==.)

g contrqual=0 if y15_Q11==5
replace contrqual=0.5 if y15_Q11<5&y15_Q11>1
replace contrqual=1 if y15_Q11==1
replace contrqual=. if y15_Q11==.

g ec = (3-empl_change)/2

*alpha js cp contrqual, item g(prosp)
*msp js cp contrqual

alpha ec js cp contrqual if wave==6, item g(prosp)

*msp ec js cp contrqual
replace prosp=100*prosp

label var prosp "Prospects"

sum prosp
*hist prosp, percent xlabel(#10) yscale(range(0 17))
*we use empq as this is derived solely from the job; whereas employment security
* involves employability, which depends more on the individual

*@ alpha is very low for prospects
*  the alpha is used to assess the reliability, but the outcomes are not
*systematically applied

********************************************************************************
******************************* Work-life balance ******************************
********************************************************************************

*@ Hours rest is new: only 2015.

*use "C:\D\edu\LLAKES\bids\eurofound\data\data_used\EWCS 2010 - Master for
*external use.dta"

*** recoding variables ***

 *** working hours per week ***
generate workh=.
replace workh=100 if y15_Q24==0 & y15_Q24<20
replace workh=75 if y15_Q24>=20 & y15_Q24<38
replace workh=50 if y15_Q24>=38 & y15_Q24<42
replace workh=25 if y15_Q24>=42 & y15_Q24<48
replace workh=0 if y15_Q24>=48 & y15_Q24<200

*@ parttime=better. Is that really true?

replace workh=100*(workh!=0)

mvdecode y15_Q37* ,mv(88,99)

*** work at night ***
generate night1=.
replace night1=100 if  y15_Q37a==00
replace night1=75 if  y15_Q37a>=1 &  y15_Q37a<=5
replace night1=50 if  y15_Q37a>=6 &  y15_Q37a<=10
replace night1=25 if  y15_Q37a>=11 &  y15_Q37a<=20
replace night1=0 if  y15_Q37a>20 &  y15_Q37a<=80

** more than 10 hours a day **
g longday=.
replace longday=100 if y15_Q37d==0
replace longday=75 if y15_Q37d>=1 & y15_Q37d<=5
replace longday=50 if y15_Q37d>=6 & y15_Q37d<=10
replace longday=25 if y15_Q37d>=11 & y15_Q37d<=20
replace longday=0 if y15_Q37d>=20 & y15_Q37d<=80

** norest**

g norest=(y15_Q38==2)*100

*** work on sundays ***
generate sunday1=.
replace sunday1=100 if y15_Q37b==00
replace sunday1=75 if y15_Q37b==1
replace sunday1=50 if y15_Q37b==2
replace sunday1=25 if y15_Q37b==3
replace sunday1=0 if y15_Q37b>=4 & y15_Q37b<=80

*** work on saturdays ***
generate saturday1=.
replace saturday1=100 if y15_Q37c==00
replace saturday1=75 if y15_Q37c==1
replace saturday1=50 if y15_Q37c==2
replace saturday1=25 if y15_Q37c==3
replace saturday1=0 if y15_Q37c>=4 & y15_Q37c<=80

mvdecode y15_Q42 y15_Q43 y15_Q47, mv(8,9)

*** working arrangements ***
g workar=(y15_Q42==1 & y15_Q43!=1)*100
replace workar=25 if y15_Q42==1 & y15_Q43==1
replace workar=50 if y15_Q42==2
replace workar=75 if y15_Q42==3
replace workar=100 if y15_Q42==4

generate workar2=100 if y15_Q42~=1 | (y15_Q42==1 & y15_Q43==1)
replace  workar2=80 if  y15_Q42==1  & y15_Q43==5
replace  workar2=60 if  y15_Q42==1  & y15_Q43==4
replace  workar2=40 if  y15_Q42==1  & y15_Q43==3
replace  workar2=20 if  y15_Q42==1  & y15_Q43==2


*** taking a couple of hours off ***
generate freeh=.
replace freeh=0 if y15_Q47==4
replace freeh=33.33 if y15_Q47==3
replace freeh=66.66 if y15_Q47==2
replace freeh=100 if y15_Q47==1


**work in free time ***
mvdecode y15_Q46, mv(7,8,9)
g y15_Q46p=((y15_Q46-1)/4)*100 if y15_Q46~=.

*Short notice
mvdecode y15_Q40, mv(7,8,9)
g y15_Q40p=(y15_Q40-1)/4

********************************************************************************
*** creating the work life balance index ***

*alpha night1 sunday1 saturday1, item g(shift) asis
alpha  night1 sunday1 saturday1 shiftwork if wave>1 , item g(shift) asis
*alpha workh shift workar freeh, item g(wlb) asis
alpha workh shift workar2 freeh longday norest y15_Q46p y15_Q40p if wave==6, item g(wlb) asis

label var wlb "Working Time Quality"

*hist wlb, percent xlabel(#10) yscale(range(0 9))

*Working time slim
by wave, sort : sum workh shift
alpha workh shift if wave>1, item asis g(wlb_slim)
label var wlb_slim "Working Time Quality slim"
by wave, sort : sum wlb wlb_slim



log close

compress

*save "`output'\JQI_2015.dta", replace
*savespss "`output'\JQI_2015_full.sav", replace

*saveold "`work'\extratests.dta", replace
*savespss "`work'\extratests.sav", replace

keep casenum wave goodsoc adincome_mth adincome_hr wq wq_slim envsec envsec_slim intens intens_slim ijq prosp wlb wlb_slim swb hp jobsat heff wlb_outcome meaning manqual
sort casenum wave

savespss "`work'\JQI_2703.sav", replace
