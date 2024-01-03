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

def generate_unique_order_part_seq_id():
    return str(uuid.uuid4())

def create_customer_party_if_not_exists(cursor, customer_party_id):
    # Check if the customer party exists
    cursor.execute("SELECT PARTY_ID FROM Party WHERE PARTY_ID = %s", (customer_party_id,))
    existing_party = cursor.fetchone()

    if not existing_party:
        # Generate a new PARTY_ID
        new_party_id = str(uuid.uuid4())

        # Insert a new entry in the Party table for the customer
        cursor.execute("INSERT INTO Party (PARTY_ID) VALUES (%s)", (new_party_id,))
        return new_party_id
    else:
        return customer_party_id

@app.route('/add_order_items', methods=['POST'])
def add_order_items():
    data = request.json

    # Check for required fields
    required_fields = ['orderId', 'partName', 'customerPartyId', 'item_details']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400

    # Set default shipment method if not provided
    shipment_method = data.get('shipmentMethodEnumId', 'ShMthGround')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        order_id = data['orderId']
        part_name = data['partName']
        customer_party_id = data['customerPartyId']
        facility_id = data.get('facilityId')
        
        # Check if the order exists in Order_Header table
        cursor.execute("SELECT ORDER_ID FROM Order_Header WHERE ORDER_ID = %s", (order_id,))
        existing_order = cursor.fetchone()

        if not existing_order:
            # Create the order in Order_Header table if it doesn't exist
            cursor.execute("INSERT INTO Order_Header (ORDER_ID) VALUES (%s)", (order_id,))
        
        # Check and create customer party if not exists
        customer_party_id = create_customer_party_if_not_exists(cursor, customer_party_id)

        # Generate unique order part sequence ID
        order_part_seq_id = generate_unique_order_part_seq_id()

        # Insert into Order_Part table
        order_part_query = """
            INSERT INTO Order_Part 
            (ORDER_ID, ORDER_PART_SEQ_ID, PART_NAME, CUSTOMER_PARTY_ID, FACILITY_ID, SHIPMENT_METHOD_ENUM_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(order_part_query, (
            order_id, order_part_seq_id, part_name, customer_party_id, facility_id, shipment_method
        ))

        # Insert items into Order_Item table
        if 'item_details' in data:
            for item in data['item_details']:
                product_id = item.get('productId')
                description = item.get('itemDescription')
                quantity = item.get('quantity')
                unit_amount = item.get('unitAmount')

                order_item_query = """
                    INSERT INTO Order_Item 
                    (ORDER_ID, ORDER_ITEM_SEQ_ID, ORDER_PART_SEQ_ID, PRODUCT_ID, ITEM_DESCRIPTION, QUANTITY, UNIT_AMOUNT)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(order_item_query, (
                    order_id, str(uuid.uuid4()), order_part_seq_id, product_id, description, quantity, unit_amount
                ))

        connection.commit()
        return jsonify({'orderId': order_id, 'orderPartSeqId': order_part_seq_id}), 201

    except Exception as e:
        return jsonify({'message': 'Failed to add order items', 'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
