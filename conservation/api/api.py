from flask import Blueprint, request
from flask_restful import Api, Resource
from conservation import db
from conservation.model.user import User
from conservation.model.students import Student
from conservation.model.missions import Missions
from conservation.model.history import History
from conservation.helpers import cast_int

users_bp = Blueprint("users", __name__, url_prefix = "/api/users")
points_bp = Blueprint("points", __name__, url_prefix = "/api/points")
missions_bp = Blueprint("missions", __name__, url_prefix = "/api/missions")
history_bp = Blueprint("history", __name__, url_prefix = "/api/history")
leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix = "/api/leaderboard")
advisor_bp = Blueprint("advisor", __name__, url_prefix = "/api/advisor")

users_api = Api(users_bp)
points_api = Api(points_bp)
missions_api = Api(missions_bp)
history_api = Api(history_bp)
leaderboard_api = Api(leaderboard_bp)
advisor_api = Api(advisor_bp)

def get_all_user_list():
    try:
        return [user for user in User.query.all()]
    except:
        return

def get_user_list():
    try:
        return [[user.id, user._username] for user in User.query.filter_by(_role=0).all()]
    except:
        return

def get_advisor_list():
    try:
        return [[user.id, user._username] for user in User.query.filter_by(_role=1).all()]
    except:
        return

def get_admin_list():
    try:
        return [[user.id, user._username] for user in User.query.filter_by(_role=2).all()]
    except:
        return

def get_user_by_name(username):
    try:
        return User.query.filter_by(_username=username).all()[0]
    except:
        return
    
def get_points_by_name(username):
    try:
        return Student.query.filter_by(_username=username).all()[0]
    except:
        return
    
def get_mission_by_name(name):
    try:
        return Missions.query.filter_by(_name=name).all()[0]
    except:
        return
    
def get_points_by_id(id):
    try:
        return Student.query.filter_by(_uuid=id).all()[0]
    except:
        return
    
def get_user_by_id(uid):
    try:
        return User.query.filter_by(id=uid).all()[0]
    except:
        return
    
def get_all_missions():
    print("Missions: ", [mission.to_dict() for mission in Missions.query.all()])
    try:
        
        return [mission.to_dict() for mission in Missions.query.all()]
    except:
        return
    
def get_mission_by_id(id):
    try:
        return Missions.query.filter_by(id=id).all()[0]
    except:
        return

def get_mission_by_visibility(uuaid):
    try:
        return [mission.to_dict() for mission in Missions.query.filter_by(_visibility=uuaid).all()]
    except:
        return []
    
def get_uuaid_for_user(id):
    try:
        return Student.query.filter_by(_uuid=id).first().to_dict()["_uuaid"]
    except:
        return
    
def get_completed_history_for_user(id):
    try:
        return [entry.to_dict() for entry in History.query.filter_by(_uuid=id, _progress=1).all()]
    except:
        return  

def get_in_progress_history_for_user(id):
    try:
        return [entry.to_dict() for entry in History.query.filter_by(_uuid=id, _progress=0).all()]
    except:
        return  
    
def get_history_entry_by_id(id):
    try:
        return History.query.filter_by(id=id).first()
    except:
        return
    
def get_user_batch(page):
    idx = 10*page
    scores_list = sorted([score.to_dict_total_score() for score in Student.query.all()], key=lambda s: s["points"], reverse=True )
    counter = 0
    batch = []
    while (counter < 10 and idx < len(scores_list)-1):
        temp = {}
        temp["username"] = scores_list[idx]["username"]
        temp["level"] = scores_list[idx]["points"] // 1000
        temp["points"] = scores_list[idx]["points"] % 1000
        batch.append(temp)
        counter+=1
        idx+=1
    return batch

def get_user_by_advisor(uuaid):
    try:
        return [student.to_dict() for student in Student.query.filter_by(_uuaid=uuaid).all()]
    except:
        return []
    

class UsersAPI(Resource):
    def get(self):
        id = cast_int(request.args.get("user_id"))
        if id == -1:
            return {"username":"broadcast"}
        elif id == -2:
            try:
                return [user.to_dict() for user in get_all_user_list()]
            except Exception as e:
                return {"message": f"server error: {e}"}, 500
        
        try:
            user = get_user_by_id(id).to_dict()
            user["uuaid"] = get_uuaid_for_user(id)
            return user
        except Exception as e:
            return {"message": f"server error: {e}"}, 500
    
    def post(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        role = request.get_json().get("role")
        try:
            user = User(username, password, role)
            db.session.add(user)
            db.session.commit()
            
            user_id = user.id
            
            if role == 2:
                student = Student(user_id, username, None, 0, 0)
                db.session.add(student)
                db.session.commit()
                return [user.to_dict(), student.to_dict()], 201
            else:
                return [user.to_dict()], 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        role = request.get_json().get("role")
        user = get_user_by_name(username)
        try:
            return user.update(username, password, role)
        except Exception as e:
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        username = request.get_json().get("username")

        user = get_user_by_name(username)
        points = get_points_by_name(username)
        if points:
            points.delete()
        try:
            user.delete()
            return {"message": f'user "{username}"deleted'}, 200
        except Exception as e:
            return {"message": f"server error: {e}"}, 500
        
class PointsAPI(Resource): # POST request for creating object should be handeled upon user creation
    # We want to retrieve points for a user
    def get(self):
        id = request.args.get("userid")
        if not id:
            points_list = []
            for user in get_all_user_list():
                user_points = get_points_by_id(id)
                if user_points:
                    points_list.append({user_points._username: {"points": user_points._points, "levels": user_points._levels}})
            try:
                return points_list
            except Exception as e:
                return {"message": f"server error: {e}"}, 500
            
        student = get_points_by_id(id)
        try:
            return {student._username:{"points":student._points, "levels":student._levels}}
        except Exception as e:
            return {"message": f"server error: {e}"}, 500
    
    def put(self):
        id = request.get_json().get("user_id")
        points = request.get_json().get("points")
        points = cast_int(points)
        try:
            if not id:
                return {"message": "No user provided"}, 404
            student = get_points_by_id(id) # student = get_points_by_id(get_user_by_name(username).id)
            if (student.points + points) >= 1000:
                # If level up
                total_points = student._points + points
                levels_to_add = total_points // 1000
                points_remaining = total_points % 1000
                student.update_points(points_remaining, student._levels + levels_to_add)
                return student.to_dict()
            elif (student.points + points >= 0):
                # If same level
                student.update_points(student._points + points, student._levels)
                return student.to_dict()
            else:
                # If lose points
                print(student.points)
                total_difference = abs(student._points - points)
                levels_to_subtract = total_difference // 1000 + 1
                points_to_subtract = total_difference % 1000
                if ((student.points + points) < 0):
                    # decrease level
                    student.update_points(1000 - points_to_subtract, student._levels - levels_to_subtract)
                else:
                    # If same level
                    student.update_points(student._points - points_to_subtract, student._levels)
                return student.to_dict()
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

class MissionsAPI(Resource):
    def get(self):
        id = request.args.get("id")
        if not id:
            return get_all_missions()
        mission_obj = get_mission_by_id(id)
        try:
            return mission_obj.to_dict()
        except Exception as e:
            return {"message": f"server error: {e}"}, 500
        
    def post(self): # name, value, visibility, description, time, location
        name = request.get_json().get("name")
        value = request.get_json().get("value")
        visibility = request.get_json().get("visibility")
        description = request.get_json().get("description")
        time = request.get_json().get("time")
        location = request.get_json().get("location")
        try:
            obj = Missions(name, value, visibility, description, time, location)
            db.session.add(obj)
            db.session.commit()
            return obj.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        id = int(request.get_json().get("id"))
        name = request.get_json().get("name")
        value = request.get_json().get("value")
        visibility = request.get_json().get("visibility")
        description = request.get_json().get("description")
        time = request.get_json().get("time")
        location = request.get_json().get("location")
        try:
            mission_obj = get_mission_by_id(id)
            return mission_obj.update(name, value, visibility, description, time, location)
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        id = cast_int(request.get_json().get("id"))
        try:
            mission_obj = get_mission_by_id(id)
            if mission_obj:
                mission_obj.delete()
                return "Mission successfully deleted", 200
            mission_obj = get_mission_by_id(id)
            if mission_obj:
                res = mission_obj.delete()
                return ""
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

class RetrieveMissionsAPI(Resource):
    def get(self):
        uuaid = cast_int(request.args.get("uuaid"))
        if not uuaid:
            return sorted(get_mission_by_visibility(-1), key = lambda m: m["value"], reverse=True)
        visible_missions = sorted(get_mission_by_visibility(uuaid) + get_mission_by_visibility(-1), key = lambda m: m["value"], reverse=True)
        return visible_missions

class HistoryAPI(Resource):
    def get(self):
        uuid = cast_int(request.args.get("user_id"))
        if not uuid:
            return []
        response = {}
        response["completed"] = get_completed_history_for_user(uuid)
        response["in_progress"] = get_in_progress_history_for_user(uuid)
        return response
    
    def post(self):
        uuid = cast_int(request.get_json().get("uuid"))
        name = request.get_json().get("name")
        value = cast_int(request.get_json().get("value"))
        visibility = request.get_json().get("visibility")
        description = request.get_json().get("description")
        time = cast_int(request.get_json().get("time"))
        location = request.get_json().get("location")
        progress = cast_int(request.get_json().get("progress"))

        try:
            obj = History(uuid, name, value, visibility, description, time, location, progress)
            db.session.add(obj)
            db.session.commit()
            return obj.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500
        
    def put(self):
        id = int(request.get_json().get("id"))
        uuid = cast_int(request.get_json().get("uuid"))
        name = request.get_json().get("name")
        value = request.get_json().get("value")
        visibility = request.get_json().get("visibility")
        description = request.get_json().get("description")
        time = request.get_json().get("time")
        location = request.get_json().get("location")
        progress = cast_int(request.get_json().get("progress"))
        try:
            history_obj = get_history_entry_by_id(id)
            print(history_obj)
            return history_obj.update(uuid, name, value, visibility, description, time, location, progress)
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500
        
    def delete(self):
        entry_id = cast_int(request.get_json().get("id"))

        entry = get_history_entry_by_id(entry_id)
        if entry_id:
            entry.delete()
            return {"message": f'entry "{entry_id}"deleted'}, 200
        return {"message": f"server error"}, 500

class LeaderboardAPI(Resource):
    def get(self):
        try:
            page = cast_int(request.args.get("page"))
            display = get_user_batch(page)
            return display
        except Exception as e:
            return {"message": f"server error: {e}"}, 500
        
class AdvisorAPI(Resource):
    def get(self):
        uuaid = cast_int(request.args.get("uuaid"))
        if uuaid:
            try:
                return get_user_by_advisor(uuaid)
            except Exception as e:
                return {"message": f"server error: {e}"}, 500
        return {"message": f"server error: {e}"}, 500

users_api.add_resource(UsersAPI, "/")
points_api.add_resource(PointsAPI, "/")
missions_api.add_resource(MissionsAPI, "/")
missions_api.add_resource(RetrieveMissionsAPI, "/retrieve")
history_api.add_resource(HistoryAPI, "/")
leaderboard_api.add_resource(LeaderboardAPI, "/")
advisor_api.add_resource(AdvisorAPI, "/")