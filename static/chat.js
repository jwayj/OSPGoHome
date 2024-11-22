document.addEventListener("DOMContentLoaded", function() {
    // 메시지 입력창 요소 선택
    const messageInput = document.getElementById("messageInput");
    // 채팅 메시지 목록 요소 선택
    const chatMessages = document.getElementById("chatMessages");
    // 보내기 버튼 요소 선택
    const sendButton = document.getElementById("sendButton");

    // 메시지를 전송하는 함수
    function sendMessage() {
        // 입력된 메시지 내용을 가져와 공백을 제거
        const messageText = messageInput.value.trim();
        // 메시지 내용이 비어 있지 않다면 실행
        if (messageText !== "") {
            // 새로운 메시지 요소(div) 생성
            const messageElement = document.createElement("div");
            // 메시지에 "message"와 "sent" 클래스를 추가하여 스타일 지정
            messageElement.classList.add("message", "sent");

            // 보낸 사람의 ID를 나타내는 요소(span) 생성
            const userIdSpan = document.createElement("span");
            userIdSpan.classList.add("user-id");
            userIdSpan.textContent = "blue";  // 사용자 ID를 "blue"로 지정

            // 메시지 내용을 나타내는 요소(span) 생성
            const messageContentSpan = document.createElement("span");
            messageContentSpan.classList.add("message-content");
            messageContentSpan.textContent = messageText;  // 입력된 메시지 내용 설정

            // 메시지를 보낸 시간을 나타내는 요소(span) 생성
            const messageTimeSpan = document.createElement("span");
            messageTimeSpan.classList.add("message-time");
            // 현재 시간을 가져와 오전/오후, 시, 분 형식으로 포맷팅
            const currentTime = new Date();
            const hours = currentTime.getHours() > 12 ? currentTime.getHours() - 12 : currentTime.getHours();
            const minutes = currentTime.getMinutes().toString().padStart(2, "0");
            const period = currentTime.getHours() >= 12 ? "오후" : "오전";
            messageTimeSpan.textContent = `${period} ${hours}:${minutes}`;

            // 메시지 요소에 ID, 내용, 시간 요소를 추가
            messageElement.appendChild(userIdSpan);
            messageElement.appendChild(messageContentSpan);
            messageElement.appendChild(messageTimeSpan);
            // 채팅 메시지 목록에 새 메시지 요소 추가
            chatMessages.appendChild(messageElement);

            // 스크롤을 아래로 자동으로 이동시켜 최근 메시지가 보이도록 설정
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // 입력창 초기화 (비워줌)
            messageInput.value = "";
        }
    }

    // Enter 키를 눌렀을 때 메시지 전송 이벤트 리스너 추가
    messageInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();  // Enter 키를 누르면 sendMessage 함수 호출
        }
    });

    // 보내기 버튼 클릭 시 메시지 전송 이벤트 리스너 추가
    sendButton.addEventListener("click", function() {
        sendMessage();  // 보내기 버튼 클릭 시 sendMessage 함수 호출
    });
});