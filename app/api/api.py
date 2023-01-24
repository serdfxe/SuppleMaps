from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

api = Blueprint("api", __name__)
