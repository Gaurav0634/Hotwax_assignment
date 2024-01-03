from flask import Flask, request, jsonify
import mysql.connector
from flask import Flask
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'onlinestoredb.cyazdfft3wxy.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Omen0634',
    'database': 'onlinestoredb'
}

@app.route('/create_person', methods=['POST'])
def create_person():
    data = request.json
    if 'PARTY_ID' not in data:
        return jsonify({'message': 'PARTY_ID is required'}), 400

    salutation = data.get('SALUTATION')
    first_name = data.get('FIRST_NAME')
    middle_name = data.get('MIDDLE_NAME')
    last_name = data.get('LAST_NAME')
    gender = data.get('GENDER')
    birth_date = data.get('BIRTH_DATE')
    marital_status_enum_id = data.get('MARITAL_STATUS_ENUM_ID')
    employment_status_enum_id = data.get('EMPLOYMENT_STATUS_ENUM_ID')
    occupation = data.get('OCCUPATION')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        
        cursor.execute("INSERT INTO Party (PARTY_ID) VALUES (%s)", (data['PARTY_ID'],))
        connection.commit()

        cursor.execute("""
            INSERT INTO Person (PARTY_ID, SALUTATION, FIRST_NAME, MIDDLE_NAME, LAST_NAME, 
                                GENDER, BIRTH_DATE, MARITAL_STATUS_ENUM_ID, 
                                EMPLOYMENT_STATUS_ENUM_ID, OCCUPATION) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['PARTY_ID'], salutation, first_name, middle_name, last_name,
              gender, birth_date, marital_status_enum_id,
              employment_status_enum_id, occupation))
        connection.commit()

        return jsonify({'message': 'Person created successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to create Person', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close() 


@app.route('/persons', methods=['GET'])
def get_persons():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Person")
        persons = cursor.fetchall()

        return jsonify(persons), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch persons', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/persons/<party_id>', methods=['GET'])
def get_person(party_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Person WHERE PARTY_ID = %s", (party_id,))
        person = cursor.fetchone()

        if person:
            return jsonify(person), 200
        else:
            return jsonify({'message': 'Person not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to fetch person', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/persons/<party_id>', methods=['PUT'])
def update_person(party_id):
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided for update'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        update_query = """
            UPDATE Person SET 
            SALUTATION = %s, 
            FIRST_NAME = %s, 
            MIDDLE_NAME = %s, 
            LAST_NAME = %s, 
            GENDER = %s, 
            BIRTH_DATE = %s, 
            MARITAL_STATUS_ENUM_ID = %s, 
            EMPLOYMENT_STATUS_ENUM_ID = %s, 
            OCCUPATION = %s 
            WHERE PARTY_ID = %s
        """

        cursor.execute(update_query, (
            data.get('SALUTATION'),
            data.get('FIRST_NAME'),
            data.get('MIDDLE_NAME'),
            data.get('LAST_NAME'),
            data.get('GENDER'),
            data.get('BIRTH_DATE'),
            data.get('MARITAL_STATUS_ENUM_ID'),
            data.get('EMPLOYMENT_STATUS_ENUM_ID'),
            data.get('OCCUPATION'),
            party_id  
        ))

        connection.commit()

        return jsonify({'message': 'Person updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update person', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
