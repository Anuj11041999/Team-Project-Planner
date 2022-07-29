from project_board_base import ProjectBoardBase
from user_base import UserBase
from team_base import TeamBase
import json

user_base = UserBase()
team_base = TeamBase()
board_base = ProjectBoardBase()
# Creating users
user_base.create_user(request=json.dumps({"name": "anuj_chilwery", "display_name": "Anuj Chilwery"}))
user_base.create_user(request=json.dumps({"name": "shravan_chaudhary", "display_name": "Shravan Chaudhary"}))
# users = user_base.list_users()
# print(json.loads(users))
# user = user_base.describe_user(json.dumps({"id": 1}))
# print(json.dumps(user))

# to_update = {
#     "id" : "1",
#     "user" : {
#         "name" : "Shravan",
#         "display_name" : "xyz"
#     }
# }

# user_base.update_user(json.dumps(to_update))

# team_base.create_team(request=json.dumps({"name": "backend", "description": "Backend", "admin" : 1}))
# team_base.create_team(request=json.dumps({"name": "frontend", "description": "Frontend", "admin" : 2}))
teams = team_base.list_teams()
print(json.loads(teams))
# team = team_base.describe_team(json.dumps({"id": 1}))
# print(json.dumps(team))

# to_update = {
#     "id" : "1",
#     "team" : {
#         "name" : "team1",
#         "description" : "xyz",
#         "admin" : 1
#     }
# }

# team_base.update_team(json.dumps(to_update))
# data = {
#     "id" : "2",
#     "users" : ["1", "2"]
# }
# team_base.add_users_to_team(json.dumps(data))
# team_base.remove_users_from_team(json.dumps(data))
# team_users = team_base.list_team_users(json.dumps({"id": 2}))
# user_teams = user_base.get_user_teams(json.dumps({"id": 1}))
# print(team_users)
# print(user_teams)

# board_base.create_board(request=json.dumps({
#     "name" : "sprint_1",
#     "description" : "Sprint 1",
#     "team" : "1",
# }))

# board_base.add_task(json.dumps({
#     "title" : "factwise_assignment",
#     "description" : "Python Assignment for factwise.",
#     "user" : "1",
#     "board": "1",
# }))

# board_base.update_task_status(json.dumps({
#     "id": 1,
#     "status": "IN_PROGRESS"
# }))
# board_base.update_task_status(json.dumps({
#     "id": 1,
#     "status": "COMPLETE"
# }))
# boards = board_base.list_boards(json.dumps({
#     "id": 1
# }))
# print(boards)
# print(board_base.close_board(json.dumps({
#     "id": 1
# })))
# board_base.export_board(json.dumps({"id": 1}))