from flask import Flask, render_template, request
import sys
from flask_paginate import Pagination, get_page_args


application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/review_list", methods=("GET",))
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

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

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

