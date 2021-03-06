from flask import render_template, Blueprint, flash, redirect, make_response
import py_012_embedded_tagging
from app.lib_master_python import ds_recipe_lib
from app.lib_master_python import ds_authentication

bp_012 = Blueprint('py_012_embedded_tagging', __name__)

@bp_012.route('/')  # Create a envelope draft and shows the result
def index():
    r = py_012_embedded_tagging.send()
    redirect_url = ds_authentication.reauthenticate_check(r, ds_recipe_lib.get_base_url())
    if redirect_url:
        return redirect(redirect_url)
    if r["err"]:
        flash(r["err"])
        return redirect(ds_recipe_lib.get_base_url(2))
    else:
        return render_template('generic_sent.html', title='Embedded Tagging--Python', data=r, base_url=ds_recipe_lib.get_base_url(2))
        # base_url is the home page in the nav bar

@bp_012.route('/get_view')  # Obtains view url and then redirects to it
def get_view():
    r = py_012_embedded_tagging.get_view()
    redirect_url = ds_authentication.reauthenticate_check(r, ds_recipe_lib.get_base_url())
    if redirect_url:
        return redirect(redirect_url)
    if r["err"]:
        flash(r["err"])
        return redirect(ds_recipe_lib.get_base_url(2))
    else:
        return redirect(r["redirect_url"])
        # We are redirecting the user to the DocuSign tag and send console
        # Note that there are multiple options for maintaining state.
        # iFrames are never needed and should never be used since the DocuSign embedded sending experience
        # needs the entire screen, especially for people sending via mobiles and tablets

@bp_012.route('/return_url')  # DocuSign redirects to here after the person finishes
def return_url():
    r = py_012_embedded_tagging.return_url()
    if r["err"]:
        flash(r["err"])
        return redirect(ds_recipe_lib.get_base_url(2))
    else:
        return render_template('generic_sent.html', title='Embedded Tagging--Python', data=r, base_url=ds_recipe_lib.get_base_url(2))
        # base_url is the home page in the nav bar



