from flask import Blueprint, render_template, request, url_for, redirect

from . import dashboard

@dashboard.route('/dashboard')
def index():
    return render_template('dashboard/dashboard.html')
