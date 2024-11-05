from flask import Flask, render_template, request
import sys

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    
    image_file=request.files["file"]
    image_file.save(f"static/images/{image_file.filename}")
    
    data=request.form
    print("User posted: ",
          request.form.get("name"),
          request.form.get("seller"),
          request.form.get("addr"),
          request.form.get("email"),
          request.form.get("category"),
          request.form.get("card"),
          request.form.get("status"),
          request.form.get("phone"),)
    return render_template("result.html", data=data, img_path=f"static/images/{image_file.filename}")
 
if __name__ == "__main__":
    application.run(host='0.0.0.0')

