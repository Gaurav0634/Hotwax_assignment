
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
import mysql.connector
import base64

app = Flask(__name__)

# Replace with your encryption key
encryption_key = b'jrd_vGkf62C7D9vVNR48WvRZx62i_VHIu1Bo0V7zgQg='

# Replace with your database credentials
db_config = {
    'host': 'onlinestoredb.cyazdfft3wxy.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Omen0634',
    'database': 'onlinestoredb'
}

# Define cipher_suite globally
cipher_suite = Fernet(encryption_key)

# Encrypts the credit card number
def encrypt_credit_card(credit_card_number):
    return cipher_suite.encrypt(credit_card_number.encode())

@app.route('/add_credit_card', methods=['POST'])
def add_credit_card():
    data = request.json

    # Check for required fields and validate data
    required_fields = ['orderId', 'creditCardNumber']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Encrypt the credit card number before storing in the database
        encrypted_credit_card = encrypt_credit_card(data['creditCardNumber'])

        # Insert the encrypted credit card into the database for the specified order
        cursor.execute("UPDATE Order_Header SET CREDIT_CARD_ENCRYPTED = %s WHERE ORDER_ID = %s",
                       (encrypted_credit_card, data['orderId']))
        
        # Commit changes
        connection.commit()

        return jsonify({'message': 'Credit card information added successfully'}), 201

    except Exception as e:
        return jsonify({'message': 'Failed to add credit card information', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_order_credit_card/<order_id>', methods=['GET'])
def get_order_credit_card(order_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT CREDIT_CARD_ENCRYPTED FROM Order_Header WHERE ORDER_ID = %s", (order_id,))
        credit_card_encrypted = cursor.fetchone()

        if credit_card_encrypted:
            decrypted_card = cipher_suite.decrypt(base64.urlsafe_b64decode(credit_card_encrypted[0]))
            return jsonify({'order_id': order_id, 'credit_card': decrypted_card.decode()}), 200
        else:
            return jsonify({'message': 'Credit card information not found for the given order ID'}), 404

    except Exception as e:
        error_msg = "Failed to fetch credit card information"
        if e:
            error_msg += f": {str(e)}"
        print("Error:", error_msg)  # Log the error for debugging
        return jsonify({'message': error_msg}), 500

    finally:
        # Close connections
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
