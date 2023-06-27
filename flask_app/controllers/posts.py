from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/create_post', methods=['POST'])
def create_post():
    print("in create route")
    print(request.form)
    Post.save(request.form)
    return redirect("/dojo_wall")

@app.route('/delete_post/<post_id>')
def delete_post(post_id):
    print("Deleting Post-", post_id)
    Post.delete_post(post_id)
    return redirect("/dojo_wall")