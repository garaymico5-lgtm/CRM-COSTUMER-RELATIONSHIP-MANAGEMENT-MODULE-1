from flask import Flask, render_template, request, redirect, session, url_for

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
        # Check kung existing na ang ID
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
# GLOBAL INSTANCES
# ============================================================

USERNAME = "admin"
PASSWORD = "1234"

crm = CRM()
im = InteractionManager()


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
    else:
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

    # find customer
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

@app.route("/interactions/add", methods=["GET", "POST"])
def add_interaction():
    if "user" not in session:
        return redirect(url_for("login"))

    message = ""
    customers = crm.get_all()

    if request.method == "POST":
        customer_id = request.form.get("customer_id")

        # Check if customer exists (linked)
        customer = None
        for c in crm.get_all():
            if c.get_id() == customer_id:
                customer = c
                break

        if not customer:
            message = "Customer not found. Please select a valid customer."
        else:
            interaction_type = request.form.get("interaction_type")
            date_time = request.form.get("date_time")
            notes = request.form.get("notes")
            message = im.add_interaction(customer_id, interaction_type, date_time, notes)

    return render_template("add_interaction.html", message=message, customers=customers)


@app.route("/interactions/view", methods=["GET", "POST"])
def view_interaction():
    if "user" not in session:
        return redirect(url_for("login"))

    customer = None
    interactions = []
    message = ""

    if request.method == "POST":
        customer_id = request.form.get("customer_id")

        for c in crm.get_all():
            if c.get_id() == customer_id:
                customer = c
                break

        if not customer:
            message = "Customer not found"
        else:
            interactions = im.get_by_customer(customer_id)
            if not interactions:
                message = "No interactions found for this customer"

    return render_template("view_interaction.html", customer=customer, interactions=interactions, message=message)


@app.route("/interactions/update/<interaction_id>", methods=["GET", "POST"])
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


@app.route("/interactions/delete/<interaction_id>")
def delete_interaction(interaction_id):
    if "user" not in session:
        return redirect(url_for("login"))

    # Get customer_id before deleting for redirect
    interaction = im.get_by_id(interaction_id)
    im.delete_interaction(interaction_id)
    return redirect(url_for("view_interaction"))


if __name__ == "__main__":
    app.run(debug=True)