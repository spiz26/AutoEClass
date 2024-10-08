# [필독] E-Class 온라인 강의 자동 출석 프로그램

안녕하세요. 서울과학기술대학교 E-Class 온라인 강의 자동 출석 프로그램입니다.

학번과 비밀번호를 입력하면, 프로그램이 알아서 미처 다 듣지 못한 강의를 모두 찾아서 들어줍니다.



### 필수 파일 설명

1. user_data.json

   user_data.json에 본인의 기본 정보를 입력합니다. 

   각 줄의 콜론(:) 앞의 "ID", "Password" 의 이름(key)은 건드리시면 안되고,

   반드시 콜론(:) 뒤의 값들만 큰 따옴표("")에 감싸서 입력해주세요.

   ---
   ① ID: 여러분의 학번을 입력하세요.

   ② Password: 여러분의 비밀번호를 입력하세요.

   ③ Delay: 페이지 로딩 대기 시간입니다. 페이지 로딩 대기 시간이 길면 오래 기다리고, 짧으면 빠르게 다음 페이지로 넘어갑니다. 
   
   ---

​		예시: 

```json
{
    "ID": "16100000",
    "Password": "Mypassword123!@#",
    "Delay": "3"
}
```

​		예시는 학번이 16100000이고, Password가 Mypassword123!@# 입니다. 페이지 로딩 대기 시간은 3초입니다 . 



2. chromedriver.exe

​		프로그램이 사용할 chrome 프로그램입니다. 반드시 현재 설치되어 있는 chrome의 버전과 맞는 driver를 설치하셔야합니다. 

​		chrome 버전 확인 방법:

​		크롬 맨 오른쪽 위 점 세 개 클릭 &rarr; 도움말 &rarr; Chrome 정보

​		chrome의 driver 버전 정보를 확인하고, 그에 맞는 driver를 google에서 찾아서 다운로드 한 뒤, 기존에 있는 chromedriver.exe를 삭제하고 넣으시면 됩니다.

## 주의 사항
 반드시 팝업창은 미리 다 꺼주세요!

## 문의 사항

문의 사항이나 버그 제보는 아래 링크의 Issues 에 해주세요.

https://github.com/spiz26/AutoEClass
