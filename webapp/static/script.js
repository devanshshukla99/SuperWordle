window.onload = function () {
    document.getElementById("help-btn").addEventListener("click", event => {
        var helpelement = document.getElementById("help")
        helpelement.classList.toggle("help-hidden")
    });

    var activeElement = document.getElementById("row-1-col-1")
    var main = document.getElementById("game")
    game.addEventListener("keydown", event => {
        // console.log(event)
        if (event.key != "Enter") {
            index = Array.prototype.indexOf.call(activeElement.parentElement.children, activeElement);

            if (event.key === "Backspace") {
                event.preventDefault()
                var prev_element = activeElement.parentElement.children[index - 1];
                activeElement.textContent = "";
                if (prev_element) {
                    activeElement = prev_element;
                    prev_element.focus();
                }
            }

            else if (event.key.match(/(\b[a-zA-Z]\b)/g)) {
                event.preventDefault();
                activeElement.textContent = event.key;
                var next_element = activeElement.parentElement.children[index + 1];
                if (next_element) {
                    activeElement = next_element;
                    next_element.focus();
                }
            }
        }
        else if (event.key === "Enter") {
            activeElement.focus();
        }
    });

    Array.from(document.getElementsByClassName("RowL-letter")).forEach((element, index) => {
        element.addEventListener("mousedown", event => {
            // console.log(event)
            event.preventDefault()
            if (event.target == document.activeElement) {
                if (event.target.classList.contains("letter-elsewhere")) {
                    event.target.classList.add("letter-correct")
                    event.target.classList.remove("letter-elsewhere")
                }
                else if (event.target.classList.contains("letter-correct")) {
                    event.target.classList.add("letter-absent")
                    event.target.classList.remove("letter-correct")
                }
                else if (event.target.classList.contains("letter-absent")) {
                    event.target.classList.add("letter-elsewhere")
                    event.target.classList.remove("letter-absent")
                }
                else {
                    event.target.classList.add("letter-absent")
                }
            }
            else {
                event.target.focus()
            }
        });
    });

    for (let i = 1; i < 6; i++) {
        document.getElementById("row-" + i + "-col-5").addEventListener("keypress", event => {
            if (event.key === "Enter") {
                var [pattern, word] = getPattern(event.target.parentElement)
                if (word.length === 5) {
                    // console.log("process")
                    const request = new XMLHttpRequest();
                    request.open("POST", `/process`);
                    request.onload = () => {
                        const response = request.responseText;
                        document.getElementById("suggest").innerHTML = response;
                        activeElement = document.getElementById("row-" + (i + 1) + "-col-1")
                        if (activeElement) {
                            activeElement.focus()
                        }
                    };
                    post_data = {
                        "pattern": pattern,
                        "word": word,
                    }
                    if (word.length === 5) {
                        // console.log(post_data)
                        document.getElementById("info").textContent = "Processing..."
                        request.send(JSON.stringify(post_data));
                    }
                }
            }
        });
    }
}

function getWord(parent) {
    word = ""
    Array.from(parent.children).forEach((element, idx,) => {
        word += element.textContent
    });
    return word
}

function getPattern(parent) {
    word = ""
    pattern = ""
    Array.from(parent.children).forEach((element, idx,) => {
        word += element.textContent
        if (element.classList.contains("letter-correct")) {
            pattern += element.textContent
        }
        else if (element.classList.contains("letter-elsewhere")) {
            pattern += "#"
        }
        else {
            pattern += "*"
        }
    });
    return [pattern, word]
}
