# Apple FY2025 목표인센티브 분석 — 1차
분석 범위: 공시 대상 임원(NEO). 일반 직원 제도로 확대 해석하지 않음.
분석 상태: SEC 원문 CD&A·지급표 대조 완료 / 보상규정 전문 및 직원 운영 미확인.
GitHub 수집 ZIP의 접근 URL이 403을 반환하여 ZIP 내부 3건은 직접 검증하지 못함. 아래 SEC 원문을 사용.

## 1. 자료
- S1: 2026 Proxy Statement (2026-01-08), pp.44–48, Summary Compensation Table, Grants of Plan-Based Awards.
  https://www.sec.gov/Archives/edgar/data/320193/000130817926000008/aapl014016-def14a.htm
- S2: FY2025 10-K, Consolidated Statements of Operations.
  https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm
- S3: 2025 Proxy Statement, FY2024 Cash Incentive Plan.
  https://www.sec.gov/Archives/edgar/data/320193/000130817925000008/aapl4359751-def14a.htm

## 2. STI 핵심값
| 항목 | 확인 결과 | 근거 |
|---|---|---|
| 대상 | CEO 및 공시 대상 임원 | S1 CD&A |
| 기준 | FY2025, 2025-09-27 종료 | S2 |
| 제도 | Executive Cash Incentive Plan | S1 p.45 |
| Target | Cook: $6m; Adams·Khan·O’Brien: 각 $2m | S1 pp.44–45 |
| 예외 | Parekh: 실제 지급 기본급의 175%; Maestri: 100%, 역할 전환 반영 | S1 p.45 |
| 지표 | GAAP 매출 50%, 영업이익 50% | S1 p.45 |
| 지표별 지급률 | Threshold 미달 0%, Threshold 50%, Target 100%, Maximum 200%; 구간 선형보간 | S1 p.45 |
| 지급수단 | 현금 | S1 |
| 실제 지급 | Cook $12m; Adams·Khan·O’Brien 각 $4m; Parekh $3,120,317; Maestri $1,638,462 | S1 Summary Compensation Table |

### 성과목표와 결과 (USD billion)
| 지표 | Threshold | Target | Maximum | FY2025 실적 |
|---|---:|---:|---:|---:|
| 매출 | 380 | 391 | 402 | 416.161 |
| 영업이익 | 113 | 118.5 | 124 | 133.050 |

목표는 S1 p.46, 정확한 실적은 S2. 두 지표 모두 최대 목표 초과.

산식 재구성(공시 규칙을 수식화):
지급액 = 개인 Target × [0.5 × 매출 지급계수 + 0.5 × 영업이익 지급계수]
FY2025는 Target의 200%. Cook: $6m × 200% = $12m.
이는 목표 대비 120% 성과가 곧 120% 지급이라는 뜻이 아님. 성과구간을 지급계수로 변환.

## 3. 예산 분류 판정
| 조사 쟁점 | 판정 |
|---|---|
| 개인 Target 기반 지급 산식 | 확인 |
| A1 전사 예산 = 개인 Target 합산 | 확인 불가 |
| A2 합산 Target × 별도 Pool factor | 확인 불가 |
| B 전사 Hurdle 충족 시 예산 개설 | 확인 불가 |
| C 별도 Pool 상한·초과분 비례감액 | 확인 불가 |
| 개인별 상한 | Target의 200% 확인 |

각 지표 Threshold는 그 지표 지급의 조건이다. 전사 예산 개설 Hurdle의 증거가 아니다.
개인별 상한 역시 전사 Pool 상한을 뜻하지 않는다.
Target보다 많은 지급은 확인되지만, '연초 확정 예산 초과 집행'이라고 단정할 수 없다.

## 4. LTI 참고
S1 pp.47–48: 신규 성과형 RSU는 FY2025–2027 상대 TSR(S&P 500 비교) 평가.
25백분위 미만 0%, 25백분위 25%, 55백분위 100%, 85백분위 이상 200%; 중간 선형보간.
절대 TSR 음수이면 최대 100%.
Cook 신규 주식보상은 성과형 75%·시간형 25%; 다른 NEO의 기본 구성은 50%·50%.
신규 부여분과 FY2025에 실제 귀속된 과거 부여분을 별도 취급한다.

## 5. 변경·보완 조사
- S3에는 FY2024 예비 지급률에 ±10% modifier 적용 가능 문구가 있음.
- S1 FY2025 STI 설명에는 동일 문구가 확인되지 않음. FY2025 산식에 과거 modifier를 자동 적용하지 않음. 정식 폐지 시점·규정은 추가 확인.
- 일반 임원·직원 Target, 평가등급 조정, 전사 예산 편성, Pool 배분은 미확인.
- 인터뷰·영상의 지급산식 직접 근거는 이번 1차 검색에서 확보하지 못함.
- 보완 후보: 2021년 Deirdre O’Brien 내부 영상 관련 보도. 보수 공정성 논의이며 FY2025 성과급 산식 근거로 채택하지 않음.
  https://www.imore.com/people-chief-deirdre-obrien-tells-apple-employees-talk-their-managers-about-pay-and-other-concerns
- 보상규정·관련 8-K·현행 담당자 직접 발언 추가 검증 필요.
