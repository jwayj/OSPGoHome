
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import sys
from flask_paginate import Pagination, get_page_args
import hashlib
from database import DBhandler



application = Flask(__name__)
application.config["SECRET_KEY"]="helloosp"
DB=DBhandler()

@application.route("/")
def hello():
    return home()

@application.route("/home") 
def home():
    # Fetch data
    reviews = DB.get_reviews()  # Review data
    items = DB.get_items()      # Item data

    # Limit reviews to 3 and split into rows of 1
    reviews = list(reviews.items())[:3]  # Only 3 reviews
    review_rows = [[review] for review in reviews]  # Each review in its own row

    # Limit items to 10 and split into rows of 5
    items = list(items.items())[:10]
    item_rows = [items[i:i + 5] for i in range(0, len(items), 5)]  # Split into rows of 5

    return render_template(
        "home.html",
        reviews=review_rows,  # Reviews as rows of 1
        rows=item_rows        # Items as rows of 5
    )

@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page=10 # item count to display per page
    per_row=5# item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_items() #read the table
    item_counts = len(data)
    #print(data.items())
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

@application.route("/chat")
def view_chat():
    return render_template("chat.html")

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("view_detail.html", name=name, data=data)

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")


#리뷰
@application.route("/review_list")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page=10 # item count to display per page
    per_row=5 #item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_reviews() #read the table
    print('DEBUG - Review Data:',data)
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == (row_count-1)) and ((tot_count%per_row) != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])     
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "review_list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)
  

@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("reg_reviews.html", name=name)

@application.route("/reg_reviews", methods=['POST'])
def reg_review():
    data=request.form
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('view_review_detail'))

@application.route("/submit_review_post", methods=['POST'])
def reg_review_submit_post():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    DB.reg_review(data, image_file.filename)
    return render_template("submit_review_post.html", data=data, img_path= "static/image/{}".format(image_file.filename))

@application.route("/chat")
def view_chat():
    return render_template("chat.html")
@application.route("/view_review_detail/<name>/")
def view_review_detail(name):

    print("###name:",name)
    data = DB.get_review_byname(str(name))
    print("####data:",data)
    return render_template("review.html", name=name, data=data)

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")
def find_user(self, id_, pw_):
    users = self.db.child("user").get()
    target_value=[]
    for res in users.each():
        value = res.val()
        if value['id'] == id_ and value['pw'] == pw_:
            return True
    return False

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    pw_confirm = data['pw_confirm']
    
    if pw != pw_confirm:
        flash("비밀번호가 일치하지 않습니다.")
        return redirect("/signup2")
    
    if DB.insert_user(data, pw_hash):
        return render_template("signup3.html", user_id=data['id'])
    else:
        #flash("user id already exist!")
        return render_template("signup2.html")

@application.route("/signup1")
def signup1():
    return render_template("signup1.html")

@application.route("/signup2", methods=['POST', 'GET'])
def signup2():
    if 'agree' not in request.form:
        flash("약관에 동의해야 합니다.")
        return redirect("/signup1")
    return render_template("signup2.html")

# @application.route("/signup3", methods=['POST'])
# def signup3():
#     # 여기서 사용자 정보를 처리하고 데이터베이스에 저장합니다.
#     data = request.form
#     print("#######debug", data)
#     pw = data['pw']
#     pw_confirm = data['pw_confirm']
    
#     if pw != pw_confirm:
#         flash("비밀번호가 일치하지 않습니다.")
#         return redirect("/signup2")
    
#     pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
#     if DB.insert_user(data, pw_hash):
#         return render_template("signup3.html", user_id=data['id'])
#     else:
#         flash("사용자 등록에 실패했습니다.")
#         return redirect("/signup2")

@application.route("/check_duplicate_id", methods=['POST'])
def check_duplicate_id():
    id_ = request.form['id']
    if DB.user_duplicate_check(id_):
        return "available"
    else:
        return "duplicate"


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("submit_item_post.html", data=data, img_path= "static/image/{}".format(image_file.filename))

@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})
@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '안좋아요 완료!'})


 
if __name__ == "__main__":
    application.run(host='0.0.0.0')

