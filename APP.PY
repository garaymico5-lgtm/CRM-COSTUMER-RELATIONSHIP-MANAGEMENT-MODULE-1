from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"


# ============================================================
# MODULE 1: CUSTOMER MANAGEMENT
# ============================================================

class Customer:
    def __init__(self, customer_id, name, contact):
        self.__customer_id = customer_id
        self.__name = name
        self.__contact = contact

    def get_id(self):
        return self.__customer_id

    def get_name(self):
        return self.__name

    def get_contact(self):
        return self.__contact

    def set_name(self, name):
        self.__name = name

    def set_contact(self, contact):
        self.__contact = contact


class CRM:
    def __init__(self):
        self.customers = []

    def add_customer(self, cid, name, contact):
        for c in self.customers:
            if c.get_id() == cid:
                return "Customer ID already exists"

        if not name or not contact:
            return "Invalid name or email"

        if "@" not in contact:
            return "Invalid email"

        customer = Customer(cid, name, contact)
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


# ============================================================
# MODULE 2: INTERACTION / COMMUNICATION MANAGEMENT
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

    def set_type(self, interaction_type):
        self.__interaction_type = interaction_type

    def set_datetime(self, date_time):
        self.__date_time = date_time


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
            return "Interaction type is required"
        if not date_time:
            return "Date/Time is required"
        if not notes:
            return "Notes cannot be empty"
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
            return "Notes cannot be empty"
        interaction = self.get_by_id(interaction_id)
        if not interaction:
            return "Interaction not found"
        interaction.set_notes(new_notes)
        return "Interaction updated successfully"

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
    
    def __init__(self, ticket_id, customer_id, description, priority, status="Open"):
        self.__ticket_id = ticket_id
        self.__customer_id = customer_id
        self.__description = description
        self.__priority = priority
        self.__status = status
        self.__created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__history = []
        self.__add_to_history(f"Ticket created with status: {status}, priority: {priority}")
    
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
    
    def __add_to_history(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__history.append(f"[{timestamp}] {action}")
    
    def set_priority(self, priority):
        if priority in self.VALID_PRIORITIES:
            old_priority = self.__priority
            self.__priority = priority
            self.__add_to_history(f"Priority changed from {old_priority} to {priority}")
            return True
        return False
    
    def set_status(self, status):
        if status in self.VALID_STATUSES:
            old_status = self.__status
            self.__status = status
            self.__add_to_history(f"Status changed from {old_status} to {status}")
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
            return "Invalid priority level"
        if not description or not description.strip():
            return "Description cannot be empty"
        ticket_id = self.generate_id()
        ticket = SupportTicket(ticket_id, customer_id, description, priority, "Open")
        self.tickets.append(ticket)
        return f"Ticket created successfully! ID: {ticket_id}"
    
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
            return "Invalid priority level"
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return "Ticket not found"
        ticket.set_priority(new_priority)
        return f"Priority updated to {new_priority}"
    
    def update_ticket_status(self, ticket_id, new_status):
        if new_status not in SupportTicket.VALID_STATUSES:
            return "Invalid status"
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return "Ticket not found"
        current_status = ticket.get_status()
        if new_status == "Closed" and current_status not in ["Resolved", "In Progress"]:
            return "Cannot close ticket yet. Ticket must be Resolved or In Progress first"
        ticket.set_status(new_status)
        return f"Status updated to {new_status}"
    
    def get_ticket_history(self, ticket_id):
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return None
        return ticket.get_history()
    
    def delete_ticket(self, ticket_id):
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            self.tickets.remove(ticket)
            return True
        return False


# ============================================================
# GLOBAL INSTANCES
# ============================================================

USERNAME = "admin"
PASSWORD = "1234"

crm = CRM()
im = InteractionManager()
tm = TicketManager()


# ============================================================
# MODULE 1 ROUTES
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            message = "Invalid username or password"
    return render_template("login.html", message=message)


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("menu.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    message = ""
    if request.method == "POST":
        cid = request.form["id"]
        name = request.form["name"]
        contact = request.form["contact"]
        message = crm.add_customer(cid, name, contact)
    return render_template("add.html", message=message)


@app.route("/view")
def view():
    if "user" not in session:
        return redirect(url_for("login"))
    customers = crm.get_all()
    return render_template("view.html", customers=customers)


@app.route("/edit/<cid>", methods=["GET", "POST"])
def edit(cid):
    if "user" not in session:
        return redirect(url_for("login"))
    customer = None
    for c in crm.get_all():
        if c.get_id() == cid:
            customer = c
            break
    if not customer:
        return "Customer not found"
    message = ""
    if request.method == "POST":
        new_name = request.form.get("name")
        new_contact = request.form.get("contact")
        if not new_name or not new_contact:
            message = "Invalid input"
        elif "@" not in new_contact:
            message = "Invalid email"
        else:
            customer.set_name(new_name)
            customer.set_contact(new_contact)
            return redirect(url_for("view"))
    return render_template("edit.html", customer=customer, message=message)


@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))
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
    if "user" not in session:
        return redirect(url_for("login"))
    crm.delete_customer(cid)
    return redirect(url_for("view"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ============================================================
# MODULE 2 ROUTES
# ============================================================

@app.route("/add_interaction", methods=["GET", "POST"])
def add_interaction():
    if "user" not in session:
        return redirect(url_for("login"))
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
    if "user" not in session:
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
                message = "No interactions found"
    return render_template("view_interaction.html", customer=customer, interactions=interactions, message=message, customers=customers)


@app.route("/update_interaction/<interaction_id>", methods=["GET", "POST"])
def update_interaction(interaction_id):
    if "user" not in session:
        return redirect(url_for("login"))
    interaction = im.get_by_id(interaction_id)
    if not interaction:
        return "Interaction not found"
    message = ""
    if request.method == "POST":
        new_notes = request.form.get("notes")
        result = im.update_interaction(interaction_id, new_notes)
        if result == "Interaction updated successfully":
            return redirect(url_for("view_interaction"))
        else:
            message = result
    return render_template("update_interaction.html", interaction=interaction, message=message)


@app.route("/delete_interaction/<interaction_id>", methods=["GET", "POST"])
def delete_interaction(interaction_id):
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        im.delete_interaction(interaction_id)
    return redirect(url_for("view_interaction"))


# ============================================================
# MODULE 3 ROUTES
# ============================================================

@app.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if "user" not in session:
        return redirect(url_for("login"))
    message = ""
    customers = crm.get_all()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        description = request.form.get("description")
        priority = request.form.get("priority")
        customer = None
        for c in customers:
            if c.get_id() == customer_id:
                customer = c
                break
        if not customer:
            message = "Invalid customer"
        else:
            result = tm.create_ticket(customer_id, description, priority)
            message = result
    return render_template("create_ticket.html", message=message, customers=customers)


@app.route("/view_tickets", methods=["GET", "POST"])
def view_tickets():
    if "user" not in session:
        return redirect(url_for("login"))
    tickets = []
    message = ""
    customers = crm.get_all()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        if customer_id == "all":
            tickets = tm.get_all_tickets()
            if not tickets:
                message = "No tickets found"
        else:
            customer = None
            for c in customers:
                if c.get_id() == customer_id:
                    customer = c
                    break
            if not customer:
                message = "Customer not found"
            else:
                tickets = tm.get_tickets_by_customer(customer_id)
                if not tickets:
                    message = "No tickets found for this customer"
    return render_template("view_tickets.html", tickets=tickets, message=message, customers=customers)


@app.route("/update_ticket_priority/<ticket_id>", methods=["GET", "POST"])
def update_ticket_priority(ticket_id):
    if "user" not in session:
        return redirect(url_for("login"))
    ticket = tm.get_ticket_by_id(ticket_id)
    if not ticket:
        return "Ticket not found"
    message = ""
    if request.method == "POST":
        new_priority = request.form.get("priority")
        result = tm.update_ticket_priority(ticket_id, new_priority)
        if "updated" in result.lower():
            return redirect(url_for("view_tickets"))
        else:
            message = result
    return render_template("update_ticket_priority.html", ticket=ticket, message=message)


@app.route("/update_ticket_status/<ticket_id>", methods=["GET", "POST"])
def update_ticket_status(ticket_id):
    if "user" not in session:
        return redirect(url_for("login"))
    ticket = tm.get_ticket_by_id(ticket_id)
    if not ticket:
        return "Ticket not found"
    message = ""
    if request.method == "POST":
        new_status = request.form.get("status")
        result = tm.update_ticket_status(ticket_id, new_status)
        if "updated" in result.lower() or "marked" in result.lower():
            return redirect(url_for("view_tickets"))
        else:
            message = result
    return render_template("update_ticket_status.html", ticket=ticket, message=message)


@app.route("/close_ticket/<ticket_id>", methods=["GET", "POST"])
def close_ticket(ticket_id):
    if "user" not in session:
        return redirect(url_for("login"))
    ticket = tm.get_ticket_by_id(ticket_id)
    if not ticket:
        return "Ticket not found"
    message = ""
    current_status = ticket.get_status()
    if current_status not in ["Resolved", "In Progress"]:
        message = "Cannot close yet. Ticket must be Resolved or In Progress first."
        return render_template("close_ticket.html", ticket=ticket, message=message)
    if request.method == "POST":
        tm.update_ticket_status(ticket_id, "Closed")
        return redirect(url_for("view_tickets"))
    return render_template("close_ticket.html", ticket=ticket, message=message)


@app.route("/ticket_history/<ticket_id>")
def ticket_history(ticket_id):
    if "user" not in session:
        return redirect(url_for("login"))
    ticket = tm.get_ticket_by_id(ticket_id)
    if not ticket:
        return "Ticket not found"
    history = tm.get_ticket_history(ticket_id)
    return render_template("ticket_history.html", ticket=ticket, history=history)


@app.route("/delete_ticket/<ticket_id>")
def delete_ticket(ticket_id):
    if "user" not in session:
        return redirect(url_for("login"))
    tm.delete_ticket(ticket_id)
    return redirect(url_for("view_tickets"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)