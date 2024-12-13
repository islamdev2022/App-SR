from customtkinter import *
from PIL import Image
from mysql.connector import Error
from tkinter import messagebox,Toplevel , Canvas, Scrollbar,CENTER
from tkcalendar import Calendar
# test_db.py
from db_connection import create_connection

def add_action_to_history(uesrname,role,action):
    print(f"User {uesrname} with role {role} performed action {action}")
    connection = create_connection()
    if not connection:
        messagebox.showerror("Database Error", "Unable to connect to the database.")
        return
    try:
        cursor = connection.cursor()
        query = "INSERT INTO actions_history (username, role, action) VALUES (%s, %s, %s)"
        cursor.execute(query, (uesrname, role, action))
        print("Action added to history")
        connection.commit()
    except Error as e:
        print(f"Error: '{e}' occurred during adding action to history")
    finally:
        cursor.close()
        connection.close()

# Login verification function
def login():
    def login_fun():
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
                try:
                    cursor = connection.cursor()
                    query = "SELECT id,role,team FROM users WHERE username = %s"
                    cursor.execute(query, (username,))
                    id,role,team = cursor.fetchone()
                    print(role)
                    print(team)
                    if role == "Admin":
                        add_action_to_history(username,role,"Login")
                        open_admin_window(username,app)
                    elif role == "Head":
                        add_action_to_history(username,f"{role} {team}","Login")
                        open_head_window(username,role,team,app)
                    else: 
                        add_action_to_history(username,role,"Login")
                        open_member_window(username,team,app,id)
                except Error as e:
                    print(f"Error: '{e}' occurred during login with role")
                finally:
                    cursor.close()
                    connection.close()
    
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Error as e:
            print(f"Error: '{e}' occurred during login")
        finally:
            cursor.close()
            connection.close()
        # Initialize login window
    app = CTk()
    app.geometry("600x480")
    app.resizable(False, False)
    app.title("Login Page")
    
    # Center the window
    center_window(app, 600, 480)
    
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
    
    CTkButton(master=frame, text="Login", fg_color="#E4080A", hover_color="#A80102" , font=("Arial Bold", 12), text_color="#ffffff", width=225, command=lambda:login_fun()).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    
    app.mainloop()
    
def logout(username,role,current_window):
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        current_window.destroy()  # Destroy the main window
        add_action_to_history(username,role,"Logout")
        login()
    
def open_member_window(username,team,app,id):
    print("Member Window")
    app.destroy()  # Close the login window
    
    employe_window = CTk()
    screen_width = employe_window.winfo_screenwidth()
    screen_height = employe_window.winfo_screenheight()
    
    # Set the window size to fill the screen
    employe_window.geometry(f"{screen_width}x{screen_height}")
    employe_window.state("zoomed")
    employe_window.title("Employe Page")
    
    connection = create_connection()
    if not connection:
        messagebox.showerror("Database Error", "Unable to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        query = "SELECT first_name, last_name FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user
            CTkLabel(master=employe_window, text=f"Hello, {first_name} {last_name}!", font=("Arial Bold", 24)).pack(pady=10)
        else:
            CTkLabel(master=employe_window, text="User not found", font=("Arial Bold", 24)).pack(pady=10)
    except Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
    
    CTkLabel(master=employe_window, text=f"Welcome to the {team} Dashboard!", font=("Arial Bold", 24)).pack(pady=10)
    
    logout_button = CTkButton(master=employe_window, text="Logout", command=lambda:logout(username,f"member {team}",employe_window))
    logout_button.pack(pady=10)
    task_header = ["Title", "Description", "Deadline", "Status"]
    def fetch_task(team, employe_window):
        # Create table headers using pack
        header_frame = CTkFrame(employe_window)
        header_frame.pack(fill="x", padx=10, pady=10)

        for header in task_header:
            header_label = CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 16, "bold"),
                fg_color="#3b82f6",
                text_color="white",
                corner_radius=5,
                width=100
            )
            header_label.pack(side="left", padx=5)

        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

        try:
            cursor = connection.cursor()
            fullname = f"{first_name} {last_name}"
            query = "SELECT id, title, description, deadline, status FROM tasks WHERE responsible_team = %s AND responsible_member = %s"
            cursor.execute(query, (team, fullname))
            tasks = cursor.fetchall()

            if not tasks:
                CTkLabel(master=employe_window, text="No tasks available", font=("Arial", 12)).pack(pady=10)
            else:
                for task in tasks:
                    task_id, task_title, task_description, task_deadline, task_status = task
                    frame = CTkFrame(master=employe_window , height=80)
                    frame.pack(fill="x", pady=5, padx=10)

                    CTkLabel(frame, text=task_title,font=("Arial", 14),
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10).pack(side="left", padx=5)
                    CTkLabel(frame, text=task_description, font=("Arial", 14), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10 ).pack(side="left", padx=5)
                    CTkLabel(frame, text=task_deadline, font=("Arial", 14), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10 ).pack(side="left", padx=5)

                    status_combobox = CTkComboBox(
                        master=frame,
                        values=["Pending", "In Progress", "Completed"],
                        width=150
                    )
                    status_combobox.set(task_status)
                    status_combobox.pack(side="left", padx=5)
                    def update_status(task_id, combobox, title):
                        new_status = combobox.get()
                        connection = create_connection()
                        if not connection:
                            messagebox.showerror("Database Error", "Unable to connect to the database.")
                            return

                        try:
                            cursor = connection.cursor()
                            update_query = "UPDATE tasks SET status = %s WHERE id = %s"
                            cursor.execute(update_query, (new_status, task_id))
                            connection.commit()
                            messagebox.showinfo("Success", f"Task '{title}' status updated to '{new_status}'.")
                        except Error as e:
                            messagebox.showerror("Database Error", f"An error occurred: {e}")
                        finally:
                            if cursor:
                                cursor.close()
                            if connection:
                                connection.close()

                    update_button = CTkButton(
                        fg_color="#34d399", 
                    hover_color="#10b981", 
                    text_color="white", 
                    corner_radius=5,
                        master=frame,
                        text="Update Status",
                        command=lambda tid=task_id, cb=status_combobox, tt=task_title: update_status(tid, cb, tt)
                    )
                    update_button.pack(side="right", padx=5)

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    fetch_task(team, employe_window)

    employe_window.mainloop()

    
    
def open_head_window(username,role, team, app):
    print("Head Window")
    app.destroy()  # Close the login window
    
    head_window = CTk()
    screen_width = head_window.winfo_screenwidth()
    screen_height = head_window.winfo_screenheight()
    
    # Set the window size to fill the screen
    head_window.state("zoomed")
    head_window.title("Head Page")
    head_window.geometry(f"{screen_width}x{screen_height}")
    
    CTkLabel(master=head_window, text=f"Welcome to the {role} of {team} Dashboard!", font=("Arial Bold", 24)).pack(pady=10)
    
    logout_button = CTkButton(master=head_window, text="Logout", command=lambda: logout(username,f"{role} {team}",head_window))
    logout_button.pack(pady=10)
    
    # Frame for task table
    task_table_frame = CTkFrame(master=head_window,width=screen_width, height=200 ,corner_radius=10, border_width=2)
    task_table_frame.pack(fill="both", expand=True, pady=10)

    def assign_to(task_id, task_title):
        assign_to_window = CTkToplevel()
        assign_to_window.title(f"Assign Task: {task_title}")
        assign_to_window.geometry("400x300")
    
        # Get the list of team members
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
    
        try:
            cursor = connection.cursor()
            query = "SELECT id, first_name, last_name FROM users WHERE team = %s AND role = 'Member'"
            cursor.execute(query, (team,))
            members = cursor.fetchall()
    
            if members:
                member_list = [(f"{member[1]} {member[2]}", member[0]) for member in members]
                member_names = [member[0] for member in member_list]
                member_combo = CTkComboBox(assign_to_window, values=member_names, width=200)
                member_combo.set(member_names[0])
                member_combo.pack(pady=10)
            
                def assign_task():
                    selected_member_name = member_combo.get()

                    if not selected_member_name:
                        messagebox.showwarning("Input Error", "Please select a valid member.")
                        return

                    connection = create_connection()
                    if not connection:
                        messagebox.showerror("Database Error", "Unable to connect to the database.")
                        return

                    try:
                        cursor = connection.cursor()
                        # Update the `responsible_member` column with the member's full name
                        query = "UPDATE tasks SET responsible_member = %s WHERE id = %s"
                        cursor.execute(query, (selected_member_name, task_id))  # Use full name instead of ID
                        connection.commit()

                        messagebox.showinfo("Success", f"Task assigned to {selected_member_name} successfully.")
                        assign_to_window.destroy()  # Close the assignment window
                        display_tasks()  # Refresh the task display to reflect changes
                    except Error as e:
                        messagebox.showerror("Database Error", f"An error occurred: {e}")
                    finally:
                        cursor.close()
                        connection.close()

                assign_button = CTkButton(assign_to_window, text="Assign Task", command=assign_task)
                assign_button.pack(pady=10)
            else:
                CTkLabel(assign_to_window, text="No team members available", font=("Arial", 12)).pack(pady=10)
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def display_tasks():
        for widget in task_table_frame.winfo_children():
            widget.destroy()  # Clear existing task details

        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, title, description, deadline, priority, status FROM tasks WHERE responsible_team = %s", (team,))
            tasks = cursor.fetchall()

            # Display headers
            headers = ["Title", "Description", "Deadline", "Priority", "Status", "Action"]
            for col, header in enumerate(headers):
                CTkLabel(task_table_frame, text=header, font=("Arial", 12, "bold"),fg_color="#3b82f6", 
                    text_color="white", 
                    corner_radius=5, 
                    width=100,
                    compound= "center").grid(row=0, column=col, padx=5, pady=5, sticky="w")
            
            if not tasks:
                CTkLabel(task_table_frame, text="No tasks available", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
            else:
                for row, task in enumerate(tasks, start=1):
                    task_id, title, description, deadline, priority, status = task
                    CTkLabel(task_table_frame, text=title,font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10,).grid(row=row, column=0, padx=5, pady=5, sticky="w")
                    CTkLabel(task_table_frame, text=description,font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10,).grid(row=row, column=1, padx=5, pady=5, sticky="w")
                    CTkLabel(task_table_frame, text=deadline,font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10,).grid(row=row, column=2, padx=5, pady=5, sticky="w")
                    CTkLabel(task_table_frame, text=priority,font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10,).grid(row=row, column=3, padx=5, pady=5, sticky="w")
                    CTkLabel(task_table_frame, text=status,font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10,).grid(row=row, column=4, padx=5, pady=5, sticky="w")
                    
                    assign_button = CTkButton(task_table_frame, text="Assign To", command=lambda t_id=task_id, t_title=title: assign_to(t_id, t_title))
                    assign_button.grid(row=row, column=5, padx=5, pady=5, sticky="w")

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    # Initial display
    display_tasks()
    head_window.mainloop()

    
####################################################    HEAD PAGE(END)  ####################################################
    
    
####################################################    ADMIN PAGE  ####################################################
def open_admin_window(username,app):
    app.destroy()  # Close the login window

    # Create the main window
    main_window = CTk()
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Set the window size to fill the screen
    main_window.state("zoomed")
    main_window.title("Admin Page")
    # Create a scrollable frame
    admin_scrollable_frame = CTkScrollableFrame(master=main_window, width=screen_width, height=screen_height)
    admin_scrollable_frame.pack(fill="both", expand=True)
    
    # Welcome label
    CTkLabel(master=admin_scrollable_frame, text="Welcome to the Admin Dashboard!", font=("Arial Bold", 24)).pack(pady=10)
    logout_button = CTkButton(master=admin_scrollable_frame, text="Logout", command=lambda:logout(username,"Admin",main_window))
    logout_button.pack(pady=10)
    
    
  
    def display_users():
          # Filter Section: ComboBoxes for Role and Team, and Search Entry
        filter_frame = CTkFrame(master=admin_scrollable_frame)
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
    
    
        # Table Frame (Scrollable content can also go here if needed)
        table_frame = CTkScrollableFrame(master=admin_scrollable_frame,width=screen_width, height=200 ,corner_radius=10, border_width=2)
        table_frame.pack(fill="both", expand=True, pady=10)
        
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
    
           # Define table headers
            headers = ["Username", "First Name", "Last Name", "Password", "Role", "Team", "delete", "update"]

            # Create table headers with styling
            for col, header in enumerate(headers):
                header_label = CTkLabel(
                    table_frame, 
                    text=header, 
                    font=("Arial", 12, "bold"), 
                    fg_color="#3b82f6", 
                    text_color="white", 
                    corner_radius=5, 
                    width=100,
                    compound= "center"
                )
                header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")

            # Alternate row colors for better readability
            for row, user in enumerate(users, start=1):
                # Add border before every row and column
                
                for col, detail in enumerate(user):
                    frame = CTkFrame(master=table_frame, border_width=1, border_color="white" ,corner_radius=0 , height=50)
                    frame.grid(row=row, column=col, sticky="w")
                    detail_label = CTkLabel(
                        table_frame, 
                        text=detail, 
                        font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w",
                        corner_radius=10, 
                        
                    )
                    detail_label.grid(row=row, column=col, padx=10, pady=5, sticky="w")

                # Add Delete button with hover effect
                delete_button = CTkButton(
                    table_frame, 
                    text="Delete", 
                    command=lambda u=user[0]: delete_user(u), 
                    fg_color="#f87171", 
                    hover_color="#ef4444", 
                    text_color="white", 
                    corner_radius=5
                )
                delete_button.grid(row=row, column=len(headers) - 2, padx=5, pady=5, sticky="w")

                # Add Update button with hover effect
                update_button = CTkButton(
                    table_frame, 
                    text="Update", 
                    command=lambda u=user[0]: update_user(username,u), 
                    fg_color="#34d399", 
                    hover_color="#10b981", 
                    text_color="white", 
                    corner_radius=5
                )
                update_button.grid(row=row, column=len(headers) - 1, padx=5, pady=5, sticky="w")

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
    
        # # Bind filter and search actions to refresh the table
        # role_filter.bind("<<ComboboxSelected>>", lambda e: display_users())
        # team_filter.bind("<<ComboboxSelected>>", lambda e: display_users())
        # search_entry.bind("<KeyRelease>", lambda e: display_users())
     
     # Function to delete user
    def delete_user(usernamem):
         connection = create_connection()
         if not connection:
             messagebox.showerror("Database Error", "Unable to connect to the database.")
             return
     
         try:
             cursor = connection.cursor()
             query = "DELETE FROM users WHERE username = %s"
             cursor.execute(query, (usernamem,))
             connection.commit()
             messagebox.showinfo("Success", f"User '{usernamem}' deleted successfully.")
             add_action_to_history(username,"Admin",f"Delete user {usernamem}")
            #  display_users()  # Refresh the user list
         except Error as e:
             messagebox.showerror("Database Error", f"An error occurred: {e}")
         finally:
             cursor.close()
             connection.close()
     
     
    
     # Function to update user
    def update_user(u,username):
        # Open a new window or dialog to get updated information from the user
        print("Updating user:", username)  # For demonstration
        update_window = CTkToplevel()  # Use CTkToplevel for a new window
        update_window.title("Update User")
        update_window.geometry("400x300")
    
        # Get the user details
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
    
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()  # Use fetchone() if expecting a single user
    
            if user:
                # Display the user details in the update window
                userName = CTkEntry(master=update_window, width=200, placeholder_text="Enter username")
                userName.insert(0, user[1])  # user[0] is username
                userName.pack(pady=5)
    
                firstName = CTkEntry(master=update_window, width=200, placeholder_text="Enter first name")
                firstName.insert(0, user[3])  # user[1] is first name
                firstName.pack(pady=5)
    
                lastName = CTkEntry(master=update_window, width=200, placeholder_text="Enter last name")
                lastName.insert(0, user[4])  # user[2] is last name
                lastName.pack(pady=5)
    
                password = CTkEntry(master=update_window, width=200, placeholder_text="Enter user account password")
                password.insert(0, user[2])  # user[3] is password
                password.pack(pady=5)
    
                # Button to update the user
                button = CTkButton(master=update_window, text="Update User", 
                                   command=lambda: update_user_data(u,userName.get(), firstName.get(), lastName.get(), password.get(), update_window))
                button.pack(pady=10)
            else:
                messagebox.showerror("User Not Found", "The user does not exist.")
    
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
        finally:
            cursor.close()
            connection.close()
    
        # Run the window event loop
        update_window.mainloop()
    
    
    def update_user_data(usernamem, first_name, last_name, password, update_window):
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
    
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET first_name = %s, last_name = %s, password = %s WHERE username = %s"
            cursor.execute(query, (first_name, last_name, password, usernamem))
            connection.commit()
            messagebox.showinfo("Success", f"User '{usernamem}' updated successfully.")
            add_action_to_history(username,"Admin",f"updated user {usernamem}")
            update_window.destroy()  # Close the update window
            display_users()  # Refresh the user list
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
    teams = ["All", "Design", "Marketing", "Development", "Data Analysis"]
    def add_user_section():
        
        create_user_frame=CTkFrame(master=admin_scrollable_frame , corner_radius=10, border_width=2 , width=900)
        create_user_frame.pack(pady=10, padx=100)
        add_user_label=CTkLabel(master=create_user_frame, text="Create User", font=("Arial Bold", 24))
        add_user_label.pack(pady=10)
        
        userName = CTkEntry(master=create_user_frame, width=200, placeholder_text="Enter username")
        userName.pack(pady=5)

        firstName = CTkEntry(master=create_user_frame, width=200, placeholder_text="Enter first name")
        firstName.pack(pady=5)

        lastName = CTkEntry(master=create_user_frame, width=200, placeholder_text="Enter last name")
        lastName.pack(pady=5)

        password = CTkEntry(master=create_user_frame, width=200, placeholder_text="Enter user account password")
        password.pack(pady=5)

        team_combo = CTkComboBox(master=create_user_frame, values=teams[1:], width=200)  # Exclude "All" from team options
        team_combo.pack(pady=5)

        is_head_var = BooleanVar()
        head_checkbox = CTkCheckBox(master=create_user_frame, text="Mark as Team Head", variable=is_head_var)
        head_checkbox.pack(pady=5)

        # Button to add a new user
        
        def create_user(userNameo):
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
                add_action_to_history(userNameo,"Admin",f"added user {username}")
                # display_users() # Refresh the user list
                
                userName.delete(0, 'end')
                firstName.delete(0, 'end')
                lastName.delete(0, 'end')
                password.delete(0, 'end')
                team_combo.set('')
                head_checkbox.deselect()
                
            except Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()

        add_user_button = CTkButton(master=create_user_frame, text="Add User", command=lambda:create_user(username))
        add_user_button.pack(pady=10)
    
    display_users()
    add_user_section()
   


    def add_task_section():
        
        create_task_frame = CTkFrame(master=admin_scrollable_frame, corner_radius=10, border_width=2, width=900)
        create_task_frame.pack(pady=10, padx=100)
        
        add_task_label = CTkLabel(master=create_task_frame, text="Create Task", font=("Arial Bold", 24))
        add_task_label.pack(pady=10)
        # Task Title Entry
        task_title = CTkEntry(master=create_task_frame, width=200, placeholder_text="Enter task title")
        task_title.pack(pady=5)

        # Task Description Entry
        task_description = CTkEntry(master=create_task_frame, width=200, placeholder_text="Enter task description")
        task_description.pack(pady=5)

        # Placeholder for Date Selection
        calendar_label = CTkEntry(master=create_task_frame, width=200, placeholder_text="Select task deadline")
        calendar_label.pack(pady=5)

        # Function to Open Date Picker Popup
        def open_date_picker():
            # Create a popup window (Toplevel)
            date_picker_window = Toplevel()
            date_picker_window.title("Select Date")
            date_picker_window.geometry("300x300")

            # Add Calendar
            calendar = Calendar(date_picker_window, selectmode="day", date_pattern="yyyy-mm-dd")
            calendar.pack(pady=20)

            # Function to Set Date and Close Popup
            def set_date():
                selected_date = calendar.get_date()
                calendar_label.delete(0, "end")
                calendar_label.insert(0, selected_date)
                date_picker_window.destroy()

            # Add Button to Confirm Date Selection
            confirm_button = CTkButton(master=date_picker_window, text="Set Date", command=set_date)
            confirm_button.pack(pady=10)

        # Add Button to Open Date Picker
        date_picker_button = CTkButton(master=create_task_frame, text="Select Deadline", command=open_date_picker)
        date_picker_button.pack(pady=5)

        # Priority Dropdown
        task_priority = CTkComboBox(master=create_task_frame, values=["Low", "Medium", "High"], width=200)
        task_priority.set("Low")
        task_priority.pack(pady=5)

        # Team Dropdown
        task_team = CTkComboBox(master=create_task_frame, values=teams[1:], width=200)
        task_team.set("Design")
        task_team.pack(pady=5)

        # Add Task Button
        def create_task(username):
            title = task_title.get()
            description = task_description.get()
            deadline = calendar_label.get()
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
                add_action_to_history(username,"Admin",f"added task {title}")
                display_tasks()
            except Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()

        add_task_button = CTkButton(master=create_task_frame, text="Add Task", command=lambda:create_task(username))
        add_task_button.pack(pady=10)

    
    

    # Table to display tasks
    task_table_frame = CTkScrollableFrame(master=admin_scrollable_frame,width=screen_width, height=200 ,corner_radius=10, border_width=2)
    task_table_frame.pack(fill="both", expand=True, pady=10)
    
    def delete_task(usrename,task_title):
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE title = %s", (task_title,))
            connection.commit()
            messagebox.showinfo("Success", f"Task '{task_title}' deleted successfully.")
            add_action_to_history(usrename,"Admin",f"deleted task {task_title}")
            display_tasks()  # Refresh the task list
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
    
    def update_task(username,task_title):
        # Open a new window or dialog to get updated information from the user
        print("Updating task:", task_title)  # For demonstration
        update_task_window = CTkToplevel()  # Use CTkToplevel for a new window
        update_task_window.title("Update Task")
        update_task_window.geometry("400x300")
        
        # Get the task details
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE title = %s", (task_title,))
            task = cursor.fetchone()  # Use fetchone() if expecting a single task
        
            if task:
                # Display the task details in the update window
                taskTitle = CTkEntry(master=update_task_window, width=200, placeholder_text="Enter task title")
                taskTitle.insert(0, task[1])  # task[1] is title
                taskTitle.pack(pady=5)
        
                taskDescription = CTkEntry(master=update_task_window, width=200, placeholder_text="Enter task description")
                taskDescription.insert(0, task[2])  # task[2] is description
                taskDescription.pack(pady=5)
        
                taskDeadline = CTkEntry(master=update_task_window, width=200, placeholder_text="Enter task deadline")
                taskDeadline.insert(0, task[3])  # task[3] is deadline
                taskDeadline.pack(pady=5)
        
                taskPriority = CTkComboBox(master=update_task_window, values=["Low", "Medium", "High"], width=200)
                taskPriority.set(task[4])  # task[4] is priority
                taskPriority.pack(pady=5)
        
                taskTeam = CTkComboBox(master=update_task_window, values=teams[1:], width=200)
                taskTeam.set(task[5])  # task[5] is responsible team
                taskTeam.pack(pady=5)
        
                taskStatus = CTkComboBox(master=update_task_window, values=["Pending", "In Progress", "Completed"], width=200)
                taskStatus.set(task[7])  # task[7] is status
                taskStatus.pack(pady=5)
        
                # Button to update the task
                button = CTkButton(master=update_task_window, text="Update Task", 
                                   command=lambda: update_task_data(taskTitle.get(), taskDescription.get(), taskDeadline.get(), taskPriority.get(), taskTeam.get(), taskStatus.get(), update_task_window))
                button.pack(pady=10)
            else:
                messagebox.showerror("Task Not Found", "The task does not exist.")
            
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        finally:
            cursor.close()
            connection.close()
            
    def update_task_data(title, description, deadline, priority, team, status, update_task_window):
        connection = create_connection()
        if not connection:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return
        
        try:
            cursor = connection.cursor()
            query = "UPDATE tasks SET description = %s, deadline = %s, priority = %s, responsible_team = %s, status = %s WHERE title = %s"
            cursor.execute(query, (description, deadline, priority, team, status, title))
            connection.commit()
            messagebox.showinfo("Success", f"Task '{title}' updated successfully.")
            add_action_to_history(username,"Admin",f"updated task {title}")
            update_task_window.destroy()  # Close the update window
            display_tasks()  # Refresh the task list
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

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
            cursor.execute("SELECT title, description, deadline, priority, responsible_team,status FROM tasks")
            tasks = cursor.fetchall()

            # Display headers for task table
            
            task_headers = ["Title", "Description", "Deadline", "Priority", "Responsible Team" , "Status" ,"Delete", "Update"]
            for col, header in enumerate(task_headers):
                header_label = CTkLabel(
                    task_table_frame, 
                    text=header, 
                    font=("Arial", 12, "bold"), 
                    fg_color="#3b82f6", 
                    text_color="white", 
                    corner_radius=5, 
                    width=100
                )
                header_label.grid(row=0, column=col, padx=10, pady=10, sticky="w")

            # Display task data
            for row, task in enumerate(tasks, start=1):
                for col, detail in enumerate(task):
                    frame = CTkFrame(master=task_table_frame, border_width=1, border_color="white",corner_radius=0, height=50)
                    frame.grid(row=row, column=col,sticky="w")
                    detail_label = CTkLabel(
                        task_table_frame, 
                        text=detail, 
                        font=("Arial", 12), 
                        text_color="#ffffff",
                        width=100, 
                        anchor="w"
                    )
                    detail_label.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                # Add Update button
                update_button = CTkButton(task_table_frame, text="Update", command=lambda u=task[0]: update_task(username,u),fg_color="#34d399", 
                    hover_color="#10b981", 
                    text_color="white", 
                    corner_radius=5)
                update_button.grid(row=row, column=len(task_headers) - 1, padx=3, pady=5, sticky="w")
                # Add Delete button
                delete_button = CTkButton(task_table_frame, text="Delete", command=lambda u=task[0]: delete_task(username,u),fg_color="#f87171", 
                    hover_color="#ef4444", 
                    text_color="white", 
                    corner_radius=5)
                delete_button.grid(row=row, column=len(task_headers) - 2, padx=3, pady=5, sticky="w")

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    # Initial display of tasks
    add_task_section()
    display_tasks()
    

    main_window.mainloop()

####################################################    ADMIN PAGE(END)     ####################################################

# Initialize login window
def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    position_x = int((screen_width - width) / 2)
    position_y = int((screen_height - height) / 2)

    # Set the position of the window
    window.geometry(f"{width}x{height}+{position_x}+{position_y}")

login()