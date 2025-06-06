import mariadb
from user import User

class Database:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="useruser",
                host="127.0.0.1",
                port=3306,
                database="127project"
            )
            self.cur = self.conn.cursor(dictionary=True)
        except mariadb.Error as e:
            print(f"Error connecting: {e}")
            raise

    def close(self):
        self.conn.close()
    
    def get_organizations(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            raise

        return self.cur.fetchall()

    # Return None if login failed, return user if login successful
    def login_user(self, username, password):
        try:
            self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        except mariadb.Error as e:
            print(f"Error in login_user: {e}")
            raise

        dbUser = self.cur.fetchone()

        if (dbUser['password'] == password and dbUser['username'] == username):
            user = User(
                dbUser['member_id'],
                dbUser['name'],
                dbUser['gender'],
                dbUser['degree_program'],
                dbUser['access_level'],
                dbUser['username'],
                "2024-2025",
                2
            )
            return user
        else: # Login Failed
            return None
        
    def username_exists(self, username):
        try:
            self.cur.execute("SELECT * FROM member WHERE username=?", (username,))
        except mariadb.Error as e:
            print(f"Error in username_exists: {e}")
            return False

        result = self.cur.fetchone()

        if result is None:
            return False
        else:
            return True
    
    def get_my_organizations(self, user: User):
        query = """
                    SELECT
                        o.organization_name AS org_name,
                        mo.batch AS org_batch,
                        mo.status AS org_status,
                        mo.role AS org_role,
                        mo.committee AS org_committee
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ?
                """
        try:
            self.cur.execute(query, (user.getMemberId(),))

            result = self.cur.fetchall()

            if result is None:
                print("get_my_organizations: None returned")
                return []

            return result
        except mariadb.Error as e:
            print(f"Error in get_my_organizations: {e}")
            return []
        
    def get_all_members(
        self,
        name= None,
        gender=None,
        degree_program=None,
        username=None
    ):
        query = "SELECT * FROM member"  

        params = []
        conditions = []

        if name is not None:
            conditions.append("name LIKE ?")
            params.append(f"%{name}%")
        
        if gender is not None:
            conditions.append("gender LIKE ?")
            params.append(f"{gender}%")

        if degree_program is not None:
            conditions.append("degree_program LIKE ?")
            params.append(f"%{degree_program}%")

        if username is not None:
            conditions.append("username LIKE ?")
            params.append(f"%{username}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            self.cur.execute(query, tuple(params))

            result = self.cur.fetchall()

            if result is None:
                print("get_all_members: None returned")
                return []

            return result
        except mariadb.Error as e:
            print(f"Error has occurred: {e}")
            return []

    
    def get_all_organization_members(
        self,
        organization_id=None,
        status=None,
        committee=None,
        role=None,
        academic_year=None,
        semester=None,
    ):
        query = """
            SELECT 
                m.member_id AS member_id,
                m.name AS member_name,
                o.organization_name AS organization_name,
                mo.batch AS member_batch,
                mo.status AS member_status,
                mo.committee AS member_committee,
                mo.role AS role,
                mo.academic_year AS academic_year,
                mo.semester AS semester
            FROM member m
            JOIN member_org mo ON m.member_id = mo.member_id
            JOIN organization o ON mo.organization_id = o.organization_id
        """

        params = []
        conditions = []

        if organization_id is not None:
            conditions.append("o.organization_id = ?")
            params.append(organization_id)
        if status is not None:
            conditions.append("mo.status LIKE ?")
            params.append(f"%{status}%")
        if committee is not None:
            conditions.append("mo.committee LIKE ?")
            params.append(f"%{committee}%")
        if role is not None:
            conditions.append("mo.role LIKE ?")
            params.append(f"%{role}%")
        if academic_year is not None:
            conditions.append("mo.academic_year = ?")
            params.append(academic_year)
        if semester is not None:
            conditions.append("mo.semester = ?")
            params.append(semester)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            self.cur.execute(query, tuple(params))
            result = self.cur.fetchall()

            if result is None:
                print("get_all_organization_members: None returned")
                return []

            return result
        except mariadb.Error as e:
            print(f"Error has occurred: {e}")
            return []
        
    def get_all_unpaid_members(self, organization_id=None, academic_year=None, semester=None):
        try:
            query = """
                SELECT DISTINCT m.member_id, m.name, f.amount, mo.role, m.gender, m.degree_program,
                    mo.batch, mo.status, mo.committee,
                    fr.academic_year, fr.semester
                FROM member m
                JOIN member_org mo ON m.member_id = mo.member_id
                JOIN fee f ON mo.member_id = f.member_id
                JOIN financial_record fr ON f.record_id = fr.record_id
                JOIN organization o ON fr.organization_id = o.organization_id
                WHERE f.payment_status = "Unpaid"
            """

            params = []

            if organization_id is not None:
                query += " AND o.organization_id = ?"
                params.append(organization_id)

            if academic_year is not None:
                query += " AND fr.academic_year = ?"
                params.append(academic_year)

            if semester is not None:
                query += " AND fr.semester = ?"
                params.append(semester)

            self.cur.execute(query, params)
            result = self.cur.fetchall()

            return result if result is not None else []

        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []
        
    def get_unpaid_fees(self, member_id):
        try:
            self.cur.execute(
                """SELECT o.organization_name, f.fee_type, f.amount, f.due_date, f.payment_status, fr.academic_year, fr.semester,
            from member m JOIN fee f on m.member_id = f.member_id JOIN financial_record fr on f.record_id = fr.record_id
            JOIN organization o ON fr.organization_id = o.organization_id WHERE m.member_id = ? AND f.payment_status = "Unpaid" """,
                (member_id,),
            )
            result = self.cur.fetchall()

            if result is None:
                print("get_unpaid_fees: None returned")
                return []

            return result
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []

    def create_user(self, name, gender, degree_program, password, access_level, username):
        try:
            self.cur.execute(
                """INSERT INTO member (`name`, `gender`, `degree_program`,
                `password`, `access_level`, `username`)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, gender, degree_program, password, access_level, username),
            )
        except mariadb.Error as e:
            print(f"Error occurred in create_user: {e}")
            return None

        if self.cur.rowcount == 1:
            print(f"User {username} successfully added")
            self.conn.commit()
            return self.cur.lastrowid
        else:
            print("Insert may have failed or user already exists")
            return None
    
    def create_org(self, organization_name, date_established):
        try:
            self.cur.execute(
                """INSERT INTO organization (`organization_name`,`date_established`) VALUES (?, ?)""",
                (organization_name, date_established),
            )
        except mariadb.Error as e:
            print(f"Error occurred in create_organization: {e}")
            return None
        
        if self.cur.rowcount == 1:
            print(f"Organization {organization_name} successfully added")
            self.conn.commit()
            return self.cur.lastrowid
        else:
            print("Insert failed")
            return None
        
    def create_membership(
            
        self, member_id, organization_id,
        batch, status, role, committee,
        acad_year, semester
        ):
        try:
            self.cur.execute(
                """INSERT INTO member_org VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    member_id,
                    organization_id,
                    batch,
                    status,
                    role,
                    committee,
                    acad_year,
                    semester,
                ),
            )

        except mariadb.Error as e:
            print(f"Error occurred in create_organization: {e}")
            return None
        
        if self.cur.rowcount == 1:
            print(f"Member {member_id} added to organization {organization_id}")
            self.conn.commit()
            return member_id
        else:
            print("Insert failed")
            return None
        
    # Returns `id` on successful creation
    # Returns None on creation failure
    # Commits change
    def create_financial_record(self, balance, academic_year, semester, organization_id):
        try:
            self.cur.execute(
                """INSERT INTO financial_record
            (`balance`, `academic_year`, `semester`, `organization_id`)
            VALUES(?, ?, ?, ?)""",
                (balance, academic_year, semester, organization_id),
            )
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return None
        
        if self.cur.rowcount == 1:
            print(f"Financial record added!")
            self.conn.commit()
            return self.cur.lastrowid
        else:
            print("Insert failed")
            return None


    # Returns `id` on successful creation
    # Returns None on creation failure
    # Commits change
    def create_fee(
        self,
        amount,
        due_date,
        date_issued,
        fee_type,
        payment_status,
        member_id,
        academic_year,
        semester,
        organization_id,
        description = None,
        pay_date = None
)   :
        try:
            # Find record first, if not found, create new.
            self.cur.execute("""
                SELECT record_id FROM financial_record
                WHERE organization_id = ? AND academic_year = ? AND semester = ?
            """, (organization_id, academic_year, semester))

            result = self.cur.fetchone()

            if result:
                record_id = result['record_id']
            else:
            
                self.cur.execute("""
                    INSERT INTO financial_record (balance, organization_id, academic_year, semester)
                    VALUES (?, ?, ?, ?)
                """, (0, organization_id, academic_year, semester))
                record_id = self.cur.lastrowid
                print(f"Created new financial record: {record_id}")

            # 3. Insert the fee using the resolved record_id
            self.cur.execute("""
                INSERT INTO fee (
                    amount, due_date, date_issued, fee_type,
                    payment_status, pay_date, description,
                    member_id, record_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                amount, due_date, date_issued, fee_type,
                payment_status, pay_date, description,
                member_id, record_id
            ))

            if self.cur.rowcount == 1:
                self.conn.commit()
                print("Fee added!")
                return self.cur.lastrowid
            else:
                print("Insert failed")
                return None

        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return None

    # Returns `id` on successful update
    # Returns None on update failure
    # Commits change
    def update_member(
        self,
        member_id,
        name=None,
        gender=None,
        degree_program=None,
        password=None,
        access_level=None,
        username=None,
    ):
        modifiedFields = []
        values = []

        if name is not None:
            modifiedFields.append("name = ?")
            values.append(name)
        if gender is not None:
            modifiedFields.append("gender = ?")
            values.append(gender) 
        if degree_program is not None:
            modifiedFields.append("degree_program = ?")
            values.append(degree_program)
        if password is not None:
            modifiedFields.append("password = ?")
            values.append(password)
        if access_level is not None:
            modifiedFields.append("access_level = ?")
            values.append(access_level)
        if username is not None:
            modifiedFields.append("username = ?")
            values.append(username)

        if not modifiedFields:
            print("No fields were modified.")
            return member_id 

        values.append(member_id)
        query = f"UPDATE member SET {', '.join(modifiedFields)} WHERE member_id = ?"

        try:
            self.cur.execute(query, values)
            if self.cur.rowcount == 0:
                print("No rows affected.")
                return member_id
            self.conn.commit()
            print("Successfully updated member!")
            return member_id
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return None

    # Returns `id` on successful update
    # Returns None on update failure
    # Commits change
    def update_organization(self, organization_id, organization_name):
        try:
            self.cur.execute(
                """UPDATE organization SET organization_name = ? WHERE organization id = ?""",
                (organization_name, organization_id),
            )
            if self.cur.rowcount == 0:
                print("Update failed: No rows affected.")
                return None
            self.conn.commit()
            print(f"Organization name successfully updated to {organization_name}")
            return organization_id
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return None

    # Returns `id` on successful update
    # Returns None on update failure
    # Commits change
    def update_membership(
        self, member_id, organization_id, status=None, role=None, committee=None
    ):
        modifiedFields = []
        values = []
        if status is not None:
            modifiedFields.append("status = ?")
            values.append(status)
        if role is not None:
            modifiedFields.append("role = ?")
            values.append(role)
        if committee is not None:
            modifiedFields.append("committee = ?")
            values.append(committee)
        if not modifiedFields:
            print("No fields were modified")
            return
        values.append(member_id, organization_id)
        query = f"UPDATE organization SET {', '.join(modifiedFields)} WHERE member_id = ? AND organization_id = ?"
        try:
            self.cur.execute(query, values)
            if self.cur.rowcount == 0:
                print("Update failed: No rows affected.")
                return None
            self.conn.commit()
            print("Successfully updated membership!")
            return member_id
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return None

    # Returns `id` on successful update
    # Returns None on update failure
    # Commits change
    def update_financial_record(self, record_id, balance=None):
        if balance is None:
            print("No fields were modified")
            return record_id
        try:
            self.cur.execute(
                """UPDATE financial_record SET balance = ? WHERE record_id = ?""",
                (balance, record_id),
            )
            if self.cur.rowcount == 0:
                print("Update failed: No rows affected.")
                return None
            self.conn.commit()
            print("Successfully updated record!")
            return record_id
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return None

    # Returns `id` on successful update
    # Returns None on update failure
    # Commits change
    def update_fee(self, fee_id, payment_status, pay_date):
        try:
            self.cur.execute(
                """UPDATE fee SET payment_status = ? AND pay_date = ? WHERE fee_id = ?""",
                (payment_status, pay_date, fee_id),
            )
            if self.cur.rowcount == 0:
                print("Update failed: No rows affected.")
                return None
            self.conn.commit()
            print("Successfully updated fee!")
            return fee_id
        except mariadb.Error as e:
            print(f"Error occurred: {e}")

#############################################################################################################################
    def get_executives_by_year(self, organization_id=None, academic_year=None):
        try:
            query = """
                SELECT m.member_id, m.name, o.organization_name, mo.role, mo.committee, mo.academic_year
                FROM member m
                JOIN member_org mo ON m.member_id = mo.member_id
                JOIN organization o ON mo.organization_id = o.organization_id
                WHERE mo.committee = "Executive"
            """

            params = []

            if organization_id is not None:
                query += " AND o.organization_id = ?"
                params.append(organization_id)

            if academic_year is not None:
                query += " AND mo.academic_year = ?"
                params.append(academic_year)

            self.cur.execute(query, params)
            result = self.cur.fetchall()

            if result is None:
                return []

            return result

        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []
    # History of all the roles within the org?
    def get_role_history(self, role, organization_id = None):
        try:
            query = """
                SELECT
                    m.member_id, m.name, o.organization_name, mo.role, mo.committee, mo.academic_year, mo.semester
                FROM member m
                JOIN member_org mo ON m.member_id = mo.member_id
                JOIN organization o ON mo.organization_id = o.organization_id
                WHERE mo.role = ?
            """
            params = []
            params.append(role)

            if organization_id is not None:
                query += " AND o.organization_id = ?"
                params.append(organization_id)

            query += " ORDER BY mo.academic_year DESC;"

            self.cur.execute(query, tuple(params))
            result = self.cur.fetchall()

            if result is None:
                print("get_role_history: None returned")
                return []

            return result

        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []



    def get_all_late_payments(self, organization_id=None, academic_year=None, semester=None):
        try:
            query = """
                SELECT m.name, f.*
                FROM
                    fee f
                JOIN
                    financial_record fr ON f.record_id = fr.record_id
                JOIN
                    organization org ON fr.organization_id = org.organization_id
                JOIN
                    member_org mo ON org.organization_id = mo.organization_id
                JOIN
                    member m ON mo.member_id = m.member_id
                WHERE
                    f.pay_date > f.due_date
                AND
                    f.payment_status = 'paid'
            """

            params = []

            if organization_id is not None:
                query += " AND org.organization_id = ?"
                params.append(organization_id)

            if academic_year is not None:
                query += " AND fr.academic_year = ?"
                params.append(academic_year)

            if semester is not None:
                query += " AND fr.semester = ?"
                params.append(semester)

            self.cur.execute(query, tuple(params))
            result = self.cur.fetchall()

            if result is None:
                print("get_all_late_payments: None returned")
                return []

            return result

        except mariadb.Error as e:
            print(f"Error has occurred: {e}")
            return []


    def get_organization_active_proportion(self, organization_id, limit):
        try:
            self.cur.execute(
                """
                SELECT
                    org.organization_name,
                    mo.academic_year,
                    mo.semester,
                    SUM(CASE WHEN mo.status = 'Active' THEN 1 ELSE 0 END) / COUNT(*) * 100 AS active_percentage,
                    SUM(CASE WHEN mo.status = 'Inactive' THEN 1 ELSE 0 END) / COUNT(*) * 100 AS inactive_percentage
                FROM
                    member_org mo
                JOIN
                    organization org ON mo.organization_id = org.organization_id
                WHERE
                    org.organization_id = ?
                GROUP BY
                    mo.academic_year,
                    mo.semester
                ORDER BY
                    mo.academic_year DESC,
                    mo.semester DESC
                LIMIT ?;
            """,
                (organization_id, int(limit)),
            )
            
            result = self.cur.fetchall()

            if result is None:
                print("get_organization_active_proportion: None returned")
                return []

            return result
        
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []

    def get_alumni_by_date(self, organization_id, given_date):
        try:
            self.cur.execute(
                """

                    SELECT mem.* FROM
                        member_org mo
                    JOIN
                        member mem ON mo.member_id = mem.member_id
                    JOIN
                        organization org ON mo.organization_id = org.organization_id
                    WHERE
                        mo.academic_year =
                            CASE
                            WHEN
                                MONTH(?) BETWEEN 6 AND 12
                            THEN
                                CONCAT(YEAR(?), "-", YEAR(?) + 1)
                            WHEN
                                MONTH(?) BETWEEN 1 AND 5
                            THEN
                                CONCAT(YEAR(?) - 1, "-", YEAR(?))
                            END
                    AND
                        mo.semester =
                            CASE
                            WHEN
                                MONTH(?) BETWEEN 6 AND 12
                            THEN
                                1
                            WHEN
                                MONTH(?) BETWEEN 1 AND 5
                            THEN
                                2
                            END
                    AND
                        org.organization_id = ?
                    AND
                        mo.status = 'Alumni';
                            """,
                (
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    organization_id,
                ),
            )

            result = self.cur.fetchall()

            if result is None:
                print("get_alumni_by_date: None returned")
                return []

            return result
        
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []

    def get_fees_as_of_date(self, organization_id, given_date):
        try:
            (
                self.cur.execute(
                    """

                    SELECT
                        org.organization_name,
                        SUM(CASE WHEN f.payment_status = 'paid' THEN f.amount ELSE 0 END) AS paid_fees,
                        SUM(CASE WHEN f.payment_status = 'unpaid' THEN f.amount ELSE 0 END) AS unpaid_fees
                    FROM
                        fee f
                    JOIN
                        financial_record fr ON f.record_id = fr.record_id
                    JOIN
                        organization org ON fr.organization_id = org.organization_id
                    JOIN
                        member_org mo ON org.organization_id = mo.organization_id
                    WHERE
                        mo.academic_year =
                            CASE
                            WHEN
                                MONTH(?) BETWEEN 6 AND 12
                            THEN
                                CONCAT(YEAR(?), "-", YEAR(?) + 1)
                            WHEN
                                MONTH(?) BETWEEN 1 AND 5
                            THEN
                                CONCAT(YEAR(?) - 1, "-", YEAR(?))
                            END
                    AND
                        mo.semester =
                            CASE
                            WHEN
                                MONTH(?) BETWEEN 6 AND 12
                            THEN
                                1
                            WHEN
                                MONTH(?) BETWEEN 1 AND 5
                            THEN
                                2
                            END
                    AND
                        org.organization_id = ?;
                            """,
                    (
                        given_date,
                        given_date,
                        given_date,
                        given_date,
                        given_date,
                        given_date,
                        organization_id,
                    ),
                ),
            )

            result = self.cur.fetchall()

            if result is None:
                print("get_alumni_by_date: None returned")
                return []

            return result
        
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []

    def get_highest_debt_as_of_date(self, organization_id, semester, academic_year):
        try:
            (
                self.cur.execute(
                    """
            SELECT 
                debt1.name1, 
                debt1.debt 
            FROM
                (SELECT 
                    m.member_id, m.name AS name1, SUM(f.amount) AS debt
                FROM 
                    member m
                JOIN 
                    member_org mo ON m.member_id = mo.member_id
                JOIN
                    organization o ON mo.organization_id = o.organization_id
                JOIN
                    financial_record fr ON o.organization_id = fr.organization_id
                JOIN 
                    fee f ON fr.record_id = f.record_id
                WHERE
                    f.payment_status = 'Unpaid'
                AND
                    o.organization_id = ?
                AND
                    mo.semester = ?
                AND
                    mo.academic_year = ?
                GROUP BY
                    m.member_id) AS debt1
            WHERE
                debt = (SELECT MAX(debt) FROM (SELECT SUM(f.amount) AS debt
                    FROM 
                            member m
                    JOIN 
                            member_org mo ON m.member_id = mo.member_id
                    JOIN
                            organization o ON mo.organization_id = o.organization_id
                    JOIN
                            financial_record fr ON o.organization_id = fr.organization_id
                    JOIN 
                            fee f ON fr.record_id = f.record_id
                    WHERE
                            f.payment_status = 'Unpaid'
                        AND
                            o.organization_id = ?
                        AND
                            mo.semester = ?
                        AND
                            mo.academic_year = ?
                    GROUP BY
                            m.member_id) 
                    AS debt2);
                    """,
                    (organization_id, semester, academic_year, organization_id, semester, academic_year),
                ),
            )

            result = self.cur.fetchall()

            if result is None:
                print("get_alumni_by_date: None returned")
                return []

            return result
        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            return []
        
    # Returns success as boolean
    def delete_member(self, member_id):
        try:
            self.cur.execute("DELETE FROM fee WHERE member_id = ?", (member_id,))
            self.cur.execute("DELETE FROM member_org WHERE member_id = ?", (member_id,))
            self.cur.execute("DELETE FROM member WHERE member_id = ?", (member_id,))

            if self.cur.rowcount == 0:
                print("No member was deleted.")
                self.conn.rollback()
                return False

            self.conn.commit()
            print(f"Deleted member {member_id} successfully.")
            return True

        except mariadb.Error as e:
            print(f"Error occurred: {e}")
            self.conn.rollback()
            return False
        
