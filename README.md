
# Photometric analysis of Gaia + PS1 data

0. [Synthetic clusters analysis](#synth)
1. [Raw data processing](#raw)
2. [Data analysis with ASteCA](#dataanalysis)
3. [Final remarks](#finalremarks)
4. [Old analysis](#oldanalysis)
    1. [1st run](#1run)
    1. [2nd run](#2run)
    1. [3rd run](#3run)
    1. [4th run](#4run)
    1. [5th run](#5run)
    1. [6th run](#6run)
    1. [7th run](#7run)
    1. [8th run](#8run)
    1. [9th run](#9run)
    1. [10th run](#10run)
    1. [11th run](#11run)
    1. [12th run](#12run)
    1. [13th run](#13run)
    1. [14th run](#14run)
    1. [15th run](#15run)
    1. [16th run](#16run)
    1. [17th run](#17run)
    1. [18th run](#17run)
    1. [19th run](#17run)


<a name="synth"></a>
## Synthetic clusters analysis

The Bayesian method to estimate the fundamental parameters was tested on 108 synthetic clusters. These are stored in the `0_synth_gaia_clusts_test/input/` folder. The `output/` folder is kept out of the repo because it is too large (~1.2 Gb).


<a name="raw"></a>
## Raw data processing

The data was downloaded and prepared as described in the following steps, and
stored in the enumerated folders:

* `1_queried_gaia_data/` Data obtained with the `GaiaQuery` code, which
also adds colors and its errors.
* `2_raw_PS1_data/` Data obtained with the `CatalogMatch` code, using the GAIA
data from the 1st step as input.
* `3_matched_data/` Output after running the `CatalogMatch` code, using the GAIA
data from the 1st step as input and cross-matching with the raw PS1 data from
the 2nd step.
* `4_final_raw_data` Data that was actually processed by `ASteCA`. It is the
`_match.dat` output from `CatalogMatch` processed by the `GAIA_PS1_comb.py`
script to select a few columns and add the PS1 colors and their errors.


<a name="dataanalysis"></a>
## Data analysis with ASteCA

After processing the raw data, it is fed to `ASteCA` for the full analysis.

Parameters for the `semi_input.dat` file for all runs:

```
NAME                c_x          c_y          rad     f_regs    MC  MR  MF
GAIA1                 0.           0.        .15         10     2   1   1
GAIA2                 0.           0.        .07         10     2   1   1
GAIA4                 0.           0.        .06         10     2   1   1
GAIA5                 0.           0.        .05         10     2   1   1
GAIA6                 0.           0.        .06         10     2   1   1
GAIA7               0.01           0.       .035         10     2   1   1
```

The PARSEC v1.2 isochrones were used with ranges:

|  Param   |   Min |  Max |  Step  |
|:--------:|:-----:|:----:|:------:|
|    z     | 0.001 | 0.06 |  0.001 |
| log(age) |   7   |  10  | 0.0075 |

in the GaiaDR2 (*Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from
Evans et al. 2018)*) and Pan-STARRS1 systems.

The published age and distance values for the clusters are:

|  Cluster | log(age) | mu_0 |
|:--------:|:--------:|:----:|
|  GAIA1   |    9.8   | 13.3 |
|  GAIA2   |    9.9   | 13.6 |
|  GAIA4   |    9.    | 13.7 |
|  GAIA5   |     ?    | 14.2 |
|  GAIA6   |     ?    | 11.9 |
|  GAIA7   |    7.85  | 13.1 |

The GAIA7 cluster also is said to be affected by a large extinction: E_BV=1.2.







<a name="oldanalysis"></a>
## Old analysis

This is the original analysis performed between late 2018 and early 2019.


<a name="1run"></a>
### 1st run

#### Input parameters

Colors used:

```
GAIA1              i-z     g-r
GAIA(2,4,5,6,7)    BP-RP   i-z
```

The `BP-RP` color for GAIA1 contains very large errors and even a cut at
`err_max=0.05` (which removes a lot of stars) still leaves behind a CMD
with a tail of stars towards the left and down in the `BP-RP`-`G` axis.

Maximum error values:

```
GAIA1              0.05
GAIA(2,4,5,6,7)    0.1
```

In general the `BP-RP` color contains very large errors for all the clusters.
The `ptemcee` parameters are:

```
     ntemps    nwalkers   nburn    nsteps     Tmax   adapt    priors
PT       10         100    1000     20000       30      y       unif
```

and the synthetic cluster parameters are:

|  Name |       z         |   log(age)   |  M (x10^3) | E_BV |  mu_0 |
|:-----:|:---------------:|:------------:|:----------:|:----:|:-----:|
| GAIA1 | .001-.06 (.002) | 9-10 (.0075) | .1-10 (.1) |  0-2 | 13-15 |
| GAIA2 |         "       | 9-10 (  "  ) |      "     |   "  | 13-14 |
| GAIA4 |         "       | 8.5-10 ( " ) |      "     |   "  | 12-14 |
| GAIA5 |         "       | 7.-10 (  " ) |      "     |   "  | 13-15 |
| GAIA6 |         "       | 7.-10 (  " ) |      "     |   "  | 11-14 |
| GAIA7 |         "       | 7.-10 (  " ) |      "     |   "  | 12-14 |

> Using 0.001 as step for `z` caused a memory error, which is why I increased
it to 0.002. Using `Tmax=n` caused the last 5 temperatures to have parameter
values of `nan`, so I used `30` instead. Each run took approx 14 hs to
complete.

#### Output parameters

The A-D test gave these values for the photometric and plx+PMs test:

| Name  | phot | plx+PM |
|:-----:|:----:|:------:|
| GAIA1 | 0.16 |  1.00  |
| GAIA2 | 0.64 |  0.78  |
| GAIA4 | 0.18 |  0.24  |
| GAIA5 | 0.32 |  0.18  |
| GAIA6 | 0.55 |  0.50  |
| GAIA7 | 0.57 |  0.39  |

The estimated distance moduli are:

|  Cluster |  Plx   | Ph (mean) | Ph (map) |   Lit  | Plx-Lit |
|:--------:|:------:|:---------:|:--------:|:------:|:-------:|
|  GAIA1   | 13.99  |   13.47   |   13.50  |  13.30 |  0.69   |
|  GAIA2   | 13.33  |   13.82   |   13.76  |  13.60 | -0.27   |
|  GAIA4   | 12.42  |   13.28   |   12.98  |  13.70 | -1.28   |
|  GAIA5   | 14.30  |   14.45   |   14.50  |  14.20 |  0.10   |
|  GAIA6   | 13.29  |   13.21   |   13.31  |  11.90 |  1.39   |
|  GAIA7   | 13.79  |   13.56   |   13.65  |  13.10 |  0.69   |

The estimated ages are:

|  Cluster |  Mean |  MAP  |  Lit  | Mean-Lit |
|:--------:|:-----:|:-----:|:-----:|:--------:|
|  GAIA1   | 9.490 | 9.535 |  9.8  |  -0.31   |
|  GAIA2   | 9.542 | 9.67  |  9.9  | -0.358   |
|  GAIA4   | 9.725 | 9.752 |  9.0  |  0.725   |
|  GAIA5   | 8.298 | 8.957 |   ?   |    --    |
|  GAIA6   | 9.482 | 9.415 |   ?   |    --    |
|  GAIA7   | 9.595 | 9.542 |  7.85 |  1.745   |


#### Remarks about the analysis

* **GAIA1** The photometric distance and the mass seem to be a bit
underestimated. The color-color diagram is completely dispersed. The
metallicity is located around a solar value.

* **GAIA2** The (mean) synthetic cluster fit is very reasonable. Almost all
the parameters show a bimodality in their distributions: the metallicity
has peaks at 0.03 (larger) and 0.05, the log(age) at 9.3 and 9.7 (larger),
the extinction at 0.22 (larger) and 0.26, the distance at 13.7 and 13.9,
and the mass at 1500 and 2200.

* **GAIA4** The post-decontamination sequence does not resemble a cluster.
The stars trace either no cluster or a *very* old one. The distance and age
found are *very* different from the literature values, because Torrealba et al.
fit the entire sequence including some stars to the right of the CMD that are
not present in our CMD. Large extinction and mass values are also assigned.

* **GAIA5** The synthetic cluster fit is rather poor, mainly because the
cluster sequence is not clearly defined in the post-decontamination
distribution. The metallicity, age, and distance uncertainties are *enormous*.
The distributions for these three parameters span almost the entire dynamical
ranges given.

* **GAIA6** The fitted (mean) synthetic cluster does not follow the sequence
up to the brightest stars, because they have small MPs. The turn-off point thus
gives a distance value that is quite larger than the one in the literature.
This photometric distance is *very similar* to the parallax distance, which
means that the literature value is wrong. The distributions for the parameters
look not so normal.

* **GAIA7** very similar to GAIA4, the decontamination process leaves no
discernible sequence to be fitted (or a *very* old one). The age assigned is
*very* different from the one in the literature because Torrealba et al. fit
the sequence up to the brightest stars which are either removed or assigned
very low MPs by the decontamination algorithm.

> The clusters with the **poorest fits** are: 4, 5 and 7. This coincides with
the A-D test, as these are the three clusters with the lowest Plx+PM p-values.


<a name="2run"></a>
### 2nd run

#### Input parameters

Colors used:

```
GAIA1              i-z
GAIA(2,4,5,6,7)    i-z     g-r
```

The `g-r` color GAIA1 contains much larger errors than the `i-z` color.
Maximum error values are `0.1` for all clusters.

The synthetic cluster parameters are kept from the **1st run**.

#### Output parameters

The A-D test gave these values for the photometric and plx+PMs test:

| Name  | phot | plx+PM |
|:-----:|:----:|:------:|
| GAIA1 | 1.00 |  1.00  |
| GAIA2 | 0.56 |  0.23  |
| GAIA4 | 0.28 |  0.32  |
| GAIA5 | 0.13 |  0.09  |
| GAIA6 | 0.35 |  0.58  |
| GAIA7 | 0.63 |  0.14  |

Compared to the **1st run** results:

* plx vs plx values

| Cluster |         Plx1         |          Plx2        |  1-2  |
|:-------:|:--------------------:|:--------------------:|:-----:|
|  GAIA1  | 13.99 (-0.07, +0.08) | 14.06 (-0.06, +0.06) | -0.07 |
|  GAIA2  | 13.33 (-0.15, +0.15) | 13.58 (-0.15, +0,14) | -0.25 |
|  GAIA4  | 12.42 (-0.27, +0.28) | 12.41 (-0.24, +0.22) |  0.01 |
|  GAIA5  | 14.30 (-0.17, +0.17) | 14.43 (-0.21, +0.21) | -0.13 |
|  GAIA6  | 13.29 (-0.13, +0.13) | 13.42 (-0.14, +0.13) | -0.13 |
|  GAIA7  | 13.79 (-0.26, +0.25) | 14.16 (-0.29, +0.26) | -0.37 |

* mean vs mean fundamental parameters values:

| Cluster |  met  |  age  | E(B-V) |  dist  |  M_i |
|:-------:|:-----:|:-----:|:------:|:------:|:----:|
|  1 1st  | 0.021 | 9.49  | 0.3536 | 13.471 | 4100 |
|  1 2nd  | 0.015 | 9.512 | 0.3177 | 13.786 | 8800 |
|  2 1st  | 0.039 | 9.542 | 0.2349 | 13.815 | 2100 |
|  2 2nd  | 0.009 | 9.887 | 0.2284 | 13.722 | 2300 |
|  4 1st  | 0.041 | 9.715 | 0.8806 | 13.276 | 7300 |
|  4 2nd  | 0.041 | 9.047 | 1.2490 | 13.484 | 1000 |
|  5 1st  | 0.023 | 8.298 | 0.1580 | 14.452 | 700  |
|  5 2nd  | 0.029 | 8.208 | 0.1426 | 14.326 | 500  |
|  6 1st  | 0.025 | 9.482 | 0.2011 | 13.214 | 1100 |
|  6 2nd  | 0.013 | 9.355 | 0.2384 | 13.289 | 1200 |
|  7 1st  | 0.017 | 9.595 | 0.7679 | 13.565 | 5000 |
|  7 2nd  | 0.041 | 7.525 | 0.9207 | 13.206 | 800  |

#### Remarks about the analysis

The second analysis allows to constrain the distances based primarily on the
parallax values found.

* **GAIA1** the metallicity seems to be bounded around solar values
(0.015-0.021) as given by Mucciarelli et al. (2017), and the age around a 9.5
value as given by Simpson et al. (2017). The extinction is bounded to a range
~0.3-0.35. The parallax distance is very much constrained (~14 mag). The
photometric distance is smaller by 0.5 mag in the **1st run**, but this value
seems to be underestimated. The mass in the **2nd run** is twice as large as
the **1st run**, but this latter value is probably underestimated (given by
the large difference between observed and synthetic stars in the final fit)

* **GAIA2** the metallicity distribution was markedly bi-model in the
**1st run**, with values larger than approx 0.03, while in this **2nd run**,
values are below approx 0.01. No constrain on the metallicity can thus be
imposed. The **1st run** also displayed bi-modality in the age. As this run
clearly indicates a log(age)>9.5, perhaps bounding the age will help bound the
metallicity. The extinction is clearly around 0.22 mag and the parallax
distance is located between 13.2-13.7 mag (this is a bit smaller than the
photometric distance). The mass is well constrained around 2200 Mo.

* **GAIA4** although the metallicity seems to be constrained around 0.04 in
both runs, the age jumps from 9.7 to 9 so it can't really be trusted. The latter
value coincides with the literature, although neither photometric distance is
equivalent to the parallax distance found in both runs of approx 12.4 mag. The
extinction is large but also uncertain. The mass can not yet be constrained.

* **GAIA5** as in the **1st run**, the metallicity, age and distance
distributions cover the entire range given, due to the dispersed and low
populated CMD that remains after the decontamination process. The parallax
distance nonetheless is well constrained, and the photometric distance has its
mean around the same value. The extinction is also well constrained as is the
mass. Perhaps constraining these three parameters will help with the
metallicity and age.
The blue-plume disappears from the CMD when the (G_BP-G_RP) color is not used.
The PS1 data also shows observational fringes in the photometry, that affect
the cluster region.

* **GAIA6** the metallicity seems to be upper bounded by 0.03; the age is in
the range 9.1-9.7. The extinction and the mass are well bounded and equivalent
in both runs. The parallax and photometric distance are very similar and well
bounded.

* **GAIA7** the age jumps from 9.6 to 7.5 with the latter being a better match
to the Torrealba et al. 7.85 value. The metallicity can not be constrained. The
parallax distance is between 13.5-14.5. Both the literature value (13.1) and
the distance associated to the better age match (13.21) are outside of this
range. The parallax diagram is very dispersed and populated by only approx 30
stars. The extinction is in the range .7-1, and the mass seems to be better
fitted in the **2nd run**.
The A-D test for the plx+PM data for this cluster throws the second lowest
value of all (below GAIA5), although the photometric A-D test value is rather
large (0.63).

> I can not constrain the metallicity and age parameters for the next run
for the clusters GAIA5 and GAIA7. In the case of GAIA4 I can only constrain the
age. For GAIA2 the metallicity can not be constrained, most likely due to the
bi-modality exhibited in the **1st run**.


<a name="3run"></a>
### 3rd run

#### Input parameters

Colors and max error used:

```
GAIA1                i-z   0.075
GAIA(1,2,4,5,6,7)    i-z   0.1
```

Synthetic cluster parameters are:

|  Name |       z         |     log(age)    |  M (x10^3) |  E_BV  |    mu_0   |
|:-----:|:---------------:|:---------------:|:----------:|:------:|:---------:|
| GAIA1 | .01-.025 (.001) |9.4-9.61 (.0075) |  4-10 (.1) | .25-.4 | 13.5-14.5 |
| GAIA2 | .001-.06 (.002) | 9.5-10  (  "  ) | .5-3 (.05) | .2-.24 | 13.2-13.7 |
| GAIA4 | .001-.06 (.002) | 9.0-10  (  "  ) | .1-10 (.1) | .8-1.3 | 12.1-12.7 |
| GAIA5 | .001-.06 (.002) | 7.-10   (  "  ) | .1-3  (.1) | .0-.3  | 14.1-14.7 |
| GAIA6 | .001-.03 (.001) | 9.1-9.7 (  "  ) |.5-1.5 (.05)|.18-.23 | 13.1-13.6 |
| GAIA7 | .001-.06 (.002) | 7.-10   (  "  ) | .1-2 (.05) | .7-1   | 13.5-14.5 |

#### Output parameters

Combined A-D test for all runs so far:

| Name  | phot | plx+PM | phot | plx+PM | phot | plx+PM |   Mean   |
|:-----:|:----:|:------:|:----:|:------:|:----:|:------:|:--------:|
| GAIA1 | 0.16 |  1.00  | 1.00 |  1.00  | 1.00 |  1.00  |   0.86   |
| GAIA2 | 0.64 |  0.78  | 0.56 |  0.23  | 0.55 |   --   |   0.55   |
| GAIA4 | 0.18 |  0.24  | 0.28 |  0.32  | 0.25 |  0.35  | **0.27** |
| GAIA5 | 0.32 |  0.18  | 0.13 |  0.09  | 0.16 |  0.12  | **0.17** |
| GAIA6 | 0.55 |  0.50  | 0.35 |  0.58  | 0.37 |  0.42  |   0.46   |
| GAIA7 | 0.57 |  0.39  | 0.63 |  0.14  | 0.31 |   --   | **0.41** |

The estimated parallax values so far are:

| Clust | Plx1  | Plx2  | Plx3  |  Lit  |
|:-----:|:-----:|:-----:|:-----:|:-----:|
| GAIA1 | 13.99 | 14.06 | 14.06 | 13.30 |
| GAIA2 | 13.33 | 13.58 | 13.54 | 13.60 |
| GAIA4 | 12.42 | 12.41 | 12.90 | 13.70 |
| GAIA5 | 14.30 | 14.43 | 14.14 | 14.20 |
| GAIA6 | 13.29 | 13.42 | 13.41 | 11.90 |
| GAIA7 | 13.79 | 14.16 | 13.95 | 13.10 |

* mean vs mean fundamental parameters values:

| Cluster |  met  |  age  | E(B-V) |  dist  |  M_i |
|:-------:|:-----:|:-----:|:------:|:------:|:----:|
|  1 1st  | 0.021 | 9.490 | 0.3536 | 13.471 | 4100 |
|  1 2nd  | 0.015 | 9.512 | 0.3177 | 13.786 | 8800 |
|  1 3rd  | 0.013 | 9.505 | 0.3781 | 13.561 | 8300 |
|   --    |   --  |  --   |   --   |   --   |  --  |
|  2 1st  | 0.039 | 9.542 | 0.2349 | 13.815 | 2100 |
|  2 2nd  | 0.009 | 9.887 | 0.2284 | 13.722 | 2300 |
|  2 3rd  | 0.013 | 9.865 | 0.2239 | 13.632 | 2250 |
|   --    |   --  |  --   |   --   |   --   |  --  |
|  4 1st  | 0.041 | 9.715 | 0.8806 | 13.276 | 7300 |
|  4 2nd  | 0.041 | 9.047 | 1.2490 | 13.484 | 1000 |
|  4 3rd  | 0.035 | 9.789 | 1.0752 | 12.279 | 2000 |
|   --    |   --  |  --   |   --   |   --   |  --  |
|  5 1st  | 0.023 | 8.298 | 0.1580 | 14.452 | 700  |
|  5 2nd  | 0.029 | 8.208 | 0.1426 | 14.326 | 500  |
|  5 3rd  | 0.033 | 8.118 | 0.1352 | 14.410 | 200  |
|   --    |   --  |  --   |   --   |   --   |  --  |
|  6 1st  | 0.025 | 9.482 | 0.2011 | 13.214 | 1100 |
|  6 2nd  | 0.013 | 9.355 | 0.2384 | 13.289 | 1200 |
|  6 3rd  | 0.017 | 9.505 | 0.2011 | 13.146 | 1050 |
|   --    |   --  |  --   |   --   |   --   |  --  |
|  7 1st  | 0.017 | 9.595 | 0.7679 | 13.565 | 5000 |
|  7 2nd  | 0.041 | 7.525 | 0.9207 | 13.206 | 800  |
|  7 3rd  | 0.041 | 7.135 | 0.9829 | 13.677 | 450  |

#### Remarks about the analysis

* **GAIA1** all parameters except the mass have very narrow distributions
around their means, which means their uncertainties are very small. The
metallicity is consistent with the approx solar value (a bit smaller).

* **GAIA2** the metallicity is again sub-solar as in the **2nd run**, its
uncertainty is large because there is a second smaller mode around 0.045. Age,
distance, and mass have reasonable distributions. The extinction's distribution
is rather flat, pointing to a too narrow initial range. The fit looks very good.

* **GAIA4** metallicity is bi-modal in 0.03 and 0.043, the rest of the
distributions look reasonably good. The age coincides with the **1st run** with
an acceptable fit. The second run fitted brighter stars with low MPs, hence the
lower age.

* **GAIA5** again, no suitable fit was found. The distributions are flat in
their entire ranges except for the mass.

* **GAIA6** age and extinction are a bit bi-modals, which make the uncertainties
large. The synthetic cluster fit looks very good.

* **GAIA7** as in the **2nd run**, the metallicity found is markedly
supra-solar. The age also coincides with the **2nd run**, while the distance
is a bit larger and the mass a bit smaller. The fit looks reasonably good.


<a name="4run"></a>
### 4th run

#### Input parameters

Colors and max error as in **3rd run**.

The fundamental parameter ranges for the metallicity, age, and mass are the
same as those used in the **1st run** (ie: the widest ranges). The extinction
and distance parameters are **fixed** to the average values for the previous
three runs. In the case of the distance, we averaged the *parallax* values:

| Name  | E_BV | mu (Plx)|
|:-----:|:----:|:-------:|
| GAIA1 | 0.35 |  14.04  |
| GAIA2 | 0.23 |  13.48  |
| GAIA4 | 1.07 |  12.58  |
| GAIA5 | 0.15 |  14.29  |
| GAIA6 | 0.21 |  13.37  |
| GAIA7 | 0.89 |  13.97  |

#### Remarks about the analysis

* **GAIA1** the images could not be generated due to an error, probably
because the parameters were completely stuck; this is not a good sign.

* **GAIA2** bi-modal in age between 9.8 and 10. The fit looks good.

* **GAIA4** similar to **GAIA1**, the chains are stuck. The fit is reasonable.

* **GAIA5** the metallicity and age distributions, as before, occupy the entire
range.

* **GAIA6** metallicity is tri-modal and age is bi-modal. The mean age is
pushed down by the lower mode, the larger mode is around 9.15. The fit is
reasonable.

* **GAIA7** the fit does not look good, mainly because the cluster shows little
structure in its CMD.

> Overall, fixing the extinction and distance seems to have the effect of
preventing the other parameters from being properly explored. This run should
**probably not be taken into account into the analysis**.


<a name="5run"></a>
### 5th run

#### Input parameters

Full parameter ranges as in **1st run**. Colors and maximum error values:

```
GAIA1              BP-RP   i-z     0.1
GAIA(2,4,5,6,7)    BP-RP   i-z     0.15
```
Maximum magnitudes:

```
GAIA1             18.5
GAIA(2,4,5,6,7)   20
```

The `ptemcee` parameters are:

```
      init_mode   popsize   maxiter
PT0    diffevol        20       100
      ntemps    nwalkers   nburn    nsteps     Tmax   adapt    priors   h_max
PT1       10          50      10     20000       30       y      unif      20
```

and the `tolstoy` likelihood and a fixed mass value of `1000`.

#### Output parameters

The estimated parallax values so far are:

| Clust | Plx1  | Plx2  | Plx3  | Plx4  | Plx5  |  Lit  |
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| GAIA1 | 13.99 | 14.06 | 14.06 | 14.16 | 13.94 | 13.30 |
| GAIA2 | 13.33 | 13.58 | 13.54 | 13.52 | 13.40 | 13.60 |
| GAIA4 | 12.42 | 12.41 | 12.90 | 12.72 | 12.79 | 13.70 |
| GAIA5 | 14.30 | 14.43 | 14.14 | 14.50 | 14.01 | 14.20 |
| GAIA6 | 13.29 | 13.42 | 13.41 | 13.30 | 13.30 | 11.90 |
| GAIA7 | 13.79 | 14.16 | 13.95 | 13.86 | 13.85 | 13.10 |

#### Remarks about the analysis

* **GAIA1** the distributions are completely stuck, and the fit is **terrible**.

* **GAIA2** almost all parameters got stuck, which means the uncertainties
assigned are of little value. The metallicity is slightly sub-solar. The fit
looks very good.

* **GAIA4** similar to GAIA2, chains are stuck. The fit is **not** reasonable.

* **GAIA5** except the age, all distributions are bi-modal. The fit is **very
poor**.

* **GAIA6** parameters stuck. The fit looks good.

* **GAIA7** the distributions look reasonable, but the fit is
**extremely poor**.

> Overall the results from this run are **very poor**. I thought `tolstoy` would
produce better results.


<a name="6run"></a>
### 6th run

#### Input parameters

Colors, maximum error values, maximum magnitudes, and `ptemcee` parameters as
in **5th run**.

I use the `dolphin` likelihood and full parameter ranges as in **1st run**,
with the exception of the distance range that is taken from the parallax
values so far:

|  Name |    mu_0   |
|:-----:|:---------:|
| GAIA1 | 13.5-14.5 |
| GAIA2 | 13.0-14.0 |
| GAIA4 | 12.0-13.5 |
| GAIA5 | 13.5-15.0 |
| GAIA6 | 13.0-14.0 |
| GAIA7 | 13.0-14.5 |

This run uses the **new method that interpolates isochrones** instead of just
pushing to the closest value in the discrete (z, age) grid.

#### Remarks about the analysis

* **GAIA1** the median is a better fit than the mean for the metallicity, as
it the distribution is close to the lower end. The age is a bit bi-modal but
overall the distributions look good. The fit looks good.
More steps are needed as the chains look not completely stable and the
autocorrelation plot shows that only the mass is well mixed. This run took
about 14 hs.

* **GAIA2** except the mass, all the distributions look a bit bi-modal.

* **GAIA4** the distributions and the chains look good but the fit is very poor.
This is mostly due to the very dispersed cluster sequence. The mass is a
particularly a bad fit.

* **GAIA5** as in previous runs the distributions for the metallicity and the
age (mostly the age) occupy almost the entire range. The fit looks reasonable.

* **GAIA6** slightly bi-modal distributions with well mixed chains and a nice
fit.

* **GAIA7** very similar to **GAIA4**: reasonable distributions but very poor
fit due to the dispersed sequence.

> Overall the distributions look **a lot better** than all the previous runs.
Since only 50 chains were used, more steps are perhaps needed. On average,
the entire process took about 14 hs.


<a name="7run"></a>
### 7th run

#### Input parameters

Same input parameters as in the **6th run**, with less chains (30) and more
steps (50000). I also reduced the number of interpolating points for the
isochrones from 1000 to 750, increased the DE runs, and set to read the MPs
(taken from the **6th run**).

#### Output parameters

* PMs means and standard deviations (for runs with different input colors):

| Cluster |   ra*  |  std  |   dec  |  std  |
|:-------:|:------:|:-----:|:------:|:-----:|
|  1 1st  | -0.284 | 1.220 |  1.164 | 1.756 |
|  1 2nd  | -0.182 | 1.292 |  1.119 | 1.795 |
|  1 3rd  | -0.187 | 1.237 |  1.159 | 1.662 |
|  1 5th  | -0.333 | 1.735 |  1.249 | 2.487 |
|   --    |   --   |   --  |   --   |  --   |
|  2 1st  | -0.428 | 1.957 |  0.352 | 1.752 |
|  2 2nd  | -0.401 | 3.657 |  0.361 | 1.628 |
|  2 3rd  | -0.853 | 1.046 |  0.385 | 1.121 |
|  2 5th  | -0.398 | 3.714 |  0.192 | 1.732 |
|   --    |   --   |   --  |   --   |  --   |
|  4 1st  |  0.480 | 1.576 | -1.477 | 1.618 |
|  4 2nd  |  0.413 | 2.529 | -1.039 | 1.769 |
|  4 3rd  |  0.452 | 1.816 | -1.130 | 1.489 |
|  4 5th  |  0.243 | 1.170 | -0.973 | 0.957 |
|   --    |   --   |   --  |   --   |  --   |
|  5 1st  | -1.311 | 0.467 |  2.137 | 0.385 |
|  5 2nd  | -0.968 | 0.215 |  2.184 | 0.619 |
|  5 3rd  | -1.107 | 0.246 |  2.874 | 0.791 |
|  5 5th  | -0.998 | 0.510 |  2.122 | 1.043 |
|   --    |   --   |   --  |   --   |  --   |
|  6 1st  | -2.359 | 1.107 |  2.521 | 1.988 |
|  6 2nd  | -2.189 | 0.887 |  2.592 | 1.563 |
|  6 3rd  | -2.139 | 0.968 |  2.790 | 1.549 |
|  6 5th  | -2.177 | 1.037 |  2.586 | 1.885 |
|   --    |   --   |   --  |   --   |  --   |
|  7 1st  |  0.082 | 1.163 | -2.784 | 2.796 |
|  7 2nd  | -0.007 | 0.653 | -2.459 | 2.244 |
|  7 3rd  | -0.023 | 0.841 | -2.493 | 2.171 |
|  7 5th  |  0.637 | 1.037 | -2.456 | 2.392 |

* combined A-D tests so far (3th==4th; 5th==6th==7th)

| Cluster |  phot  | plx+PM |
|:-------:|:------:|:------:|
|  1 1st  |  0.16  |  1.00  |
|  2  "   |  0.64  |  0.78  |
|  4  "   |  0.18  |  0.24  |
|  5  "   |  0.32  |  0.18  |
|  6  "   |  0.55  |  0.50  |
|  7  "   |  0.57  |  0.39  |
|   --    |   --   |   --   |
|  1 2nd  |  1.00  |  1.00  |
|  2  "   |  0.56  |  0.23  |
|  4  "   |  0.28  |  0.32  |
|  5  "   |  0.13  |  0.09  |
|  6  "   |  0.35  |  0.58  |
|  7  "   |  0.63  |  0.14  |
|   --    |   --   |   --   |
|  1 3rd  |  1.00  |  1.00  |
|  2  "   |  0.55  |   --   |
|  4  "   |  0.25  |  0.35  |
|  5  "   |  0.16  |  0.12  |
|  6  "   |  0.37  |  0.42  |
|  7  "   |  0.31  |   --   |
|   --    |   --   |   --   |
|  1 5th  |  0.28  |  1.00  |
|  2  "   |  0.57  |  0.62  |
|  4  "   |  0.31  |  0.25  |
|  5  "   |  0.23  |  0.21  |
|  6  "   |  0.51  |  0.41  |
|  7  "   |  0.32  |  0.30  |
|   --    |   --   |   --   |

#### Remarks about the analysis

* **GAIA1** the metallicity is again really low as in the last run, and the
age is less bi-modal. The mass distribution is a bit more dispersed, most
parameters look like they need more steps in their chains.

* **GAIA2** opposite to the previous run, now only the mass distribution looks
a bit bi-modal.

* **GAIA4** mass and metallicity are bi-modal. The fit looks as poor as the
previous run.

* **GAIA5** as in the previous run the age distribution is very disperse. The
fit looks reasonable but with large uncertainties, particularly in the age and
distance.

* **GAIA6** all distributions are markedly bi-modal, so the means are not
a representative point estimate of the best fit. In the table above I selected
the median values, which also coincide with the MAPs.

* **GAIA7** the distributions and chains look good, as in the previous run and
the mean values are almost identical. Also as in the previous run, the fit does
not look all that good, mainly due to the disperse sequence.

> Except for **GAIA6** whose distributions are bi-modal, all the clusters have
very similar distributions and mean values as in the **6th run**.



<a name="8run"></a>
### 8th run

#### Input parameters

Same input parameters as in the **7th run**, but now using only the `i-z` color,
a maximum error value of `0.1`, and **no** maximum magnitude cut.

I forgot to change the decontamination method and kept `read` with the MP
values obtained from the **6th run**, where the `BP-RP, i-z` colors were used.
This has an impact particularly on GAIA1, and **in a good way.**

#### Remarks about the analysis

* **GAIA1** all distributions look rather bi-modal, so the values in the table
above are the medians. The unintentional two-step decontamination process worked
in favor as the sequence is very clear. Unlike the **6th, 7th** runs the fit
looks very good since the sequence is deeper and with higher contrast. Unlike
the two previous runs, the metallicity is no longer very small and is located
around solar value. Overall it looks like more iterations are needed to obtain
more definite distributions. With 30 chains and 500000 steps, it took 15h35m
to finish the analysis.

* **GAIA2** some distributions are a bit bi-modal but this looks like an effect
the chains getting stuck around the "best fit" value or needing more steps.
The metallicity is half the value found in the two previous runs, where
`BP-RP` was used.

* **GAIA4** although the fit looks better than the previous runs, the
distributions do not. The metallicity can not be constrained. The distance
is much closer to the parallax distance found. The mass is very different from
the previous runs and this one looks more reasonable.

* **GAIA5** nothing can be obtained from this.

* **GAIA6** the distributions are no longer bi-modal, but this could be because
the MCMC stopped at approx 25000 iterations due to the tau convergence, instead
of performing the 50000 steps requested. The fit looks very good, better than
the two previous runs.

* **GAIA7** the fit looks a bit nicer but given the low number of stars and
weak (or non-existent) structure, it's hard to asses the goodness of fit.
The metallicity distribution occupies the entire range and the distance is
markedly bi-modal. The mass is very different from the previous runs but it
still looks reasonable.


<a name="9run"></a>
### 9th run

#### Input parameters

The serendipitous use of the MPs estimated with the `BP-RP, i-z` colors in the
case where only the `i-z` color is used in the **8th run**, translated into
stars with large `BP-RP` errors being assigned a low MP when analyzing only
the `i-z` color. This means we are now using information from `BP-RP` without
the need to include that color, which contains very large photometric errors.
**This is good.**

The number of temperatures (10) seems unnecessarily large and the number of
walkers (30) too small. I'll increase the walkers to 100, but selecting the
number of temperatures and the max temp is not straightforward. Options:

1. Tmax=inf, ntemps=5
1. Tmax=30, ntemps=5
1. Tmax=XX, ntemps=None

Some tests resulted in `Tmax=30` not being a large temperature enough. Since
selecting a large temperature and `ntemps=n` results in the method using
`ntemps=5`, I'll go with `Tmax=inf, ntemps=5`.

Since the `BP-RP` color has a large uncertainty, and its information is already
present in the MPs, I'll use the `i-z` color, a maximum error value of `0.1`,
and **no** maximum magnitude cut as in the previous run.

Summary of `ptemcee` parameters:

    Tmax=inf, ntemps=5, nwalkers=100, nsteps=50000, hmax=20

After trying the above parameters, only the GAIA1 run finished and the chains
mixed **very** poorly. The `ptemcee` sampler threw a lot of `RuntimeWarning:
overflow encountered in multiply` messages. So I changed the parameters to:

    Tmax=inf, ntemps=10, nwalkers=50, nsteps=50000, hmax=20

With these parameters I got again many warnings:

    RuntimeWarning: overflow encountered in multiply
    RuntimeWarning: invalid value encountered in add


#### Remarks about the analysis

* **GAIA1** distributions are a bit bi-modal but overall the means/medians are
similar to those from the previous run. The exception is the mass but this is
closer given the number of stars in th CMD.

* **GAIA2** in cases of bi-modality, the median is selected. Very similar to the
previous run, with the metallicity more bi-modal.

* **GAIA4** the metallicity is bi-modal

* **GAIA5** same, all distributions dispersed.

* **GAIA6** age is a bit bi-modal, I use the median.

* **GAIA7** the metallicity is uni-modal but not well constrained, so I use the
median. The distance is also not so well constrained, but better than the
previous run.

> The `Tswap AF` seems to converge to 0.4 for almost all clusters (except
GAIA5). The GAIA1 plotted chain is not properly mixed, so these results should
be taken with caution. Overall the MAFs are very low (as with most other runs).


<a name="10run"></a>
### 10th run

#### Input parameters

After some tests, I realized that the `Tmax=inf` parameter is not optimal and
`Tmax=50` is better. Also, using more temperatures improves the AF of the cold
chain, so I'll increase it to `ntemps=100` and reduce the chains to
`nwalkers=20`. To decrease the memory usage, I'll also decrease the number
of steps to `nsteps=10000`.

#### Remarks about the analysis

* **GAIA1** the distributions look stuck. The mass is halve of what it should
be taking the number of stars into account.

* **GAIA2** distributions stuck and bi-modal for metallicity, age, and mass, so
I use the median.


> The `Tswap AFs` look like they need more steps to converge. Clearly 100
temperatures is too much. **Perhaps this run should not be taken into account.**



<a name="11run"></a>
### 11th run

#### Input parameters

The previous run did not work as expected, the chains are very much stuck,
mainly for GAIA1 and GAIA2. The `Tswap AF` are all larger than 0.90 for all
clusters and I'm not sure this is good (the optimal value is 0.234 according
to Atchadé et al 2011). The `AFs` for the cold chain increased a bit, but is
still outside the 0.25-0.50 range.

This run uses fewer temperatures and more walkers:

    Tmax=50, ntemps=50, nwalkers=50, nsteps=20000, hmax=20

#### Remarks about the analysis



<a name="12run"></a>
### 12th run

#### Input parameters

The previous run was very good, but more steps are likely needed. This run thus
uses fewer temperatures and walkers, and more steps (the previous run consumed
the 20hs max time with less than 15000 steps on average):

    Tmax=50, ntemps=24, nwalkers=24, nsteps=50000, hmax=20

#### Remarks about the analysis



<a name="13run"></a>
### 13th run

#### Input parameters

    Tmax=50, ntemps=15, nwalkers=12, nsteps=200000, hmax=20

#### Remarks about the analysis

The chains don't look well mixed for GAIA2.



<a name="14run"></a>
### 14th run

#### Input parameters

    Tmax=50, ntemps=15, nwalkers=50, nsteps=200000, hmax=20

#### Remarks about the analysis



<a name="15run"></a>
### 15th run

#### Input parameters

    Tmax=100, ntemps=50, nwalkers=12, nsteps=200000, hmax=20

#### Remarks about the analysis



<a name="16run"></a>
### 16th run

#### Input parameters

    Tmax=100, ntemps=50, nwalkers=100, nsteps=20000, hmax=20

#### Remarks about the analysis



<a name="17run"></a>
### 17th run

#### Input parameters

    Tmax=100, ntemps=10, nwalkers=200, nsteps=20000, hmax=20

#### Remarks about the analysis



<a name="18run"></a>
### 18th run

#### Input parameters

Run for GAIA2 , divided into two runs: one for the lower half of the
metallicity range [0.001, 0.03], and one for the upper half [0.03, 0.06].

Used the following `ptemcee` values:

1. `Ntemps=10, nchains=200, nsteps=20000, Tmax=100`
2. `Ntemps=10, nchains=20, nsteps=200000, Tmax=100`
3. `Ntemps=25, nchains=100, nsteps=100000, Tmax=100`
4. `Ntemps=50, nchains=50, nsteps=100000, Tmax=100`

#### Remarks about the analysis

The 3rd test for the lower half (input_05) shows bi-modality in the metallicity,
age, and mass. Probably because a large portion of the chain was discarded as
burn in, and the chains needed more steps con converge.



<a name="19run"></a>
### 19th run

#### Input parameters

This runs is performed to obtain the parallax and PMs with a lengthy Bayesian
MCMC. The parallax data is corrected adding th +0.029 mas, according to
Lindegren et al. (2018).

| Run |  Colors   | e_max |
|:---:|:---------:|:-----:|
| 1   |   BR-RP   |  0.1  |
| 2   |    i-z    |  0.1  |
| 3   | BR-RP,i-z |  0.1  |
| 4   |   BR-RP   |  0.05 |
| 5   |    i-z    |  0.05 |
| 6   | BR-RP,i-z |  0.05 |




<a name="finalremarks"></a>
### Final remarks

Input parameters used:

|      Run(s)      |       Colors       |    e_max   | mag cut  |
|:----------------:|:------------------:|:----------:|:--------:|
|  1st (G1; G2-7)  | i-z,g-r; BR-RP,i-z | 0.05; 0.1  |   none   |
|  2nd (G1; G2-7)  |     i-z; i-z,g-r   |     0.1    |   none   |
|  3rd,4th (G1-7)  |         i-z        | 0.075; 0.1 |   none   |
|  5th-7th (G1-7)  |      i-z,BP-RP     |  0.1; 0.15 | 18.5; 20 |
|  8th-18th (G1-7) |         i-z        |     0.1    |   none   |

Summary of relevant information for each run:

* **1st, 2nd**: mostly trial runs.

* **3rd**: the parameter ranges were constrained according to the
values obtained in the previous runs.

* **4th**: extinction and distance were fixed, with poor results.

* **5th**: I used the `tolstoy` likelihood with maximum magnitude
cuts, with very poor results.

* **6th**: from this run onwards I use the **new method** that interpolates
isochrones, instead of just pushing to the closest value in the discrete
(z, age) grid. The resulting distributions look a lot better than in the
previous runs.

* **7th**: uses the same input parameters and MPs as the previous run,
changing the `ptemcee` parameter a bit. The results are similar to those in the
**6th run** except for GAIA6 that shows bi-modal distributions.

* **8th**: from this run onwards I use the MPs obtained using the `BP-RP, i-z`
colors but only the `i-z` color in the Bayesian analysis. This improved the
field stars removal particularly for GAIA1.

* **9th**: used `Tmax=inf` and the GAIA1 chains did not mix properly and most
distributions look bi-modal.

* **10h**: used 100 temperatures and this appeared to be too much as
the chains got stuck.

* **11th-17th**: for these runs I use a maximum of 50 temperatures. These are
the runs we'll use to estimate the cluster's fundamental parameters, with the
exception of GAIA2 which is processed in the following run.

* **18th**: the metallicity estimated for the GAIA2 cluster in the 11-17 runs
varies from small (~0.007) to large (~0.04) values. To pin down this parameter
we make four new runs for this cluster alone, with the lower and upper half of
z processed separately.

* **19th**: performed a long Bayesian MCMC run for the parallax and PMs. The
Lindegren correction is applied to the parallax.

For runs that are particularly bi-modal or non-normal, we use the median values
instead of the means. When the median values are also not good estimators
(extreme cases of bi-modality), we default to the mode. If the distribution is
bi-modal but the change from mean to median|mode is very small, we just keep
the mean as the estimator. We don't bother with GAIA5 since its posteriors are
always uniform (except for the mass)

|   Runs   |    z   |  age  |  ext  |  dst  |  M   |
|:--------:|:------:|:-----:|:-----:|:-----:|:----:|
| 11 - G2  | 0.0416 | 9.715 | 0.215 | 13.79 |  --  |
| 11 - G4  |   --   |   --  |   --  | 12.31 | 2110 |
| 11 - G6  |   --   |   --  | 0.296 | 13.77 | 1169 |
| 11 - G7  | 0.0169 | 7.315 |   --  |   --  |  --  |
| 12 - G1  |   --   |  --   | 0.346 |   --  |  --  |
| 12 - G2* | 0.0094 |  --   | 0.242 |   --  | 2188 |
| 12 - G4* | 0.0559 |  --   |   --  |   --  |  --  |
| 12 - G6  | 0.0175 |  --   | 0.235 | 13.26 | 927  |
| 12 - G7  |   --   | 7.324 |   --  |   --  |  --  |
| 13 - G2  | 0.0434 |  --   |   --  |   --  |  --  |
| 13 - G7  |   --   | 7.173 |   --  | 13.55 |  --  |
| 14 - G1  |   --   |  --   | 0.379 |   --  | 5642 |
| 14 - G2  | 0.0317 | 9.641 |   --  |   --  | 2520 |
| 14 - G4  | 0.0199 |  --   |   --  |   --  |  --  |
| 14 - G6  |   --   |  --   |   --  |   --  | 880  |
| 14 - G7  | 0.0244 | 7.209 |   --  |   --  |  --  |
| 15 - G1  | 0.0177 | 9.554 |   --  | 13.52 |  --  |
| 15 - G2  |   --   | 9.737 |   --  |   --  | 2875 |
| 15 - G4  | 0.0308 | 9.851 | 1.053 | 12.40 |  --  |
| 15 - G7  | 0.0103 | 7.245 |   --  | 12.75 | 307  |
| 16 - G2* | 0.0094 | 9.649 | 0.215 | 13.89 | 2333 |
| 16 - G4* | 0.0294 |  --   |   --  |   --  | 1744 |
| 16 - G6  | 0.0143 |  --   |   --  |   --  |  --  |
| 17 - G2  |   --   | 9.662 |   --  | 13.92 |  --  |
| 17 - G6  | 0.0444 | 8.873 |   --  |   --  | 720  |
| 17 - G7  | 0.0170 | 7.144 | 1.010 | 13.45 |  --  |

The * marks cases of **extreme** bi-modality. In total, 63 values were selected
from either the median or the mode. This represents 30% of the 210 parameters
estimated (6 clusters * 5 parameters * 7 runs).

These  are the **18th run** values for GAIA2:

|   Runs   |    z   |  age  |  ext  |  dst   |  M   |
|:--------:|:------:|:-----:|:-----:|:------:|:----:|
| 1 - G2 l | 0.0139 | 9.524 | 0.261 | 13.908 | 2200 |
| 2 - G2 l | 0.0075 | 9.773 | 0.248 | 13.781 | 2100 |
| 3 - G2 l | 0.0089 | 9.635 | 0.265 | 13.867 | 2100 |
| 4 - G2 l | 0.0047 | 9.737 | 0.264 | 13.893 | 2500 |

in all cases the lower metallicity range analysis shows more normal looking
distributions and smaller standard deviations. The exception is the 3rd test
run, where the metallicity looks bi-modal for the lower range run. Still,
the deviation is smaller here too.

The parallax and PMs obtained from the **19th run** are:

\begin{table}[]
\begin{tabular}{ccccccccccccc}
\multicolumn{1}{c}{} & \multicolumn{2}{l}{G1} & \multicolumn{2}{l}{G2} & \multicolumn{2}{l}{G4} & \multicolumn{2}{l}{G5} & \multicolumn{2}{l}{G6} & \multicolumn{2}{l}{G7} \\
Runs &  Plx & (\mu_{\alpha}^{*}, \mu_{\delta}) & Plx & (\mu_{\alpha}^{*}, \mu_{\delta}) & Plx & (\mu_{\alpha}^{*}, \mu_{\delta})  & Plx & (\mu_{\alpha}^{*}, \mu_{\delta}) & Plx & (\mu_{\alpha}^{*}, \mu_{\delta}) & Plx & (\mu_{\alpha}^{*}, \mu_{\delta}) \\
1 &           &          &           &          &           &          &           &          &           &          &           &          \\
2 &           &          &           &          &           &          &           &          &           &          &           &          \\
3 &           &          &           &          &           &          &           &          &           &          &           &          \\
4 &           &          &           &          &           &          &           &          &           &          &           &          \\
5 &           &          &           &          &           &          &           &          &           &          &           &          \\
6 &           &          &           &          &           &          &           &          &           &          &           &         
\end{tabular}
\end{table}

% \usepackage{multirow}
\begin{table}[]
\begin{tabular}{l|ccccccc}
\hline
\hline
\multicolumn{7}{c}{Plx [pc]}\\
& 1 & 2 & 3 & 4 & 5 & 6 \\
\hline
G1 & 
$5478_{5304}^{5662}$ & $5775_{5639}^{5904}$ & 
$5536_{5367}^{5713}$ & $5772_{5487}^{6067}$ & 
$_{}^{}$ & $_{}^{}$ \\
G2 & 
$4086_{3812}^{4343}$ & $4862_{4532}^{5203}$ & 
$3999_{3724}^{4292}$ & $4423_{4126}^{4744}$ & 
$_{}^{}$ & $_{}^{}$ \\
G4 & 
$3073_{2716}^{3485}$ & $3521_{3170}^{3891}$ & 
$3087_{2701}^{3497}$ & $2216_{1840}^{2699}$ & 
$_{}^{}$ & $_{}^{}$ \\
G5 & 
$6514_{5995}^{7052}$ & $6853_{6123}^{7586}$ & 
$6679_{6131}^{7226}$ & $5076_{4505}^{5639}$ & 
$_{}^{}$ & $_{}^{}$ \\
G6 & 
$4414_{4127}^{4708}$ & $4126_{3870}^{4388}$ & 
$4415_{4165}^{4672}$ & $4450_{4173}^{4750}$ & 
$_{}^{}$ & $_{}^{}$ \\
G7 & 
$6973_{6199}^{7762}$ & $5781_{5086}^{6494}$ & 
$5119_{4474}^{5791}$ & $3104_{2483}^{3784}$ & 
$_{}^{}$ & $_{}^{}$ \\
\end{tabular}
\end{table}


\begin{table}[]
\begin{tabular}{l|ccccccc}
\hline
\hline
\multicolumn{7}{c}{($\mu_{\alpha}^{*}, \mu_{\delta}) [mas/yr]$}\\
& 1 & 2 & 3 & 4 & 5 & 6 \\
\hline
G1 &
\makecell{$(-0.212,1.213)\pm$\\$(1.052,1.885)$} & 
\makecell{$(-0.152,1.103)\pm$\\$(1.222,1.774)$} & 
\makecell{$(-0.343,1.262)\pm$\\$(1.699,1.262)$} & 
\makecell{$(-0.475,1.026)\pm$\\$(2.145,3.133)$} & 
\makecell{$(,)\pm$\\$(,)$} & 
\makecell{$(,)\pm$\\$(,)$} \\
%
G2 &
\makecell{$(-0.375,0.203)\pm$\\$(1.992,2.151)$} & 
\makecell{$(-0.672,0.417)\pm$\\$(1.621,1.167)$} & 
\makecell{$(-0.391,0.244)\pm$\\$(2.360,1.489)$} & 
\makecell{$(-0.504,0.184)\pm$\\$(1.422,1.687)$} & 
\makecell{$(,)\pm$\\$(,)$} & 
\makecell{$(,)\pm$\\$(,)$} \\
%
G4 &
\makecell{$(0.242,-1.039)\pm$\\$(1.055,0.658)$} & 
\makecell{$(0.736,-1.189)\pm$\\$(2.626,1.835)$} & 
\makecell{$(0.014,-1.170)\pm$\\$(1.202,0.689)$} & 
\makecell{$(0.651,-0.921)\pm$\\$(1.146,0.736)$} & 
\makecell{$(,)\pm$\\$(,)$} & 
\makecell{$(,)\pm$\\$(,)$} \\
%
G5 &
\makecell{$(-0.622,2.056)\pm$\\$(1.611,0.711)$} & 
\makecell{$(-1.016,2.776)\pm$\\$(0.469,0.819)$} & 
\makecell{$(-1.079,1.816)\pm$\\$(0.517,1.036)$} & 
\makecell{$(-1.390,1.964)\pm$\\$(1.505,0.959)$} & 
\makecell{$(,)\pm$\\$(,)$} & 
\makecell{$(,)\pm$\\$(,)$} \\
%
G6 &
\makecell{$(-2.218,2.983)\pm$\\$(0.617,1.207)$} & 
\makecell{$(-2.256,2.923)\pm$\\$(1.244,1.423)$} & 
\makecell{$(-2.245,2.602)\pm$\\$(1.059,1.954)$} & 
\makecell{$(-2.296,3.157)\pm$\\$(0.962,1.010)$} & 
\makecell{$(,)\pm$\\$(,)$} & 
\makecell{$(,)\pm$\\$(,)$} \\
%
G7 &
\makecell{$(0.394,-2.438)\pm$\\$(1.983,1.867)$} & 
\makecell{$(0.136,-2.571)\pm$\\$(0.593,2.104)$} & 
\makecell{$(0.216,-2.828)\pm$\\$(1.051,2.809)$} & 
\makecell{$(1.529,-3.876)\pm$\\$(2.283,3.772)$}
\makecell{$(,)\pm$\\$(,)$} & 
\makecell{$(,)\pm$\\$(,)$} & 
\end{tabular}
\end{table}