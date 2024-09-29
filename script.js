function SubmitPaste() {
    const content = document.getElementById("Content").value;
    const title = document.getElementById("PasteName").value;
    
    if (content && title) {
        fetch('http://localhost:5000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: title,
                content: content
            })
        })
        .then(response => response.json())
        .then(data => {
            window.location.href = `/files/${data.file}`;
            console.log(data)
        })
        .catch(error => console.error('Error:', error));
    }
    else {
        const errorlabel = document.getElementById("ErrorLabel")
        errorlabel.innerHTML = "All fields required!"
        errorlabel.style.display = "block";
    }
}