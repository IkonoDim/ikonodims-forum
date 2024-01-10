// this script handles the logins

document.addEventListener("DOMContentLoaded", () => {
    const username_field = document.getElementById("username_field");
    const password_field = document.getElementById("password_field");

    document.getElementById("form_submit_button").addEventListener("click", function (message) {
        // checks if the user even entered something as his username / password
        if (username_field.value.length === 0) {
            return postUserMessage("red", "info", "Bitte gib einen Nutzernamen an.", 1.5);
        }
        if (password_field.value.length === 0) {
            return postUserMessage("red", "info", "Bitte gib ein Passwort an.", 1.5);
        }

        // starts a loading animation in the user notification area
        postUserMessage("white", null, `<loading><ball></ball><ball></ball><ball></ball></loading>`, "infinite");

        // this is the login request
        request("POST", "/login", {
            username: username_field.value, password: password_field.value
        }, function (status, request) {
            if (status) {
                // if the status is not an error it posts a user message and after 500ms redirects him to the home-page
                postUserMessage("green", "check", "Login erfolgreich. Du wirst nun weitergeleitet.", "infinite")
                setTimeout(() => {
                    window.location = "/home";
                }, 500)
            } else {
                // else the user gets a warning message that disappears after 1.5s
                postUserMessage("red", "info", "Login fehlgeschlagen. Bitte versuche es erneut.", 1.5)
            }
        })
    })
})