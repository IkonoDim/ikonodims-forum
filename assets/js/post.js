// This script handles all interactions on a post-page

document.addEventListener("DOMContentLoaded", function () {
    const answer_field = document.getElementById("answer_field");
    const answer_submit_button = document.getElementById("answer_submit_btn")

    const like_button = document.getElementById("like_btn");
    const dislike_button = document.getElementById("dislike_btn");


    // here it checks if there are more than 3 and less than 2000 characters in the input field.
    // Else the user won't be able to post his comment
    answer_field.addEventListener("input", () => {
        if (answer_field.value.length > 3) {
            answer_submit_button.classList.add("active");
        } else if (answer_field.value.length > 2000) {
            answer_submit_button.classList.remove("active");
        } else {
            answer_submit_button.classList.remove("active");
        }
    })

    // this listener listens to the send button and sends a simple request to the backend.
    // after the request is done it reloads the page
    answer_submit_button.addEventListener("click", () => {
        postUserMessage("white", null, `<loading><ball></ball><ball></ball><ball></ball></loading>`, "infinite");

        request("POST", window.location, {
            content: answer_field.value
        }, (status, request) => {
            if (status) {
                postUserMessage("green", "check", "Dein Kommentar wurde hochgeladen!", 3);
                location.reload();
            } else {
                postUserMessage("red", "info", "Es ist ein Fehler aufgetreten!", 1.5)
            }
        })
    })

    // this listener handles the like interaction.
    like_button.addEventListener("click", () => {
        // loading animation
        postUserMessage("white", null, `<loading><ball></ball><ball></ball><ball></ball></loading>`, "infinite");

        // I referred to this in my post.html . The "interacted" class. If it is active and the user clicks this button
        // the interaction is DELETED from the database via a simple request to the backend. Else a new one is added
        if (like_button.classList.contains("interacted")) {
            request("DELETE", window.location.href + "/like", null, (status, request) => {
                if (status) {
                    location.reload();
                } else {
                    postUserMessage("red", "info", "Es ist ein Fehler aufgetreten!", 3)
                }
            })
        } else {
            if (dislike_button.classList.contains("interacted")) {
                return postUserMessage(null, null, "", 0);
                // ending the loading animation and returning because the user can't like and dislike the same time
            }

            request("POST", window.location.href + "/like", null, (status, request) => {
                if (status) {
                    location.reload();
                } else {
                    postUserMessage("red", "info", "Es ist ein Fehler aufgetreten!", 3)
                }
            })
        }


    })

    // The exact same as the like listener
    dislike_button.addEventListener("click", () => {
        console.log(getComputedStyle(like_button).pointerEvents)
        if (getComputedStyle(like_button).pointerEvents === "none") {
            return;
        }

        postUserMessage("white", null, `<loading><ball></ball><ball></ball><ball></ball></loading>`, "infinite");

        if (dislike_button.classList.contains("interacted")) {
            request("DELETE", window.location.href + "/dislike", null, (status, request) => {
                if (status) {
                    location.reload();
                } else {
                    postUserMessage("red", "info", "Es ist ein Fehler aufgetreten!", 3)
                }
            })
        } else {
            if (like_button.classList.contains("interacted")) {
                return postUserMessage(null, null, "", 0);
            }
            request("POST", window.location.href + "/dislike", null, (status, request) => {
                if (status) {
                    location.reload();
                } else {
                    postUserMessage("red", "info", "Es ist ein Fehler aufgetreten!", 3)
                }
            })
        }
    })
})