

function openPopup(id) {
    document.getElementById(id).style.display = 'flex';
}

function closePopup(id) {
    document.getElementById(id).style.display = 'none';
}
function check_duplicate(){ //여기 () 빠져있었어서 추가했어요
    document.getElementById("check-duplicate").addEventListener("click", function () {
        const userId = document.getElementById("id").value;
        const messageElement = document.getElementById("duplicate-message");
    
        if (!userId) {
            messageElement.textContent = "아이디를 입력하세요.";
            messageElement.style.color = "red";
            return;
        }
    
        // AJAX 요청
        fetch("/check_duplicate_id", { //따옴표 없어서 오류나길래 추가했어요
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: userId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                messageElement.textContent = "이미 사용 중인 아이디입니다.";
                messageElement.style.color = "red";
            } else {
                messageElement.textContent = "사용 가능한 아이디입니다.";
                messageElement.style.color = "green";
            }
        })
        .catch(error => {
            console.error("오류 발생:", error);
            messageElement.textContent = "오류가 발생했습니다. 다시 시도해주세요.";
            messageElement.style.color = "red";
        });
    });
}



