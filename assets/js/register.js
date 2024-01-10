// About the same as the login.js so I won't need to explain this

document.addEventListener("DOMContentLoaded", () => {

    const username_field = document.getElementById("username_field");
    const password_field = document.getElementById("password_field");
    const password_field2 = document.getElementById("password_field2");
    const submit_button = document.getElementById("form_submit_button");

    submit_button.addEventListener("click", function () {
        if (username_field.value.length > 20) {
            return postUserMessage("red", "info", "Der Nutzername is zu lang!", 3);
        } else if (username_field.value.length < 5) {
            return postUserMessage("red", "info", "Der Nutzername is zu kurz!", 3);
        } else if (! /^[a-z_]+$/.test(username_field.value)) {
            return showFormError("username-character-error", "username_field");
        }

        if (password_field.value.length === 0) {
            hideFormError("password-short-error");
        } else if (password_field.value.length < 8) {
            return showFormError("password-short-error", "password_field");
        } else {
            hideFormError("password-short-error");
        }

        if (password_field2.value !== password_field.value) {
            return showFormError("password-matching-error", "password_field2");
        }

        postUserMessage("white", null, `<loading><ball></ball><ball></ball><ball></ball></loading>`, "infinite")

        request("POST", "/register", {
            username: username_field.value, password: password_field.value
        }, function (status, request) {
            if (status) {
                postUserMessage("green", "check", "Registrierung erfolgreich. Du wirst nun weitergeleitet.", "infinite")
                setTimeout(() => {
                    window.location = "/home";
                }, 1000)
            } else {
                postUserMessage("red", "info", "Registrierung fehlgeschlagen. Bitte versuche es erneut.", 1.5)

            }
        })


    })
})
