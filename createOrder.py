from flask import Flask, request, jsonify
import mysql.connector
import uuid

app = Flask(__name__)

db_config = {
    'host': 'onlinestoredb.cyazdfft3wxy.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Omen0634',
    'database': 'onlinestoredb'
}

# Function to generate a unique order ID
def generate_unique_order_id():
    return str(uuid.uuid4())

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json

    if 'orderName' not in data or 'placedDate' not in data:
        return jsonify({'message': 'Order name and placed date are required'}), 400

    # Setting defaults for unspecified parameters
    currency_uom_id = data.get('currencyUomId', 'USD')
    status_id = data.get('statusId', 'OrderPlaced')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Generating a unique ORDER_ID
        order_id = generate_unique_order_id()

        insert_query = """
            INSERT INTO Order_Header 
            (ORDER_ID, ORDER_NAME, PLACED_DATE, APPROVED_DATE, STATUS_ID, 
            CURRENCY_UOM_ID, PRODUCT_STORE_ID, SALES_CHANNEL_ENUM_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            order_id,
            data['orderName'],
            data['placedDate'],
            data.get('approvedDate'),
            status_id,
            currency_uom_id,
            data.get('productStoreId'),
            data.get('salesChannelEnumId')
        ))

        connection.commit()

        return jsonify({'orderId': order_id}), 201  
    except Exception as e:
        return jsonify({'message': 'Failed to create order', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port = 5002)
