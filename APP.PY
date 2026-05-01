from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret123"


# ============================================================
# SAVE/LOAD USERS USING TEXT FILE
# ============================================================

USERS_FILE = "users.txt"

def load_users_from_file():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        user_id, username, password, role = parts
                        user = SystemUser(user_id, username, password, role)
                        users.append(user)
    return users

def save_users_to_file(users):
    with open(USERS_FILE, 'w') as f:
        for user in users:
            f.write(f"{user.get_user_id()}|{user.get_username()}|{user.get_password()}|{user.get_role()}\n")


# ============================================================
# MODULE 1: CUSTOMER MANAGEMENT
# ============================================================

class Customer:
    def __init__(self, customer_id, name, contact, password):
        self.__customer_id = customer_id
        self.__name = name
        self.__contact = contact
        self.__password = password

    def get_id(self):
        return self.__customer_id

    def get_name(self):
        return self.__name

    def get_contact(self):
        return self.__contact
    
    def get_password(self):
        return self.__password

    def set_name(self, name):
        self.__name = name

    def set_contact(self, contact):
        self.__contact = contact
    
    def set_password(self, password):
        self.__password = password


class CRM:
    def __init__(self):
        self.customers = []

    def add_customer(self, cid, name, contact, password):
        for c in self.customers:
            if c.get_id() == cid:
                return "Customer ID already exists"

        if not name or not contact or not password:
            return "All fields required"

        if "@" not in contact:
            return "Invalid email"

        customer = Customer(cid, name, contact, password)
        self.customers.append(customer)
        return "Added successfully"

    def get_all(self):
        return self.customers

    def delete_customer(self, cid):
        for c in self.customers:
            if c.get_id() == cid:
                self.customers.remove(c)
                return "Deleted successfully"
        return "Customer not found"
    
    def authenticate(self, customer_id, password):
        for c in self.customers:
            if c.get_id() == customer_id and c.get_password() == password:
                return c
        return None


# ============================================================
# MODULE 2: INTERACTION MANAGEMENT
# ============================================================

class Interaction:
    def __init__(self, interaction_id, customer_id, interaction_type, date_time, notes):
        self.__interaction_id = interaction_id
        self.__customer_id = customer_id
        self.__interaction_type = interaction_type
        self.__date_time = date_time
        self.__notes = notes

    def get_id(self):
        return self.__interaction_id

    def get_customer_id(self):
        return self.__customer_id

    def get_type(self):
        return self.__interaction_type

    def get_datetime(self):
        return self.__date_time

    def get_notes(self):
        return self.__notes

    def set_notes(self, notes):
        self.__notes = notes


class InteractionManager:
    def __init__(self):
        self.interactions = []
        self.__counter = 1

    def generate_id(self):
        iid = f"INT{self.__counter:03d}"
        self.__counter += 1
        return iid

    def add_interaction(self, customer_id, interaction_type, date_time, notes):
        if not interaction_type:
            return "Interaction type required"
        if not date_time:
            return "Date/Time required"
        if not notes:
            return "Notes required"
        iid = self.generate_id()
        interaction = Interaction(iid, customer_id, interaction_type, date_time, notes)
        self.interactions.append(interaction)
        return "Interaction Recorded Successfully"

    def get_by_customer(self, customer_id):
        return [i for i in self.interactions if i.get_customer_id() == customer_id]

    def get_by_id(self, interaction_id):
        for i in self.interactions:
            if i.get_id() == interaction_id:
                return i
        return None

    def update_interaction(self, interaction_id, new_notes):
        if not new_notes:
            return "Notes required"
        interaction = self.get_by_id(interaction_id)
        if not interaction:
            return "Interaction not found"
        interaction.set_notes(new_notes)
        return "Interaction updated"

    def delete_interaction(self, interaction_id):
        interaction = self.get_by_id(interaction_id)
        if not interaction:
            return False
        self.interactions.remove(interaction)
        return True


# ============================================================
# MODULE 3: SUPPORT TICKET SYSTEM
# ============================================================

class SupportTicket:
    VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
    VALID_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
    
    def __init__(self, ticket_id, customer_id, description, priority):
        self.__ticket_id = ticket_id
        self.__customer_id = customer_id
        self.__description = description
        self.__priority = priority
        self.__status = "Open"
        self.__created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__history = [f"[{self.__created_date}] Ticket created"]
    
    def get_id(self):
        return self.__ticket_id
    
    def get_customer_id(self):
        return self.__customer_id
    
    def get_description(self):
        return self.__description
    
    def get_priority(self):
        return self.__priority
    
    def get_status(self):
        return self.__status
    
    def get_created_date(self):
        return self.__created_date
    
    def get_history(self):
        return self.__history
    
    def set_priority(self, priority):
        if priority in self.VALID_PRIORITIES:
            self.__priority = priority
            return True
        return False
    
    def set_status(self, status):
        if status in self.VALID_STATUSES:
            self.__status = status
            return True
        return False


class TicketManager:
    def __init__(self):
        self.tickets = []
        self.__counter = 1
    
    def generate_id(self):
        tid = f"TKT{self.__counter:04d}"
        self.__counter += 1
        return tid
    
    def create_ticket(self, customer_id, description, priority):
        if priority not in SupportTicket.VALID_PRIORITIES:
            return "Invalid priority"
        if not description:
            return "Description required"
        ticket_id = self.generate_id()
        ticket = SupportTicket(ticket_id, customer_id, description, priority)
        self.tickets.append(ticket)
        return f"Ticket created! ID: {ticket_id}"
    
    def get_ticket_by_id(self, ticket_id):
        for ticket in self.tickets:
            if ticket.get_id() == ticket_id:
                return ticket
        return None
    
    def get_tickets_by_customer(self, customer_id):
        return [t for t in self.tickets if t.get_customer_id() == customer_id]
    
    def get_all_tickets(self):
        return self.tickets
    
    def update_ticket_priority(self, ticket_id, new_priority):
        if new_priority not in SupportTicket.VALID_PRIORITIES:
            return "Invalid priority"
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return "Ticket not found"
        ticket.set_priority(new_priority)
        return "Priority updated"
    
    def update_ticket_status(self, ticket_id, new_status):
        if new_status not in SupportTicket.VALID_STATUSES:
            return "Invalid status"
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return "Ticket not found"
        ticket.set_status(new_status)
        return "Status updated"
    
    def delete_ticket(self, ticket_id):
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            self.tickets.remove(ticket)
            return True
        return False


# ============================================================
# MODULE 4: SYSTEM MANAGEMENT
# ============================================================

class SystemUser:
    ROLES = ["Admin", "Staff", "Support"]
    
    def __init__(self, user_id, username, password, role):
        self.__user_id = user_id
        self.__username = username
        self.__password = password
        self.__role = role
        self.__created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_user_id(self):
        return self.__user_id
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def get_role(self):
        return self.__role
    
    def get_created_date(self):
        return self.__created_date
    
    def set_username(self, username):
        self.__username = username
    
    def set_password(self, password):
        self.__password = password
    
    def set_role(self, role):
        if role in self.ROLES:
            self.__role = role
            return True
        return False


class UserManager:
    def __init__(self):
        self.users = load_users_from_file()
        self.__counter = len(self.users) + 1
        
        if not self.users:
            self._create_default_admin()
            save_users_to_file(self.users)
    
    def _create_default_admin(self):
        default_admin = SystemUser("USR001", "admin", "1234", "Admin")
        self.users.append(default_admin)
    
    def generate_id(self):
        uid = f"USR{self.__counter:03d}"
        self.__counter += 1
        return uid
    
    def is_username_unique(self, username):
        for user in self.users:
            if user.get_username() == username:
                return False
        return True
    
    def add_user(self, username, password, role):
        if not self.is_username_unique(username):
            return "Username already exists"
        if not password or password.strip() == "":
            return "Password cannot be empty"
        if role not in SystemUser.ROLES:
            return f"Invalid role. Choose: Admin, Staff, Support"
        user_id = self.generate_id()
        user = SystemUser(user_id, username, password, role)
        self.users.append(user)
        save_users_to_file(self.users)
        return f"User added successfully! User ID: {user_id}"
    
    def get_all_users(self):
        return self.users
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.get_user_id() == user_id:
                return user
        return None
    
    def get_user_by_username(self, username):
        for user in self.users:
            if user.get_username() == username:
                return user
        return None
    
    def update_user(self, user_id, new_username=None, new_password=None, new_role=None):
        user = self.get_user_by_id(user_id)
        if not user:
            return "User not found"
        if new_username:
            if not self.is_username_unique(new_username) and new_username != user.get_username():
                return "Username already exists"
            user.set_username(new_username)
        if new_password:
            if not new_password.strip():
                return "Password cannot be empty"
            user.set_password(new_password)
        if new_role:
            if new_role not in SystemUser.ROLES:
                return "Invalid role"
            user.set_role(new_role)
        save_users_to_file(self.users)
        return "User updated successfully"
    
    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        if user.get_username() == "admin":
            return False
        self.users.remove(user)
        save_users_to_file(self.users)
        return True
    
    def authenticate(self, username, password):
        user = self.get_user_by_username(username)
        if user and user.get_password() == password:
            return user
        return None


# ============================================================
# MODULE 6: REPORTING MANAGEMENT
# ============================================================

from collections import Counter
from datetime import datetime, timedelta

class ReportManager:
    def __init__(self, crm, im, tm):
        self.crm = crm
        self.im = im
        self.tm = tm
    
    def get_customer_report(self):
        customers = self.crm.get_all()
        return {
            'total_customers': len(customers),
            'customers': customers
        }
    
    def get_interactions_per_period(self, period):
        interactions = self.im.interactions
        now = datetime.now()
        
        filtered_interactions = []
        
        for interaction in interactions:
            try:
                interaction_date = datetime.strptime(interaction.get_datetime()[:10], "%Y-%m-%d")
            except:
                continue
            
            if period == "daily":
                if interaction_date.date() == now.date():
                    filtered_interactions.append(interaction)
            elif period == "weekly":
                week_ago = now - timedelta(days=7)
                if interaction_date >= week_ago:
                    filtered_interactions.append(interaction)
            elif period == "monthly":
                if interaction_date.year == now.year and interaction_date.month == now.month:
                    filtered_interactions.append(interaction)
        
        return {
            'period': period,
            'count': len(filtered_interactions),
            'interactions': filtered_interactions
        }
    
    def get_most_common_interaction_type(self):
        interactions = self.im.interactions
        
        if not interactions:
            return {
                'has_data': False,
                'message': 'No interaction records found'
            }
        
        type_counts = Counter()
        for interaction in interactions:
            interaction_type = interaction.get_type()
            type_counts[interaction_type] += 1
        
        if type_counts:
            most_common = type_counts.most_common(1)[0]
            return {
                'has_data': True,
                'type_counts': dict(type_counts),
                'most_common_type': most_common[0],
                'most_common_count': most_common[1],
                'total_interactions': len(interactions)
            }
        
        return {
            'has_data': False,
            'message': 'No interaction records found'
        }
    
    def get_support_ticket_report(self):
        tickets = self.tm.get_all_tickets()
        
        if not tickets:
            return {
                'has_data': False,
                'message': 'No tickets found'
            }
        
        status_counts = Counter()
        priority_counts = Counter()
        
        for ticket in tickets:
            status_counts[ticket.get_status()] += 1
            priority_counts[ticket.get_priority()] += 1
        
        return {
            'has_data': True,
            'total_tickets': len(tickets),
            'status_counts': dict(status_counts),
            'priority_counts': dict(priority_counts),
            'tickets': tickets
        }


# ============================================================
# GLOBAL INSTANCES
# ============================================================

crm = CRM()
im = InteractionManager()
tm = TicketManager()
um = UserManager()
report_manager = ReportManager(crm, im, tm)

# SAMPLE CUSTOMER
sample_customer = Customer("CUST001", "Juan Dela Cruz", "juan@email.com", "1234")
crm.customers.append(sample_customer)

# SAMPLE INTERACTION
sample_interaction = Interaction("INT001", "CUST001", "Call", "2026-05-01 10:00", "Test interaction")
im.interactions.append(sample_interaction)

# SAMPLE TICKET
sample_ticket = SupportTicket("TKT0001", "CUST001", "Test ticket", "High")
tm.tickets.append(sample_ticket)


# ============================================================
# LOGIN ROUTE
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = um.authenticate(username, password)
        
        if user:
            session["user"] = username
            session["role"] = user.get_role()
            session["type"] = "system_user"
            return redirect(url_for("home"))
        
        customer = crm.authenticate(username, password)
        
        if customer:
            session["user"] = customer.get_id()
            session["name"] = customer.get_name()
            session["role"] = "Customer"
            session["type"] = "customer"
            return redirect(url_for("customer_home"))
        
        message = "Invalid username or password"
    
    return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================================
# MODULE 1 ROUTES
# ============================================================

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    if session.get("type") == "customer":
        return redirect(url_for("customer_home"))
    return render_template("menu.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Support":
        return "Access Denied", 403
    
    message = ""
    if request.method == "POST":
        cid = request.form["id"]
        name = request.form["name"]
        contact = request.form["contact"]
        password = request.form["password"]
        message = crm.add_customer(cid, name, contact, password)
    return render_template("add.html", message=message)


@app.route("/view")
def view():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Support":
        return "Access Denied", 403
    
    customers = crm.get_all()
    return render_template("view.html", customers=customers)


@app.route("/edit/<cid>", methods=["GET", "POST"])
def edit(cid):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Support":
        return "Access Denied", 403
    
    customer = None
    for c in crm.get_all():
        if c.get_id() == cid:
            customer = c
            break
    if not customer:
        return "Customer not found"
    if request.method == "POST":
        new_name = request.form.get("name")
        new_contact = request.form.get("contact")
        customer.set_name(new_name)
        customer.set_contact(new_contact)
        return redirect(url_for("view"))
    return render_template("edit.html", customer=customer)


@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Support":
        return "Access Denied", 403
    
    customer = None
    message = ""
    if request.method == "POST":
        search_id = request.form["id"]
        for c in crm.get_all():
            if c.get_id() == search_id:
                customer = c
                break
        if not customer:
            message = "Customer not found"
    return render_template("search.html", customer=customer, message=message)


@app.route("/delete/<cid>")
def delete(cid):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    crm.delete_customer(cid)
    return redirect(url_for("view"))


# ============================================================
# MODULE 2 ROUTES
# ============================================================

@app.route("/add_interaction", methods=["GET", "POST"])
def add_interaction():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
 
    message = ""
    customers = crm.get_all()
    
    message = ""
    customers = crm.get_all()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        customer = None
        for c in customers:
            if c.get_id() == customer_id:
                customer = c
                break
        if not customer:
            message = "Customer not found"
        else:
            interaction_type = request.form.get("interaction_type")
            date_time = request.form.get("date_time")
            notes = request.form.get("notes")
            message = im.add_interaction(customer_id, interaction_type, date_time, notes)
    return render_template("add_interaction.html", message=message, customers=customers)


@app.route("/view_interactions", methods=["GET", "POST"])
def view_interaction():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    
    customer = None
    interactions = []
    message = ""
    customers = crm.get_all()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        for c in customers:
            if c.get_id() == customer_id:
                customer = c
                break
        if not customer:
            message = "Customer not found"
        else:
            interactions = im.get_by_customer(customer_id)
            if not interactions:
                message = "No interactions"
    return render_template("view_interaction.html", customer=customer, interactions=interactions, message=message, customers=customers)


@app.route("/update_interaction/<interaction_id>", methods=["GET", "POST"])
def update_interaction(interaction_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Support":
        return "Access Denied", 403
    
    interaction = im.get_by_id(interaction_id)
    if not interaction:
        return "Interaction not found"
    
    if request.method == "POST":
        new_notes = request.form.get("notes")
        im.update_interaction(interaction_id, new_notes)
        return redirect(url_for("view_interaction"))
    
    return render_template("update_interaction.html", interaction=interaction)


@app.route("/delete_interaction/<interaction_id>")
def delete_interaction(interaction_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    im.delete_interaction(interaction_id)
    return redirect(url_for("view_interaction"))


# ============================================================
# MODULE 3 ROUTES
# ============================================================

@app.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") not in ["Admin", "Support"]:
        return "Access Denied", 403
    
    message = ""
    customers = crm.get_all()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        description = request.form.get("description")
        priority = request.form.get("priority")
        result = tm.create_ticket(customer_id, description, priority)
        message = result
    return render_template("create_ticket.html", message=message, customers=customers)


@app.route("/view_tickets", methods=["GET", "POST"])
def view_tickets():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") not in ["Admin", "Support"]:
        return "Access Denied", 403
    
    tickets = []
    message = ""
    customers = crm.get_all()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        if customer_id == "all":
            tickets = tm.get_all_tickets()
        else:
            tickets = tm.get_tickets_by_customer(customer_id)
        if not tickets:
            message = "No tickets"
    return render_template("view_tickets.html", tickets=tickets, message=message, customers=customers)


@app.route("/update_ticket_priority/<ticket_id>", methods=["GET", "POST"])
def update_ticket_priority(ticket_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") not in ["Admin", "Support"]:
        return "Access Denied", 403
    
    ticket = tm.get_ticket_by_id(ticket_id)
    if request.method == "POST":
        new_priority = request.form.get("priority")
        tm.update_ticket_priority(ticket_id, new_priority)
        return redirect(url_for("view_tickets"))
    return render_template("update_ticket_priority.html", ticket=ticket)


@app.route("/update_ticket_status/<ticket_id>", methods=["GET", "POST"])
def update_ticket_status(ticket_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") not in ["Admin", "Support"]:
        return "Access Denied", 403
    
    ticket = tm.get_ticket_by_id(ticket_id)
    if request.method == "POST":
        new_status = request.form.get("status")
        tm.update_ticket_status(ticket_id, new_status)
        return redirect(url_for("view_tickets"))
    return render_template("update_ticket_status.html", ticket=ticket)


@app.route("/delete_ticket/<ticket_id>")
def delete_ticket(ticket_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    tm.delete_ticket(ticket_id)
    return redirect(url_for("view_tickets"))


# ============================================================
# MODULE 4 ROUTES (Admin Only)
# ============================================================

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        result = um.add_user(username, password, role)
        message = result
        if "successfully" in result.lower():
            return redirect(url_for("view_users"))
    
    return render_template("add_user.html", message=message, roles=SystemUser.ROLES)


@app.route("/view_users")
def view_users():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    users = um.get_all_users()
    return render_template("view_users.html", users=users)


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    user = um.get_user_by_id(user_id)
    if not user:
        return "User not found"
    
    message = ""
    if request.method == "POST":
        new_username = request.form.get("username")
        new_password = request.form.get("password")
        new_role = request.form.get("role")
        result = um.update_user(user_id, new_username, new_password, new_role)
        message = result
        if "successfully" in result.lower():
            return redirect(url_for("view_users"))
    
    return render_template("edit_user.html", user=user, message=message, roles=SystemUser.ROLES)


@app.route("/assign_role/<user_id>", methods=["GET", "POST"])
def assign_role(user_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    user = um.get_user_by_id(user_id)
    if not user:
        return "User not found"
    
    message = ""
    if request.method == "POST":
        new_role = request.form.get("role")
        result = um.update_user(user_id, None, None, new_role)
        message = result
        if "successfully" in result.lower():
            return redirect(url_for("view_users"))
    
    return render_template("assign_role.html", user=user, message=message, roles=SystemUser.ROLES)


@app.route("/delete_user/<user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") != "Admin":
        return "Access Denied", 403
    
    user = um.get_user_by_id(user_id)
    if not user:
        return "User not found"
    
    if user.get_username() == "admin":
        return "Cannot delete the default admin user"
    
    if request.method == "POST":
        um.delete_user(user_id)
        return redirect(url_for("view_users"))
    
    return render_template("delete_user.html", user=user)


# ============================================================
# MODULE 6 ROUTES
# ============================================================

@app.route("/reports")
def reports():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Customer":
        return "Access Denied", 403
    
    return render_template("reports.html")


@app.route("/report/customers")
def report_customers():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Customer":
        return "Access Denied", 403
    
    report = report_manager.get_customer_report()
    return render_template("report_customers.html", report=report)


@app.route("/report/interactions", methods=["GET", "POST"])
def report_interactions():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Customer":
        return "Access Denied", 403
    
    report = None
    period = None
    if request.method == "POST":
        period = request.form.get("period")
        report = report_manager.get_interactions_per_period(period)
    return render_template("report_interactions.html", report=report, period=period)


@app.route("/report/interaction-types")
def report_interaction_types():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Customer":
        return "Access Denied", 403
    
    report = report_manager.get_most_common_interaction_type()
    return render_template("report_interaction_types.html", report=report)


@app.route("/report/tickets")
def report_tickets():
    if "user" not in session or session.get("type") == "customer":
        return redirect(url_for("login"))
    if session.get("role") == "Customer":
        return "Access Denied", 403
    
    report = report_manager.get_support_ticket_report()
    return render_template("report_tickets.html", report=report)


# ============================================================
# CUSTOMER ROUTES
# ============================================================

@app.route("/customer_home")
def customer_home():
    if "user" not in session or session.get("type") != "customer":
        return redirect(url_for("login"))
    return render_template("customer_menu.html", name=session.get("name"), id=session.get("user"))


@app.route("/customer_tickets")
def customer_tickets():
    if "user" not in session or session.get("type") != "customer":
        return redirect(url_for("login"))
    customer_id = session.get("user")
    tickets = tm.get_tickets_by_customer(customer_id)
    return render_template("customer_tickets.html", tickets=tickets)


@app.route("/customer_create_ticket", methods=["GET", "POST"])
def customer_create_ticket():
    if "user" not in session or session.get("type") != "customer":
        return redirect(url_for("login"))
    message = ""
    if request.method == "POST":
        customer_id = session.get("user")
        description = request.form.get("description")
        priority = request.form.get("priority")
        message = tm.create_ticket(customer_id, description, priority)
    return render_template("customer_create_ticket.html", message=message)


@app.route("/customer_interactions")
def customer_interactions():
    if "user" not in session or session.get("type") != "customer":
        return redirect(url_for("login"))
    customer_id = session.get("user")
    interactions = im.get_by_customer(customer_id)
    return render_template("customer_interactions.html", interactions=interactions)


if __name__ == "__main__":
    app.run(debug=True, port=8000)