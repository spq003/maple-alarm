# maple-alram
OpenCV기반 메이플스토리 알리미<br>
게임 내 화면을 캡쳐하여 특정 패턴·스킬을 자동 감지하고 알림으로 알려주는 도구입니다.

### 주요 기능
```
1. 악몽선경 ‘틀린그림찾기’ 자동 감지
2. 설치형 스킬 재사용 알림
3. 보스 패턴 스택형 스킬 감지

화면 이미지 분석, 재사용 가능 시 알림음 & GUI 표시
```

### 실행 방법
```
Python 3.12.6 환경에서 테스트되었습니다.

가상환경 생성:
>> python -m venv venv
>> venv\Scripts\activate

종속성 주입: (프로젝트 루트 폴더에서)
>> pip install -r requirements.txt

프로그램 실행:
>> python start.py
```

### 디렉토리 구조
```
├── core
│   ├── analysis.py              # 템플릿 매칭 스레드
│   ├── capture.py               # 화면 캡쳐 스레드
│   ├── DXGI_screen_capture.cpp  # .pyd 모듈 소스코드
│   └── DXGI_screen_capture.pyd  # 화면 캡쳐 모듈(pybind)
│
├── img
│   └── *.png                    # 템플릿 이미지들
│
├── core
│   ├── mainWindow.py            # 프로그램 메인 루프
│   └── mainWindow.ui            # PyQt UI
│
├── main.py                      # 프로그램 시작점
│
├── requirements.txt             # 필요 패키지 목록
├── .gitignore
├── README.md
│
└── old/
```
