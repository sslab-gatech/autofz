#!/usr/bin/env python3
import argparse
import glob
import logging
import math
import os
import sys
from collections import ChainMap

# FIXME
if __package__ is None:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    # __package__="autofz"

import matplotlib
import matplotlib.pyplot as plt
import natsort
import numpy as np
import pandas as pd
import rich
import seaborn as sns
from autofz import config as Config
from autofz import utils
from autofz.common import IS_DEBUG, nested_dict
from matplotlib import rc
from matplotlib.lines import Line2D

from draw.draw_utils import (get_info_from_log, get_jobs_from_log,
                             get_name_from_log, get_target_from_log,
                             get_timeout_from_log, parse_log)

# sns.set(font_scale=1.5, rc={'text.usetex' : True})
rc('font', **{
    'family': 'serif',
    'serif': ['Computer Modern Roman'],
    'size': 9.5
})
# rc('text', usetex=True)
rc('figure', autolayout=True)
plt.rcParams['svg.fonttype'] = 'none'

config = Config.CONFIG
logger = logging.getLogger('autofz.draw_main')

logging.getLogger('matplotlib').setLevel(logging.WARNING)

FORMAT = 'jpg'
ARGS = None

TARGET = None

TARGETS = []

DIR = None

OUTPUT = None

FIG = None

TIMEOUT = None

METRIC = None

ALGOS = []

MAP = nested_dict()

LOGS = []

DELTA = 300

PERIOD = 3600

TICK = 60

normal12 = [(235, 172, 35), (184, 0, 88), (0, 140, 249), (0, 110, 0),
            (0, 187, 173), (209, 99, 230), (178, 69, 2), (255, 146, 135),
            (89, 84, 214), (0, 198, 248), (135, 133, 0), (0, 167, 108),
            (189, 189, 189)]

MARKER_LIST = [
    ',', '.', 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd',
    'P', 'X'
]

PALETTE = None
MARKERS = None

THRESHOLD = 10

SYS = r"\sys"

AUTOFZ_NAMES = [
    'autofz',
    'autofz-10',
    'autofz-6',
    SYS,
]

INDIVIDUAL_FUZZER = [
    'focus_afl',
    'focus_aflfast',
    'focus_mopt',
    'focus_angora',
    'focus_qsym',
    'focus_fairfuzz',
    'focus_lafintel',
    'focus_learnafl',
    'focus_libfuzzer',
    'focus_radamsa',
    'focus_redqueen',
]

INDIVIDUAL_FUZZER_NAME = [
    'AFL',
    'AFLFast',
    'MOpt',
    'FairFuzz',
    'LAF-Intel',
    'LearnAFL',
    'Angora',
    'QSYM',
    'LibFuzzer',
    'Radamsa',
    'RedQueen',
]

UNIFUZZ = [
    'exiv2',
    'ffmpeg',
    'imginfo',
    'infotocap',
    'lame',
    'mp42aac',
    'mujs',
    'nm',
    'objdump',
    'pdftotext',
    'tcpdump',
    'tiffsplit',
]

FTS = [
    'freetype2-2017',
    'harfbuzz-1.3.2',
    'libarchive-2017-01-04',
    'libjpeg-turbo-07-2017',
    'boringssl-2016-02-12',
    # 'openthread-2018-02-27-radio',
    'woff2-2016-05-06',
    'wpantund-2018-02-27',
    # 'boringssl-2016-02-12',
    'c-ares-CVE-2016-5180',
    'guetzli-2017-3-30',
    # 'json-2017-02-12',
    'lcms-2017-03-21',
    'libpng-1.2.56',
    're2-2014-12-09',
    'sqlite-2016-11-14',
    # 'vorbis-2017-12-11'
]

COMMON_TARGET = [
    'libarchive-2017-01-04',
    'exiv2',
    'imginfo',
    'tiffsplit',
    'freetype2-2017',
    'infotocap',
    'nm',  # oom killer
    'pdftotext',
    'mujs',
    'tcpdump',
    'ffmpeg',
    'boringssl-2016-02-12',
]

CUPID_TARGET = [
    'boringssl-2016-02-12', 'lcms-2017-03-21', 'woff2-2016-05-06',
    'freetype2-2017', 'libarchive-2017-01-04', 'wpantund-2018-02-27'
]

CHOSEN_MULTI = []

NAME_MAP = {}

TARGET_MAP = {
    'boringssl': 'boringssl-2016-02-12',
    'guetzli': 'guetzli-2017-3-30',
    'libarchive': 'libarchive-2017-01-04',
    'freetype2': 'freetype2-2017',
    'woff2': 'woff2-2016-05-06',
    'wpantund': 'wpantund-2018-02-27',
    'lcms': 'lcms-2017-03-21',
    'vorbis': 'vorbis-2017-12-11',
    're2': 're2-2014-12-09',
    'sqlite': 'sqlite-2016-11-14',
    'libjpeg': 'libjpeg-turbo-07-2017',
    'json': 'json-2017-02-12',
    'libpng': 'libpng-1.2.56',
    'openssl-f': 'openssl-1.0.1f',
}


def pick_algo_figure3():
    name = f'autofz'
    NAME_MAP[name] = 'autofz'
    CHOSEN_MULTI.append(name)
    CHOSEN_MULTI.extend(INDIVIDUAL_FUZZER)


def pick_algo_figure7():
    name = 'autofz_parallel'
    NAME_MAP[name] = f'autofz-10'
    CHOSEN_MULTI.append(name)
    name = 'enfuzzq_parallel'
    NAME_MAP[name] = 'CUPID-4, ENFUZZ-Q'
    CHOSEN_MULTI.append(name)
    name = 'cupid_pool_unifuzz_autofz_parallel'
    NAME_MAP[name] = 'autofz-6'
    CHOSEN_MULTI.append(name)

NAME_MAP = ChainMap(
    NAME_MAP, {
        'focus_afl': 'AFL',
        'focus_aflfast': 'AFLFast',
        'focus_mopt': 'MOpt',
        'focus_fairfuzz': 'FairFuzz',
        'focus_lafintel': 'LAF-Intel',
        'focus_learnafl': 'LearnAFL',
        'focus_angora': 'Angora',
        'focus_qsym': 'QSYM',
        'focus_libfuzzer': 'LibFuzzer',
        'focus_radamsa': 'Radamsa',
        'focus_redqueen': 'RedQueen',
    })


def _draw_one(log):
    start_time = get_info_from_log(log)['start_time']
    jobs = get_jobs_from_log(log)
    x_axis = []
    y_axis = []
    last = None
    timeout_seconds = utils.parse_delta(ARGS.timeout).total_seconds()
    SPAN = ARGS.span
    NOW = SPAN
    for entry in log['log']:
        timestamp = entry['timestamp']
        # changde to CPU time
        elasp = (timestamp - start_time) * jobs
        if elasp < NOW:
            continue
        if elasp > (timeout_seconds + 3600): continue
        # elasp_hour = elasp / PERIOD
        global_cov = entry['global_coverage']['line']
        global_ub = entry['global_unique_bugs']
        global_bitmap = entry['global_bitmap']
        if isinstance(global_bitmap, dict):
            global_bitmap = global_bitmap['count']
        x = int(elasp / TICK)
        y = None
        if METRIC == 'bitmap':
            # FIXME: 65536 is max
            y = (global_bitmap)
        elif METRIC == 'bitmap-density':
            y = (global_bitmap / 65536 * 100)
        elif METRIC == 'ub':
            y = (global_ub['unique_bugs_ip'])
        else:
            assert False
        x_axis.append(NOW / 60)
        y_axis.append(y)
        if elasp < (timeout_seconds + 300):
            last = y
        NOW += SPAN
    return x_axis, y_axis, last


def draw_overview():
    global ARGS, METRIC, FORMAT
    global FIG, MAP, TARGET

    def _draw_overview(df, algorithms, algo_order, maxx):
        global PALETTE
        df.rename(columns={'algo': 'Selected Fuzzer'}, inplace=True)
        #overall setting
        #print(algo_order)
        # print(PALETTE)
        g = sns.FacetGrid(
            df,
            col='target',
            hue='Selected Fuzzer',
            sharey=False,
            col_wrap=4,  # NOTE: change based on the total number
            # col_wrap=3,
            height=1.5,
            aspect=2,
            # hue_order=algo_order,
            palette=PALETTE)

        g.map_dataframe(
            sns.lineplot,
            y='cov',
            x='time',
            size='autofz',
            sizes={
                "True": 3,
                "False": 1.2
            },
            # legend='auto',
            # hue_order=algo_order,
            ci=ARGS.ci if not ARGS.no_ci else None,
            n_boot=500,
            estimator='mean',  # default
            # palette = PALETTE
        )
        g.tight_layout(pad=0.03, w_pad=0.004)

        #label and legends
        g.set_titles(col_template='{col_name}')

        ylabel = None
        if METRIC == 'bitmap':
            ylabel = 'Bitmap Count'
        elif METRIC == 'bitmap-density':
            ylabel = r'Bitmap Density (\%)'
        elif METRIC == 'ub':
            ylabel = r'Unique bugs'
        g.set_axis_labels('CPU Time (CPU Hour)', ylabel, fontsize=8)

        legend_handles = []
        for algo in algo_order:
            lw = 3 if algo in AUTOFZ_NAMES else 1.2
            l = Line2D([0], [0], color=PALETTE[algo], label=algo, lw=lw)
            legend_handles.append(l)

        g.figure.legend(handles=legend_handles,
                        bbox_to_anchor=(1.0, 0.25),
                        loc="lower left",
                        borderaxespad=0,
                        ncol=1,
                        frameon=False)

        timeout_seconds = utils.parse_delta(ARGS.timeout).total_seconds()
        print(timeout_seconds)
        ticks = np.arange(0, (timeout_seconds + 1) / 60, 60 * 6)
        ticklabels = [f'{int(tick/60)}' for tick in ticks]
        print(ticklabels)
        g.set(xticks=ticks)
        g.set_xticklabels(ticklabels)

        # g.set(xlim=(0,1440)
        g.set(xlim=(0, timeout_seconds / 60))
        for ax in g.axes.flatten():
            ax.get_yaxis().set_label_coords(-0.2, 0.5)

        d = os.path.join(OUTPUT, f"growth_{ARGS.timeout}_{METRIC}")
        os.makedirs(d, exist_ok=True)
        plt.savefig(os.path.join(d, f"overview.{FORMAT}"),
                    format=FORMAT,
                    bbox_inches='tight')

    algorithms = []
    data = []
    data_last = []
    count = 0
    maxx = -1
    maxy = -1
    minxx = 2**30
    minyy = 2**30
    minyy_last = 2**30
    for target in TARGETS:
        for algo, logs in MAP[target].items():
            algorithms.append(algo)
            for log in logs:
                x_axis, y_axis, last = _draw_one(log)
                if (algo in INDIVIDUAL_FUZZER_NAME):
                    individual = 'True'
                else:
                    individual = 'False'

                if (algo in AUTOFZ_NAMES):
                    autofz = 'True'
                else:
                    autofz = 'False'
                assert len(x_axis) == len(y_axis)
                for x, y in zip(x_axis, y_axis):
                    count += 1
                    if y is None:
                        continue
                    data.append([algo, x, y, target, individual, autofz])
                    maxx = max(maxx, x)
                    minxx = min(minxx, x)
                    maxy = max(maxy, y)
                    minyy = min(minyy, y)
                minyy_last = min(minyy_last, last)
                data_last.append([algo, last, target])

    algorithms = list(set(algorithms))
    df = pd.DataFrame(
        data,
        columns=['algo', 'time', 'cov', 'target', 'individual', 'autofz'])
    df_last = pd.DataFrame(data_last, columns=['algo', 'cov', 'target'])
    means = df_last.groupby('algo')['cov'].mean()
    medians = df_last.groupby('algo')['cov'].median()
    means.rename('mean cov', inplace=True)
    algo_order = means.sort_values(ascending=False).index
    algo_order_median = medians.sort_values(ascending=False).index
    print('algo order', algo_order)
    print('algo order (median)', algo_order_median)
    # print('median', medians)
    print('start drawing')
    print(df)
    _draw_overview(df, algorithms, algo_order_median, maxx)


def get_log_files(targets: list[str], algos: list[str], timeout: str,
                  directory: str):
    global ARGS, MAP
    m = nested_dict()
    count = nested_dict()
    timeout_seconds = utils.parse_delta(timeout).total_seconds()
    for target in targets:
        m[target] = {}
        count[target] = {}
        for fuzzer in algos:
            m[target][fuzzer] = []
            count[target][fuzzer] = 0
    seen = set()
    for target in targets:
        if not ARGS.no_log:
            print(f'{directory}/**/{target}*.json')

        log_files = natsort.natsorted(
            glob.glob(f'{directory}/**/{target}*.json', recursive=True))
        for log_file in log_files:
            if log_file in seen:
                continue
            seen.add(log_file)
            dirname = os.path.dirname(os.path.dirname(log_file))
            log = parse_log(log_file)
            if not log: continue

            start_time = log['start_time']
            end_time = log.get('end_time', None)
            logs = log['log']
            if not len(logs):
                if not ARGS.no_log:
                    logger.critical(f'{log_file} no log!!')
                continue
            if end_time is None:
                last = logs[-1]
                if 'global_coverage' not in last: continue
                end_time = last.get('timestamp', None)
            log_target = get_target_from_log(log)
            log_fuzzer = get_name_from_log(log)
            log_jobs = get_jobs_from_log(log)
            print(log_file, log_target, log_fuzzer)

            # print(log_fuzzer)
            if log_fuzzer not in algos:
                # debug only
                # print(dirname, log_file, log_fuzzer)
                # ban.add(dirname)
                del log
                continue
            # print(dirname, log_file, log_fuzzer, log_target)
            log_timeout_seconds = get_timeout_from_log(log)
            if not end_time:
                if not ARGS.no_log:
                    logger.critical(f'{log_file} end_time error!!')
                continue
            # NOTE: total CPU time
            if (log_timeout_seconds * log_jobs) < timeout_seconds:
                print(log_timeout_seconds, timeout_seconds)
                continue
            elasp = end_time - start_time
            logger.debug(f'{log_fuzzer} {log_file}: {elasp/PERIOD} hours')
            if (elasp * log_jobs) < timeout_seconds:
                if not ARGS.no_log:
                    logger.critical(
                        f'{log_file} elasp error!! timeout: {timeout_seconds} elasp: {elasp}'
                    )
                continue
            if len(log['log']) == 0:
                if not ARGS.no_log:
                    logger.critical(f'{log_file} log length is zero!!')
                continue

            if log_fuzzer in algos:
                # NOTE: only count upto THRESHOLD logs
                if count[log_target][
                        log_fuzzer] >= THRESHOLD and not ARGS.no_threshold:
                    continue
                m[log_target][log_fuzzer].append(log)
                count[log_target][log_fuzzer] += 1
    ret = False
    for target in targets:
        ok = True
        for fuzzer in algos:
            if fuzzer not in NAME_MAP: continue
            f = NAME_MAP[fuzzer]
            if m[target][fuzzer] and len(m[target][fuzzer]):
                if f not in MAP[target]: MAP[target][f] = []
                MAP[target][f] += m[target][fuzzer]
                ret = True
            else:
                ok = False
        if ok:
            ret = True
        else:
            pass
    # rich.print(count)
    return ret


def parse_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-o",
                   dest="output",
                   help="An output directory",
                   required=True)
    p.add_argument(
        "-T",
        dest="timeout",
        type=str,
        default='24h',
        help=
        "Timeout to draw. Log files with fuzzing time less than timeout will not be included."
    )
    p.add_argument("-m",
                   dest="metric",
                   type=str,
                   default='bitmap-density',
                   choices=['bitmap-density', 'bitmap', 'ub'],
                   help="Metric to draw")
    p.add_argument("--no-ci",
                   action="store_true",
                   default=False,
                   help="Don't draw confidence interval")
    p.add_argument("--ci", type=int, default=97, help="confidence interval")
    p.add_argument("--pdf",
                   action="store_true",
                   default=False,
                   help="output pdf file")
    p.add_argument("--svg",
                   action="store_true",
                   default=False,
                   help="output svg file")
    p.add_argument("--no-log",
                   action="store_true",
                   default=False,
                   help="Don't output some debug logs")
    p.add_argument(
        "--no-threshold",
        action="store_true",
        default=False,
        help=
        "use unlimited log files, default is first 10 logs for each (algorithm, target) pair"
    )
    p.add_argument("--span", default=900, type=int)
    p.add_argument(
        '-d',
        '--directory',
        required=True,
        help=
        "directories to scan the log json files. Choose carefully; it spends a lot of time in large directories."
    )
    p.add_argument(
        "-t",
        dest="target",
        type=str,
        nargs='+',
        required=True,
        help=
        'target binaires to include in the figure. special keywords: all, unifuzz, fts'
    )
    p.add_argument(
        "--collab",
        action="store_true",
        default=False,
        help="Draw collab fuzzing (figure 7), default is drawing figure 3.")

    return p.parse_args()


def get_algos():
    global ALGOS, ARGS
    ALGOS += CHOSEN_MULTI


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def main():
    global ARGS, TARGET, TARGETS, DIR, OUTPUT, TIMEOUT, METRIC, ALGOS, FORMAT, PALETTE, MARKERS, COLORS
    global TARGET_MAP
    if not IS_DEBUG:
        matplotlib.use('Agg')
    sns.set()

    #color translate
    COLORS = []
    for (x, y, z) in normal12:
        COLORS.append((rgb2hex(x, y, z)))
    ARGS = parse_args()
    OUTPUT = ARGS.output
    TIMEOUT = ARGS.timeout
    METRIC = ARGS.metric

    if ARGS.collab:
        pick_algo_figure7()
    else:
        pick_algo_figure3()

    if ARGS.svg:
        FORMAT = 'svg'
    elif ARGS.pdf:
        FORMAT = 'pdf'
    DIR = os.path.realpath(ARGS.directory)

    if 'all' in ARGS.target:
        TARGETS = COMMON_TARGET
    elif 'cupid' in ARGS.target:
        TARGETS = CUPID_TARGET
    elif 'unifuzz' in ARGS.target:
        TARGETS = UNIFUZZ
    else:
        TARGETS = ARGS.target

    for index, target in enumerate(TARGETS):
        if target in TARGET_MAP:
            TARGETS[index] = TARGET_MAP[target]

    get_algos()
    PALETTE_ALGOS = []
    for algo in ALGOS:
        if algo in NAME_MAP:
            PALETTE_ALGOS.append(NAME_MAP[algo])
        else:
            print(f'{algo} not in NAME_MAP')
    # unique
    PALETTE_ALGOS = sorted(list(set(PALETTE_ALGOS)))
    # print('palette algos', PALETTE_ALGOS)
    assert PALETTE_ALGOS is not None
    if len(PALETTE_ALGOS) < len(COLORS):
        PALETTE = dict(zip(PALETTE_ALGOS, sns.color_palette(COLORS)))
    else:
        print(len(sns.color_palette('tab20')))
        PALETTE = dict(zip(PALETTE_ALGOS, sns.color_palette('tab20')))

    assert PALETTE is not None
    # print('palette', PALETTE)
    if len(PALETTE_ALGOS) < len(MARKER_LIST):
        MARKERS = dict(zip(PALETTE_ALGOS, MARKER_LIST))
    if not get_log_files(TARGETS, ALGOS, ARGS.timeout, DIR):
        logger.error(f'targets: {TARGETS}, log_files is None')
        exit(1)
    os.makedirs(OUTPUT, exist_ok=True)
    draw_overview()


if __name__ == '__main__':
    main()
