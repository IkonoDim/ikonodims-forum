// This function makes a http way easier. It takes the method, url, jsonData (aka. payload), the headers
// and a callback function that is triggered when the request finishes and gets the status in a boolean format and
// the xhr variable passed.

function request(method, url, jsonData, callback, headers=null) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    for (const key in headers) {
        xhr.setRequestHeader(key, headers[key])
    }

    xhr.onreadystatechange = function ()  {
        // What's the xhr.readyState?
        // UNSENT (0): The request has not been initialized.
        // OPENED (1): The request has been set up.
        // HEADERS_RECEIVED (2): Headers have been received.
        // LOADING (3): The response is being received.
        // DONE (4): The request is complete.

        if (xhr.readyState === 4) {
            if (Math.floor(xhr.status / 100) === 2) {  // returns true if the request is in the 200s
                callback(true, xhr);
            } else {
                console.error('Error:', xhr.status);  // else it prints the status code and passes false to the callback func
                callback(false, xhr);
            }
        }
    };

    xhr.send(JSON.stringify(jsonData));  // initializes the request
}