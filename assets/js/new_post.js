// This script right here is handling the creation of new posts.
// The method this works is like the login.js script, so I won't need explain that again

document.addEventListener("DOMContentLoaded", function () {
    const title_input = document.getElementById("title_input");
    const content_input = document.getElementById("content_input");
    const submit_button = document.getElementById("form_submit_button");

    submit_button.addEventListener("click", () => {
        if (title_input.value.length < 8) {
            return postUserMessage("red", "info", "Der Titel ist zu kurz!", 3);
        } else if (title_input.value.length > 65) {
            return postUserMessage("red", "info", "Der Titel ist zu lang!", 3);
        }

        if (content_input.value.length < 20) {
            return postUserMessage("red", "info", "Der Inhalt ist zu kurz!", 3);
        } else if (content_input.value.length > 2500) {
            return postUserMessage("red", "info", "Der Inhalt ist zu lang!", 3);
        }

        postUserMessage("white", null, `<loading><ball></ball><ball></ball><ball></ball></loading>`, "infinite")

        request("POST", "/new_post", {
            title: title_input.value, content: content_input.value
        }, (status, request) => {
            if (status) {
                postUserMessage("green", "check", "Dein Post wurde hochgeladen. Du wirst nun weitergeleitet.", "infinite")
                setTimeout(() => {
                    window.location = `/post/${request.responseText}`;
                }, 1000)
            } else {
                postUserMessage("red", "info", "Es ist ein Fehler aufgetreten!", 1.5)
            }
        })
    })
})