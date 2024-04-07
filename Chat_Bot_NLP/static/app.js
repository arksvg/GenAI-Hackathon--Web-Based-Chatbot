class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;
        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;
        if (this.state) {
            chatbox.classList.add('chatbox--active')
        }

        else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        console.log("Text : ",text1);
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        let response = '';

        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = { name: "Sam", message: r.answer };
                response = r.answer;

                const voiceBtn = document.querySelector('#voice-btn');
                if (voiceBtn.dataset.voice == '1') {
                    const btnSpeak = document.querySelector('#btnSpeak');
                    const txtInput = document.querySelector('#txtInput');
                    txtInput.value = '';
                    console.log('response', response);
                    if (response.includes('href')) {
                        txtInput.value = 'Click here to view detailed information';
                    }else if(response.includes('src')){
                        txtInput.value = 'here are the images';
                    } 
                    else if(response.includes('br')){
                        txtInput.value = 'Here are the Generated Response';
                    } 
                    else {
                        txtInput.value = response;
                    }
                    btnSpeak.click();
                    voiceBtn.dataset.voice = 0;
                }

                this.messages.push(msg2);
                this.updateChatText(chatbox)
                textField.value = ''
            }).catch((error) => {
                console.error('Error: ', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function (item, index) {
            if (item.name === "Sam") {
                html += '<div class="message__item message__item--visitor">' + item.message + ' &nbsp;</div>'
                console.log(item.message);


                // item.message = '';
            }
            else {
                html += '<div class= "message__item messages__item--operator">&nbsp;' + item.message + ' &nbsp;</div>'
            }


        });
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

}

const chatbox = new Chatbox();
chatbox.display();  