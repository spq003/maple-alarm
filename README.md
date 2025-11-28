# maple-alram
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
