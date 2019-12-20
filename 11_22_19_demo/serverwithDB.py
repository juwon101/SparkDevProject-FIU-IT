from flask import Flask
from flask import send_from_directory
from flask import request
from dateutil.relativedelta import relativedelta
from socket import socket, SOCK_DGRAM, AF_INET
import pymongo
import time
import datetime
import random

app = Flask(__name__)
client = pymongo.MongoClient("localhost", 27017)
db = client["sparkdev"]  # db name
table = db['sparkdev'] # pick table

fiudb = client["FIU"]
student_table = fiudb['students']

clientSocket = socket(AF_INET, SOCK_DGRAM)

def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac)) 

@app.route("/stats")
def stats():
    pipeline = [{'$group': {'_id': '$EMAIL', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 1}]
    results = table.aggregate(pipeline)
    return str(results.next()['_id'])

@app.route('/.well-known/<path:filename>')
def wellKnownRoute(filename):
    return send_from_directory(app.root_path + '/.well-known/', filename, conditional=True)



@app.route("/", methods=['GET','POST'])
def mainPost():
    resp = { 'fulfillmentText': "Hello from PG6 conference room"}

    if request.method == "POST":
        data = request.get_json()
        action = data["queryResult"]["parameters"]["action"]

        if action == "total_count":
            pipeline = [{'$count': 'id'}]
            user_type = data["queryResult"]["parameters"]["user_type"]
            building = data["queryResult"]["parameters"]["buildings"]
            if user_type == "guest":
                pipeline = [{'$match': {'PID': None}},{'$project': {'_id': 1}}] + pipeline
            elif user_type == "faculty":
                pipeline = [{'$match': {'TYPE': 'FACULTY'}},{'$project': {'_id': 1}}] + pipeline
            elif user_type == "student":
                pipeline = [{'$match': {'TYPE': 'STUDENT'}},{'$project': {'_id': 1}}] + pipeline

            if user_type != "users" and building != "":
                    pipeline[0]['$match']['BUILDING'] = building.upper()
            elif user_type == "users" and building != "":
                    pipeline = [{'$match': {"BUILDING" : building.upper()}},{'$project': {'_id': 1}}] + pipeline
                
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "The count is "+str(results.next()['id'])}

        if action == "user_by_major":
            print("in userbymajor")
            pipeline = [{'$count': 'id'}]
            user_type = data["queryResult"]["parameters"]["user_type"]
            building = data["queryResult"]["parameters"]["buildings"]
            major = data["queryResult"]["parameters"]["majors"]
            if user_type == "student":
                pipeline = [{'$match': {'TYPE': 'STUDENT', 'MAJOR' : major}},{'$project': {'_id': 1}}] + pipeline
            elif user_type == "faculty":
                pipeline = [{'$match': {'TYPE': 'FACULTY', 'DEPARTMENT' : major}},{'$project': {'_id': 1}}] + pipeline
            if user_type != "users" and building != "":
                    pipeline[0]['$match']['BUILDING'] = building.upper()
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "The count is "+str(results.next()['id'])}
            

        if action == "top_user":
            pipeline = [{'$group': {'_id': '$EMAIL', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 1}]
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "The top user is  "+str(results.next()['_id'])}

        if action == "top_building":
            user_type = data["queryResult"]["parameters"]["user_type"]
            pipeline = [{'$group': {'_id': '$BUILDING', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 1}]
            if not (user_type == '' or  user_type == 'users' or user_type == 'guest'):
                pipeline = [{'$match': {'TYPE': user_type.upper()}}] + pipeline
            elif user_type == 'guest':
                pipeline = [{'$match': {'PID': None}}] + pipeline
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "The building with most " + user_type + " is  the "+str(results.next()['_id']) + " building."}

        if action == "top_major":
            pipeline = [{'$group': {'_id': '$MAJOR', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 1}]
            user_type = data["queryResult"]["parameters"]["user_type"]
            building = data["queryResult"]["parameters"]["buildings"]
            if user_type == "student":
                pipeline = [{'$match': {'MAJOR': {'$not': {'$eq': None}}}}] + pipeline
                #delete the faculty part. you might need to change the group aggregator.
            elif user_type == "faculty":
                pipeline = [{'$match': {'TYPE': 'FACULTY'}}] + pipeline
            if user_type != "users" and building != "":
                    pipeline[0]['$match']['BUILDING'] = building.upper()
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "Most students are "+str(results.next()['_id']) + " majors"}

        #if action == "tell_building":


        if action == "last_5min":
            pipeline =[{'$group':{'_id':{'$concat':[{'$toString':{'$year':'$DATE'}},'-',{'$cond':[{'$lte':[{'$month':'$DATE'},9]},{'$concat':['0',{'$toString':{'$month':'$DATE'}}]},{'$toString':{'$month':'$DATE'}}]},'-',{'$cond':[{'$lte':[{'$dayOfMonth':'$DATE'},9]},{'$concat':['0',{'$toString':{'$dayOfMonth':'$DATE'}}]},{'$toString':{'$dayOfMonth':'$DATE'}}]},'T',{'$cond':[{'$lte':[{'$hour':'$DATE'},9]},{'$concat':['0',{'$toString':{'$hour':'$DATE'}}]},{'$toString':{'$hour':'$DATE'}}]},':',{'$cond':[{'$lte':[{'$subtract':[{'$minute':'$DATE'},{'$mod':[{'$minute':'$DATE'},5]}]},9]},{'$concat':['0',{'$toString':{'$subtract':[{'$minute':'$DATE'},{'$mod':[{'$minute':'$DATE'},5]}]}}]},{'$toString':{'$subtract':[{'$minute':'$DATE'},{'$mod':[{'$minute':'$DATE'},5]}]}}]},':00.000Z']},'count':{'$sum':1}}},{'$limit':1}]
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "In the last 5 minutes we had  "+str(results.next()['count'])}

        if action == "bussiest_hour":
            print("use logic from above to determine the hours you might have to play with the numbers")

        if action == "last_x":
            print("How many users were added in the last x minutes")
            #minutes or hours?
            
            last_time = data["queryResult"]["parameters"]["number"]
            time_unit = data["queryResult"]["parameters"]["my_times"]
            #can you go by day?
            end = datetime.datetime.today()
            start = None
            if time_unit == "minute":
                start = end - relativedelta(minutes = last_time)
            elif time_unit == "hour":
                start = end - relativedelta(hours = last_time)
            
            print(start, end)
            pipeline = [{'$match': {'DATE': {'$lt': end,'$gte': start}}}, {'$count': 'id'}]
            results = table.aggregate(pipeline)
            try:
                resp = { 'fulfillmentText': "The count is "+str(results.next()['id'])}
            except StopIteration:
                resp = { 'fulfillmentText': "0 users added since"}

        if action  == "devices":
            pipeline = [{'$group': {'_id': '$MAC', 'count': {'$sum': 1}}}, {"$count" : "id"}]
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "There are "+str(results.next()['id'])+ " devices registered today."}

        if action == "disctinct_users":
            #this needs to be fixed. first should get all non guests and count by their ids. the second one should get ONLY guests and count by their unique email....???? But to do that you need to randomize guest data more!
            user_type = data["queryResult"]["parameters"]["user_type"]
            if user_type == "student" or user_type == "faculty":
                pipeline = [{'$group': {'_id': '$PID', 'count': {'$sum': 1}}}, {"$count" : "id"}]
            elif user_type == "guests":
                pipeline = [{'$group': {'_id': '$EMAIL', 'count': {'$sum': 1}}}, {"$count" : "id"}]
            
            results = table.aggregate(pipeline)
            resp = { 'fulfillmentText': "There are "+str(results.next()['id'])+ " distinct users registered today."}
        
        if action == "building_unique":
            building = data["queryResult"]["parameters"]["buildings"]
            pipeline = [{'$match': {"BUILDING": building.upper(), '$or': [{'TYPE': {'$eq': 'STUDENT'}}, {'TYPE': {'$eq': 'FACULTY'}}]}},{'$group': {'_id': '$PID', 'count': {'$sum': 1}}}, {"$count" : "id"}]
            results = table.aggregate(pipeline)
            first_q = results.next()['id']
            pipeline = [{'$match': {'PID': None}},{'$group': {'_id': '$EMAIL', 'count': {'$sum': 1}}}, {"$count" : "id"}]
            results = table.aggregate(pipeline)
            second_q = results.next()['id']
            resp = { 'fulfillmentText': "There are "+str(first_q + second_q)+ " distinct users in the " + building + " building."}
        

        if action == "id_present":
            print("will search for a specific student")
            student_id = data["queryResult"]["parameters"]["number-sequence"]
            pipeline_spark = [{'$match': {'TYPE': 'STUDENT','PID': student_id}}, {'$sort': {'DATE': -1}}, {'$limit': 1}]
            pipeline_fiu = [{'$match': {'PID': student_id}}]
            name = None
            result_fiu = None
            try:
                result_fiu = student_table.aggregate(pipeline_fiu).next()
                name = result_fiu['FNAME'] + " " + result_fiu['LNAME']
                print(name)
            except StopIteration:
                resp = { 'fulfillmentText': "Student Doesn't exist"}
            #print(name)
            try:
                result_spark = table.aggregate(pipeline_spark).next()
                if name != None:
                    resp = {'fulfillmentText': name + " was last seen in building "+ result_spark["BUILDING"] + " at " +  result_spark["DATE"].strftime('%I:%M %p %b %d, %Y')}
            except StopIteration:
                resp = { 'fulfillmentText': "Student Not in Campus"}
            
                
            
        if action == "random_story":
            print("could be fun for demo one could trace a student's day by location of his wareabouts")
            #group students that have more than 3 entries. then sort by date and tell their story of today!

            pipeline = [{'$match': {'TYPE': 'STUDENT'}}, {'$group': {'_id': '$PID','count': {'$sum': 1}}}, {'$match': {'count': {'$gte': 2}}}, {'$sample': {'size': 1}}]
            results = table.aggregate(pipeline).next()
            student_id = results["_id"]
            print(student_id)
            results = student_table.aggregate([{'$match': {'PID': str(student_id)}}]).next()
            name = results["FNAME"]+" "+ results["LNAME"]
            print(name)
            pipeline = [{'$match': {'PID': student_id}}, {'$sort': {'DATE': 1}}]
            results = table.aggregate(pipeline)
            message_start = name + " registered today "
            message_list = []
            for x in results:
                message_string = "on the " + x["BUILDING"] + " building at " + x["DATE"].strftime('%I:%M %p %b %d, %Y')#[:-8]
                message_list.append(message_string) 
            resp = { 'fulfillmentText': message_start + " and then ".join(message_list)}

        if action == "new_entry":
            print("running demo, creating a student session and pushing it through Dialogflow")
            #uses their flow feature.   
            pid = data["queryResult"]["parameters"]["user_id"]
            fiuEmail = data["queryResult"]["parameters"]["email"]
            building = data["queryResult"]["parameters"]["buildings"]
            major = data["queryResult"]["parameters"]["major"]
            #fix user type
            user_type = data["queryResult"]["parameters"]["user_type"]
            ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            mac = randomMAC()
            message = building.upper() + " " + ip + " " + mac + " " + pid + " " + \
            str(datetime.datetime.now().isoformat()) + " " + fiuEmail + " STUDENT " + major + "\n"
            clientSocket.sendto(message.encode(), ("127.0.0.1", 514))
            print(message)
            resp = { 'fulfillmentText': "User added successfully"}
    return resp



if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=443, ssl_context=('/etc/letsencrypt/live/DOMAIN/cert.pem', '/etc/letsencrypt/live/DOMAIN/privkey.pem'))
    app.run(host="0.0.0.0", port=443, ssl_context=('/etc/letsencrypt/live/sparkdevcris.ddns.net/cert.pem', '/etc/letsencrypt/live/sparkdevcris.ddns.net/privkey.pem'))
    
