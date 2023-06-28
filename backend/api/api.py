from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from backend import db
from backend.model.user import User
from backend.model.students import Student
from backend.model.missions import Missions
from backend.helpers import cast_int

users_bp = Blueprint("users", __name__, url_prefix = "/api/users")
points_bp = Blueprint("points", __name__, url_prefix = "/api/points")
missions_bp = Blueprint("missions", __name__, url_prefix = "/api/missions")
users_api = Api(users_bp)
points_api = Api(points_bp)
missions_api = Api(missions_bp)

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
    
def get_all_missions():
    print("Missions: ", [mission.read() for mission in Missions.query.all()])
    try:
        
        return [mission.read() for mission in Missions.query.all()]
    except:
        return
    
def get_mission_by_id(id):
    try:
        return Missions.query.filter_by(id=id).all()[0]
    except:
        return

class UsersAPI(Resource):
    def get(self):
        username = request.get_json().get("username")
        if not username:
            try:
                return [user.to_dict() for user in get_all_user_list()]
            except Exception as e:
                return {"message": f"server error: {e}"}, 500
        
        user = get_user_by_name(username)
        try:
            return user.to_dict()
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
        username = request.get_json().get("username")
        if not username:
            points_list = []
            for user in get_all_user_list():
                user_points = get_points_by_id(user.id)
                if user_points:
                    points_list.append({user_points._username: {"points": user_points._points, "levels": user_points._levels}})
            try:
                return points_list
            except Exception as e:
                return {"message": f"server error: {e}"}, 500
            
        student = get_points_by_name(username)
        try:
            return {student._username:{"points":student._points, "levels":student._levels}}
        except Exception as e:
            return {"message": f"server error: {e}"}, 500
    
    def put(self):
        username = request.get_json().get("username")
        points = request.get_json().get("points")
        points = cast_int(points)
        try:
            if not username:
                return {"message": "No user provided"}, 404
            student = get_points_by_name(username) # student = get_points_by_id(get_user_by_name(username).id)
            if (student.points + points) >= 1000:
                # If level up
                total_points = student._points + points
                levels_to_add = total_points // 1000
                points_remaining = total_points % 1000
                student.update_points(points_remaining, student._levels + levels_to_add)
                return student.read()
            elif (student.points + points >= 0):
                # If same level
                student.update_points(student._points + points, student._levels)
                return student.read()
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
                return student.read()
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

class MissionsAPI(Resource):
    def get(self):
        id = request.get_json().get("id")
        if not id:
            return get_all_missions()
        mission_obj = get_mission_by_id(id)
        try:
            res = mission_obj.read()
            return res
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

users_api.add_resource(UsersAPI, "/")
points_api.add_resource(PointsAPI, "/")
missions_api.add_resource(MissionsAPI, "/")