from tables import Teams, TeamMembers, Users
import json
from session import Session
session = Session()

class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        data = json.loads(request)
        team = Teams(**data)
        session.add(team)
        session.commit()

    # list all teams
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        return json.dumps([team.as_dict() for team in session.query(Teams).order_by(Teams.created_at).all()])


    # describe team
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        id = json.loads(request)["id"]
        team = session.get(Teams, id)
        return json.dumps(team.as_dict())

    # update team
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        data = json.loads(request)
        session.query(Teams).filter(Teams.id==data["id"]).update(data["team"])
        session.commit()

    # add users to team
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        data = json.loads(request)
        team_id = data["id"]
        users = data["users"]
        team = session.get(Teams, team_id)
        for user_id in users:
          session.add(TeamMembers(team=team.id, user=session.get(Users, user_id).id))
          session.commit()


    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        data = json.loads(request)
        team_id = data["id"]
        users = data["users"]
        for user_id in users:
          team_member = session.query(TeamMembers).filter(Users.id==user_id,Teams.id==team_id).first()
          session.delete(team_member)
          session.commit()


    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        data = json.loads(request)
        team_id = data["id"]
        users = []
        team_members = session.query(TeamMembers).filter(TeamMembers.team==team_id)
        for team_member in team_members:
          user = session.get(Users, team_member.user)
          users.append(user.as_dict())
        return json.dumps(users)

