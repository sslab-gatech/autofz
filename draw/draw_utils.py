import copy
import json
import os

from autofz import utils

AFL = 'afl'
AFLFAST = 'aflfast'
FAIRFUZZ = 'fairfuzz'
MOPT = 'mopt'
QSYM = 'qsym'
ANGORA = 'angora'
RADAMSA = 'radamsa'
REDQUEEN = 'redqueen'
LEARNAFL = 'learnafl'
LAFINTEL = 'lafintel'
LIBFUZZER = 'libfuzzer'

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
    'freetype2-2017', 'harfbuzz-1.3.2', 'libarchive-2017-01-04',
    'libjpeg-turbo-07-2017', 'openssl-1.0.1f', 'openssl-1.0.2d',
    'boringssl-2016-02-12', 'openthread-2018-02-27-radio', 'woff2-2016-05-06',
    'wpantund-2018-02-27', 'boringssl-2016-02-12', 'c-ares-CVE-2016-5180',
    'guetzli-2017-3-30', 'json-2017-02-12', 'lcms-2017-03-21', 'libpng-1.2.56',
    're2-2014-12-09', 'sqlite-2016-11-14', 'vorbis-2017-12-11'
]

ENFUZZA_FUZZERS = ['afl', 'aflfast', 'fairfuzz', 'afl']
ENFUZZQ_FUZZERS = ['afl', 'aflfast', 'fairfuzz', 'qsym']
ENFUZZ_BEST_FUZZERS = ['afl', 'fairfuzz', 'libfuzzer', RADAMSA]

CUPID_FUZZERS = ['afl', 'fairfuzz', 'libfuzzer', 'qsym']
CUPID_FUZZERS_POOL = [
    'fairfuzz', 'qsym', 'libfuzzer', 'afl', 'aflfast', 'radamsa'
]
CUPID_FUZZERS_POOL_UNIFUZZ = [
    'fairfuzz', 'qsym', 'lafintel', 'afl', 'aflfast', 'radamsa'
]
TOP_FUZZERS = [
    'redqueen',
    'lafintel',
    'afl',
    'mopt',
    'learnafl',
    'aflfast',
    'fairfuzz',
    'qsym',
    'angora',
    'radamsa',
]


def get_autofz_args(log):
    '''
    to support old key name
    '''
    if 'autofz_args' in log:
        return log['autofz_args']
    elif 'autofuzz_args' in log:
        return log['autofuzz_args']
    return None


def get_autofz_config(log):
    '''
    to support old key name
    '''
    if 'autofz_config' in log:
        return log['autofz_config']
    elif 'autofuzz_config' in log:
        return log['autofuzz_config']
    return None


def get_fuzzers_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    fuzzers = autofz_args['fuzzer']
    if 'all' in fuzzers:
        fuzzers = list(autofz_config['fuzzer'].keys())
    return fuzzers


def get_focus_one_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    fuzzers = autofz_args['fuzzer']
    if 'all' in fuzzers:
        fuzzers = list(autofz_config['fuzzer'].keys())
    focus = autofz_args['focus_one']
    assert focus in fuzzers
    return focus


def get_fuzzer_num_from_log(log):
    fuzzers = get_fuzzers_from_log(log)
    return len(fuzzers)


def get_target_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    target = autofz_args['target']
    return target


def get_jobs_from_log(log):
    autofz_args = get_autofz_args(log)
    jobs = autofz_args.get('jobs', 1)
    return jobs


def get_timeout_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    timeout = autofz_args['timeout']
    seconds = utils.parse_delta(timeout).total_seconds()
    return seconds


def get_prep_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    prep = autofz_args['prep']
    return prep


def get_focus_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    focus = autofz_args['focus']
    return focus


def get_sync_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    sync = autofz_args.get('sync', 0)
    return sync


def get_autofz_parameter_from_log(log):
    prep = get_prep_from_log(log)
    focus = get_focus_from_log(log)
    sync = get_sync_from_log(log)
    return {'prep': prep, 'focus': focus, 'sync': sync}


def get_name_from_log(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    name = None
    is_autofz = True

    if autofz_args.get('focus_one', None):
        name = f"focus_{autofz_args['focus_one']}"
        is_autofz = False
    elif autofz_args.get('enfuzz', None):
        if is_cupid(log):
            name = f'cupid'
        elif is_cupid_pool(log):
            name = f'cupid_pool'
        elif is_cupid_pool_unifuzz(log):
            name = f'cupid_pool_unifuzz'
        elif is_enfuzzq(log):
            name = f'enfuzzq'
        elif is_enfuzza(log):
            name = f'enfuzza'
        else:
            name = f'enfuzz'
        is_autofz = False
    else:
        if is_cupid_pool(log):
            name = f'cupid_pool_autofz'
        elif is_cupid_pool_unifuzz(log):
            name = f'cupid_pool_unifuzz_autofz'
        else:
            name = f'autofz'

    parallel = autofz_args.get('parallel', False)

    if parallel:
        name = f'{name}_parallel'

    suffix = autofz_args.get('suffix', '')
    if suffix:
        name = f'{name}_{suffix}'

    return name


def is_enfuzz(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    return autofz_args.get('enfuzz', False)


def is_focus(log):
    autofz_args = get_autofz_args(log)
    autofz_config = get_autofz_config(log)
    if autofz_args['focus_one']:
        return True
    return False


def is_cupid(log):
    global CUPID_FUZZERS
    fuzzers = get_fuzzers_from_log(log)
    # if not is_enfuzz(log): return False
    return set(fuzzers) == set(CUPID_FUZZERS)


def is_cupid_pool(log):
    global CUPID_FUZZERS_POOL
    fuzzers = get_fuzzers_from_log(log)
    return set(fuzzers) == set(CUPID_FUZZERS_POOL)


def is_cupid_pool_unifuzz(log):
    global CUPID_FUZZERS_POOL_UNIFUZZ
    fuzzers = get_fuzzers_from_log(log)
    return set(fuzzers) == set(CUPID_FUZZERS_POOL_UNIFUZZ)


def is_enfuzzq(log):
    global ENFUZZQ_FUZZERS
    fuzzers = get_fuzzers_from_log(log)
    return set(fuzzers) == set(ENFUZZQ_FUZZERS)


def is_enfuzza(log):
    global ENFUZZA_FUZZERS
    fuzzers = get_fuzzers_from_log(log)
    return set(fuzzers) == set(ENFUZZA_FUZZERS)


def map_coverage_to_line(coverage):
    ret = {}
    for f, cov in coverage.items():
        ret[f] = cov['line']
    return ret


def get_info_from_log(log):
    jobs = get_jobs_from_log(log)
    start_time = log.get('start_time', None)
    end_time = log.get('end_time', None)

    return copy.deepcopy({
        'fuzzers': get_fuzzers_from_log(log),
        'target': get_target_from_log(log),
        'timeout': get_timeout_from_log(log),
        'start_time': start_time,
        'end_time': end_time,
        'jobs': jobs
    })


def find_entry(entries, time_point, start_time):
    if time_point is None: return entries[-1]
    s = utils.time_to_seconds(time_point)
    last = None
    # ordered
    for entry in entries:
        timestamp = entry['timestamp']
        elasp = timestamp - start_time
        if elasp > s: return entry
        last = entry
    # timestamp = last['timestamp']
    # elasp = timestamp - start_time
    # if (elasp + 300) >= s: return last
    assert False


def find_last_entry(entries, time_point, start_time):
    if time_point is None: return entries[-1], -1
    s = utils.time_to_seconds(time_point)
    last = None
    last_elasp = None
    # ordered
    for entry in entries:
        timestamp = entry['timestamp']
        elasp = timestamp - start_time
        if elasp > s: break
        last = entry
        last_elasp = elasp
    return last, last_elasp


def parse_log(log_file):
    if not os.path.exists(log_file):
        print(f'{log_file} does not exists')
        return None
    log = None
    try:
        with open(log_file, 'r') as f:
            log = json.load(f)
    except json.decoder.JSONDecodeError:
        log = None
    return log


def get_last(log, timeout):
    start_time = log['start_time']
    last_entry, last_elasp = find_last_entry(log['log'], timeout, start_time)
    assert last_entry
    # last_entry = log['log'][-1]
    global_ub = last_entry['global_unique_bugs']
    global_bitmap = last_entry['global_bitmap']
    last_ub = None
    last_bitmap = None
    if isinstance(global_bitmap, dict):
        global_bitmap = global_bitmap['count']
    last_bitmap = global_bitmap
    last_ub = global_ub
    assert last_bitmap
    assert last_ub
    return last_bitmap, last_ub
