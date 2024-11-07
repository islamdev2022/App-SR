from customtkinter import *
from tkinter import Canvas, Scrollbar
from PIL import Image
from mysql.connector import Error
from tkinter import messagebox

# test_db.py
from db_connection import create_connection

# Get the connection
connection = create_connection()

# Login verification function
def login():
    connection = create_connection()
    if not connection:
        messagebox.showerror("Database Error", "Unable to connect to the database.")
        return

    username = username_entry.get()
    password = password_entry.get()

    # Verify credentials
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", "Welcome, " + username + "!")
            open_admin_window()  # Call function to open new window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except Error as e:
        print(f"Error: '{e}' occurred during login")
    finally:
        cursor.close()
        connection.close()



def open_admin_window():
    app.destroy()  # Close the login window

    main_window = CTk()
    # Get the screen width and height
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Set the window size to fill the screen
    main_window.geometry(f"{screen_width}x{screen_height}")
    main_window.title("Main Application")
    
    # # Create a canvas and a scrollbar
    # canvas = Canvas(main_window)
    # scrollbar = Scrollbar(main_window, orient="vertical", command=canvas.yview)
    # scrollable_frame = CTkFrame(canvas)

    # scrollable_frame.bind(
    #     "<Configure>",
    #     lambda e: canvas.configure(
    #         scrollregion=canvas.bbox("all")
    #     )
    # )

    # canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # canvas.configure(yscrollcommand=scrollbar.set)

    # # Pack the canvas and scrollbar
    # canvas.pack(side="left", fill="both", expand=True)
    # scrollbar.pack(side="right", fill="y")

    CTkLabel(master=main_window, text="Welcome to the Admin Dashboard!", font=("Arial Bold", 24)).pack(pady=10)

   




    # Filter Section: ComboBoxes for Role and Team, and Search Entry
    filter_frame = CTkFrame(master=main_window)
    filter_frame.pack(pady=10)

    roles = ["All", "Head", "Member"]
    teams = ["All", "Design", "Marketing", "Development", "Data Analysis"]
    
    role_filter = CTkComboBox(master=filter_frame, values=roles, width=100)
    role_filter.set("All")
    role_filter.pack(side="left", padx=5)
    
    team_filter = CTkComboBox(master=filter_frame, values=teams, width=100)
    team_filter.set("All")
    team_filter.pack(side="left", padx=5)

    search_entry = CTkEntry(master=filter_frame, width=200, placeholder_text="Search by username or name")
    search_entry.pack(side="left", padx=5)

    # Input fields for adding a new user
     # Table to display users
    table_frame = CTkFrame(master=main_window)
    table_frame.pack(fill="both", expand=True, pady=10)
    def display_users():
    # Clear existing user details
        for widget in table_frame.winfo_children():
            widget.destroy()

    # Establish database connection
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
    
        try:
            cursor = connection.cursor()
    
            # Build the query based on filters
            query = "SELECT username, first_name, last_name, password, role, team FROM users WHERE 1=1"
            filters = []
    
            # Apply role filter
            selected_role = role_filter.get()
            if selected_role != "All":
                query += " AND role = %s"
                filters.append(selected_role)
    
            # Apply team filter
            selected_team = team_filter.get()
            if selected_team != "All":
                query += " AND team = %s"
                filters.append(selected_team)
    
            # Apply search filter
            search_text = search_entry.get()
            if search_text:
                query += " AND (username LIKE %s OR first_name LIKE %s OR last_name LIKE %s)"
                filters.extend([f"%{search_text}%"] * 3)
    
            # Execute the query with the filters
            cursor.execute(query, tuple(filters))
            users = cursor.fetchall()
    
            # Display headers in the table
            headers = ["Username", "First Name", "Last Name", "Password", "Role", "Team"]
            for col, header in enumerate(headers):
                header_label = CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
    
            # Display user data in the table
            for row, user in enumerate(users, start=1):
                for col, detail in enumerate(user):
                    detail_label = CTkLabel(table_frame, text=detail)
                    detail_label.grid(row=row, column=col, padx=5, pady=5, sticky="w")
    
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
        
         # Table to display users
         # Bind filter and search actions to refresh the table
    role_filter.bind("<<ComboboxSelected>>", lambda e: display_users())
    team_filter.bind("<<ComboboxSelected>>", lambda e: display_users())
    search_entry.bind("<KeyRelease>", lambda e: display_users())



    def add_user_section():
        userName = CTkEntry(master=main_window, width=200, placeholder_text="Enter username")
        userName.pack(pady=5)

        firstName = CTkEntry(master=main_window, width=200, placeholder_text="Enter first name")
        firstName.pack(pady=5)

        lastName = CTkEntry(master=main_window, width=200, placeholder_text="Enter last name")
        lastName.pack(pady=5)

        password = CTkEntry(master=main_window, width=200, placeholder_text="Enter user account password")
        password.pack(pady=5)

        team_combo = CTkComboBox(master=main_window, values=teams[1:], width=200)  # Exclude "All" from team options
        team_combo.pack(pady=5)

        is_head_var = BooleanVar()
        head_checkbox = CTkCheckBox(master=main_window, text="Mark as Team Head", variable=is_head_var)
        head_checkbox.pack(pady=5)

        # Button to add a new user
        
        def create_user():
            username = userName.get()
            first_name = firstName.get()
            last_name = lastName.get()
            user_password = password.get()
            role = "Head" if is_head_var.get() else "Member"
            team = team_combo.get()

            if not username or not first_name or not last_name or not user_password or not team:
                messagebox.showwarning("Input Error", "Please enter all required fields.")
                return

            connection = create_connection()
            if not connection:
                messagebox.showerror("Database Error", "Unable to connect to the database.")
                return

            try:
                cursor = connection.cursor()

                if role == "Head":
                    check_query = "SELECT * FROM users WHERE team = %s AND role = 'Head'"
                    cursor.execute(check_query, (team,))
                    if cursor.fetchone():
                        messagebox.showerror("Error", f"The {team} team already has a head.")
                        return

                query = "INSERT INTO users (username, password, first_name, last_name, role, team) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (username, user_password, first_name, last_name, role, team))
                connection.commit()
                messagebox.showinfo("Success", f"User '{username}' added successfully.")
                
            except Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()

        add_user_button = CTkButton(master=main_window, text="Add User", command=create_user)
        add_user_button.pack(pady=10)

    add_user_section()
    display_users()
    # --- Task Management Section ---
    def add_task_section():
        task_title = CTkEntry(master=main_window, width=200, placeholder_text="Enter task title")
        task_title.pack(pady=5)

        task_description = CTkEntry(master=main_window, width=200, placeholder_text="Enter task description")
        task_description.pack(pady=5)

        task_deadline = CTkEntry(master=main_window, width=200, placeholder_text="Enter task deadline (YYYY-MM-DD)")
        task_deadline.pack(pady=5)

        task_priority = CTkComboBox(master=main_window, values=["Low", "Medium", "High"], width=200)
        task_priority.set("Low")
        task_priority.pack(pady=5)

        task_team = CTkComboBox(master=main_window, values=teams[1:], width=200)
        task_team.set("Design")
        task_team.pack(pady=5)

        # Button to add a new task
        def create_task():
            title = task_title.get()
            description = task_description.get()
            deadline = task_deadline.get()
            priority = task_priority.get()
            team = task_team.get()

            if not title or not description or not deadline or not priority or not team:
                messagebox.showwarning("Input Error", "Please fill all task details.")
                return

            connection = create_connection()
            if not connection:
                messagebox.showerror("Database Error", "Unable to connect to the database.")
                return

            try:
                cursor = connection.cursor()
                query = "INSERT INTO tasks (title, description, deadline, priority, responsible_team) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (title, description, deadline, priority, team))
                connection.commit()
                messagebox.showinfo("Success", f"Task '{title}' added successfully.")
                display_tasks()
            except Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()

        add_task_button = CTkButton(master=main_window, text="Add Task", command=create_task)
        add_task_button.pack(pady=10)

    add_task_section()

    # Table to display tasks
    task_table_frame = CTkFrame(master=main_window)
    task_table_frame.pack(fill="both", expand=True, pady=10)

    def display_tasks():
        for widget in task_table_frame.winfo_children():
            widget.destroy()  # Clear existing task details

        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

        try:
            cursor = connection.cursor()

            # Build the query to fetch tasks
            cursor.execute("SELECT title, description, deadline, priority, responsible_team FROM tasks")
            tasks = cursor.fetchall()

            # Display headers for task table
            task_headers = ["Title", "Description", "Deadline", "Priority", "Responsible Team"]
            for col, header in enumerate(task_headers):
                header_label = CTkLabel(task_table_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

            # Display task data
            for row, task in enumerate(tasks, start=1):
                for col, detail in enumerate(task):
                    detail_label = CTkLabel(task_table_frame, text=detail)
                    detail_label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    # Initial display of tasks
    display_tasks()

    main_window.mainloop()


# Initialize login window
app = CTk()
app.geometry("600x480")
app.title("Login Interface")

side_img_data = Image.open("side-img.png")
user_icon_data = Image.open("icons8-user-64.png")
password_icon_data = Image.open("icons8-password-50.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
username_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(20,20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Welcome Back!", text_color="#E4080A", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Username:", text_color="#E4080A", anchor="w", justify="left", font=("Arial Bold", 14), image=username_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#E4080A", border_width=1, text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#E4080A", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#E4080A", border_width=1, text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

CTkButton(master=frame, text="Login", fg_color="#E4080A", hover_color="#A80102" , font=("Arial Bold", 12), text_color="#ffffff", width=225, command=login).pack(anchor="w", pady=(40, 0), padx=(25, 0))

app.mainloop()