
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re


def main():
    bfr_mode = 'bfixed_0'  # 'bfree'

    data_true, data_mean, data_map, err_asteca = get_massclean_data(bfr_mode)
    print(data_true.shape)
    masscleaPlot(bfr_mode, data_true, data_mean, data_map, err_asteca)
    print("Finished")


def skip_comments(f):
    '''
    Read lines that DO NOT start with a # symbol.
    '''
    for line in f:
        if not line.strip().startswith('#'):
            yield line


def get_massclean_data(bfr_mode):
    '''
    Read the ASteCA output data file 'asteca_output.dat' for the synthetic
    clusters generated with MASSCLEAN.
    '''

    synth_names = []
    data_true, data_mean, data_map, err_asteca = [], [], [], []
    print("Filtered out: mass error > 200%")
    with open('asteca_output_{}.dat'.format(bfr_mode)) as f:
        for line in skip_comments(f):
            delimiters = "/", "_"
            regexPattern = '|'.join(map(re.escape, delimiters))
            mma = re.split(regexPattern, line.split()[0])
            mass = float(mma[0])
            dist = 5. * np.log10(float(mma[1])) - 5.
            ext = float(mma[2]) / 3.1
            met = float('0.' + mma[4][1:])
            age = float(mma[5]) * 0.01
            bfr = float(mma[6])
            # Read clusters parameters obtained by ASteCA.
            data = list(map(float, line.split()[17:-10]))

            if abs(mass - data[12]) / mass < 2.:
                synth_names.append(line.split()[0])
                data_true.append([met, age, ext, dist, mass, bfr])
                data_mean.append(data[0::3])
                data_map.append(data[1::3])
                err_asteca.append(data[2::3])
            else:
                print(line.split()[0])

    print("\nMass error > 100%")
    j = 0
    for i, dt in enumerate(data_true):
        rel_err = abs(dt[4] - data_mean[i][4]) / dt[4]
        if rel_err > 1:
            print(j, rel_err, synth_names[i])
            j += 1

    print("z error > 500%")
    j = 0
    for i, dt in enumerate(data_true):
        rel_err = abs(dt[0] - data_mean[i][0]) / dt[0]
        if rel_err > 5:
            print(j, rel_err, synth_names[i])
            j += 1

    print("\n N clusters read:", len(synth_names))
    return np.array(data_true).T, np.array(data_mean).T,\
        np.array(data_map).T, np.array(err_asteca).T


def rand_jitter(arr, jitter):
    """
    Add random scatter to array.
    """
    stdev = jitter * (max(arr) - min(arr))
    return arr + np.random.randn(len(arr)) * stdev


def masscleaPlot(bfr_mode, data_true, data_mean, data_map, err_asteca):
    """
    Plot MASSCLEAN true metallicities versus the metallicity estimates obtained
    by ASteCA, and its relation with the masses.
    """
    plt.style.use('seaborn-darkgrid')

    plot_pars = [
        [1, r"$z$", r'$\Delta z$', r"$\log(age)$", "o", "viridis"],
        [0, r"$\log(age)$", r'$\Delta \log(age)$', r"$z$", "v", "magma"],
        [1, r'$E_{(B-V)}$', r'$\Delta E_{(B-V)}$', r"$\log(age)$", "s",
         "viridis"],
        [4, r'$\mu_0$', r'$\Delta \mu_0$', r"$M\;[M_{\odot}]$", "*", "magma"],
        [2, r'$M\;[M_{\odot}]$', r'$\Delta M\;[M_{\odot}]$', r"$E_{(B-V)}$",
         "^", "viridis"]
    ]
    #     [4, r"$b_{fr}$", r'$\Delta b_{fr}$', r"$M\;[M_{\odot}]$", "o", "magma"]
    # ]

    true_vals = []
    for dt in data_true:
        true_vals.append(sorted(set(dt)))

    for di, data_asteca in enumerate([data_mean, data_map]):
        mean_map_name = ['mean', 'map']
        # Generate plot.
        fig = plt.figure(figsize=(30, 30))
        gs = gridspec.GridSpec(12, 12)

        for i, par in enumerate(plot_pars):
            print(par[1])

            ax = plt.subplot(gs[2 * i:2 + (2 * i), 0:2])
            delta_p = data_true[i] - data_asteca[i]
            mn, std = np.median(delta_p), np.std(delta_p)
            frm = ["{:.4f}", "{:.2f}", "{:.3f}", "{:.2f}", "{:.0f}", "{:.1f}"]
            p = frm[i]
            ax.set_title((p + r"$\pm$" + p).format(mn, std))

            plt.plot([-10000., 10000.], [-10000., 10000.], c='r', ls='--',
                     zorder=1)
            x = rand_jitter(data_true[i], .1)
            plt.errorbar(
                x, data_asteca[i], yerr=err_asteca[i], linestyle="None")
            ax.scatter(
                x, data_asteca[i],
                c=data_true[par[0]], marker=par[4], s=150, alpha=.7,
                cmap=par[-1], zorder=4)
            for val in true_vals[i]:
                plt.axvline(x=val, color='g', ls='--')
            delt = (true_vals[i][-1] - true_vals[i][0]) * .75
            plt.xlim(true_vals[i][0] - delt, true_vals[i][-1] + delt)
            plt.ylim(true_vals[i][0] - delt, true_vals[i][-1] + delt)
            ax.set_xlabel(par[1], fontsize=20)
            ax.set_ylabel(par[1] + " (ASteCA)", fontsize=20)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)

            ax = plt.subplot(gs[2 * i:2 + (2 * i), 2:8])
            if i == 0:
                ax.set_title(r"$\Delta=(True-\mathtt{ASteCA})$",
                             fontsize=20)

            delta_p_rel = 100. * (data_true[i] - data_asteca[i]) / data_true[i]

            SC = plt.scatter(
                rand_jitter(data_true[i], .07), delta_p_rel, s=150,
                alpha=.7, c=data_true[par[0]], marker=par[4], lw=1.5,
                cmap=par[-1])

            mn, std = np.median(delta_p_rel), np.std(delta_p_rel)
            plt.axhline(
                y=mn, color='k', ls='--', label=(r"${:.2f}\pm{:.2f}$").format(
                    mn, std))
            plt.axhline(y=mn - std, color='r', ls=':')
            plt.axhline(y=mn + std, color='r', ls=':')

            for val in true_vals[i]:
                plt.axvline(x=val, color='g', ls='--')

            plt.legend(fontsize=15, handlelength=0.)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            ax.set_xlabel(par[1], fontsize=20)
            ax.set_ylabel(par[2], fontsize=20)

            # Colorbar.
            cbar = plt.colorbar(SC, ax=ax, pad=0.01)
            cbar.set_label(par[3], fontsize=15, labelpad=10)

        # Output png file.
        fig.tight_layout()
        plt.savefig(
            'results_{}_{}.png'.format(
                bfr_mode, mean_map_name[di]), dpi=300, bbox_inches='tight')
        plt.clf()
        plt.close()


if __name__ == '__main__':
    main()
