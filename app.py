from bottle import get, static_file, template, error, delete


###############################
@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

###############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

###############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

####################
@get("/")
def _():
    return template("index.html")


###############################
@error(404)
def _(error):
    return 'Nothing here, sorry :('


###############################
import routes.get_users
import routes.create_user
import routes.delete_user
import routes.update_user
