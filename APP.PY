from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "secret123" 


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
    

USERNAME = "admin"
PASSWORD = "1234"


crm = CRM()


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


# RUN
if __name__ == "__main__":
    app.run(debug=True)