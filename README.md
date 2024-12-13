# OSPGoHome

오픈SW플랫폼 "**4시귀가희망**"팀의 팀프로젝트 "**귀가 후 마켓**" 입니다. <br><br>

[기술블로그](https://repeated-beluga-c1a.notion.site/OSP-14d3ef0c46d180c4b094fc4c0c1848ef) <<click here<br>
[기술보고서](https://whimsical-saturday-f75.notion.site/SW-158cd59241b380929a04c07f13374dc6) <<click here<br>

## 🥬 Key Features

+ 로그인/회원가입
+ 홈 화면 (리뷰, 상품 미리보기, 더치트 연결 )
+ 리뷰 조회
+ 리뷰 등록
+ 상품 조회
+ 상품 등록
+ 채팅

## 📂 Directory Structure

```
📂 OSPGOHOME
├─ 📂 authentication    ▶︎ 사용자 인증 기능 관련 모듈
├─ 📂 static            ▶︎ 정적 파일들이 저장된 디렉토리
│  ├─ 📂 fonts
│  ├─ 📂 image          
│  ├─ 📂 js
│  ├─ 📜 main.js 
│  └─ 📜 style.css
├─ 📂 templates         ▶︎ Flask 템플릿 파일들을 보유한 디렉토리
├─ 📜 application.py    ▶︎ Flask 애플리케이션의 메인 파일
├─ 📜 database.py       ▶︎ 데이터베이스 관련 설정과 연결을 다루는 파일
├─ LICENSE
└─ README.md
```

## 🦴 Menu Structure

<img width="1145" alt="image" src="https://github.com/user-attachments/assets/b651a1a2-8256-44e5-a5c9-8553f5b38a85" />



## 📋 API 

<img width="1171" alt="image" src="https://github.com/user-attachments/assets/ac5829f2-1848-446f-9771-d90906c68af0" />



## 🖥️ DB 

```
📂 DB
├─ 📂 RoomMessages        ▶︎ 채팅 데이터
│  ├─ 📂 [roomId]
│  │  ├─ 📂 [messgeId]
│  │  │  ├─ message        ▶︎ 메시지 내용
│  │  │  ├─ timestamp      ▶︎ 발송 시간
│  └─ └─ └─ user           ▶︎ 발송한 유저
├─ 📂 UserRooms            ▶︎ 유저별 채팅방 목록  
│  ├─ 📂 [userId]
│  │  ├─ 📂 [상대userId]
│  │  │  ├─ roomId         
│  └─ └─ └─ unread          ▶︎ 읽지 않은 메시지 수
├─ 📂 heart                ▶︎ 좋아요  
│  ├─ 📂 [userId]
│  │  ├─ 📂 [itemName]
│  └─ └─ └─ interested      ▶︎ 좋아요 여부 
├─ 📂 item                 ▶︎ 상품 데이터  
│  ├─ 📂 [itemName]
│  │  ├─ addr
│  │  ├─ availability
│  │  ├─ categotry
│  │  ├─ directtransaction
│  │  ├─ explanation
│  │  ├─ img_path
│  │  ├─ name
│  │  ├─ price
│  │  ├─ seller
│  └─ └─ status
├─ 📂 review                ▶︎ 리뷰 데이터  
│  ├─ 📂 [itemName]
│  │  ├─ categotry
│  │  ├─ img_path
│  │  ├─ rating
│  │  ├─ review
│  │  ├─ reviewTitle
│  │  ├─ reviewerId
│  └─ └─ status
├─ 📂 user                  ▶︎ 유저 데이터 
│  ├─ 📂 [userId]
│  │  ├─ id
│  │  ├─ name
│  │  ├─ email
└─ └─ └─ pw
```



## 🥗 Contributors

|팀장|팀원|팀원|팀원|팀원|팀원|
|-|-|-|-|-|-|
|[윤현진](https://github.com/hjyoon5790)|[강민서](https://github.com/childstone)|[김윤서](https://github.com/Westyoon)|[성은재](https://github.com/dabiih)|[좌연주](https://github.com/jwayj)|[전희원](https://github.com/isc10120)|

<br>

## 🛠️ Tech Stacks

<b>FE</b>
HTML, CSS, JavaScript
<br>

<b>BE</b>
Flask, Firebase
<br>

<b>Cowork</b>
Notion, Figma, GitHub, Git
<br>
