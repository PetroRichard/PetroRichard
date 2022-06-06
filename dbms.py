import pymysql.cursors



class DBMS:


   def __init__(self,server,user,database,password):
       self.connection = pymysql.connect(host=server,
                                    user=user,
                                    password=password,
                                    db=database,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)


# Connect to the database
   def  execute(self,name):

    try:

        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `name`,`reg`,`phone`,`email`,`programme`  FROM `student` WHERE `name` like %s"
            cursor.execute(sql, ('%{}%'.format(name),))
            result = cursor.fetchone()

            response=""
            for key in result:
                response+="{}:{}\n".format(key,result[key])
            result=response
            return result

    except:
        #self.connection.close()
        return "none found"

# Connect to the database
   def transaction(self, transaction,amount,name,mobile):

            try:

                with self.connection.cursor() as cursor:
                    # Read a single record
                    sql = "INSERT INTO `payments` (`transaction_id`,`amount`,`name`,`mobile_no`) VALUES (%s,%s,%s,%s)"
                    cursor.execute(sql, (transaction,amount,name,mobile))
                    self.connection.commit()

                    # sql = "UPDATE `applications` SET `application_state`=3 WHERE `id` IN (SELECT applications.id FROM `applications` JOIN `users` ON users.id=applications.user_id WHERE users.mobile_no=255746034823)"
            except Exception as e:
                # self.connection.close()
                print(e.args)

   def close(self):
       try:
           self.connection.close()
       except :
        pass
