from flask import Flask, render_template, Blueprint, redirect, url_for, session

from amigo.main.utils.data_utils import get_data, encode_url
from amigo.main.utils.events_utils import access_required

from amigo import redis_conn

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Returns & renders the index page.

    Args:
        None
    
    Returns:
        _render: A rendered page.
    """
    return render_template("index.html")

@main.route("/steam")
def send_request():
    """Acts as the middleman while authenticating the user, redirect to the encoded URL.

    Args:
        None
    
    Returns:
        redirect: A page redirect.
    """
    encoded_url = encode_url()
    return redirect(encoded_url)

@main.route("/process")
def process():
    """Tries to obtain user data, if a KeyError is thrown, redirect to game not found page.

    Args:
        None
    
    Returns:
        redirect: A page redirect.
    """
    try:
        get_data()
    except KeyError:
        return redirect(url_for("errors.notfound"))
        
    return redirect(url_for("main.waiting"))

@main.route("/waiting")
@access_required()
def waiting():
    """Returns & renders the waiting page.

    Args:
        None
    
    Returns:
        _render: A rendered page.
    """
    return render_template("waiting.html")

@main.route("/chat")
@access_required()
def chat():
    """Returns & renders the chat page.

    Args:
        None
    
    Returns:
        _render: A rendered page.
    """
    return render_template("chat.html")


@main.route("/help")
def help():
    """Returns & renders the help page.

    Args:
        None
    
    Returns:
        _render: A rendered page.
    """
    
    # temporary way to flush

    redis_conn.delete(session["steam_id"])
    session.pop("steam_id", None)
    redis_conn.flushall()

    return render_template("help.html")
