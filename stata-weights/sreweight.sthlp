{smcl}
{* Sept2012/}{...}
{cmd:help sreweight}{right: ({browse "http://www.stata-journal.com/article.html?article=st0322":SJ14-1: st0322})}
{hline}

{title:Title}

{p2colset 5 18 20 2}{...}
{p2col :{hi:sreweight} {hline 2}}Reweight survey variables using external totals{p_end}
{p2colreset}{...}


{title:Syntax}

{p 8 15 2}{cmd:sreweight}
{varlist} {ifin}{cmd:,}
{opth sw:eight(varname)}
{opth nw:eight(newvar)}
{cmdab:tot:al}({it:matrix})
{cmdab:df:unction}({it:name})
[{cmdab:sv:alues}({it:matrix})
{cmdab:tol:erance(}{it:#}{cmd:)}
{cmdab:nit:er(}{it:#}{cmd:)}
{cmdab:nt:ries(}{it:#}{cmd:)}
{cmdab:upb:ound(}{it:#}{cmd:)}
{cmdab:lowb:ound(}{it:#}{cmd:)}
{cmdab:rb:ounds(}{it:#}{cmd:)}
{cmdab:rlowb:ound(}{it:# #}{cmd:)}
{cmdab:rupb:ound(}{it:# #}{cmd:)}]


{title:Description}

{pstd}
{cmd:sreweight} calibrates survey data to external totals.  The methodology
closely follows Deville and S{c a:}rndal (1992), and the recursive algorithm
that implements the calibration is from Creedy (2003).


{title:Options}

{phang}
{opth sweight(varname)} specifies a numeric variable to be used for the
original survey weights.  {cmd:sweight()} is required.

{phang}
{opth nweight(newvar)} contains the name of the variable to be
created with the new weights.  {cmd:nweight()} is required.

{phang}
{opt total(matrix)} contains a 1 x K matrix with the user-provided totals,
which is ordered as the variables in {varlist}.  The arguments must be
inserted in the same order as the K calibrating variables in {it:varlist}.
{cmd:total()} is required.

{phang}
{opt dfunction(name)} specifies the distance function to be used when
computing the new weights.  The allowed functions are the chi-squared
({cmd:chi2}), the modified chi-squared ({cmd:mchi2}), Deville and
S{c a:}rndal's (1992) function ({cmd:ds}), and the functions we defined as
type A ({cmd:a}), type B ({cmd:b}), and type C ({cmd:c}).  Note that for all
functions but the chi-squared, {cmd:sreweight} works with the recursion
outlined in the previous section.  {cmd:dfunction()} is required.

{phang}
{opt svalues(matrix)} specifies user-provided starting values.  Starting
values must be put in a Stata 1 x K matrix following the same order as the
variables in {varlist}.  The default is a vector with the Lagrange multipliers
obtained from the chi-squared distance function.

{phang}
{opt tolerance(#)} specifies the tolerance level that enters the iterative
algorithm to declare convergence.  The default is {cmd:tolerance(0.000001)}.
{cmd:sreweight} uses a double criterion to assess convergence.  The first is
that the difference between the estimated and external totals must be lower
than the tolerance level.  The second is that from one iteration to the other,
the percentage variations of the estimated distance between the new and the
original weights must be lower than the tolerance level for each observation
in the sample.

{phang}
{opt niter(#)} specifies the number of maximum iterations.  The default is
{cmd:niter(50)}.

{phang}
{opt ntries(#)} specifies the maximum number of "tries" when the algorithm
does not achieve convergence within the maximum number of iterations.  This
option can be useful when the external totals are significantly different from
the survey totals.  In such situations, the algorithm automatically restarts
with new random starting values up to {it:#} times.  The default is
{cmd:ntries(0)}.

{phang}
{opt upbound(#)} specifies the upper bound of the ratio between the new and
the original weights when using either the modified chi-squared or Deville and
S{c a:}rndal's (1992) distance function.  The default is {cmd:upbound(4)}.
Note that this value must be bigger than 1.

{phang}
{opt lowbound(#)} specifies the lower bound of the ratio between the new and
the original weights when using either the modified chi-squared or Deville and
S{c a:}rndal's (1992) distance function.  The default is {cmd:lowbound(0.2)}.
Note that this value must be between 0 and 1.

{phang}
{opt rbounds(#)} is a relevant option only for the modified chi-squared and
Deville and S{c a:}rndal's (1992) distance functions when the {cmd:ntries()}
option is effective.  In this case, if the recursion does not achieve
convergence, the algorithm restarts with both a new set of starting values and
a new set of random bounds.  The allowed values for this option are {cmd:0}
(no random bounds) and {cmd:1} (allow for random bounds).  The default is
{cmd:rbounds(0)}.

{phang}
{opt rlowbound(# #)} and {opt rupbound(# #)} are relevant options only for the
modified chi-squared and Deville and S{c a:}rndal's (1992) distance functions
when the options {cmd:ntries()} and {cmd:rbounds()} are both effective.  In
this case, the two values in {opt rlowbound()} (or {opt rupbound()})
define the support of the uniform distribution from which the new lower (or
upper) bound is drawn.  Hence, if the user sets {cmd:rlowbound(0.2 0.8)}, the
new lower bound will be drawn from a uniform distribution with support
0.2-0.8.  When the {cmd:rbounds()} option is effective, the default values for
these options are {cmd:rlowbound(0.1 0.7)} and {cmd:rupbound(1.5 6)}.


{title:Example}

{pstd}
Consider the following example from Creedy (2003).  {cmd:id} is the
identification number of each unit included in the survey, {cmd:x1}, {cmd:x2},
{cmd:x3}, and {cmd:x4} are variables included in the survey, and {cmd:weight}
is the vector of original survey weights:

{phang2}{cmd}. use http://fmwww.bc.edu/RePEc/bocode/s/sreweight{p_end}
{phang2}. list{p_end}

        id	        x1	x2	x3	x4	weight
        1	        1	1	0	0	3
        2        	0	1	0	0	3
        3        	1	0	2	0	5
        4        	0	0	6	1	4
        5        	1	0	4	1	2
        6	        1	1	0	0	5
        7	        1	0	5	0	5
        8        	0	0	6	1	4
        9        	0	1	0	0	3
        10    	        0	0	3	1	3
        11	        1	0	2	0	5
        12       	1	1	0	1	4
        13        	1	0	3	1	4
        14	        1	0	4	0	3
        15              0	0	5	0	5
        16       	0	1	0	1	3
        17	        1	0	2	1	4
        18	        0	0	6	0	5
        19	        1	0	4	1	4
        20       	0	1	0	0	3{txt}

{pstd}The survey weights produce the following aggregate totals:

{cmd}        1.    tabstat x1   x2   x3    x4 [w=weight], s(su)
        2.    stats   x1   x2   x3    x4
        3.    sum     44   24   213   32{txt}

{pstd}Now let us assume that external information on these variables are
available and that the real population totals are

        {cmd}stats   x1      x2      x3      x4
                50      20      230     35{txt}

{pstd}In this case, {cmd:sreweight} can be used to calibrate the original
survey weights so that the new estimated totals will be equal to the
population totals:

{phang2}{cmd:. matrix t=(50 \ 20 \ 230 \ 35)}{p_end}
{phang2}{cmd:. sreweight x1 x2 x3 x4, sweight(weight) nweight(wchi2) total(t) dfunction(chi2)}{p_end}
{phang2}{cmd:. sreweight x1 x2 x3 x4, sweight(weight) nweight(wa) total(t) dfunction(a)}{p_end}
{phang2}{cmd:. sreweight x1 x2 x3 x4, sweight(weight) nweight(wb) total(t) dfunction(b)}{p_end}
{phang2}{cmd:. sreweight x1 x2 x3 x4, sweight(weight) nweight(wc) total(t) dfunction(c)}{p_end}
{phang2}{cmd:. sreweight x1 x2 x3 x4, sweight(weight) nweight(wds) total(t) dfunction(ds)}{p_end}

{phang2}{cmd:. list w*}{p_end}{cmd}
         weight	wchi2	wa	wb	wc	wds
         3      2.753   2.674   2.654   2.697   2.706
         3      2.109   2.228   2.260   2.193   2.178
         5      5.945   5.998   6.012   5.982   5.976
         4      4.005   3.944   3.926   3.963   3.974
         2      2.484   2.514   2.521   2.505   2.501
         5 	4.589   4.456   4.423   4.495   4.510
         5      5.752   5.729   5.717   5.739   5.747
         4      4.005   3.944   3.926   3.963   3.974
         3      2.109   2.228   2.260   2.193   2.178
         3      3.120   3.086   3.074   3.098   3.106
         5      5.945   5.998   6.012   5.982   5.976
         4      3.985   3.814   3.762   3.870   3.897
         4      5.019   5.108   5.136   5.080   5.065
         3      3.490   3.490   3.487   3.491   3.494
         5      4.678   4.665   4.666   4.667   4.665
         3      2.345   2.370   2.380   2.360   2.355
         4      5.070   5.191   5.232   5.150   5.128
         5      4.614   4.603   4.604   4.603   4.600
         4      4.967   5.028   5.043   5.010   5.001
         3      2.109   2.228   2.260   2.193   2.178{txt}

{pstd}This gives the same values as in Creedy (2003).


{title:References}

{phang}
Creedy, J.  2003.  Survey reweighting for tax microsimulation modelling.
Treasury Working Paper Series 03/17, New Zealand Treasury.

{phang}
Deville, J.-C., and C.-E. S{c a:}rndal.  1992.  Calibration estimators in
survey sampling.  {it:Journal of the American Statistical Association} 87:
376-382.


{title:Author}

{pstd}Comments and suggestions are welcome.

{pstd}Daniele Pacifico{p_end}
{pstd}Italian Department of the Treasury{p_end}
{pstd}Rome, Italy{p_end}
{pstd}daniele.pacifico@tesoro.it{p_end}


{title:Also see}

{p 4 14 2}Article:  {it:Stata Journal}, volume 14, number 1: {browse "http://www.stata-journal.com/article.html?article=st0322":st0322}{p_end}
