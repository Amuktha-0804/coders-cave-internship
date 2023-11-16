let inputEditor,editor,outputEditor;

window.onload = function() {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/c_cpp");
    editor.setFontSize("20px");

    inputEditor = ace.edit("input");
    inputEditor.setTheme("ace/theme/monokai");
    inputEditor.session.setMode("ace/mode/text");
    inputEditor.setFontSize("20px");

    outputEditor = ace.edit("output");
    outputEditor.setTheme("ace/theme/monokai");
    outputEditor.session.setMode("ace/mode/text");
    outputEditor.setFontSize("20px");
}


function changeLanguage() {

    let language = $("#languages").val();

    if(language == 'c' || language == 'cpp')editor.session.setMode("ace/mode/c_cpp");
    else if(language == 'python')editor.session.setMode("ace/mode/python");
    else if(language == 'Java')editor.session.setMode("ace/mode/java");
    else if(language == 'node')editor.session.setMode("ace/mode/javascript");
}

function executeCode() {
    const runButton = document.getElementById('runbutton');
    runButton.classList.add('button-clicked');
    runButton.classList.add('button-up');
    setTimeout(() => {
        runButton.classList.remove('button-clicked', 'button-up');
    }, 1000);

    var userCode = editor.getValue();
    var input = inputEditor.getValue();

    const requestData = {
        userCode: userCode,
        inputText: input
    };

    var language = document.getElementById("languages").value;
    fetch('http://localhost:3000/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Language': language,
        },
        mode: 'cors',
        body: JSON.stringify(requestData),
    })
    .then(response => response.text())
    .then(output => {
        document.querySelector('.output').innerText = output;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

