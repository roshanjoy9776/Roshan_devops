from flask import Flask, render_template, request, redirect, jsonify
from database import DB
from models import Bill
from services.billing_service import calculate_total

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bills.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB.init_app(app)

with app.app_context():
    DB.create_all()

@app.route('/')
def home():
    bills = Bill.query.all()
    return render_template('index.html', bills=bills)

@app.route('/add', methods=['POST'])
def add_bill():
    customer_name = request.form['customer_name']
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    total = calculate_total(quantity, price)

    new_bill = Bill(
        customer_name=customer_name,
        product_name=product_name,
        quantity=quantity,
        price=price,
        total=total
    )

    DB.session.add(new_bill)
    DB.session.commit()

    return redirect('/')

@app.route('/api/bills', methods=['GET'])
def get_bills():

    bills = Bill.query.all()

    output = []

    for bill in bills:
        bill_data = {
            "id": bill.id,
            "customer_name": bill.customer_name,
            "product_name": bill.product_name,
            "quantity": bill.quantity,
            "price": bill.price,
            "total": bill.total
        }

        output.append(bill_data)

    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)