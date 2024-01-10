import logging
import exceptions.assets
import models
from exceptions import *
import flask
from models.site_builder import *
from models.database import *
import helpers.database
import helpers.site_builder
import utils.logging
import utils.httpstatus
import helpers.assets
import utils.jsontools

app = flask.Flask("")
host = ["0.0.0.0", 5000]

# This is the base configuration for all sites. The html files like head, nav and footer and the title-prefix
# are specified here.
template = Template(
    head=helpers.assets.load_asset(Asset(filetype="html", name="head")).value.__str__(),
    nav=helpers.assets.load_asset(Asset(filetype="html", name="nav")).value.__str__(),
    footer=helpers.assets.load_asset(Asset(filetype="html", name="footer")).value.__str__(),
    title_prefix="Forum"
)

# A list of all the site configurations. Here you can specify the css and js files and the navigation elements
# displayed on top in the nav-bar
sites = {
    "home": Site("Home",
                 helpers.assets.load_asset(Asset("favicon", "ico")),
                 helpers.assets.load_asset(Asset("home", "html")),
                 [
                     helpers.assets.load_asset(Asset("nav", "css")),
                     helpers.assets.load_asset(Asset("struct", "css")),
                     helpers.assets.load_asset(Asset("footer", "css")),
                     helpers.assets.load_asset(Asset("animations", "css")),
                     helpers.assets.load_asset(Asset("index_page", "css"))
                 ],
                 nav_elements=[
                     ["Home", "/"], ["Neuer Post", "/new_post"], ["Playground", "/playground"]
                 ],
                 scripts=[
                     Asset("utils", "js"),
                     Asset("cookies", "js"),
                     Asset("requests", "js"),
                     Asset("home", "js"),
                 ]
                 ),
    "login": Site("Login",
                  helpers.assets.load_asset(Asset("favicon", "ico")),
                  helpers.assets.load_asset(Asset("login", "html")),
                  [
                      helpers.assets.load_asset(Asset("nav", "css")),
                      helpers.assets.load_asset(Asset("struct", "css")),
                      helpers.assets.load_asset(Asset("footer", "css")),
                      helpers.assets.load_asset(Asset("animations", "css")),
                      helpers.assets.load_asset(Asset("page_login", "css"))
                  ],
                  nav_elements=[
                      ["Registrieren", "/register"]
                  ],
                  scripts=[
                      Asset("utils", "js"),
                      Asset("cookies", "js"),
                      Asset("login", "js"),
                      Asset("requests", "js")
                  ]
                  ),
    "register": Site("Registrieren",
                     helpers.assets.load_asset(Asset("favicon", "ico")),
                     helpers.assets.load_asset(Asset("register", "html")),
                     [
                         helpers.assets.load_asset(Asset("nav", "css")),
                         helpers.assets.load_asset(Asset("struct", "css")),
                         helpers.assets.load_asset(Asset("footer", "css")),
                         helpers.assets.load_asset(Asset("animations", "css")),
                         helpers.assets.load_asset(Asset("page_register", "css"))
                     ],
                     nav_elements=[
                         ["Einloggen", "/login"]
                     ],
                     scripts=[
                         Asset("utils", "js"),
                         Asset("cookies", "js"),
                         Asset("register", "js"),
                         Asset("requests", "js")
                     ]),
    "new_post": Site("Neuer Post",
                     helpers.assets.load_asset(Asset("favicon", "ico")),
                     helpers.assets.load_asset(Asset("new_post", "html")),
                     [
                         helpers.assets.load_asset(Asset("nav", "css")),
                         helpers.assets.load_asset(Asset("struct", "css")),
                         helpers.assets.load_asset(Asset("footer", "css")),
                         helpers.assets.load_asset(Asset("animations", "css")),
                         helpers.assets.load_asset(Asset("page_new_post", "css"))
                     ],
                     nav_elements=[
                         ["Home", "/"], ["Neuer Post", "/new_post"]
                     ],
                     scripts=[
                         Asset("utils", "js"),
                         Asset("cookies", "js"),
                         Asset("new_post", "js"),
                         Asset("requests", "js")
                     ]),
    "post": Site("Post",
                 helpers.assets.load_asset(Asset("favicon", "ico")),
                 helpers.assets.load_asset(Asset("post", "html")),
                 [
                     helpers.assets.load_asset(Asset("nav", "css")),
                     helpers.assets.load_asset(Asset("struct", "css")),
                     helpers.assets.load_asset(Asset("footer", "css")),
                     helpers.assets.load_asset(Asset("animations", "css")),
                     helpers.assets.load_asset(Asset("page_post", "css"))
                 ],
                 nav_elements=[
                     ["Home", "/"], ["Neuer Post", "/new_post"]
                 ],
                 scripts=[
                     Asset("utils", "js"),
                     Asset("post", "js"),
                     Asset("cookies", "js"),
                     Asset("requests", "js")
                 ]),
    "imprint": Site("Impressum",
                    helpers.assets.load_asset(Asset("favicon", "ico")),
                    helpers.assets.load_asset(Asset("imprint", "html")),
                    [
                        helpers.assets.load_asset(Asset("nav", "css")),
                        helpers.assets.load_asset(Asset("struct", "css")),
                        helpers.assets.load_asset(Asset("footer", "css")),
                        helpers.assets.load_asset(Asset("animations", "css")),
                        helpers.assets.load_asset(Asset("page_text", "css"))
                    ],
                    nav_elements=[
                        ["Home", "/"], ["Neuer Post", "/new_post"]
                    ],
                    scripts=[]),
    "privacy-policy": Site("Datenschutzerklärung",
                           helpers.assets.load_asset(Asset("favicon", "ico")),
                           helpers.assets.load_asset(Asset("privacy-policy", "html")),
                           [
                               helpers.assets.load_asset(Asset("nav", "css")),
                               helpers.assets.load_asset(Asset("struct", "css")),
                               helpers.assets.load_asset(Asset("footer", "css")),
                               helpers.assets.load_asset(Asset("animations", "css")),
                               helpers.assets.load_asset(Asset("page_text", "css"))
                           ],
                           nav_elements=[
                               ["Home", "/"], ["Neuer Post", "/new_post"]
                           ],
                           scripts=[]),
    "ich_kann_sachen": Site("Ich kann Sachen",
                            helpers.assets.load_asset(Asset("favicon", "ico")),
                            helpers.assets.load_asset(Asset("playground", "html")),
                            [
                                helpers.assets.load_asset(Asset("nav", "css")),
                                helpers.assets.load_asset(Asset("struct", "css")),
                                helpers.assets.load_asset(Asset("footer", "css")),
                                helpers.assets.load_asset(Asset("animations", "css")),
                                helpers.assets.load_asset(Asset("playground", "css"))
                            ],
                            nav_elements=[
                                ["Home", "/"], ["Neuer Post", "/new_post"]
                            ],
                            scripts=[])
}
sb = helpers.site_builder.SiteBuilder(template)
db = helpers.database.DatabaseConnection("database.sqlite")

# Disabling the internal flask-default logger, because i made my own
logging.getLogger("werkzeug").setLevel(logging.ERROR)


# A check for every site that requires a login
def check_if_client_is_logged_in(request: flask.Request) -> (bool, models.database.Session):
    if not request.cookies.get("accountSessionIdentifier"):
        return False, None
    try:
        session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
    except InvalidSessionIdentifier as e:
        response = flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
        response.headers.add("error", str(e))
        return False, None

    return True, session


# Logging all the Outgoing requests
@app.after_request
async def _request_logger(response, request=flask.request):
    utils.logging.log_request(response, request)
    return response


# The Homepage
# This fundamental explanation will not be done again as all the sites are based on this concept.
@app.route("/")
@app.route("/home")
async def home(request=flask.request):
    # First it checks if the client has an active session in his cookies.
    # If not he is getting redirected to the login page. Else the process continues
    check, session = check_if_client_is_logged_in(request)
    if not check:
        return flask.Response(status=utils.httpstatus.Redirection.TEMPORARY_REDIRECT, headers={"Location": "/login"})

    # Here we see the site builder in action. It takes the "home"-site from the configuration and build the html
    site = sb.build(sites["home"])
    # Here it returns the rendered string. All the additional so-called context is specified for the html files
    # in order for them to be able to take e.g. the "session" to display the client's username
    return flask.render_template_string(site.html.value,
                                        title=f"{template.title_prefix} | {site.title}",
                                        host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site,
                                        session=session, posts=db.grab_posts(10, 0))


@app.route("/playground/", methods=["GET"])
@app.route("/playground", methods=["GET"])
async def _playground(request=flask.request):
    site = sb.build(sites["ich_kann_sachen"])
    return flask.render_template_string(site.html.value.__str__(),
                                        title=f"{template.title_prefix} | {site.title}",
                                        host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site)


@app.route("/privacy-policy/", methods=["GET"])
@app.route("/privacy-policy", methods=["GET"])
async def _privacy_policy(request=flask.request):
    site = sb.build(sites["privacy-policy"])
    return flask.render_template_string(site.html.value.__str__(),
                                        title=f"{template.title_prefix} | {site.title}",
                                        host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site)


@app.route("/imprint/", methods=["GET"])
@app.route("/imprint", methods=["GET"])
async def _imprint(request=flask.request):
    site = sb.build(sites["imprint"])
    return flask.render_template_string(site.html.value.__str__(),
                                        title=f"{template.title_prefix} | {site.title}",
                                        host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site)


@app.route("/post/<post_id>/", methods=["GET", "POST"])
@app.route("/post/<post_id>", methods=["GET", "POST"])
async def _post_id(post_id, request=flask.request):
    # Here we have our first site that takes the "GET" and the "POST" methods. When "GET" it displays the post
    # from the specified id. If "POST" it creates a comment, grabbing the information from the request's json-payload

    match request.method:
        case "GET":
            check, session = check_if_client_is_logged_in(request)
            if not check:
                return flask.Response(status=utils.httpstatus.Redirection.TEMPORARY_REDIRECT,
                                      headers={"Location": "/login"})

            site = sb.build(sites["post"])
            post = db.get_post(post_id)
            user = db.get_user(User(session.session_user.user_identifier))
            if not post.post_id in user.viewed_posts:
                db.view_post(post, user)

            print(post.user.user_identifier, user.liked_posts)
            return flask.render_template_string(site.html.value.__str__(),
                                                title=f"{template.title_prefix} | {site.title}",
                                                host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site,
                                                post=post, user=user, session=session)
        case "POST":
            if not request.cookies.get("accountSessionIdentifier"):
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
            try:
                session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
            except InvalidSessionIdentifier as e:
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)

            if not request.json.get("content"):
                return flask.Response(status=utils.httpstatus.ClientError.BAD_REQUEST)

            db.create_comment(models.database.Comment(content=request.json.get("content"), post=db.get_post(post_id),
                                                      user=db.get_user(User(session.session_user.user_identifier))))

            return flask.Response(status=utils.httpstatus.Successful.CREATED)


@app.route("/post/<post_id>/like/", methods=["GET", "POST", "DELETE"])
@app.route("/post/<post_id>/like", methods=["GET", "POST", "DELETE"])
async def _post_id_like(post_id, request=flask.request):
    # This route displays the total like if "GET", adds another like if "POST" and removes a like if "DELETE"
    # However the client needs to have an active user-session in the request's cookies

    match request.method:
        case "GET":
            return db.get_post(post_id).likes

        case "POST":
            if not request.cookies.get("accountSessionIdentifier"):
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
            try:
                session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
            except InvalidSessionIdentifier as e:
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)

            user = db.get_user(session.session_user)
            if post_id in user.disliked_posts or post_id in user.liked_posts:
                return flask.Response(status=utils.httpstatus.ClientError.FORBIDDEN)

            db.like_post(db.get_post(post_id), session.session_user)

            return flask.Response(status=utils.httpstatus.Successful.OK)

        case "DELETE":
            if not request.cookies.get("accountSessionIdentifier"):
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
            try:
                session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
            except InvalidSessionIdentifier as e:
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)

            user = db.get_user(session.session_user)
            if not post_id in user.liked_posts:
                return flask.Response(status=utils.httpstatus.ClientError.FORBIDDEN)

            db.remove_like_post(db.get_post(post_id), session.session_user)

            return flask.Response(status=utils.httpstatus.Successful.OK)


@app.route("/post/<post_id>/dislike/", methods=["GET", "POST", "DELETE"])
@app.route("/post/<post_id>/dislike", methods=["GET", "POST", "DELETE"])
async def _post_id_dislike(post_id, request=flask.request):
    # This route does the same as the /like-route do but it dislikes the post instead of liking it
    match request.method:
        case "GET":
            return db.get_post(post_id).dislikes

        case "POST":
            if not request.cookies.get("accountSessionIdentifier"):
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
            try:
                session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
            except InvalidSessionIdentifier as e:
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)

            user = db.get_user(session.session_user)
            if post_id in user.disliked_posts or post_id in user.liked_posts:
                return flask.Response(status=utils.httpstatus.ClientError.FORBIDDEN)

            db.dislike_post(db.get_post(post_id), session.session_user)

            return flask.Response(status=utils.httpstatus.Successful.OK)

        case "DELETE":
            if not request.cookies.get("accountSessionIdentifier"):
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
            try:
                session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
            except InvalidSessionIdentifier as e:
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)

            user = db.get_user(session.session_user)
            if not post_id in user.disliked_posts:
                return flask.Response(status=utils.httpstatus.ClientError.FORBIDDEN)

            db.remove_dislike_post(db.get_post(post_id), session.session_user)

            return flask.Response(status=utils.httpstatus.Successful.OK)


@app.route("/post/", methods=["GET"])
@app.route("/post", methods=["GET"])
async def _post(request=flask.request):
    # This redirects the incoming requests to /post that don't have any post-id to the "home"-route
    return flask.Response(status=utils.httpstatus.Redirection.TEMPORARY_REDIRECT, headers={"Location": "/"})


@app.route("/new_post/", methods=["GET", "POST"])
@app.route("/new_post", methods=["GET", "POST"])
async def _new_post(request=flask.request):
    match request.method:
        case "GET":
            check, session = check_if_client_is_logged_in(request)
            if not check:
                return flask.Response(status=utils.httpstatus.Redirection.TEMPORARY_REDIRECT,
                                      headers={"Location": "/login"})

            site = sb.build(sites["new_post"])
            return flask.render_template_string(site.html.value.__str__(),
                                                title=f"{template.title_prefix} | {site.title}",
                                                host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site,
                                                session=session)
        case "POST":
            if not request.cookies.get("accountSessionIdentifier"):
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
            try:
                session = db.get_session(Session(request.cookies.get("accountSessionIdentifier")))
            except InvalidSessionIdentifier as e:
                return flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)

            if not request.json.get("title") or not request.json.get("content"):
                return flask.Response(status=utils.httpstatus.ClientError.BAD_REQUEST)

            post_id = db.create_post(models.database.Post(title=request.json["title"], content=request.json["content"],
                                                          user=session.session_user))

            return flask.Response(str(post_id), status=utils.httpstatus.Successful.CREATED)


@app.route("/login/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
async def _login_page(request=flask.request):
    match request.method:
        case "POST":
            try:
                user = User(username=request.json.get("username"), user_password=request.json.get("password"))
                db.validate_login_information(user)
            except InvalidLoginDetails as e:
                response = flask.Response(status=utils.httpstatus.ClientError.UNAUTHORIZED)
                response.headers.add("error", str(e))
                return response
            except InvalidArgumentsException as e:
                response = flask.Response(status=utils.httpstatus.ClientError.BAD_REQUEST)
                response.headers.add("error", str(e))
                return response

            new_session = db.create_session(User(user_identifier=db.get_user_identifier(user)))
            response = flask.Response(status=utils.httpstatus.Successful.OK)
            response.set_cookie("accountSessionIdentifier", str(new_session.session_identifier),
                                max_age=48 * 60 * 60 - 60)

            return response

        case "GET":
            site = sb.build(sites["login"])
            return flask.render_template_string(site.html.value.__str__(),
                                                title=f"{template.title_prefix} | {site.title}",
                                                host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site)


@app.route("/register/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
async def _register_page(request=flask.request):
    match request.method:
        case "POST":
            try:
                user = User(username=request.json.get("username"), user_password=request.json.get("password"))
                db.create_user(user)
            except UsernameNotAvailableException as e:
                response = flask.Response(status=utils.httpstatus.ClientError.CONFLICT)
                response.headers.add("error", str(e))
                return response
            except InvalidArgumentsException as e:
                response = flask.Response(status=utils.httpstatus.ClientError.BAD_REQUEST)
                response.headers.add("error", str(e))
                return response

            new_session = db.create_session(user)
            response = flask.Response(status=utils.httpstatus.Successful.CREATED)  # , headers={"Location": "/home"})
            response.set_cookie("accountSessionIdentifier", str(new_session.session_identifier),
                                max_age=48 * 60 * 60 - 60, secure=True, samesite="strict")
            return response
        case "GET":
            site = sb.build(sites["register"])
            return flask.render_template_string(site.html.value.__str__(),
                                                title=f"{template.title_prefix} | {site.title}",
                                                host=f"{host[0]}:{str(host[1])}", icon=site.icon.name, site=site)


@app.route("/logout/", methods=["GET"])
@app.route("/logout", methods=["GET"])
async def _logout():
    # This route deletes the session-cookie and redirects the client to the login page
    response = flask.Response(status=utils.httpstatus.Redirection.TEMPORARY_REDIRECT, headers={"Location": "/login"})
    response.delete_cookie("accountSessionIdentifier")
    return response


@app.route("/favicon.ico/", methods=["GET"])
@app.route("/favicon.ico", methods=["GET"])
async def _favicon():
    # This route redirects the browser to the favicon because some browsers search for the favicon in the
    # "/favicon.ico" route by default
    return flask.Response(status=utils.httpstatus.Redirection.PERMANENT_REDIRECT,
                          headers={"Location": "/assets/ico/favicon"})


@app.route("/grab_posts/", methods=["GET"])
@app.route("/grab_posts", methods=["GET"])
async def _grab_posts(request=flask.request):
    # This route is made for the frontend to be able to responsively load new content when the user scrolls down.

    # It first tries to get the specifications from the request's headers. But if they don't exist it just defaults
    # to giving it back the 5 latest posts
    try:
        posts = db.grab_posts(int(request.headers["amount"]), int(request.headers["offset"]))
    except KeyError:
        posts = db.grab_posts(5, 0)

    # Now it iterates through the returned list, converts them into a string and returns it to the client
    return utils.jsontools.stringify([{
            "title": post.title,
            "post_id": post.post_id,
            "content": post.content,
            "user": {
                "username": post.user.username,
                "user_identifier": post.user.user_identifier
            },
            "timestamp": post.timestamp,
            "views": post.views
        } for post in posts])


@app.route("/assets/<filetype>/<name>/", methods=["GET"])
async def _assetloader(filetype: str, name: str):
    # This route loads assets/files such as css, js or image files that are accessed from the websites frontend
    asset = Asset(name=name, filetype=filetype)
    try:
        loaded_asset = helpers.assets.load_asset(asset)
    except exceptions.assets.FileNotFoundException:
        return flask.abort(code=utils.httpstatus.ClientError.NOT_FOUND)

    return flask.Response(loaded_asset.value, mimetype=str(asset.mimetype))


app.run(host=host[0], port=host[1])
