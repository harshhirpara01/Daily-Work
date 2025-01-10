from fastapi import FastAPI
import pymysql.cursors
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse,Response
from starlette.responses import Response as HTTPResponse
from fastapi import HTTPException, Request
import datetime
import random
import re
class user(BaseModel):

    email : str
    fname : str
    lname : str

class login(BaseModel):
    email : str
    password : str



class checklogin(BaseModel):
    email : str
    password : str
    verifycode : str


class userdelete(BaseModel):

    email : str

class isverify(BaseModel):
    email : str
    password : str
    verifycode : str

class fetch_data(BaseModel):
    email : str


class user_register(BaseModel):
    username : str
    email : str
    fname : str
    lname : str
    password : str
    mobileno : str
    is_verify : bool = False


class insert(BaseModel):
    username: str = Field(..., min_length=1, description="Username cannot be empty")
    email: str
    fname: str = Field(..., min_length=1, description="First name cannot be empty")
    lname: str = Field(..., min_length=1, description="Last name cannot be empty")
    password: str = Field(..., min_length=6, description="Password must be at least 6 char long")
    mobileno: str = Field(..., min_length=10, max_length=15, description="Mobile number must be valid")
    city: str = Field(..., min_length=1, description="City cannot be empty")
    country: str = Field(..., min_length=1, description="Country cannot be empty")
    state: str = Field(..., min_length=1, description="State cannot be empty")
    pincode: str = Field(..., min_length=5, max_length=10, description="Pincode must be valid")
    birthdate: datetime.date
    is_delete: bool = False

app = FastAPI()


def randome_code():
    return random.randint(100000,999999)

def randome_otp():
    return random.randint(100,999)

code = randome_code()





def data_connection():
    return pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        password = '2833',
        database = 'harsh',
        cursorclass = pymysql.cursors.DictCursor
    )

connection = data_connection()


    # query = """
    #     INSERT INTO tbl_user (username, email, fname, lname, password, mobileno, city, country, state, pincode, birthdate)
    #     VALUES ('darshan', 'dspatel@gmail.com', 'darshan', 'patel', '5874', '99077286085', 'imli', 'india', 'gujarat', '369550', '1947-08-11')
    #      """



    # cursor.execute(query)
@app.get("/getting")
async def get_data():
    cursor = connection.cursor()
    cursor.execute("select * from tbl_user")
    connection.commit()
    result = cursor.fetchall()
    connection.close()

    return {"message " : result}






@app.post("/update data")
async def check_data(User:user):
    cursor = connection.cursor()
    check_query = """
    select email from tbl_user where email = %s
    """
    cursor.execute(check_query,(User.email,))
    user_exist = cursor.fetchone()

    if not user_exist:
        cursor.close()
        connection.close()

        return {"message":"user not found"}


    update_query = """
        update tbl_user
        set fname = %s,lname = %s
        where email = %s
        """

    cursor.execute(update_query,(User.fname,User.lname,User.email))
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"user updated succesfully"}


@app.delete("/delete")
async def delete(delete: userdelete):
    cursor = connection.cursor()
    check_query = """
        select email from tbl_user where email = %s
        """
    cursor.execute(check_query, (delete.email,))
    user_existed = cursor.fetchall()

    if not user_existed:
        cursor.close()
        connection.close()

        return {"message": "user not found"}

    delated_query = """
           update  tbl_user
           set is_delete = TRUE
           where email = %s
           """
    cursor.execute(delated_query,(delete.email,))
    connection.commit()
    cursor.close()
    connection.close()


    return {"message" : "user deleted succesfully"}

    
@app.post("/insert_data")
async def insert_data(data : insert):

    if data.is_delete:
        raise HTTPException(status_code=400, detail="Invalid value for is_delete")

    email_check = r"(^[\w]+@[\w]+\.[a-z]{2,3}$)"
    if not re.match(email_check, data.email):
        raise HTTPException(status_code=400, detail="Invalid email format.")

       # if not data.username or not data.fname or not data.lname or not data.email or not data.birthdate or not data.pincode

    cursor = connection.cursor()
    query = """
    insert into tbl_user
    (username,email,fname,lname,password,mobileno,city,country,state,pincode,
    birthdate,is_delete)values (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query,(data.username,data.email,data.fname,data.lname,data.password,data.mobileno,data.city,data.country,data.state,data.pincode,data.birthdate,data.is_delete))
    connection.commit()
    connection.close()

    return {"status_code": 200, "message": "data inserted successfully"}





#REGISTER - username, email, fname, lname , password, mobileno , is_verify , verifycode
#when user register then insert data in table generate code

#verify register - email,passwprdf , verifycode


@app.post("/register_user")
async def register_user(register: user_register):

    if register.is_verify:
        raise HTTPException(status_code= 400 , detail = "invalid value for is verify")

    email_check = r"(^[\w]+@[\w]+\.[a-z]{2,3}$)"
    if not re.match(email_check, register.email):
        raise HTTPException(status_code=400, detail="Invalid email format.")

    cursor = connection.cursor()

    #
    #
    # check_query = """
    # select * from users where username = %s or email = %s or mobileno = %s
    #
    # """
    # cursor.execute(check_query,(register.username,register.email,register.mobileno))
    # existuser = cursor.fetchone()
    #
    # if existuser:
    #     cursor.close()
    #     connection.close()
    #
    #
        # if existuser["username"]== register.username:
        #     raise HTTPException(status_code = 400,detail = 'username is already exists')

        # if existuser["email"]== register.email:
        #     raise HTTPException(status_code = 400,detail = 'email is already exists')

        # if existuser["mobileno"]== register.mobileno:
        #     raise HTTPException(status_code = 400,detail = 'mobile number is already exists')


    verification_code = randome_code()



    connection = data_connection()
    cursor = connection.cursor()
    query = """
insert into users(username,email,fname,lname,password,mobileno,is_verify,verifycode)
values(%s,%s,%s,%s,%s,%s,%s,%s)

"""
    cursor.execute(query,(register.username,register.email,register.fname,register.lname,register.password,register.mobileno,register.is_verify,verification_code))
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"user succesfully registred","verification code":verification_code}


@app.get("/show_registeruser")
async def show_user():
    cursor = connection.cursor()

    query = """
    select * from users
    
    """
    cursor.execute(query)
    connection.commit()
    result = cursor.fetchall()
    connection.close()

    return {"users":result}



@app.post("/check_verification")
async def check_verifyuser(verify:isverify):
    cursor = connection.cursor()

    try:

           query = """
        select email, password, verifycode, is_verify
        from users
        where email = %s
        order by created_at desc
                     """
           cursor.execute(query,(verify.email,))
           result = cursor.fetchone()


           if not result:
                return {"message":"user not verified. invalid detail"}

           if result["is_verify"]:
               return {"message": "user is already verified."}

           if result['email'] != verify.email:
               return {"message":"email does not match"}

           if result['password'] != verify.password:
               return {"message":"password does not match"}

           if result['verifycode'] != verify.verifycode:
               return {"message":"verifycode does not match"}


           qeury2 = """
              update users
                  set is_verify = true
                     where email = %s and password = %s and verifycode = %s
                      """
           cursor.execute(qeury2,(verify.email,verify.password,verify.verifycode))

           return {"message":"user verified succesfully"}
    finally:
        connection.commit()
        cursor.close()
        connection.close()




@app.post("/fetch_latest_data")
async def fetching_data(fetch:fetch_data):

    cursor = connection.cursor()

    query = """
    select verifycode,password from users where email = %s
    order by created_at desc
    
    """

    cursor.execute(query,(fetch.email,))
    fetch_result = cursor.fetchone()
    cursor.close()
    connection.close()

    if not fetch_result:
        raise HTTPException(status_code = 404, detail = "user not found")

    return {"latest-data":fetch_result}



@app.post("/login")
async def login(userlogin:login):
    cursor = connection.cursor()

    try:
          query = """
    
               select email,password from users 
               where email = %s and
               password = %s and is_verify = True
               
            """
          cursor.execute(query,(userlogin.email,userlogin.password))
          login_exist = cursor.fetchone()

          if not login_exist:
              raise HTTPException(status_code = 400,detail = "invalid detail or user not verified")

          login_otp = randome_otp()
          print("login_otp-->>",login_otp)

          qury_update_otp = f"""
            update users
		    set verifycode = '{login_otp}'
		    where  email='{userlogin.email}'  and password = '{userlogin.password}';
            """

          cursor.execute(qury_update_otp)

          connection.commit()



          return {"message":"otp generate succesfully","otp":login_otp}









    finally:
        connection.commit()
        cursor.close()
        connection.close()


@app.post("/check_login")
async def check_login(check: checklogin):
    cursor = connection.cursor()
    email_check = r"(^[\w]+@[\w]+\.[a-z]{2,3}$)"
    if not re.match(email_check, check.email):
        raise HTTPException(status_code=400, detail="Invalid email format.")
    try:
        query = """
        SELECT email, password, verifycode, is_verify 
        FROM users
        WHERE email = %s and is_verify = 1 order by 
        created_at desc
        """

        cursor.execute(query, check.email)
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=400, detail="User not verified or invalid details")

        if result['email'] != check.email:
            raise HTTPException(status_code=400, detail="Email does not match")

        if result['password'] != check.password:
            raise HTTPException(status_code=400, detail="Password does not match")

        if result['verifycode'] != check.verifycode:
            raise HTTPException(status_code=400, detail="Verify code does not match")

        return {"message": "User login successfully.........."}
    finally:
        connection.commit()
        cursor.close()
        connection.close()

#JSONRESPONSE, RESPONSE, HTTPRESPONSE

@app.get("/json_responce")
async def responce_json():
    content = {"message":"hello sir how can i help you to learn response"}
    return JSONResponse(content,status_code = 200)


@app.get("/response")
async def response():
    content = "<h1>this is html responce</h1>"
    return Response(content, media_type = "text/html")

@app.get("/https-responce")
async def https_binary(request:Request):
    heaeee= request.headers
    print(heaeee)
    content = b"custome binary response"

    headers = {"X-Example-Header": "CustomHeader"}

    print(request.headers)
    return HTTPResponse(content = content,status_code=200,headers = headers,media_type= "application/octet-stream")