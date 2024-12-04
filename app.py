
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import sys
from flask_paginate import Pagination, get_page_args
import hashlib
import math
from database import DBhandler




application = Flask(__name__)
application.config["SECRET_KEY"]="helloosp"
DB=DBhandler()

###홈 화면
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

###상품 전체조회 화면
@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    status = request.args.get("status", "all")
    addr = request.args.get("addr","all")
    price_order = request.args.get("price", "all")
    availability=request.args.get("availability","all")
    #print("주소 출력",addr)
    #print("지역 출력",addr)
    #print("debug",page, status)
    #print("debug",page, addr)
    per_page=10 # item count to display per page
    per_row=5# item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    # data=DB.get_items()
    # if status!="all":
    #     items={k:v for k,v in data.items() if v['status']==status}
    # if addr!=all:
    #     items={k:v for k,v in data.items() if v['addr']==addr}
    data=DB.get_items()
    if status != "all":
        data={k: v for k,v in data.items() if v['status']==status}
    if addr!="all":
        data={k: v for k,v in data.items() if v['addr']==addr}

    
    for key, value in data.items():
        if DB.get_review_byname(key):
            value['availability']="sold_out"
        else:
            value['availability']="available"

    if availability!="all":
        data={k: v for k,v in data.items() if v['availability']==availability}
    
    if price_order=="low":
        data=dict(sorted(data.items(), key=lambda x: int(x[1]["price"])))
    elif price_order=="high":
        data=dict(sorted(data.items(), key=lambda x: int(x[1]["price"]), reverse=True))
    elif price_order=="all":
        data=data
    print("data 출력",data)
    #print("debug data",data, "지역도 출력", addr, "상태도 출력",status)
    item_counts = len(data)
    if item_counts<=per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])
    print(data.items())
    #data = dict(list(data.items())[start_idx:end_idx])
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
        page_count=int(math.ceil(item_counts/per_page)),
        total=item_counts,
        status=status,
        addr=addr,
        price_order=price_order,
        availability=availability)

@application.route("/chat")
def chat():
    last_chatted_user = DB.get_last_chatroom(session['id'])
    print(last_chatted_user)
    return redirect(url_for("view_chat", opponent_id=last_chatted_user))
    
@application.route("/chat/<opponent_id>")
def view_chat(opponent_id):
    user = session['id']
    return render_template("chat.html", opponent=opponent_id, user=user)

###상품 상세 화면
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("view_detail.html", name=name, data=data)

###리뷰 등록 화면
@application.route("/reg_items")
def reg_item():
    if 'id' in session:
        return render_template("reg_items.html")
    flash("로그인이 필요합니다") #로그아웃 상태일 때 상품 등록 제한, 로그인페이지로 이동
    return redirect(url_for('login'))
    
@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    if 'id' in session:
        return render_template("reg_reviews.html", name=name)
    flash("로그인이 필요합니다") #로그아웃 상태일 때 리뷰 등록 제한, 로그인페이지로 이동
    return redirect(url_for('login'))
    

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
    return view_review_detail(data['name'])

#리뷰 전체 조회 화면
@application.route("/review_list", methods=("GET",))
def review_list():
    page, per_page, offset = get_page_args(per_page=10)
    # 현재 페이지, 페이지당 아이템 수, 현재 페이지는 몇 번째 아이템부터 보여주는가

    posts_all = DB.get_reviews()
    total = len(posts_all)
    posts = dict(list(posts_all.items())[offset:offset+per_page])

    return render_template(
        "/review_list.html",
        posts=posts.items(),
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

# @application.route("/reg_review_init/<name>/")
# def reg_review_init(name):
#     return render_template("reg_reviews.html", name=name)

# @application.route("/reg_reviews", methods=['POST'])
# def reg_review():
#     data=request.form
#     image_file=request.files["file"]
#     image_file.save("static/image/{}".format(image_file.filename))
#     DB.reg_review(data, image_file.filename)
#     return redirect(url_for('view_review_detail'))

# @application.route("/submit_review_post", methods=['POST'])
# def reg_review_submit_post():
#     image_file=request.files["file"]
#     image_file.save("static/image/{}".format(image_file.filename))
#     data=request.form
#     DB.reg_review(data, image_file.filename)
#     return render_template("submit_review_post.html", data=data, img_path= "static/image/{}".format(image_file.filename))

@application.route("/view_review_detail/<name>/")
def view_review_detail(name):
    print("###name:",name)
    data = DB.get_review_byname(str(name))
    print("####data:",data)
    return render_template("review.html", name=name, data=data)

###로그인
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

###로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

###회원가입
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

@application.route("/check_duplicate_id", methods=['POST'])
def check_duplicate_id():
    id_ = request.form['id']
    if DB.user_duplicate_check(id_):
        return "available"
    else:
        return "duplicate"

###
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():

    image_file=request.files.get("file")
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    DB.insert_item(data['name'], data, image_file.filename)
    return view_item_detail(data['name'])

###좋아요
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

### 자릿수 포맷팅
@application.template_filter('comma_format')
def comma_format(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value 


 
if __name__ == "__main__":
    application.run(host='0.0.0.0')

