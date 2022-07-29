from tables import Task, Users
from tables import Board, Teams
import json
from session import Session
session = Session()
class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        data = json.loads(request)
        data.update(status="OPEN")
        board = Board(**data)
        session.add(board)
        session.commit()

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        data = json.loads(request)
        task = session.query(Task).filter(Task.board==data["id"])
        for task in task:
          if task.status != 'COMPLETE':
            return json.dumps({"result": "Failed"})
        board = session.get(Board, data["id"])
        board.status = "CLOSED"
        session.commit()
        return json.dumps({"result": "Success"})
        
    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        data = json.loads(request)
        board = session.get(Board , data["board"])
        if board.status == 'OPEN':
              data.update(status="OPEN")
              task = Task(**data)
              session.add(task)
              session.commit()

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        data = json.loads(request)
        task = session.get(Task , data["id"])
        task.status=data["status"]
        session.commit()


    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        data = json.loads(request)
        return json.dumps([board.as_dict() for board in session.query(Board).filter(Teams.id==data["id"]).order_by(Board.created_at).all()])


    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        data = json.loads(request)
        board = session.get(Board, data["id"])
        lines = []
        lines.append(f"Name: {board.name}   Status: {board.status}   Team: {board.team}\n")
        lines.append("\n")
        lines.append("Tasks: \n")
        tasks = session.query(Task).filter(Board.id==data["id"]).all()
        for task in tasks:
          assinged_to_name = session.get(Users, task.user).display_name
          lines.append(f"Task: {task.title}   Assigned To: {assinged_to_name}   Status: {task.status}\n")
        with open(f"out/{board.name}.txt", "w+") as f:
          f.writelines(lines)
