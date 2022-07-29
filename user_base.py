from tables import TeamMembers, Teams, Users
import json
from session import Session
session = Session()
class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        data = json.loads(request)
        user = Users(**data)
        session.add(user)
        session.commit()

    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        return json.dumps([user.as_dict() for user in session.query(Users).order_by(Users.created_at).all()])

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        id = json.loads(request)["id"]
        user = session.get(Users, id)
        return json.dumps(user.as_dict())

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        data = json.loads(request)
        data["user"].pop("name")
        session.query(Users).filter(Users.id==data["id"]).update(data["user"])
        session.commit()

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        data = json.loads(request)
        user_id = data["id"]
        teams = []
        team_members = session.query(TeamMembers).filter(TeamMembers.user==user_id)
        for team_member in team_members:
          team = session.get(Teams, team_member.team)
          teams.append(team.as_dict())
        return json.dumps(teams)

