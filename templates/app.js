const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const roleDropdown = document.getElementById('role-dropdown');
const gradeCheckboxes = document.querySelectorAll('input[name="grade"]');
const subjectCheckboxes = document.querySelectorAll('input[name="subject"]');
const grade9checkbox = document.getElementById('grade-9');

sendBtn.addEventListener('click', sendMessage);

grade9checkbox.addEventListener('checked',addText);


gradeCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateTextInput);
});

subjectCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateTextInput);
});

function addText(){
    console.log('test');
    var cb = document.getElementById("grade-9");
    var text = document.getElementById("text");
    if(cb.checked == true){
        console.log(text);
        text.style.display = "block";
    }
}
function updateTextInput() {
    const selectedGrades = Array.from(document.querySelectorAll('input[name="grade"]:checked')).map(grade => grade.value);
    const selectedSubjects = Array.from(document.querySelectorAll('input[name="subject"]:checked')).map(subject => subject.value);
    const selectedRole = roleDropdown.value;

    const checkboxValues = [
        `Grades: ${selectedGrades.join(', ')}`,
        `Subjects: ${selectedSubjects.join(', ')}`,
        `Role: ${selectedRole}`
    ];
    userInput.value = grade9checkbox.name;
    userInput.value = checkboxValues.filter(value => value !== '').join('\n');
    chatBox.value = grade9checkbox.name;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    const userMessage = `${message}\n${userInput.value}`;

    appendMessage('sent', userMessage);
    //userInput.value = '';

    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.response;
        appendMessage('received', botResponse);
        appendResponse(botResponse);
    })
    .catch(error => console.error('Error:', error));
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    messageElement.textContent = message;
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendResponse(response) {
    const responseBox = document.getElementById('response-box');
    const responseElement = document.createElement('div');
    responseElement.className = 'response';
    responseElement.innerHTML = response;
    responseBox.appendChild(responseElement);
}