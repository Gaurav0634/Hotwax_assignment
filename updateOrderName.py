from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import mysql.connector

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'omen'  # Replace with your secret key
jwt = JWTManager(app)

db_config = {
    'host': 'onlinestoredb.cyazdfft3wxy.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Omen0634',
    'database': 'onlinestoredb'
}

# Protected endpoint example with JWT authentication
@app.route('/update_order', methods=['PUT'])
@jwt_required()  
def update_order():
    current_user = get_jwt_identity()
    data = request.json

    # Check if all required fields are present in the request body
    required_fields = ['orderId', 'orderName']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        update_query = "UPDATE Order_Header SET ORDER_NAME = %s WHERE ORDER_ID = %s"
        cursor.execute(update_query, (data['orderName'], data['orderId']))
        connection.commit()

        # Fetch updated order details
        select_query = """
            SELECT ORDER_ID, ORDER_NAME, CURRENCY_UOM_ID, SALES_CHANNEL_ENUM_ID, STATUS_ID,
                PRODUCT_STORE_ID, PLACED_DATE, APPROVED_DATE, GRAND_TOTAL
            FROM Order_Header
            WHERE ORDER_ID = %s
        """
        cursor.execute(select_query, (data['orderId'],))
        updated_order = cursor.fetchone()

        if not updated_order:
            return jsonify({'message': 'Order not found'}), 404

        return jsonify(updated_order), 200

    except Exception as e:
        return jsonify({'message': 'Failed to update order', 'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5005)
