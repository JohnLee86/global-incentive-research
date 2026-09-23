# 글로벌 목표인센티브 조사
15개사 FY2025 보상제도를 원문 근거로 비교하는 조사 저장소입니다.

## 대상
Alphabet, Apple, NVIDIA, Micron, Intel, Qualcomm, Microsoft, IBM, Broadcom,
Whirlpool, TSMC, Sony Group, Lonza Group, SK하이닉스, ㈜한화(000880).

## 현재 구현 범위
- 15개사 목록 및 공통 조사표
- SEC 12개사(미국 10 + TSMC·Sony) 공시 후보 수집, HTML·텍스트·해시·출처 저장
- 과거 제출 인덱스 조회, 속도 제한, 재시도, 실패 기록
- 비미국 현지 공시·인터뷰·뉴스용 근거표 및 조사 기준
- 문서 분석·기업별 제도 판정은 아직 미완료. AI 자동 분석 API는 연결하지 않았습니다.
- 8-K·첨부 보상규정·현지 공시·영상은 이 수집기로 자동 수집하지 않습니다.

## GitHub에서 실행
1. Settings → Secrets and variables → Actions → New repository secret.
2. 이름: SEC_USER_AGENT
3. 값: 실제 소속/이름과 연락 이메일 (예: Research Team real-contact@your-domain.com).
   실제 연락처로 바꾸세요. 코드나 공개 파일에 이메일을 넣지 않습니다.
4. Actions → Collect public filings → Run workflow.
5. 첫 실행은 company에 apple 입력. 전체는 빈칸.
6. 완료된 실행의 Artifacts에서 public-filings-실행번호 다운로드.
   manifest.json은 문서 목록, status.json은 오류·수동수집 대상입니다.

결과는 Actions artifact로 90일 보관되며 Git 저장소에 자동 커밋되지 않습니다.
공개 저장소이므로 사내자료·내부 보상정보는 올리지 마세요.
장기 보존할 검토 결과는 research/에 커밋해 관리합니다.

## 로컬 실행
Python 3.12 권장.
```bash
pip install -r requirements.txt
python -m unittest discover -s tests
# SEC_USER_AGENT 환경변수를 실제 연락처로 설정한 뒤:
python scripts/collect_sec.py --company apple
```

공시 제출연도와 보상 회계연도는 다릅니다. 수집 결과의 fiscal_year_verified는
검토 전 항상 false입니다. 자동 수집 완료는 제도 분석 완료를 의미하지 않습니다.

## 자료
- config/companies.json: 대상 목록
- research/methodology.md: 분석·분류 기준
- research/company_template.md: 기업별 조사표
- research/evidence.csv: 출처와 주장
- research/search_queue.csv: 기업별 보완 조사 검색어

## 공식 기술 근거
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
