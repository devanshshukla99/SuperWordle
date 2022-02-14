window.onload = function () {
    Array.from(document.getElementsByClassName("RowL-letter")).forEach((element, index) => {
        index++
        element.addEventListener("keydown", (event) => {
            // console.log(event)
            if (event.key.match(/(\b[a-zA-Z]\b)/g)) {
                event.preventDefault()
                var next_element = element.parentElement.children[index % 5]
                event.target.textContent = event.key
                event.target.classList.add("letter-absent")
                if (index % 5 != 0) {
                    if (next_element) {
                        next_element.focus();
                    }
                }
            }
            else if (event.key === "Backspace") {
                var next_element = element.parentElement.children[(index - 2) % 5]
                event.target.textContent = ""
                if (index % 5 != 1) {
                    if (next_element) {
                        next_element.focus();
                    }
                }
            }
        });
        element.addEventListener("wheel", event => {
            if (event.deltaY < 0) {
                // console.log("up")
                if (event.target.classList.contains("letter-correct")) {
                    event.target.classList.add("letter-absent")
                    event.target.classList.remove("letter-correct")
                }
                else {
                    event.target.classList.add("letter-elsewhere")
                    event.target.classList.remove("letter-absent")
                }
            }
            else {
                // console.log("down")
                if (event.target.classList.contains("letter-elsewhere")) {
                    event.target.classList.add("letter-absent")
                    event.target.classList.remove("letter-elsewhere")
                }
                else {
                    event.target.classList.add("letter-correct")
                    event.target.classList.add("letter-absent")
                }
            }
        });
        element.addEventListener("click", event => {
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
        });
    });


    for (let i = 1; i < 6; i++) {
        document.getElementById("row-" + i + "-col-5").addEventListener("keypress", event => {
            if (event.key === "Enter") {
                document.getElementById("row-" + (i + 1) + "-col-1").focus()
                var [pattern, word, pos, pos_idx] = getPattern(event.target.parentElement)
                if (word.length === 5) {
                    console.log("process")
                    const request = new XMLHttpRequest();
                    request.open("POST", `/process`);
                    request.onload = () => {
                        const response = request.responseText;
                        document.getElementById("suggest").innerHTML = response;
                    };
                    post_data = {
                        "pattern": pattern,
                        "word": word,
                        "possible": pos,
                        "possible_index_tried": pos_idx
                    }
                    console.log(post_data)
                    request.send(JSON.stringify(post_data));
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
    possible = ""
    possible_idx = []
    Array.from(parent.children).forEach((element, idx,) => {
        word += element.textContent
        if (element.classList.contains("letter-correct")) {
            pattern += element.textContent
        }
        else if (element.classList.contains("letter-elsewhere")) {
            possible += element.textContent
            possible_idx.push(idx)
            pattern += "*"
        }
        else {
            pattern += "*"
        }
    });
    return [pattern, word, possible, possible_idx]
}
