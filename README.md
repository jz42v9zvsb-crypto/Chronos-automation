# Chronos OS

> 류안영의 AI 운영체제. 단순한 프롬프트 모음이 아니다.

---

## 철학

에이전트 하나가 모든 걸 하면 망한다.
각자의 역할이 명확한 팀을 만들고, 결과는 쌓이고, 연결된다.

---

## 구조

```
Chronos-automation/
│
├── agents/                  # 각 에이전트 헌법
│   ├── hermes/              # 리서처 — 사실만 수집
│   ├── athena/              # 전략가 — 해석과 의미
│   ├── apollo/              # 작가 — 스크립트·콘텐츠
│   ├── hephaestus/          # 자동화 — 코드·API·n8n
│   └── zeus/                # 총괄 — 라우팅만
│
├── memory/                  # 리서치 누적 저장소
│   ├── luxury/              # 감도 채널 브랜드 조사
│   ├── amway/               # Amway Korea 자료
│   ├── hospital/            # AXIS 클리닉 관련
│   └── investment/          # 주식·투자 리서치
│
├── projects/                # 진행 중인 프로젝트
│   ├── gamdo/               # 감도 채널
│   ├── amway-stp/           # STP 모더나이제이션
│   └── axis/                # AXIS 성형외과
│
├── shared/                  # 에이전트 공통 규칙
│   ├── confidence.md        # Confidence 판단 기준
│   ├── formatting.md        # 공통 출력 형식
│   └── routing.md           # 어떤 일을 누구에게
│
└── README.md
```

---

## 에이전트 현황

| 에이전트 | 역할 | 상태 |
|---------|------|------|
| Hermes | 리서치·사실 수집 | ✅ v1.1 활성 |
| Athena | 해석·전략 | 🔜 설계 예정 |
| Apollo | 스크립트·콘텐츠 | 🔜 설계 예정 |
| Hephaestus | 자동화·코드 | 🔜 설계 예정 |
| Zeus | 라우팅·총괄 | 🔜 마지막 |

---

## Memory 시스템

리서치는 사라지지 않는다.
Hermes가 조사한 내용은 `memory/`에 쌓인다.
같은 주제를 다시 조사하면 → 업데이트된 내용만 추가한다.

```
memory/luxury/burberry.md     ← 버버리 누적 리서치
memory/luxury/chanel.md       ← 샤넬 누적 리서치
memory/amway/personas.md      ← 페르소나 데이터 누적
```

---

## 사용 흐름 예시

```
나: "버버리 Daniel Lee 이후 전략 변화 조사해줘"

Hermes: memory/luxury/burberry.md 확인
        → 기존 조사 있음 (2024-01-15)
        → 추가된 내용만 수집
        → memory 업데이트
        → Athena에 넘길 팩트 패키지 출력

Athena: 팩트 받아서 "그래서 감도 영상 각도는?"
Apollo: 각도 받아서 스크립트 작성
```

---

## 버전 히스토리

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2025-01 | Hermes 헌법 초안 |
| v2.0 | 2025-01 | OS 구조 재설계, Memory 시스템 도입 |
