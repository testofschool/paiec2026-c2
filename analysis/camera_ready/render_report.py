"""Render the Korean release report from verified run artifacts and the local commit audit."""
import csv
import json
from math import fsum
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT, RUN, REPO = ROOT / 'out', ROOT / 'run', ROOT / 'repo'
SOURCE = REPO / 'analysis/camera_ready'
EVIDENCE = REPO / 'verification/evidence/camera_ready'
BUDGETS = (0, 1, 3, 7, 15, 31)


def load(file):
    return json.loads(file.read_bytes())


def fmt(value, digits=7):
    if value is None:
        return '—'
    return f'{value:.{digits}f}'


def interval(values):
    return '[' + ', '.join(fmt(x) for x in values) + ']'


def cell(x):
    return str(x).replace('|', r'\|').replace('\n', ' ')


def table(header, rows):
    lines = ['| ' + ' | '.join(map(cell, header)) + ' |', '| ' + ' | '.join('---' for _ in header) + ' |']
    lines.extend('| ' + ' | '.join(map(cell, row)) + ' |' for row in rows)
    return '\n'.join(lines)


def full_method_scores(expected_count):
    values = {method: {b: [] for b in BUDGETS} for method in ['frozen', 'C2']}
    count = 0
    for file in sorted((RUN / 'camera_ready_m5').glob('*/scores.csv')):
        with file.open() as f:
            for row in csv.DictReader(f):
                count += 1
                for method, bins in values.items():
                    for b in BUDGETS:
                        bins[b].append(float(row[f'{method}_b{b}']))
    if count != expected_count:
        raise ValueError('Incomplete uncapped pair scores')
    return {m: {str(b): fsum(v) / count for b, v in bins.items()} for m, bins in values.items()}


def confidence_gap(stats):
    """Mean confidence in the predicted binary outcome minus observed accuracy."""
    gap = 0.0
    for b in stats['bins']:
        n = b['responses']
        if n:
            signed = b['mean_prediction'] - b['observed_rate']
            gap += n * (signed if b['lower'] >= .5 else -signed)
    return gap / stats['responses']


def success_probability_gap(stats):
    return fsum(b['responses'] * (b['mean_prediction'] - b['observed_rate'])
                for b in stats['bins'] if b['responses']) / stats['responses']


def report():
    results = load(SOURCE / 'RESULTS_v21.json')
    t7, t0 = load(OUT / 'T7.json'), load(OUT / 'T0.json')
    repro = results['repro_gate']
    m = results['measurements']
    m2, m3, m4, m5, m6 = (m[x]['values'] for x in ['M2','M3','M4','M5','M6'])
    adapter, wrapper, design = m['M2']['adapter_gate'], m['M5']['wrapper_gate'], m['M3']['design_check']
    prereg = load(EVIDENCE / 'source_preregistration.json')['checks']
    bl = load(EVIDENCE / 'baselines.json')
    data = load(RUN / 'data_receipt.json')
    counts = m['M0']['values']
    count_keys = ['inventory_benchmarks', 'benchmarks_any_pair_n_ge_5', 'benchmarks_positive_eligible_pairs']
    sections = ['# PAIEC v21 카메라레디 측정 결과',
        ' · '.join(['T0 기록', 'REPRO_GATE ' + repro['status'], 'M0 ' + '/'.join(str(counts[k]) for k in count_keys),
                    'M2 ' + m['M2']['status'], 'M3 cap별 쌍 ' + '/'.join(str(m3[str(c)]['pairs']) for c in (1,2,4,8,16)),
                    'design_check ' + design['status'], 'M4 ' + m['M4']['status'], 'M5 wrapper_gate ' + wrapper['status'],
                    'M6 ' + m['M6']['status'], 'commit ' + t7['commit'][:8]]),
        '이번 실행은 공개 측정 데이터의 split2에서 논문 수치와 추가 분석을 확인했다. Brier 점수와 여섯 예산의 가중합인 ALC는 값이 낮을수록 좋다. 각 쌍은 전체 ALC에서 같은 가중치를 갖는다.',
        '## 실행 환경과 입력',
        f"{t0['cpu']['stdout']} ({t0['architecture']['stdout']}), macOS {t0['macos']['stdout']}, "
        f"메모리 {int(t0['memory_bytes']['stdout'])/2**30:.0f} GiB, {t0['python']['version']['stdout']}. "
        f"등록된 measurement-db 리비전 `{data['public_revision']}`의 파일 {data['files']:,}개 "
        f"({data['bytes']:,}바이트)가 입력 해시 검사를 통과했다.",
        '첫 번째 준비 시도에서 로컬 캐시에 필요한 테이블 일부가 없었고 다음 시도에서는 오프로드된 파일을 감지했다. '
        f"초기 {t0['pinned_data']['initially_available_of_652']}개 파일에 나머지 {t0['pinned_data']['initially_missing_of_652']}개를 "
        '같은 리비전에서 확보해 다시 실행했다. 아래 RSS는 각 명령의 최대 상주 메모리다.']
    runs = []
    for filename, category in [('T1_partial_hf_cache.json','초기 캐시'),('T1_offloaded.json','오프로드 검사'),('T1_stages.json','최종 실행')]:
        for s in load(OUT / filename):
            rss = s['peak_rss_bytes']
            runs.append([category, s['stage'],s['exit'],fmt(s['wall_seconds'],2),fmt(rss/2**30,3) if rss is not None else '—'])
    sections.extend([table(['시도','단계','종료 코드','소요 시간(초)','최대 RSS(GiB)'],runs),
                     '## 사전등록 대조',
                     '공개 저장소와 첨부파일에서 직접 읽은 값이다. 이 표의 split2 등록값을 새 실행 결과와 대조한 값은 바로 아래 표에 있다.',
                     table(['항목','기대값','출처에서 읽은 값','차이','판정'],[
                         [r['name'],str(r['expected']),str(r['actual']),r['difference'] if r['difference'] is not None else '동일' if r['status']=='MATCH' else '다름',r['status']] for r in prereg]),
                     table(['새 실행 지표','기대값','실측값','절대차','허용 오차'],[
                         [k,repr(v['expected']),repr(v['actual']),f"{v['absolute_difference']:.3g}",repro['tolerance']] for k,v in repro['checks'].items()]),
                     '## M0 · 벤치마크와 쌍의 수',
                     table(['조건','기대','실측','차이'],[
                         [label,m['M0']['expected'][k],counts[k],counts[k]-m['M0']['expected'][k]]
                         for label,k in zip(['등록된 인벤토리','이진 응답이 5개 이상인 쌍이 하나 이상','평가 자격을 충족한 쌍이 하나 이상'],count_keys)]),
                     f"사전분포를 적합할 때는 벤치마크와 전체 subject 설정을 한 쌍으로 센다. 이진 응답이 5개 이상인 쌍 "
                     f"{counts['pairs_n_ge_5']:,}개가 {counts[count_keys[1]]}개 벤치마크에 걸쳐 있다. split2 평가는 벤치마크 내 원래 subject ID에 "
                     f"서로 다른 item이 80개 이상인 {counts['scored_raw_pairs']:,}개 쌍을 사용한다.",
                     f"M1은 실행 문서에 측정 정의가 없으며 TeX의 보류 표시에는 {', '.join(m['M1']['values']['tex_pending_ids'])}만 나온다. "
                     f"결과 파일의 M1 상태는 `{m['M1']['status']}`다.",
                     '## M2 · 공식 경험 평균 및 M6 · Beta(1,1)',
                     f"평가 표본은 {bl['benchmarks']}개 벤치마크, {bl['pairs']:,}개 쌍이다. "
                     '공식 경험 평균은 같은 벤치마크에서 표시된 subject 속성이 일치하는 획득 라벨을 평균하고, '
                     '라벨이 없으면 0.5를 예측한다. Beta(1,1)은 해당 쌍의 라벨만 사용해 (1+s)/(2+n)을 예측한다. '
                     f"공식 소스 파일의 SHA-256은 `{bl['official_model']['sha256']}`이다."])
    training = load(RUN / 'artifacts/prepare_summary.json')
    failed = [r['bench'] for r in training['fits'] if not r['success']]
    historic = load(REPO / 'verification/fresh_training_summary.json')['fit_summary']
    same = set(failed) == {r['bench'] for r in historic['nonconverged_fits']}
    sections.insert(sections.index('## 사전등록 대조'),
                    f"분산 적합 {training['benchmarks']}건 중 {training['fit_successes']}건이 수렴했다. "
                    + ', '.join(failed) + "에서는 500회 반복 한도에 도달했다. "
                    + ("세부 목록이 기존 릴리스의 비수렴 목록과 일치한다. " if same else "기존 릴리스와 목록이 다르다. ")
                    + "등록된 절차대로 이 추정값도 분산 계산에 포함했다.")
    sections.append("원래의 경험평균 채점 파일은 검색 범위에서 식별되지 않았다. 이번 재계산에서 생성한 "
                    "`verification/evidence/camera_ready/empirical_mean/benchmark_sums.csv`는 "
                    "벤치마크별 쌍 수와 점수 합계를 담고 있어 표의 전체 평균과 신뢰구간을 재계산할 수 있다.")
    scores = full_method_scores(bl['pairs'])
    rows = []
    for label, alc, br in [('Base',adapter['observed']['frozen_ALC'],scores['frozen']),('C2',adapter['observed']['C2_ALC'],scores['C2']),
                           ('공식 경험 평균',m2['alc'],m2['brier']),('Beta(1,1)',m6['alc'],m6['brier'])]:
        rows.append([label,fmt(alc),*(fmt(br[str(b)]) for b in BUDGETS)])
    sections.append(table(['방법','ALC',*(f'B{b}' for b in BUDGETS)],rows))
    ref = m['M2']['reference_displayed']
    ref_rows = [('ALC',ref['alc'],m2['alc']), *((f'B{b}',ref['brier'][str(b)],m2['brier'][str(b)]) for b in BUDGETS),
                *((f'경험 평균 − C2, CI {side}',e,a) for side,e,a in zip(['하한','상한'],ref['baseline_minus_C2_ci95'],m2['baseline_minus_C2_ci95']))]
    sections.extend([f"M2의 제출 PDF 표시값과 재계산값 판정은 `{m['M2']['status']}`다. 각 값의 허용 절대차는 {bl['M2']['tolerance']}다.",
        table(['대조 항목','제출 PDF','재계산값','절대차'],[[n,fmt(e,4),fmt(a,9),fmt(abs(a-e),9)] for n,e,a in ref_rows]),
        '두 차이의 부호를 표에 명시했다. C2 승수는 각 fold의 평균 ALC가 비교 방법보다 엄격하게 낮은 횟수다. '
        '95% 구간은 벤치마크를 복원추출하고 그 표본 안에서 쌍에 같은 가중치를 둔 백분위 구간이다(2,000회, seed 0).',
        table(['비교 방법','C2 − 비교 방법','95% CI','비교 방법 − C2, 95% CI','C2 승수 / fold'],[
            [label,fmt(r['C2_minus_baseline']),interval(r['C2_minus_baseline_ci95']),interval(r['baseline_minus_C2_ci95']),
             f"{r['C2_fold_wins']} / {len(r['fold_C2_minus_baseline'])}"] for label,r in [('공식 경험 평균',m2),('Beta(1,1)',m6)]]),
        table(['fold','C2 − 경험 평균','C2 − Beta(1,1)'],[[fold,fmt(v),fmt(m6['fold_C2_minus_baseline'][fold])] for fold,v in sorted(m2['fold_C2_minus_baseline'].items())]),
        '## M3 · 벤치마크별 subject 수 제한',
        '각 벤치마크에서 자격을 충족한 subject ID를 사전 계획의 SHA-256 순서로 정렬하고 각 cap까지 남겼다. '
        '남은 subject의 라벨만 공개하고 각 fold의 학습 사전분포와 분산을 재사용했다. Beta(1.5,1.5)는 (1.5+s)/(3+n)이다.',
        f"이번 선택 규칙과 split2 계획은 {load(SOURCE / 'sparse_plan_receipt.json')['recorded_at']}에 고정했다. "
        "10월 27일에 등록한 v14 계획은 다른 선택 해시와 split4, bootstrap seed 20261026을 사용했다. "
        "따라서 초안에 적힌 10월 27일 사전등록 날짜는 이번 v21 측정의 등록 날짜로 인용할 수 없다.",
        table(['cap','벤치마크','쌍','방법','ALC',*(f'B{b}' for b in BUDGETS)],
              [[cap,r['benchmarks'],r['pairs'],{'frozen':'Base','C2':'C2','beta15':'Beta(1.5,1.5)'}[name],
                fmt(row['ALC']),*(fmt(row['Brier'][str(b)]) for b in BUDGETS)]
               for cap,r in sorted(m3.items(),key=lambda v:int(v[0])) for name,row in r['methods'].items()]),
        '다음 표에서 양수는 C2의 ALC가 낮음을 뜻한다. 95% 구간은 M2와 동일한 벤치마크 단위 재표집으로 구했다.',
        table(['cap','비교 방법','비교 방법 − C2','95% CI','C2 − 비교 방법, 95% CI','C2 승수 / fold','동률'],[
                [cap,'Base' if k=='frozen' else 'Beta(1.5,1.5)',fmt(c['difference']),interval(c['ci95']),
                 interval([-c['ci95'][1],-c['ci95'][0]]),
                 f"{c['C2_fold_wins']} / {len(c['fold_mean_differences'])}",c['ties']]
                for cap,r in sorted(m3.items(),key=lambda v:int(v[0])) for k,c in r['comparisons'].items()])])
    for key, label in [('frozen','Base'),('beta15','Beta(1.5,1.5)')]:
        tied, worse, crosses = [], [], []
        for cap, r in sorted(m3.items(),key=lambda v:int(v[0])):
            diff = r['comparisons'][key]['difference']
            low, high = r['comparisons'][key]['ci95']
            if abs(diff) <= 1e-12:
                tied.append(cap)
            elif diff < 0:
                worse.append(cap)
            if low <= 0 <= high:
                crosses.append(cap)
        caplist = lambda caps: ', '.join(caps) if caps else '없음'
        sections.append(f"{label}와 비교한 C2의 ALC 점추정에서 동률인 cap(절대차 ≤ 1e-12)은 {caplist(tied)}, "
                        f"C2 손실이 더 큰 cap은 {caplist(worse)}이다. 두 방법 간 차이의 95% 구간이 0을 포함하는 cap은 {caplist(crosses)}이다.")
    reference = m['M3']['reference_v14']
    if isinstance(reference, dict) and 'caps' in reference:
        sections.extend(['v14은 실행 기기와 subject 선택 규칙이 달라 참고값으로 병기한다.',
                         table(['cap','v14 쌍','v14 C2 ALC','v21 쌍','v21 C2 ALC'],[
                             [c,r['pairs'],fmt(r['C2_ALC']),m3[c]['pairs'],fmt(m3[c]['methods']['C2']['ALC'])] for c,r in reference['caps'].items()])])
    else:
        sections.append(f"v14 참고값은 `{reference}`로 기록했다.")
    sections.extend(['## M4 · C2E 완료 영수증',
            f"발견한 {m4['discovered_directories']}개 폴더 중 {m4['fixture_directories']}개가 테스트 fixture였다. "
            f"총 {m4['total_receipts_examined']}개 영수증을 확인했고, 마감({m4['stop_line_kst']}) 이전 완료 시각, "
            f"벤치마크·단계·보존 파일이 연결된 영수증으로 확인한 벤치마크는 {len(m4['verified_benchmarks_before_stop'])}개였다. "
            f"상태는 `{m['M4']['status']}`다. " + ('당시 완료된 벤치마크 총수는 확인할 수 없다.' if m4['historical_completed_count'] is None else f"확인된 완료 개수는 {m4['historical_completed_count']}개다."),
            '## M5 · 응답 가중 신뢰도',
            '각 예산의 응답을 예측 성공 확률에 따라 폭이 같은 10개 구간에 배치했다. ECE는 구간별 평균 예측과 관측 성공률의 절대차를 구간 응답 수로 가중한 평균이다. '
            '성공 확률의 방향은 평균 예측 확률에서 관측 성공률을 뺀 응답 가중 차이로 나타냈다. '
            '별도로 이진 분류의 과신을 측정하기 위해 각 응답의 예측 결과(성공 확률 0.5 이상이면 성공)에 부여한 확신도에서 해당 결과의 실제 적중률을 뺐다. '
            '마지막 열이 양수이면 이 평가 표본에서 평균 확신도가 적중률보다 높았다.',
            table(['방법','예산','응답 수','ECE','평균 예측 성공률 − 관측 성공률','평균 확신도 − 적중률'],[
               ['Base' if method=='frozen' else method,b,r['responses'],fmt(r['ECE']),fmt(success_probability_gap(r)),fmt(confidence_gap(r))] for method, group in m5.items() for b,r in group.items()])])
    for b in ['15','31']:
        gap = confidence_gap(m5['C2'][b])
        direction = '높았다' if gap > 0 else '낮았다' if gap < 0 else '같았다'
        comparison = f"{abs(gap)*100:.3f}%p {direction}" if gap else direction
        sections.append(f"C2 B{b}에서 평균 확신도는 관측 적중률과 비교해 {comparison}. "
                        f"해당 예산의 ECE는 {fmt(m5['C2'][b]['ECE'])}였다.")
    sections.extend(['빈 구간은 평균을 계산할 수 없어 대시로 표시한다. 마지막 구간은 1을 포함한다. 벡터 그림은 `verification/evidence/camera_ready/reliability.pdf`에 있다.',
            table(['방법','예산','예측 구간','응답 수','평균 예측','관측 성공률'],[
                ['Base' if method=='frozen' else method,b,f"[{bn['lower']:.1f}, {bn['upper']:.1f}"+(']' if bn['upper']==1 else ')'),
                 bn['responses'],fmt(bn['mean_prediction']),fmt(bn['observed_rate'])]
                for method, group in m5.items() for b,r in group.items() for bn in r['bins']]),
            '## T7 · 재현성과 변경 범위',
            table(['관문','항목','절대차','허용 오차','판정'],
              [['REPRO_GATE',k,format(r['absolute_difference'],'.4g'),repro['tolerance'],repro['status']] for k,r in repro['checks'].items()]
              + [[name,k,format(diff,'.4g'),gate['tolerance'],gate['status']] for name,gate in [('adapter_gate',adapter),('wrapper_gate',wrapper)] for k,diff in gate['absolute_differences'].items()]
              + [['design_check','cap 1 Base/C2 ALC',format(design['absolute_difference'],'.4g'),design['tolerance'],design['status']]]),
            f"기준 커밋 `{t7['base']}`, 로컬 `{t7['branch']}` 커밋 `{t7['commit']}`. "
            f"동결 파일 {len(t7['frozen'])}개 중 해시가 다른 파일은 {sum(not f['unchanged'] for f in t7['frozen'])}개다. "
            f"허용된 경로 밖에서 바뀐 파일 {len(t7['paths_outside_scope'])}개, 홈 경로 문자열 일치 {len(t7['home_path_matches'])}건이다.",
            table(['동결 파일','실행 전 SHA-256','실행 후 SHA-256','기준 커밋과 일치'],[
                [r['path'],r['before'],r['after'],'예' if r['unchanged'] else '아니오'] for r in t7['frozen']]),
            f"작업 트리 검사(`git status --porcelain`) 출력은 {repr(t7['git_status_porcelain'])}다. "
            f"패치를 기준 커밋에 적용하여 커밋의 파일 트리가 재구성되는지 확인한 결과는 {'PASS' if t7['patch_rebuilds_commit_tree'] else 'FAIL'}다.",
            '기준 커밋 대비 변경 파일과 diff 통계',
            '\n'.join('- `'+path+'`' for path in t7['files']),
            '```text\n'+t7['git_diff_stat'].rstrip()+'\n```',
            '## 해석 범위와 전달 파일',
            '각 점수와 구간은 공개 데이터에서 동기화된 라벨 예산으로 수행한 split2 시뮬레이션 결과다. '
            'M3의 cap 효과와 M5의 보정 경향은 위 선택 규칙과 평가 표본을 기준으로 해석한다. '
            '비동기 획득 예산이나 비공개 대회 평가에서의 성능은 이번에 측정하지 않았다.',
            '첨부된 formative 기록은 과거 제출 화면의 전사본이다. 종점수와 상세 항목의 확인 날짜가 다르며, 상세 항목의 재검증 여부는 `formative/records.json`에 기록되어 있다.',
            '측정별 원숫자, 상태, 코드 해시와 입력은 `analysis/camera_ready/RESULTS_v21.json`에 있다. '
            '아카이브 내부의 `out/FILES.json`은 자기 자신을 제외한 수록 파일별 경로·SHA-256·바이트·수정 시각을 담는다. '
            '전달용 tar.gz와 파일 목록의 SHA-256은 아카이브 옆의 `SHA256SUMS.txt`에서 확인할 수 있다.'])
    verification_file = EVIDENCE / 'score_verification.json'
    if verification_file.exists():
        v = load(verification_file)
        largest = max(v['max_absolute_difference_by_field'].values())
        pos = sections.index('## T7 · 재현성과 변경 범위') + 1
        sections.insert(pos, f"M5 래퍼와 공개 저장소의 split2 채점기가 낸 {v['benchmarks']}개 벤치마크, {v['pairs']:,}개 쌍을 모두 대조했다. "
                        f"쌍별 {len(v['pair_fields_compared'])}개 ALC·예산별 Brier 항목에서 최대 절대차는 {largest:.4g}, "
                        f"허용 오차는 {v['pair_tolerance']}, 판정은 {v['status']}다. "
                        f"각 방법·예산의 전체 응답 수 {v['responses_per_method_budget']:,}개와 6개 ECE 값의 재검산 결과는 "
                        f"{'PASS' if v['all_six_reliability_totals_and_ECE_verified'] else 'FAIL'}다.")
    (OUT / 'REPORT.md').write_text('\n\n'.join(sections) + '\n',encoding='utf-8')


if __name__ == '__main__':
    report()
