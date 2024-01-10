document.addEventListener("DOMContentLoaded", () => {
    const post_container = document.getElementById("scroll_window");
    let offset = 0;

    // This listener listens to the container where the latest posts are displayed. When the user scrolls to the bottom
    // it loads 5 new posts everytime
    document.getElementById('scroll_window').addEventListener('scroll', function() {
        console.log(this.scrollHeight)
        if (this.scrollTop + this.clientHeight === this.scrollHeight) {
            offset += 5; // this is the offset from the first. It tells the backend from which index it wants the latest posts
            request("GET", "/grab_posts", {}, function (status, request) {
                const posts = JSON.parse(request.responseText);

                for (let post in posts) {

                    // creating and inserting the new element
                    let currentPost = posts[post]
                    let newElement = document.createElement("sec");
                    newElement.onclick = function () {
                        window.location = '/post/' + currentPost["post_id"]; // this part is responsible for the redirection, so if the user clicks on the post he gets redirected there
                    }
                    newElement.innerHTML = `<h2>${currentPost["title"]}</h2><p>${currentPost["content"]}</p>
                                            <container class="statistics"><statistic><i class="fa-regular fa-user"></i> 
                                            @${currentPost["user"]["username"]}</statistic><statistic>
                                            <i class="fa-regular fa-clock"></i>
                                            <timestamp>${currentPost["timestamp"]}</timestamp></statistic>
                                            <statistic><i class="fa-regular fa-eye"></i>${currentPost["views"]}</statistic>
                                            </container>`

                    post_container.appendChild(newElement);

                }
            }, {
                offset: offset, amount: 5
            })
        }
    });
})