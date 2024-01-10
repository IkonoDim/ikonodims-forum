// This script handles the cookiebanner. If the "cookieBannerAccepted" value in the localStorage is "yes" it doesn't
// display the banner. If not it creates the banner element.

document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("cookieBannerAccepted") !== "yes") {
        let newElement = document.createElement("cookiebanner")

        newElement.innerHTML = `<i class="fa-solid fa-cookie-bite"></i>
                              <i onclick="localStorage.setItem('cookieBannerAccepted', 'yes'); 
                                          document.querySelector('cookiebanner').style.display='none'" 
                                          role="button" class="fa-solid fa-xmark"></i>
                              <h4>Diese Website nutzt Cookies...</h4>
                              <p>Diese Website verwendet Cookies, um deine aktuelle Sitzung zu speichern und dir ein 
                              besseres Erlebnis zu bieten. 
                              <strong>Durch die Nutzung stimmst du der Verwendung von Cookies zu.</strong>
                              <a href="/privacy-policy">Datenschutzerklärung</a>.</p>`

        document.body.appendChild(newElement)
    }
})