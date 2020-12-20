from flask import Flask, render_template, request,session,send_from_directory
import os
import EmailSending

app=Flask(__name__)
app.secret_key = 'jsbcdsjkvbdjkbvdjcbkjf'

import pymysql
conn=pymysql.connect(host="localhost",user="root",password="root",db="storyboard")
cursor=conn.cursor()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
  return render_template('adminlog.html')

@app.route('/channel')
def channel():
  return render_template('channel.html')

@app.route('/reporter')
def reporter():
  return render_template('reporter.html')

@app.route('/adminlog1')
def adminlog1():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'admin' and  password=='admin':
        return render_template('adminhome.html')
    else:
        return render_template('adminlog.html')




@app.route('/userlogin')
def userlogin():
  return render_template('userlogin.html')

@app.route('/userregister')
def userregister():
  return render_template('userregister.html')

@app.route('/channelregister')
def channelregister():
  return render_template('channelregister.html')


@app.route('/userregister1')
def register1():
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    phone = request.args.get('phone')
    result= cursor.execute(" insert into userreg(name,username,email,password,phone)values('"+name+"','"+username+"','"+email+"','"+password+"','"+phone+"')");
    conn.commit()

    if result > 0:
        return render_template('userlogin.html')
    else:
        return render_template('userregister.html')


@app.route('/channelregister1')
def channelregister1():
    cname = request.args.get('cname')
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    phone = request.args.get('phone')
    result= cursor.execute(" insert into channel(cname,name,username,email,password,phone)values('"+cname+"','"+name+"','"+username+"','"+email+"','"+password+"','"+phone+"')");
    conn.commit()

    if result > 0:
        return render_template('channel.html')
    else:
        return render_template('channel.html')



@app.route('/userlogin1')
def login1():
    username = request.args.get('username')
    password = request.args.get('password')

    result = cursor.execute(" select * from userreg where username='" + username + "' and password='" + password + "'  and status1='yes'")
    conn.commit()

    if result > 0:
        session['username'] = username
        return render_template('userhome.html')
    else:
        return render_template('userlogin.html')

@app.route('/channel1')
def channel1():
    username = request.args.get('username')
    password = request.args.get('password')

    result = cursor.execute(" select * from channel where username='" + username + "' and password='" + password + "'  and status1='yes'")
    conn.commit()
    deltails= cursor.fetchall()

    for row in deltails:
         cname=row[1]
         if result > 0:
            session['username'] = username
            session['cname'] = cname
            return render_template('channelhome.html')
         else:
            return render_template('channel.html')


@app.route('/reporter1')
def reporter1():
    username = request.args.get('username')
    password = request.args.get('password')

    result=cursor.execute(" select * from nreporter where username='" + username + "' and password='" + password + "' ")
    details = cursor.fetchall()
    conn.commit()
    if result > 0:
        for roww in details:
             z = roww[6]
             session['username'] = username
             session['cname']=z
        return render_template('reporterhome.html')
    else:
          return render_template('channel.html')


@app.route('/adminlogout')
def adminlogout():
     return render_template('index.html')

@app.route('/userlogout')
def userlogout():
    print("hellow message")
    session.pop('username', None)
    return render_template("index.html")

@app.route('/clogout')
def clogout():
    print("hellow message")
    session.pop('username', None)
    return render_template("index.html")


@app.route('/reporterlogout')
def reporterlogout():
    print("hellow message")
    session.pop('username', None)
    return render_template("index.html")




@app.route('/allusers')
def alldrivers():

    resultvalue = cursor.execute("select * from userreg ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allusers.html', userDetails=userDetails)
    else:
        return render_template('adminMsg.html',msg="Users are not available")


@app.route('/allchannel')
def allchannel():

    resultvalue = cursor.execute("select * from channel ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allchannel.html', userDetails=userDetails)
    else:
        return render_template('adminMsg.html',msg="Users are not available")



@app.route('/verifyusers')
def verifyDriver():
        req_id=request.args.get('Id')

        resultvalue = cursor.execute("update userreg set status1='yes' where  user_id='"+req_id+"' ")
        userDetails = cursor.fetchall()
        conn.commit()
        if resultvalue > 0:
            return alldrivers()
        else:
            return render_template('adminMsg.html',msg='Verification Fails')

@app.route('/verifyusers1')
def verifyusers1():
        req_id=request.args.get('Id')

        resultvalue = cursor.execute("update channel set status1='yes' where  user_id='"+req_id+"' ")
        userDetails = cursor.fetchall()
        conn.commit()
        if resultvalue > 0:
            return allchannel()
        else:
            return render_template('adminMsg.html',msg='Verification Fails')


@app.route('/profile')
def profile():
    username=session['username']

    resultvalue = cursor.execute("select * from userreg where username='"+username+"'  ")
    conn.commit()

    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('profile.html', userDetails=userDetails)




@app.route('/nreporter')
def nreporter():
  return render_template('nreporter.html')



@app.route('/neporter1')
def neporter1():
    cusername=session['username']
    cname = session['cname']
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    phone = request.args.get('phone')
    result= cursor.execute(" insert into nreporter(name,username,email,password,phone,cname,cusername)values('"+name+"','"+username+"','"+email+"','"+password+"','"+phone+"','"+cname+"','"+cusername+"')");
    conn.commit()

    if result > 0:
        EmailSending.EmailSending.send_email("Your UerName  & assword", "UserName is:", username+"  "+ password,email)

        return allreporters()
    else:
        return render_template('channelMsg.html?msg='+"Reporter Added Fails")



@app.route('/allreporters')
def allreporters():
    cname=session['cname']
    username=session['username']
    print(username)

    resultvalue = cursor.execute("select * from nreporter where cname='"+cname+"'  and cusername='"+username+"'")
    print(resultvalue)
    conn.commit()
    userDetails = cursor.fetchall()
    msg = 'Reporter Not Available'
    if resultvalue > 0:
        return render_template('allreporters.html', userDetails=userDetails)
    else:
        return render_template('channelMsg.html',msg='reporters not available')



@app.route('/deleteusers')
def deleteusers():
        req_id=request.args.get('Id')

        resultvalue = cursor.execute("delete from nreporter where  user_id='"+req_id+"' ")

        conn.commit()
        if resultvalue > 0:
            return allreporters()
        else:
            return render_template('allreporters.html')



@app.route('/uploadnews')
def uploadnews():
  return render_template('uplofile.html')

@app.route('/uploadfile1',methods=['POST'])
def uploadfile1():
    username = session['username']
    cname = session['cname']

    target = os.path.join(APP_ROOT, 'images/')
    for upload in request.files.getlist("file"):
        category = request.form.get('category')
        newsname = request.form.get('newsname')
        pdate = request.form.get('pdate')
        desc = request.form.get('desc')
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
        resultvalue = cursor.execute("insert into news(category,name,descc,datee,upby,pic,cname) values('" + category + "','" + newsname + "','" + desc + "','" + pdate + "','" + username + "','" + upload.filename + "','"+cname+"')")
        conn.commit()
        if resultvalue > 0:
                return  render_template('reporterMsg.html',msg='New Uploded Sucessfully')
        else:
                return render_template('reporterMsg.html',msg='news Uploded Fails')






@app.route('/publish')
def publish():
    username=session['cname']

    resultvalue = cursor.execute("select * from news where cname='"+username+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allnews.html', userDetails=userDetails)
    else:
        return render_template('channelMsg.html',msg='News not available')

@app.route('/publishnews')
def publishnews():
        req_id=request.args.get('Id')

        resultvalue = cursor.execute("update news set status1='Published' where  user_id='"+req_id+"' ")

        conn.commit()
        if resultvalue > 0:
            return render_template('allnews.html')
        else:
            return render_template('allnews.html')



@app.route('/rejectnews')
def rejectnews():
        req_id=request.args.get('Id')

        resultvalue = cursor.execute("update news set status1='Rejected' where  user_id='"+req_id+"' ")

        conn.commit()
        if resultvalue > 0:
            return render_template('allnews.html')
        else:
            return render_template('allnews.html')


@app.route('/viewpnews')
def viewpnews():
    username = session['cname']

    resultvalue = cursor.execute("select * from news where cname='" + username + "' and status1='Published' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allpubnews.html', userDetails=userDetails)
    else:
        return render_template('channelMsg.html',msg="Published News not available")

@app.route('/viewrnews')
def viewrnews():
    username = session['cname']

    resultvalue = cursor.execute("select * from news where cname='" + username + "' and status1='Rejected' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('alltrejews.html', userDetails=userDetails)
    else:
        return render_template('channelMsg.html',msg="Rejected News not available")

@app.route('/rnews')
def rnews():
    username = session['username']

    resultvalue = cursor.execute("select * from news where upby='" + username + "' and status1='Rejected' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allmypub.html', userDetails=userDetails)
    else:
        return render_template('reporterMsg.html',msg='details are not available')


@app.route('/viewnews')
def viewnews():
    username = session['username']

    resultvalue = cursor.execute("select * from news where upby='" + username + "' and status1='Published' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allpubnews1.html', userDetails=userDetails)
    else:
        return render_template('reporterMsg.html',msg="details not available")



@app.route('/UserHome')
def UserHome():


        resultvalue = cursor.execute("select * from news where  status1='Published' ")
        conn.commit()
        userDetails = cursor.fetchall()
        if resultvalue > 0:
            return render_template("userhome.html", image_names=userDetails)


        else:
            return render_template("userMsg.html", msg='news Not Available')


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/viewnews1')
def viewnews1():
    req_id = request.args.get('id')

    resultvalue = cursor.execute("select * from news where user_id='" + req_id + "' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewnews.html', userDetails=userDetails)
    else:
        return render_template('userhome.html')


@app.route('/feedback')
def feedback():
    req_id = request.args.get('id')
    return render_template('feedback.html',cname=req_id)

@app.route('/report')
def report():
    req_id = request.args.get('id')
    return render_template('report.html',cname=req_id)


@app.route('/report1')
def report1():
    username=session['username']
    cname = request.args.get('cname')
    report = request.args.get('report')

    result= cursor.execute(" insert into report(report,cname,rby)values('"+report+"','"+cname+"','"+username+"')");
    conn.commit()

    if result > 0:

        return render_template('userhome.html')
    else:
        return render_template('report.html')


@app.route('/feedback1')
def feedback1():
    username = session['username']
    cname = request.args.get('cname')
    report = request.args.get('feedback')

    result = cursor.execute(
        " insert into feedback(feedback,cname,rby)values('" + report + "','" + cname + "','" + username + "')");
    conn.commit()

    if result > 0:

        return render_template('userhome.html')
    else:
        return render_template('report.html')


@app.route('/search1')
def search1():
    req_id = request.args.get('search')
    username = session['username']
    cursor.execute("select * from report where  rby='" + username + "' ")
    conn.commit()
    reportdetails = cursor.fetchall()
    for a in reportdetails:
        cname = a[3]
        print(cname + "dfghjk")
        resultvalue = cursor.execute("select * from news where name='" + req_id + "'  and cname='"+cname+"'")
        conn.commit()
        userDetails = cursor.fetchall()
        if resultvalue > 0:
           return render_template('viewnews.html', userDetails=userDetails)


        else:
            return render_template('userMsg.html', msg='details not found')


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/cpassword')
def cpassword():
    return render_template('cpassword.html')


@app.route('/pass')
def pass1():
    username = session['username']
    password = request.args.get('password')
    password1 = request.args.get('password1')

    resultvalue = cursor.execute("select * from nreporter where password='" + password + "' and username='"+username+"'")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        a=cursor.execute("update nreporter set password='"+password1+"' where username='"+username+"'")
        if a > 0:

            return render_template('reporterMsg.html', msg="Password Changed Sucessfully")
        else:
            return render_template('reporterMsg.html', msg="Password Changed Fails")

    else:
        return render_template('reporterMsg.html', msg="InCorrect Password ")


@app.route('/allchafeedback')
def allchafeedback():

    resultvalue = cursor.execute("select * from feedback ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewfeedbacks.html', userDetails=userDetails)
    else:
        return render_template('adminMsg.html',msg="Feedbacks Not Available")

@app.route('/allchannelrep')
def allchannelrep():

    resultvalue = cursor.execute("select * from report ")
    conn.commit()
    if resultvalue > 0:
         userDetails = cursor.fetchall()
         for row in userDetails:
              a=row[3]
              cursor.execute("select COUNT(report) from report where cname='"+a+"'")
              conn.commit()
              count=cursor.fetchone()[0]
              if count > 10:
                 x=cursor.execute("delete from channel where cname='"+a+"'")
                 conn.commit()
                 if x > 0 :
                     y = cursor.execute("delete from nreporter where cname='" + a + "'")
                     conn.commit()
                     if y > 0 :
                         return render_template('viewreports.html', userDetails=userDetails)
                     else:
                         return render_template('amsg.html', msg='news reporters are not available')

                 else:
                     return render_template('amsg.html', msg='news channels are not available')



              else:
                return render_template('viewreports.html', userDetails=userDetails)



    else:
            print("hi")
            return render_template('viewreports.html',msg='details are not available')



@app.route('/cfeedback')
def cfeedback():
    cname = session['cname']
    resultvalue = cursor.execute("select * from feedback where cname='"+cname+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewfeedbacks1.html', userDetails=userDetails)
    else:
        return render_template('channelMsg.html',msg="Feedback not available")


@app.route('/creports')
def creports():
    cname = session['cname']
    resultvalue = cursor.execute("select * from report where cname='"+cname+"'")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewreports1.html', userDetails=userDetails)
    else:
        return render_template('channelMsg.html',msg="Report not available")


@app.route('/reporterHome')
def reporterHome():
    return render_template('reporterhome.html')



if __name__ == '__main__':
    app.run(debug=True)
