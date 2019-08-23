
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt

data = ascii.read("asteca_output_all.dat")

# These are the median/mode values used instead of the means when the
# the mean does not look like a proper summary of the distribution.
#
# Given the re-analysis of GAIA2 splitted into two metallicity ranges, I'll
# use these values to replace the 4 instances where metallicities in the upper
# z range where obtained:
# 18-1-1 -> 11, 18-2-3 -> 13, 18-3-5 -> 14, 18-4-7 -> 17.
# I replace *all* the parameters, not just the metallicity. I also use the
# standard deviations from these runs, stored in the 'par_errs' dictionary.
#
# Summary:
# 1. Read the combined 11-17 runs data from 'asteca_output_all.dat'
# 2. Replace means for medians/modes when necessary, and store in 'par_vals'
# 3. Replace in 'par_vals' for GAIA2 the parameters in runs 11, 13, 14, 17,
#    with the parameters from the 18th run (lower z range).

par_vals = {
    '11': {'2': ('0.0139', '9.524', '0.261', '13.908', '2200'),
           '4': ('--', '--', '--', '12.31', '2110'),
           '6': ('--', '--', '0.296', '13.77', '1169'),
           '7': ('0.0169', '7.315', '--', '--', '--')
           },
    '12': {'1': ('--', '--', '0.346', '--', '--'),
           '2': ('0.0094', '--', '0.242', '--', '2188'),
           '4': ('0.0559', '--', '--', '--', '--'),
           '6': ('0.0175', '--', '0.235', '13.26', '927 '),
           '7': ('--', '7.324', '--', '--', '--')
           },
    '13': {'2': ('0.0075', '9.773', '0.248', '13.781', '2100'),
           '7': ('--', '7.173', '--', '13.55', '--')
           },
    '14': {'1': ('--', '--', '0.379', '--', '5642'),
           '2': ('0.0089', '9.635', '0.265', '13.867', '2100'),
           '4': ('0.0199', '--', '--', '--', '--'),
           '6': ('--', '--', '--', '--', '880 '),
           '7': ('0.0244', '7.209', '--', '--', '--')
           },
    '15': {'1': ('0.0177', '9.554', '--', '13.52', '--'),
           '2': ('--', '9.737', '--', '--', '2875'),
           '4': ('0.0308', '9.851', '1.053', '12.40', '--'),
           '7': ('0.0103', '7.245', '--', '12.75', '307 ')
           },
    '16': {'2': ('0.0094', '9.649', '0.215', '13.89', '2333'),
           '4': ('0.0294', '--', '--', '--', '1744'),
           '6': ('0.0143', '--', '--', '--', '--')
           },
    '17': {'2': ('0.0047', '9.737', '0.264', '13.893', '2500'),
           '6': ('0.0444', '8.873', '--', '--', '720 '),
           '7': ('0.0170', '7.144', '1.010', '13.45', '--')
           }
}

# Standard deviations for GAIA2, taken from the low range metallicity runs.
par_errs = {
    '11': {'2': ('0.00597', '0.1031', '0.0114', '0.0689', '370')},
    '13': {'2': ('0.0055', '0.093', '0.0132', '0.083', '221')},
    '14': {'2': ('0.00534', '0.1232', '0.0075', '0.055', '722')},
    '17': {'2': ('0.0036', '0.0526', '0.0107', '0.056', '160')
           }
}

# Number of samples in each run for each cluster = nsteps*nchains. For GAIA2,
# the number of samples for the 11, 13, 14, 17 runs were taken from the 18th
# run (1-1, 2-3, 3-5, 4-7)
par_N = {
    '11': {'1': 557800, '2': 4e6, '4': 793750, '5': 959600, '6': 710000,
           '7': 832550},
    '12': {'1': 1.2e6, '2': 1.2e6, '4': 1.2e6, '5': 1.2e6, '6': 1.2e6,
           '7': 1.2e6},
    '13': {'1': 1.93e6, '2': 3.85e6, '4': 2.4e6, '5': 2.4e6, '6': 2.4e6,
           '7': 2.4e6},
    '14': {'1': 2e6, '2': 870500, '4': 2.6e6, '5': 3.2e6, '6': 2.5e6,
           '7': 4.8e6},
    '15': {'1': 538000, '2': 747696, '4': 861120, '5': 981504, '6': 705864,
           '7': 1.43e6},
    '16': {'1': 544800, '2': 692800, '4': 744300, '5': 902400, '6': 676700,
           '7': 1380600},
    '17': {'1': 2.82e6, '2': 378850, '4': 3.95e6, '5': 4e6, '6': 4e6,
           '7': 4e6}
}

cols = {'1': 'b', '2': 'c', '4': 'g', '5': 'orange', '6': 'r', '7': 'purple'}
mrkr = {'1': 's', '2': 'o', '4': '^', '5': '*', '6': 'p', '7': 'v'}

x_offset = [np.nan, -.25, -.15, np.nan, -.05, .05, .15, .25]

params = (
    ('met_me', 'e_m'), ('age_me', 'e_a'), ('E(B-V)_me', 'e_E'),
    ('dist_me', 'e_d'), ('M_i_me', 'e_M'))
p_idx = {
    'met_me': (0, "z", "{:.4f}"), 'age_me': (1, r"$\log(age)$", "{:.2f}"),
    'E(B-V)_me': (2, r"$E_{BV}$", "{:.2f}"),
    'dist_me': (3, r"$\mu_0$", "{:.2f}"),
    'M_i_me': (4, r"$M_{\odot}$", "{:.0f}")}

# For each parameter
par_mean_std_N = [[] for _ in range(5)]
for param in params:
    fig = plt.figure(figsize=(15, 7))
    plt.style.use('seaborn-darkgrid')
    ax = plt.subplot(111)
    plt.xlabel("Runs", fontsize=14)
    plt.ylabel(p_idx[param[0]][1], fontsize=14)

    # For each cluster
    j = [np.nan, 1, 1, np.nan, 1, 1, 1, 1]
    for cl in data:
        idx, run = int(cl['NAME'][4]), cl['NAME'][6:]
        # print(run, idx)

        try:
            y = par_vals[str(run)][str(idx)][p_idx[param[0]][0]]
            if y == '--':
                # Use mean value from 'data' array.
                y = cl[param[0]]
            else:
                print(str(run), str(idx), p_idx[param[0]][0])
                y = float(y)
        except KeyError:
            y = cl[param[0]]

        try:
            ey = float(par_errs[str(run)][str(idx)][p_idx[param[0]][0]])
            print(str(run), str(idx), ey)
        except KeyError:
            ey = cl[param[1]]

        # For each cluster obtain its overall mean and standard deviation,
        # for this parameter.
        p, s, N = np.array([y, ey, par_N[str(run)][str(idx)]]).T
        c_mean = np.sum(p * N) / N.sum()
        c_stddev = np.sqrt(
            np.sum((N - 1) * s**2 + N * (p - c_mean)**2) / (N.sum() - 1.))

        if j[idx] == 1:
            frmt = p_idx[param[0]][2]
            lbl = 'GAIA' + str(idx) + r"$\; ($" + frmt.format(c_mean) +\
                r"$\pm$" + frmt.format(c_stddev) + r"$)$"
        else:
            lbl = None
        plt.errorbar(
            j[idx] + x_offset[idx], y, yerr=ey, fmt='o',
            c=cols[str(idx)], marker=mrkr[str(idx)], label=lbl)
        j[idx] += 1

    # plt.ylim(0., 0.06)
    # plt.ylim(7., 10.)
    handles, labels = ax.get_legend_handles_labels()
    # sort both labels and handles by labels
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(
        handles, labels, fontsize=10, fancybox=True, framealpha=0.75,
        frameon=True)

    # plt.legend()
    fig.tight_layout()
    plt.savefig(param[0][:-3] + '_final.png', dpi=300, bbox_inches='tight')
    plt.close()

# gaias = np.array([np.array(_) for _ in gaias])
# for gi in (1, 2, 4, 5, 6, 7):
#     print(gi, gaias[gi].T[0], np.mean(gaias[gi].T[0]), np.std(gaias[gi].T[0]))

#     plt.subplot(121)
#     plt.scatter(gaias[gi].T[0], gaias[gi].T[1], label='GAIA' + str(gi))
#     plt.legend()
#     p_mean, p_std = np.mean(gaias[gi].T[0]), np.std(gaias[gi].T[0])
#     # plt.plot((0., .06), (0., .06), c='r')
#     # plt.plot((7., 10.), (7., 10.), c='r')
#     plt.plot(
#         (p_mean - 5 * p_std, p_mean + 5 * p_std),
#         (p_mean - 5 * p_std, p_mean + 5 * p_std), c='r')

#     plt.subplot(122)
#     plt.hist(gaias[gi].T[0], alpha=.5, label='Mean')
#     plt.hist(gaias[gi].T[1], alpha=.5, label='ML')
#     plt.legend()

#     plt.show()
