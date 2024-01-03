from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'onlinestoredb.cyazdfft3wxy.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Omen0634',
    'database': 'onlinestoredb'
}

@app.route('/get_all_orders', methods=['GET'])
def get_all_orders():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT oh.ORDER_ID AS orderId, oh.ORDER_NAME AS orderName, oh.CURRENCY_UOM_ID AS currencyUom,
                oh.SALES_CHANNEL_ENUM_ID AS salesChannelEnumId, oh.STATUS_ID AS statusId,
                oh.PLACED_DATE AS placedDate, oh.GRAND_TOTAL AS grandTotal,
                p.PARTY_ID AS customerPartyId, pe.FIRST_NAME AS firstName, pe.MIDDLE_NAME AS middleName,
                pe.LAST_NAME AS lastName,
                op.ORDER_PART_SEQ_ID AS orderPartSeqId, op.PART_NAME AS partName, op.STATUS_ID AS partStatusId,
                op.FACILITY_ID AS facilityId, op.SHIPMENT_METHOD_ENUM_ID AS shipmentMethodEnumId,
                op.PART_TOTAL AS partTotal,
                oi.ORDER_ITEM_SEQ_ID AS orderItemSeqId, oi.PRODUCT_ID AS productId,
                oi.ITEM_DESCRIPTION AS itemDescription, oi.QUANTITY AS quantity, oi.UNIT_AMOUNT AS unitAmount
            FROM Order_Header oh
            LEFT JOIN Order_Part op ON oh.ORDER_ID = op.ORDER_ID
            LEFT JOIN Order_Item oi ON oh.ORDER_ID = oi.ORDER_ID AND op.ORDER_PART_SEQ_ID = oi.ORDER_PART_SEQ_ID
            LEFT JOIN Party p ON op.CUSTOMER_PARTY_ID = p.PARTY_ID
            LEFT JOIN Person pe ON p.PARTY_ID = pe.PARTY_ID
            LEFT JOIN Product pr ON oi.PRODUCT_ID = pr.PRODUCT_ID
            ORDER BY oh.ORDER_ID, op.ORDER_PART_SEQ_ID, oi.ORDER_ITEM_SEQ_ID
        """
        cursor.execute(query)
        orders = cursor.fetchall()

        return jsonify({'orders': orders}), 200

    except Exception as e:
        return jsonify({'message': 'Failed to fetch orders', 'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5003)
