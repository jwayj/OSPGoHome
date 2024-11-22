
from flask import Flask, render_template, request, flash, redirect, url_for, session
import sys
from flask_paginate import Pagination, get_page_args
import hashlib
from database import DBhandler



application = Flask(__name__)
application.config["SECRET_KEY"]="helloosp"
DB=DBhandler()

@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('view_list'))

@application.route("/home") 
def home():
    page = request.args.get("page", 0, type=int)
    per_page=10 # item count to display per page
    per_row=5# item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_items() #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "home.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

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

@application.route("/review_list", methods=["GET"])
def review_list():
    page, per_page, offset = get_page_args(per_page=10)
    # 현재 페이지, 페이지당 아이템 수, 현재 페이지는 몇 번째 아이템부터 보여주는가

    # cur = get_cur()
    # cur.execute("SELECT COUNT(*) FROM posts;")  # 일단 총 몇 개의 포스트가 있는지를 알아야합니다.
    # total = cur.fetchone()[0]
    # cur.execute(
    #     "SELECT * FROM posts ORDER BY created "  # SQL SELECT로 포스트를 가져오되,
    #     "DESC LIMIT %s OFFSET %s;",  # offset부터 per_page만큼의 포스트를 가져옵니다.
    #     (per_page, offset),
    # )
    # posts = cur.fetchall()
    posts_all = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] # 임시 전체 아이템
    total = len(posts_all)
    posts = posts_all[offset:offset+per_page]

    return render_template(
        "/review_list.html",
        posts=posts,
        pagination=Pagination(
            page=page,  # 지금 우리가 보여줄 페이지는 1 또는 2, 3, 4, ... 페이지인데,
            total=total,  # 총 몇 개의 포스트인지를 미리 알려주고,
            per_page=per_page,  # 한 페이지당 몇 개의 포스트를 보여줄지 알려주고,
            prev_label="< Back",  # 전 페이지와,
            next_label="Next >",  # 후 페이지로 가는 링크의 버튼 모양을 알려주고,
            format_total=True,  # 총 몇 개의 포스트 중 몇 개의 포스트를 보여주고있는지 시각화,
            css_framework='foundation'
        ),
        search=True,  # 페이지 검색 기능을 주고,
        bs_version=5,  # Bootstrap 사용시 이를 활용할 수 있게 버전을 알려줍니다.
    )

@application.route("/review")  # 디버깅용
def view_review():
    return render_template("review.html")

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("view_detail.html", name=name, data=data)

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

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
    if DB.insert_user(data,pw_hash):
        return render_template("signup3.html")
    else:
        flash("user id already exist!")
        return render_template("signup2.html")

@application.route("/signup1")
def signup1():
    return render_template("signup1.html")

@application.route("/signup2", methods=['POST'])
def signup2():
    if 'agree' not in request.form:
        flash("약관에 동의해야 합니다.")
        return redirect("/signup1")
    return render_template("signup2.html")

@application.route("/signup3", methods=['POST'])
def signup3():
    # 여기서 사용자 정보를 처리하고 데이터베이스에 저장합니다.
    data = request.form
    pw = data['pw']
    pw_confirm = data['pw_confirm']
    
    if pw != pw_confirm:
        flash("비밀번호가 일치하지 않습니다.")
        return redirect("/signup2")
    
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("signup3.html", user_id=data['id'])
    else:
        flash("사용자 등록에 실패했습니다.")
        return redirect("/signup2")

@application.route("/check_duplicate_id", methods=['POST'])
def check_duplicate_id():
    id_ = request.form['id']
    is_available = DB.user_duplicate_check(id_)
    if is_available:
        flash("사용 가능한 아이디입니다.")
    else:
        flash("이미 사용 중인 아이디입니다.")
        return redirect("/signup2")


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("submit_item_post.html", data=data, img_path= "static/images/{}".format(image_file.filename))


 
if __name__ == "__main__":
    application.run(host='0.0.0.0')

