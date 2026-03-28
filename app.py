from flask import Flask, render_template,request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ss@20",
    database="hrms_db"
)

cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/testdb")
def testdb():
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    return f"Connected to {result}"

@app.route("/employee")
def employee():
    return render_template("employee.html")

@app.route("/add_employee", methods=["POST"])
def add_employee():
    emp_name = request.form["emp_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    department = request.form["department"]
    designation = request.form["designation"]
    salary = request.form["salary"]

    query = """
    INSERT INTO employees 
    (emp_name, email, phone, department, designation, salary)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (emp_name, email, phone, department, designation, salary)

    cursor.execute(query, values)
    db.commit()

    return "Employee Added Successfully"

@app.route("/view_employees")
def view_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template("view_employees.html", employees=employees)

@app.route("/delete_employee/<int:id>")
def delete_employee(id):
    query = "DELETE FROM employees WHERE emp_id = %s"
    cursor.execute(query, (id,))
    db.commit()

    return "Employee Deleted Successfully"

@app.route("/edit_employee/<int:id>")
def edit_employee(id):
    query = "SELECT * FROM employees WHERE emp_id = %s"
    cursor.execute(query, (id,))
    emp = cursor.fetchone()

    return render_template("update_employee.html", emp=emp)


@app.route("/update_employee/<int:id>", methods=["POST"])
def update_employee(id):
    emp_name = request.form["emp_name"]
    email = request.form["email"]
    phone = request.form["phone"]

    query = """
    UPDATE employees
    SET emp_name=%s, email=%s, phone=%s
    WHERE emp_id=%s
    """

    values = (emp_name, email, phone, id)

    cursor.execute(query, values)
    db.commit()

    return "Employee Updated Successfully"



@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/add_attendance", methods=["POST"])
def add_attendance():
    emp_id = request.form["emp_id"]
    emp_name = request.form["emp_name"]
    attendance_date = request.form["attendance_date"]
    clock_in = request.form["clock_in"]
    clock_out = request.form["clock_out"]
    status = request.form["status"]

    query = """
    INSERT INTO attendance
    (emp_id, emp_name, attendance_date, clock_in, clock_out, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        emp_id,
        emp_name,
        attendance_date,
        clock_in,
        clock_out,
        status
    )

    cursor.execute(query, values)
    db.commit()

    return "Attendance Added Successfully"

@app.route("/leave")
def leave():
    return render_template("leave.html")

@app.route("/apply_leave", methods=["POST"])
def apply_leave():
    emp_id = request.form["emp_id"]
    emp_name = request.form["emp_name"]
    leave_type = request.form["leave_type"]
    from_date = request.form["from_date"]
    to_date = request.form["to_date"]
    reason = request.form["reason"]

    query = """
    INSERT INTO leaves
    (emp_id, emp_name, leave_type, from_date, to_date, reason, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        emp_id,
        emp_name,
        leave_type,
        from_date,
        to_date,
        reason,
        "Pending"
    )

    cursor.execute(query, values)
    db.commit()

    return "Leave Applied Successfully"

@app.route("/view_leaves")
def view_leaves():
    cursor.execute("SELECT * FROM leaves")
    leave_data = cursor.fetchall()

    return render_template("view_leaves.html", leaves=leave_data)

@app.route("/approve_leave/<int:id>")
def approve_leave(id):
    query = "UPDATE leaves SET status = %s WHERE leave_id = %s"
    cursor.execute(query, ("Approved", id))
    db.commit()

    return "Leave Approved Successfully"

@app.route("/reject_leave/<int:id>")
def reject_leave(id):
    query = "UPDATE leaves SET status = %s WHERE leave_id = %s"
    cursor.execute(query, ("Rejected", id))
    db.commit()

    return "Leave Rejected Successfully"

@app.route("/payroll")
def payroll():
    return render_template("payroll.html")

@app.route("/add_payroll", methods=["POST"])
def add_payroll():
    emp_id = request.form["emp_id"]
    emp_name = request.form["emp_name"]
    basic_salary = float(request.form["basic_salary"])
    tax = float(request.form["tax"])
    bonus = float(request.form["bonus"])
    month = request.form["month"]

    net_salary = basic_salary + bonus - tax

    query = """
    INSERT INTO payroll
    (emp_id, emp_name, basic_salary, tax, bonus, net_salary, month)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        emp_id,
        emp_name,
        basic_salary,
        tax,
        bonus,
        net_salary,
        month
    )

    cursor.execute(query, values)
    db.commit()

    return f"Payroll Generated Successfully. Net Salary = {net_salary}"

@app.route("/dashboard")
def dashboard():
    # total employees
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    # total leaves
    cursor.execute("SELECT COUNT(*) FROM leaves")
    total_leaves = cursor.fetchone()[0]

    # total attendance
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    # total payroll
    cursor.execute("SELECT COUNT(*) FROM payroll")
    total_payroll = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        total_leaves=total_leaves,
        total_attendance=total_attendance,
        total_payroll=total_payroll
    )


if __name__ == "__main__":
    app.run(debug=True)