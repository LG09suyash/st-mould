import sqlite3
import pandas as pd
import streamlit as st
import altair as alt


def main():
    #st.title("Injection Moulding Maintenance Management Web App")

    # Navigation sidebar
    menu = st.sidebar.selectbox("Menu", ['Home', 'Machine Management', 'Task Management', 'Scheduling', 'Reporting','User Guide'])

    if menu == 'Home':
        home_page()

    elif menu == 'Machine Management':
        machine_management()

    elif menu == 'Task Management':
        task_management()

    elif menu == 'Scheduling':
        schedule_management()

    elif menu == 'Reporting':
        reporting()
    
    elif menu == "User Guide":  # Add this block
        user_guide()

#Home page
def home_page():
    st.title("Injection Moulding Maintenance Management")
    # st.image("https://source.unsplash.com/featured/?injection,moulding", use_column_width=True)

    # Fetch KPI data
    # total_machines, total_tasks, total_schedules = fetch_kpi_data(conn)

    # # Display KPIs
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.header("Total Machines")
    #     st.subheader(total_machines)
    # with col2:
    #     st.header("Total Tasks")
    #     st.subheader(total_tasks)
    # with col3:
    #     st.header("Total Schedules")
    #     st.subheader(total_schedules)

    st.write("""
    Welcome to the Injection Moulding Maintenance Management Web App!

    This app is designed to help injection moulding companies manage their machines, tasks, schedules, and reporting with ease.

    Use the menu on the left to navigate through the app's features:
    - Machine Management: Add, update, and delete machine information.
    - Task Management: Add, update, and delete tasks related to machine maintenance.
    - Scheduling: Add, update, and delete schedules for tasks.
    - Reporting: View reports and visualizations related to machine maintenance.
    - User Guide: Learn how to use the app's features.

    If you have any questions or need assistance, please refer to the User Guide or contact our support team at support@example.com.
    """)


def fetch_kpi_data(conn):
    # Total machines
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM machines")
    total_machines = cur.fetchone()[0]

    # Total tasks
    cur.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cur.fetchone()[0]

    # Total schedules
    cur.execute("SELECT COUNT(*) FROM schedules")
    total_schedules = cur.fetchone()[0]

    return total_machines, total_tasks, total_schedules


#user guide

def user_guide():
    st.title("User Guide")

    st.header("Machine Management")
    st.write("""
    In this section, you can manage machines by adding, updating, and deleting machine information.
    - To add a new machine, fill in the Machine ID, Name, Location, and Status, then click the "Add Machine" button.
    - To update a machine's information, select the Machine ID from the dropdown, modify the information, and click the "Update Machine" button.
    - To delete a machine, select the Machine ID from the dropdown and click the "Delete Machine" button.
    """)

    st.header("Task Management")
    st.write("""
    In this section, you can manage tasks by adding, updating, and deleting task information.
    - To add a new task, fill in the Task ID, Machine ID, Description, Technician, Due Date, and Status, then click the "Add Task" button.
    - To update a task's information, select the Task ID from the dropdown, modify the information, and click the "Update Task" button.
    - To delete a task, select the Task ID from the dropdown and click the "Delete Task" button.
    """)

    st.header("Scheduling")
    st.write("""
    In this section, you can manage schedules by adding, updating, and deleting schedule information.
    - To add a new schedule, fill in the Schedule ID, Task ID, Start Time, and End Time, then click the "Add Schedule" button.
    - To update a schedule's information, select the Schedule ID from the dropdown, modify the information, and click the "Update Schedule" button.
    - To delete a schedule, select the Schedule ID from the dropdown and click the "Delete Schedule" button.
    """)

    st.header("Reporting")
    st.write("""
    In this section, you can view various reports and visualizations related to machines, tasks, and schedules.
    - Select a report type from the dropdown to view the corresponding report or visualization.
    """)

    st.header("Support")
    st.write("""
    If you need assistance or encounter any issues, please contact our support team at support@example.com.
    """)


        
# Database connection and setup
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS machines
                      (machine_id TEXT PRIMARY KEY, machine_name TEXT, location TEXT, status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                      (task_id TEXT PRIMARY KEY, machine_id TEXT, description TEXT, technician TEXT, due_date TEXT, status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedules
                      (schedule_id TEXT PRIMARY KEY, task_id TEXT, start_time TEXT, end_time TEXT)''')
    conn.commit()


# machine management crud

def insert_machine(conn, machine):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO machines(machine_id, machine_name, location, status)
                      VALUES(?, ?, ?, ?)''', machine)
    conn.commit()

def update_machine(conn, machine):
    cursor = conn.cursor()
    cursor.execute('''UPDATE machines SET machine_name = ?, location = ?, status = ? WHERE machine_id = ?''',
                   (machine[1], machine[2], machine[3], machine[0]))
    conn.commit()

def delete_machine(conn, machine_id):
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM machines WHERE machine_id = ?''', (machine_id,))
    conn.commit()

def list_machines(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM machines''')
    machines = cursor.fetchall()
    return machines

# task management crud 

def insert_task(conn, task):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tasks(task_id, machine_id, description, technician, due_date, status)
                      VALUES(?, ?, ?, ?, ?, ?)''', task)
    conn.commit()

def update_task(conn, task):
    cursor = conn.cursor()
    cursor.execute('''UPDATE tasks SET machine_id = ?, description = ?, technician = ?, due_date = ?, status = ? WHERE task_id = ?''',
                   (task[1], task[2], task[3], task[4], task[5], task[0]))
    conn.commit()

def delete_task(conn, task_id):
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM tasks WHERE task_id = ?''', (task_id,))
    conn.commit()

def list_tasks(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM tasks''')
    tasks = cursor.fetchall()
    return tasks

def get_task_status_index(status):
    if status == "Pending":
        return 0
    elif status == "In Progress":
        return 1
    elif status == "Completed":
        return 2
    else:
        return 3

# schedule management crud

def insert_schedule(conn, schedule):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO schedules(schedule_id, task_id, start_time, end_time)
                      VALUES(?, ?, ?, ?)''', schedule)
    conn.commit()

def delete_schedule(conn, schedule_id):
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM schedules WHERE schedule_id = ?''', (schedule_id,))
    conn.commit()

def list_schedules(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM schedules''')
    schedules = cursor.fetchall()
    return schedules

#reporting handler functions

def machine_status_summary(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT status, COUNT(*) FROM machines GROUP BY status''')
    result = cursor.fetchall()
    return result

def task_status_summary(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT status, COUNT(*) FROM tasks GROUP BY status''')
    result = cursor.fetchall()
    return result

def maintenance_tasks_by_machine(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT machine_id, COUNT(*) FROM tasks GROUP BY machine_id''')
    result = cursor.fetchall()
    return result

def tasks_by_technician(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT technician, COUNT(*) FROM tasks GROUP BY technician''')
    result = cursor.fetchall()
    return result

def overdue_tasks(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM tasks WHERE status = "Overdue"''')
    result = cursor.fetchall()
    return result

def completed_tasks_by_date_range(conn, start_date, end_date):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM tasks WHERE status = "Completed" AND due_date BETWEEN ? AND ?''', (start_date, end_date))
    result = cursor.fetchall()
    return result

def machine_utilization(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT machine_id, status, COUNT(*) FROM tasks WHERE status IN ("Pending", "In Progress", "Completed") GROUP BY machine_id, status''')
    result = cursor.fetchall()
    return result

conn = create_connection("demo_data.sqlite3")
create_tables(conn)

# Complete machine management feature
def add_machine():
    st.subheader("Add Machine")
    machine_id = st.text_input("Machine ID")
    machine_name = st.text_input("Machine Name")
    location = st.text_input("Location")
    status = st.selectbox("Status", ["Operational", "Under Maintenance", "Out of Service"])

    if st.button("Add"):
        machine = (machine_id, machine_name, location, status)
        insert_machine(conn, machine)
        st.success(f"Machine {machine_name} added successfully!")

def edit_machine():
    st.subheader("Edit Machine")
    machine_id = st.text_input("Machine ID to Edit")
    if st.button("Load"):
        machines = list_machines(conn)
        for machine in machines:
            if machine_id == machine[0]:
                machine_name = st.text_input("Machine Name", machine[1])
                location = st.text_input("Location", machine[2])
                status = st.selectbox("Status", ["Operational", "Under Maintenance", "Out of Service"], index=get_status_index(machine[3]))
                if st.button("Save Changes"):
                    updated_machine = (machine_id, machine_name, location, status)
                    update_machine(conn, updated_machine)
                    st.success(f"Machine {machine_name} updated successfully!")
                break
        else:
            st.warning("Machine not found. Please enter a valid Machine ID.")

def get_status_index(status):
    if status == "Operational":
        return 0
    elif status == "Under Maintenance":
        return 1
    else:
        return 2

def delete_machine_ui():
    st.subheader("Delete Machine")
    machine_id = st.text_input("Machine ID to Delete")
    if st.button("Delete"):
        delete_machine(conn, machine_id)
        st.success(f"Machine {machine_id} deleted successfully!")

def list_machines_ui():
    st.subheader("List Machines")
    machines = list_machines(conn)
    machines_df = pd.DataFrame(machines, columns=['Machine ID', 'Machine Name', 'Location', 'Status'])
    st.dataframe(machines_df)

def machine_management():
    st.subheader("Machine Management")
    machine_action = st.selectbox("Action", ['Add Machine', 'Edit Machine', 'Delete Machine', 'List Machines'])
    if machine_action == 'Add Machine':
        add_machine()

    elif machine_action == 'Edit Machine':
        edit_machine()

    elif machine_action == 'Delete Machine':
        delete_machine_ui()

    elif machine_action == 'List Machines':
        list_machines_ui()

# Task management feature
# User interface functions

def add_task():
    st.subheader("Add Task")
    task_id = st.text_input("Task ID")
    machine_id = st.text_input("Machine ID")
    description = st.text_area("Task Description")
    technician = st.text_input("Assigned Technician")
    due_date = st.date_input("Due Date")
    status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "Overdue"])

    if st.button("Add"):
        task = (task_id, machine_id, description, technician, due_date.strftime("%Y-%m-%d"), status)
        insert_task(conn, task)
        st.success(f"Task {task_id} added successfully!")

def edit_task():
    st.subheader("Edit Task")
    task_id = st.text_input("Task ID to Edit")
    if st.button("Load"):
        tasks = list_tasks(conn)
        for task in tasks:
            if task_id == task[0]:
                machine_id = st.text_input("Machine ID", task[1])
                description = st.text_area("Task Description", task[2])
                technician = st.text_input("Assigned Technician", task[3])
                due_date = st.date_input("Due Date", pd.to_datetime(task[4]))
                status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "Overdue"], index=get_task_status_index(task[5]))
                if st.button("Save Changes"):
                    updated_task = (task_id, machine_id, description, technician, due_date.strftime("%Y-%m-%d"), status)
                    update_task(conn, updated_task)
                    st.success(f"Task {task_id} updated successfully!")
                break
        else:
            st.warning("Task not found. Please enter a valid Task ID.")

def delete_task_ui():
    st.subheader("Delete Task")
    task_id = st.text_input("Task ID to Delete")
    if st.button("Delete"):
        delete_task(conn, task_id)
        st.success(f"Task {task_id} deleted successfully!")

def list_tasks_ui():
    st.subheader("List Tasks")
    tasks = list_tasks(conn)
    if len(tasks) > 0:
        tasks_df = pd.DataFrame(tasks, columns=['Task ID', 'Machine ID', 'Description', 'Technician', 'Due Date', 'Status'])
        st.dataframe(tasks_df)
    else:
        st.warning("No tasks found.")

def task_management():
    st.subheader("Task Management")
    task_action = st.selectbox("Action", ['Add Task', 'Edit Task', 'Delete Task', 'List Tasks'])

    if task_action == 'Add Task':
        add_task()

    elif task_action == 'Edit Task':
        edit_task()

    elif task_action == 'Delete Task':
        delete_task_ui()

    elif task_action == 'List Tasks':
        list_tasks_ui()


# schedule management
def add_schedule():
    st.subheader("Add Schedule")
    schedule_id = st.text_input("Schedule ID")
    task_id = st.text_input("Task ID")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")

    if st.button("Add"):
        schedule = (schedule_id, task_id, start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"))
        insert_schedule(conn, schedule)
        st.success(f"Schedule {schedule_id} added successfully!")

def delete_schedule_ui():
    st.subheader("Delete Schedule")
    schedule_id = st.text_input("Schedule ID to Delete")
    if st.button("Delete"):
        delete_schedule(conn, schedule_id)
        st.success(f"Schedule {schedule_id} deleted successfully!")

def list_schedules_ui():
    st.subheader("List Schedules")
    schedules = list_schedules(conn)
    schedules_df = pd.DataFrame(schedules, columns=['Schedule ID', 'Task ID', 'Start Time', 'End Time'])
    st.dataframe(schedules_df)

def schedule_management():
    st.subheader("Schedule Management")
    schedule_action = st.selectbox("Action", ['Add Schedule', 'Delete Schedule', 'List Schedules'])

    if schedule_action == 'Add Schedule':
        add_schedule()

    elif schedule_action == 'Delete Schedule':
        delete_schedule_ui()

    elif schedule_action == 'List Schedules':
        list_schedules_ui()


# reporting feature

def display_pie_chart(data, title):
    chart_data = pd.DataFrame(data, columns=["Category", "Count"])
    chart = alt.Chart(chart_data).mark_bar().encode(
        alt.X("Category"),
        alt.Y("Count"),
        tooltip=["Category", "Count"],
        color="Category"
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)

def reporting():
    st.subheader("Reporting")
    report_type = st.selectbox("Report Type", ["Machine Status Summary", "Task Status Summary", "Maintenance Tasks by Machine",
                                               "Tasks by Technician", "Overdue Tasks", "Completed Tasks by Date Range", "Machine Utilization"])

    if report_type == "Machine Status Summary":
        data = machine_status_summary(conn)
        display_pie_chart(data, "Machine Status Summary")

    elif report_type == "Task Status Summary":
        data = task_status_summary(conn)
        display_pie_chart(data, "Task Status Summary")

    elif report_type == "Maintenance Tasks by Machine":
        data = maintenance_tasks_by_machine(conn)
        display_pie_chart(data, "Maintenance Tasks by Machine")

    elif report_type == "Tasks by Technician":
        data = tasks_by_technician(conn)
        display_pie_chart(data, "Tasks by Technician")

    elif report_type == "Overdue Tasks":
        data = overdue_tasks(conn)
        tasks_df = pd.DataFrame(data, columns=['Task ID', 'Machine ID', 'Description', 'Technician', 'Due Date', 'Status'])
        st.dataframe(tasks_df)

    elif report_type == "Completed Tasks by Date Range":
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        if st.button("Show"):
            data = completed_tasks_by_date_range(conn, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            tasks_df = pd.DataFrame(data, columns=['Task ID', 'Machine ID', 'Description', 'Technician', 'Due Date', 'Status'])
            st.dataframe(tasks_df)
    
    elif report_type == "Machine Utilization":
        data = machine_utilization(conn)
        utilization_df = pd.DataFrame(data, columns=['Machine ID', 'Status', 'Count'])
        chart = alt.Chart(utilization_df).mark_bar().encode(
            alt.X("Machine ID"),
            alt.Y("Count"),
            tooltip=["Machine ID", "Status", "Count"],
            color="Status"
        ).properties(title="Machine Utilization")
        st.altair_chart(chart, use_container_width=True)



if __name__ == "__main__":
    main()