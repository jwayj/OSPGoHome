import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    #item 정보
    def insert_item(self, name, data, img_path):
        item_info ={
            "name": data['name'],
            "category": data['category'],
            "explanation": data['explanation'],
            "price": data['price'],
            "seller": data['seller'],
            "addr": data['addr'],
            "gun":data['gun'],
            "img_path": img_path,
            "status": data['status'],
            "directtransaction": data['directtransaction']
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
        return target_value
    
    #user 정보
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'], "pw": pw,
            "name": data['name'] }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data) 
            return True
        else:
            return False
           
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True
    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False
    
    #review 정보
    def reg_review(self, data, img_path):
        review_info ={
        "reviewerId": data['reviewerId'],
        "category": data['category'],
        "status": data['status'],
        "rating": data['rating'],
        "reviewTitle": data['reviewTitle'],
        "review": data['review'],
        "img_path": img_path
        }
        #받아올 정보: 상품명
        self.db.child("review").child(data['name']).set(review_info)
        print(data, img_path)
        return True
    
    def get_reviews(self):
        reviews=self.db.child("review").get().val()
        return reviews
    
    def get_review_byname(self, name):
        reviews = self.db.child("review").get()
        target_value=""
        print("###########",name)
        for res in reviews.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
        return target_value

    #heart
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()
        return target_value

    def update_heart(self, user_id, isHeart, item):
        heart_info ={
        "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    
    #list.html에서 status에 따라 다른 값 출력
    def get_items_bystatus_and_addr(self, cate1, cate2):
        print("카테고리",cate1, "지역",cate2)
        items = self.db.child("item").get() 
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()
            if value['status'] == cate1 and value['addr'] == cate2:
                target_value.append(value) 
                target_key.append(key_value)
        print("######target_value",target_value) 
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    def get_items_bystatus(self, cate):
        print("카테고리",cate)
        items = self.db.child("item").get() 
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['status'] == cate:
                target_value.append(value) 
                target_key.append(key_value)
        print("######target_value",target_value) 
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    def get_items_byaddr(self, cate):
        print("지역",cate)
        items = self.db.child("item").get() 
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['addr'] == cate:
                target_value.append(value) 
                target_key.append(key_value)
        print("######target_value",target_value) 
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    
    def get_last_chatroom(self, user_id):
        user_rooms = self.db.child("UserRooms").child(user_id).get()
        last_chatted_user = ""
        last_chatted_time = 0
        temp_user = ""
        temp_time = 0
        
        try:
            for room in user_rooms.each():
                messages = self.db.child("RoomMessages").child(room.val()['roomId']).get()
                
                for message in messages.each():
                    message_time = message.val()['timestamp']
                    
                    if message.val()['user'] == user_id:
                        if message_time > last_chatted_time:
                            last_chatted_time = message_time
                            last_chatted_user = room.key()
                    elif last_chatted_user == "":
                        if message_time > last_chatted_time:
                            temp_time = message_time
                            temp_user = room.key()
            
            if last_chatted_user == "":
                last_chatted_user = temp_user
                last_chatted_time = temp_time
        except:
            return ""
        return last_chatted_user
            