from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pymysql

app = Flask(__name__)


@app.route("/add/user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html")

    username = request.form.get("user")
    mobile = request.form.get("mobile")
    gender = request.form.get("gender")
    age = request.form.get("age")
    date = request.form.get("date")
    
    
    # ########## 对用户输入的数据进行校验 ###########
    for i in [username, mobile]:
        if not i:
            return "参数不能为空"
    if not mobile.isdigit():
        return "手机号必须是数字"
    if len(mobile) != 11:
        return "手机号必须是11位"
    if age and not age.isdigit():
        return "年龄必须是数字"
    if int(age) > 150 or int(age) < 0:
        return "请输入正确的年龄"
    # ########## 将用户信息保存到数据库 ###########
    # 1.连接MySQL
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="123456", charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送指令
    sql = "insert into admin(username, mobile, gender, age, date) values(%s, %s, %s, %s, %s)"
    cursor.execute(sql, [username, mobile, gender, age, date])
    conn.commit()

    # 3.关闭
    cursor.close()
    conn.close()

    return "添加成功"

@app.route("/show/user")
def show_user():
    # ########## 从数据库获取所有用户信息 ###########
    # 1.连接MySQL
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="123456", charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送指令
    sql = "select * from admin"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    # 3.关闭
    cursor.close()
    conn.close()

    print(data_list)


    # 1.找到index.html的文件，读取所有的内容。
    # 2.找到内容中 `特殊的占位符` ，将数据替换。
    # 3.将替换完成的字符串返回给用户的浏览器。
    return render_template('show_user.html',data_list=data_list)


@app.route("/delete/user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    # 1.连接MySQL
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="123456", charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送删除指令
    sql = "DELETE FROM admin WHERE id = %s"
    cursor.execute(sql, (user_id,))
    conn.commit()

    # 3.关闭
    cursor.close()
    conn.close()

    return redirect(url_for('show_user'))

if __name__ == '__main__':
    app.run()
