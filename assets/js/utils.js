// This is the utilities (utils.js) script. Here we've got many functions and listeners that make many things way
// easier

// Once the content of the website is loaded this function iterates through all <timestamp> elements and converts
// their integer timestamp into human-readable format.
document.addEventListener("DOMContentLoaded", () => {
    const timestampTags = document.querySelectorAll('timestamp');

    timestampTags.forEach(tag => {
        const timestamp = parseInt(tag.innerHTML);
        tag.innerHTML = timeAgo(timestamp * 1000);
    });
})

// This posts messages into the notification area in the nav (if you read the css it is the
// "nav section:nth-of-type(4)" in line 65 "nav.ccs")
function postUserMessage (color, icon, value, timeOnScreen) {
    console.log(value)
    const userMessageArea = document.getElementById("user-message-area")
    const iconList = {
        "info": "<i class=\"fa-regular fa-circle-info\"></i>",
        "check": "<i class=\"fa-regular fa-circle-check\"></i>",
        null: ""
    }

    userMessageArea.innerHTML = iconList[icon] + value
    userMessageArea.style.color = color

    if (timeOnScreen !== "infinite") {
        setTimeout(() => {
            userMessageArea.innerHTML = null;
        }, timeOnScreen * 1000)
    }
}

// This is for errors that need to be displayed directly in/near the input field. But it is only really useful in the
// "register.js". I won't explain it any further because this is just a simple animation.
function showFormError(id, inputFieldId) {
    const element = document.getElementById(id);
    const inputElement = document.getElementById(inputFieldId);

    element.style.display = "unset";

    setTimeout(() => {
        element.style.opacity = ".4";

        setTimeout(() => {
            element.style.color = "red";
            element.style.opacity = "2";

            inputElement.style.animation = "horizontal-shaking .3s forwards";


            setTimeout(() => {
                element.style.color = "var(--font-clr-primary)";
                element.style.opacity = ".4";
                inputElement.style.animation = "unset";

                setTimeout(() => {
                    element.style.opacity = "0";

                    setTimeout(() => {
                        element.style.display = "none";
                    }, 200)
                }, 750)
            }, 300)
        }, 200)
    }, 10)
}

// This function hides form errors
function hideFormError(id) {
    const element = document.getElementById(id)

    element.style.opacity = "0";


    setTimeout(() => {
        element.style.display = "none";
    }, 200)
}

// This is the function that converts timestamps to human-readable format, I referenced to in the <timestamp> listener.
function timeAgo(timestamp) {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    const intervals = [60, 3600, 86400, 604800, 2629746, 31556952];
    const units = ['Sekunde(n)', 'Minute(n)', 'Stunde(n)', 'Tage(n)', 'Woche(n)', 'Monat(en)', 'Jahr(en)'];

    for (let i = 0; i < intervals.length; i++) {
        const interval = intervals[i];
        const unit = units[i];

        if (seconds < interval) {
            const count = Math.floor(seconds / (intervals[i - 1] || 1));
            return `vor ${count} ${unit}`;
        }
    }

    const count = Math.floor(seconds / intervals[intervals.length - 1]);
    return `vor ${count} ${units[units.length - 1]}`;
}