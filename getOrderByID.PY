from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'onlinestoredb.cyazdfft3wxy.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Omen0634',
    'database': 'onlinestoredb'
}

@app.route('/get_order/<orderId>', methods=['GET'])
def get_order(orderId):
    if not orderId:
        return jsonify({'message': 'Please provide an orderId'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT oh.ORDER_ID AS orderId, op.PART_NAME AS partName, op.FACILITY_ID AS facilityId,
                op.SHIPMENT_METHOD_ENUM_ID AS shipmentMethodEnumId, op.CUSTOMER_PARTY_ID AS customerPartyId,
                oi.PRODUCT_ID AS productId, oi.ITEM_DESCRIPTION AS itemDescription,
                oi.QUANTITY AS quantity, oi.UNIT_AMOUNT AS unitAmount
            FROM Order_Header oh
            LEFT JOIN Order_Part op ON oh.ORDER_ID = op.ORDER_ID
            LEFT JOIN Order_Item oi ON oh.ORDER_ID = oi.ORDER_ID AND op.ORDER_PART_SEQ_ID = oi.ORDER_PART_SEQ_ID
            WHERE oh.ORDER_ID = %s
        """
        cursor.execute(query, (orderId,))
        order_info = cursor.fetchall()

        if not order_info:
            return jsonify({'message': 'Order not found'}), 404

        formatted_order = {
            'orderId': order_info[0]['orderId'],
            'partName': order_info[0]['partName'],
            'facilityId': order_info[0]['facilityId'],
            'shipmentMethodEnumId': order_info[0]['shipmentMethodEnumId'],
            'customerPartyId': order_info[0]['customerPartyId'],
            'item_details': [{
                'productId': item['productId'],
                'itemDescription': item['itemDescription'],
                'quantity': item['quantity'],
                'unitAmount': item['unitAmount']
            } for item in order_info]
        }

        return jsonify(formatted_order), 200

    except Exception as e:
        return jsonify({'message': 'Failed to fetch order', 'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port = 5004)