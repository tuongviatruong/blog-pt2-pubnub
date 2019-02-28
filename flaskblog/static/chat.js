const chatInterface = document.getElementById('chat-interface');

const usernameModal = document.getElementById('username-input-modal');
const usernameInput = document.getElementById('username-input');
const joinButton = document.getElementById('join-button');


const chat = document.getElementById('chat');
const log = document.getElementById('log');
const messageInput = document.getElementById('message-input');
const submit = document.getElementById('submit');

const hide = 'hide';
const uuid = newUuid();

let username; // local user name

// Prompt user for a username input
getLocalUserName().then((myUsername) => {
    username = myUsername;
    usernameModal.classList.add(hide);

    // Connect ChatEngine after a username and UUID have been made
    ChatEngine.connect(uuid, {
        username
    }, 'auth-key');
});

// Send a message when Enter key is pressed
messageInput.addEventListener('keydown', (event) => {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
        return;
    }
});

// Send a message when the submit button is clicked
submit.addEventListener('click', sendMessage);

// Disconnect ChatEngine before a user navigates away from the page
window.onbeforeunload = (event) => {
    ChatEngine.disconnect();
};

// Init ChatEngine
const ChatEngine = ChatEngineCore.create({
    publishKey: 'pub-c-99549f36-c60c-41b6-a20e-4a1d3ef8b114',
    subscribeKey: 'sub-c-b9a57d62-297f-11e9-8eef-42c9ad3619d5'
}, {
    globalChannel: 'chat-example'
});




// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// UI Render Functions
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
function renderMessage(message) {
    const messageDomNode = createMessageHTML(message);

    log.append(messageDomNode);

    // Sort messages in chat log based on their timetoken
    sortNodeChildren(log, 'id');

    chat.scrollTop = chat.scrollHeight;
}

function getLocalUserName() {
    return new Promise((resolve) => {
        usernameInput.focus();
        usernameInput.value = '';

        usernameInput.addEventListener('keyup', (event) => {
            const nameLength = usernameInput.value.length;

            if (nameLength > 0) {
                joinButton.classList.remove('disabled');
            } else {
                joinButton.classList.add('disabled');
            }

            if (event.keyCode === 13 && nameLength > 0) {
                resolve(usernameInput.value);
            }
        });

        joinButton.addEventListener('click', (event) => {
            const nameLength = usernameInput.value.length;
            if (nameLength > 0) {
                resolve(usernameInput.value);
            }
        });
    });
}

function createUserListItem(userId, name) {
    const div = document.createElement('div');
    div.id = userId;

    const img = document.createElement('img');
    img.src = './user.png';

    const span = document.createElement('span');
    span.innerHTML = name;

    div.appendChild(img);
    div.appendChild(span);

    return div;
}

function createMessageHTML(message) {
    const text = message.data.text;
    const user = message.sender.state.username;
    const jsTime = parseInt(message.timetoken.substring(0,13));
    const dateString = new Date(jsTime).toLocaleString();

    const div = document.createElement('div');
    const b = document.createElement('b');

    div.id = message.timetoken;
    b.innerHTML = `${user} (${dateString}): `;

    div.appendChild(b);
    div.innerHTML += text;

    return div;
}

// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Utility Functions
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
function sendMessage() {
    const messageToSend = messageInput.value.replace(/\r?\n|\r/g, '');
    const trimmed = messageToSend.replace(/(\s)/g, '');

    if (trimmed.length > 0) {
        ChatEngine.global.emit('message', {
            text: messageToSend
        });
    }

    messageInput.value = '';
}

// Makes a new, version 4, universally unique identifier (UUID). Written by
//     Stack Overflow user broofa
//     (https://stackoverflow.com/users/109538/broofa) in this post
//     (https://stackoverflow.com/a/2117523/6193736).
function newUuid() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(
        /[018]/g,
        (c) => (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4)
            .toString(16)
    );
}

// Sorts sibling HTML elements based on an attribute value
function sortNodeChildren(parent, attribute) {
    const length = parent.children.length;
    for (let i = 0; i < length-1; i++) {
        if (parent.children[i+1][attribute] < parent.children[i][attribute]) {
            parent.children[i+1].parentNode
                .insertBefore(parent.children[i+1], parent.children[i]);
            i = -1;
        }
    }
}