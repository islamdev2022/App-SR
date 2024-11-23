import customtkinter as ctk


def show_frame(frame):
    """Bring the specified frame to the front."""
    frame.tkraise()


def create_users_page(container):
    """Create the Users page."""
    users_frame = ctk.CTkFrame(container)

    label = ctk.CTkLabel(users_frame, text="Users Page", font=("Arial", 20))
    label.pack(pady=20)

    desc = ctk.CTkLabel(users_frame, text="Manage users here.")
    desc.pack(pady=10)

    return users_frame


def create_tasks_page(container):
    """Create the Tasks page."""
    tasks_frame = ctk.CTkFrame(container)

    label = ctk.CTkLabel(tasks_frame, text="Tasks Page", font=("Arial", 20))
    label.pack(pady=20)

    desc = ctk.CTkLabel(tasks_frame, text="Manage tasks here.")
    desc.pack(pady=10)

    return tasks_frame


def main():
    # Initialize the app
    app = ctk.CTk()
    app.title("Multi-Page App with Header")
    app.geometry("600x400")

    # Header (Navigation Bar)
    header = ctk.CTkFrame(app, height=50)
    header.pack(side="top", fill="x")

    # Container for pages
    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    # Create pages
    users_page = create_users_page(container)
    tasks_page = create_tasks_page(container)

    # Place pages in the container
    for frame in (users_page, tasks_page):
        frame.grid(row=0, column=0, sticky="nsew")

    # Add navigation buttons
    users_button = ctk.CTkButton(
        header, text="Users", width=100, 
        command=lambda: show_frame(users_page)
    )
    users_button.pack(side="left", padx=10, pady=5)

    tasks_button = ctk.CTkButton(
        header, text="Tasks", width=100, 
        command=lambda: show_frame(tasks_page)
    )
    tasks_button.pack(side="left", padx=10, pady=5)

    # Show the initial page
    show_frame(users_page)

    app.mainloop()


if __name__ == "__main__":
    main()
