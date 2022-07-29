Tables: 

User:
1. name
2. display_name
3. id
4. created_at

Team:
1. name
2. description
3. admin
4. id
5. created_at

TeamMember
1. user_id ->foreign_key User
2. team_id -> foreign_key Team
3. id

Board
1. name
2. description
3. team
4. created_at
5. status

Task:
1. Title
2. description
3. user -> foreign_key User
4. created_at
5. status
6. board_id -> foreign_key Board