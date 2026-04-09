from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
        if not name or not contact:
            return "Invalid name or contact"

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


crm = CRM()

# ===== ROUTES =====

@app.route("/")
def home():
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
    customers = crm.get_all()
    return render_template("view.html", customers=customers)


@app.route("/delete/<cid>")
def delete(cid):
    crm.delete_customer(cid)
    return redirect(url_for("view"))


# RUN
if __name__ == "__main__":
    app.run(debug=True)