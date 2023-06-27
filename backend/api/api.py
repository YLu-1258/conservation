from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from backend import db
from backend.model.user import User
from backend.model.students import Student
from backend.model.missions import Missions

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
            return [user.to_dict() for user in get_all_user_list()]
        
        user = get_user_by_name(username)
        if user:
            return user.to_dict()
        return {"message": "User not found"}, 404
    
    def post(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        role = int(request.get_json().get("role"))
        obj = User(username, password, role, 0, 0)
        try:
            db.session.add(obj)
            db.session.commit()
            return obj.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500
        
    def put(self):
        pass

    def delete(self):
        pass
        
class PointsAPI(Resource):
    # We want to retrieve points for a user
    def get(self):
        username = request.get_json().get("username")
        if not username:
            points_list = []
            for user in get_all_user_list():
                user_points = get_points_by_id(user.id)
                if user_points:
                    points_list.append({user_points._username: {"points": user_points._points, "levels": user_points._levels}})
            return points_list
        student = get_points_by_id(get_user_by_name(username).id)
        if student:
            return {student._username:{"points":student._points, "levels":student._levels}}
        return {"message": student}, 404
    
    def post(self):
        username = request.get_json().get("username")
        points = int(request.get_json().get("points"))
        if not username:
            return {"message": "No user provided"}, 404
        student = get_points_by_id(get_user_by_name(username).id)
        if (student._points + points) >= 1000:
            # If level up
            total_points = student._points + points
            levels_to_add = total_points // 1000
            points_remaining = total_points % 1000
            student.update_points(points_remaining, student._levels + levels_to_add)
            return student.read()
        elif (student._points + points >= 0):
            # If same level
            student.update_points(student._points + points, student._levels)
            return student.read()
        else:
            # If lose points
            total_difference = abs(student._points - points)
            levels_to_subtract = total_difference // 1000 + 1
            points_to_subtract = total_difference % 1000
            if (student._points - points < 0):
                # decrease level
                student.update_points(1000 - points_to_subtract, student._levels - levels_to_subtract)
            else:
                # If same level
                student.update_points(student._points - points_to_subtract, student._levels)
            return student.read()

class MissionsAPI(Resource):
    def get(self):
        id = int(request.get_json().get("id"))
        if not id:
            return get_all_missions()
        mission_obj = get_mission_by_id(id)
        if mission_obj:
            res = mission_obj.read()
            return res
        
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        id = int(request.get_json().get("id"))
        mission_obj = get_mission_by_id(id)
        if mission_obj:
            mission_obj.delete()
            return "Mission successfully deleted", 200
        mission_obj = get_mission_by_id(id)
        if mission_obj:
            res = mission_obj.read()
            return res
        pass

users_api.add_resource(UsersAPI, "/")
points_api.add_resource(PointsAPI, "/")
missions_api.add_resource(MissionsAPI, "/")