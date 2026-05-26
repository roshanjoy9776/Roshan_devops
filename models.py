from database import DB

class Bill(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    customer_name = DB.Column(DB.String(100))
    product_name = DB.Column(DB.String(100))
    quantity = DB.Column(DB.Integer)
    price = DB.Column(DB.Float)
    total = DB.Column(DB.Float)

    def __repr__(self):
        return f"<Bill {self.customer_name}>"