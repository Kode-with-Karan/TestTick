function startPolling(sessionId) {
    setInterval(function() {
        fetch(`/quiz/api/quiz_status/${sessionId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('question').innerText = data.question;
            // update options
            document.getElementById('optionA').innerText = data.options[0];
            document.getElementById('optionB').innerText = data.options[1];
            document.getElementById('optionC').innerText = data.options[2];
            document.getElementById('optionD').innerText = data.options[3];
            document.getElementById('timer').innerText = data.time_left + "s";
        });
    }, 1000);
}
