from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to db successful")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    return connection


connect = create_connection(
    'cis2368fall.c7cw0mymmpoj.us-east-1.rds.amazonaws.com',  
    'admin',  
    'ZlatanIbra1',  
    'cisfall2368db'  
)

@app.route('/api/investors', methods=['POST'])
def create_investor():
    data = request.get_json()
    connection = connect
    cursor = connection.cursor()
    cursor.execute("INSERT INTO investor (firstname, lastname) VALUES (%s, %s)", 
                   (data['firstname'], data['lastname']))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Investor added successfully!'}), 201

@app.route('/api/investors', methods=['GET'])
def get_investors():
    connection = connect
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM investor")
    investors = cursor.fetchall()
    cursor.close()
    return jsonify(investors), 200

@app.route('/api/investors/<int:id>', methods=['PUT'])
def update_investor(id):
    data = request.get_json()
    connection = connect
    cursor = connection.cursor()
    cursor.execute("UPDATE investor SET firstname = %s, lastname = %s WHERE id = %s", 
                   (data['firstname'], data['lastname'], id))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Investor updated successfully!'}), 200

@app.route('/api/investors/<int:id>', methods=['DELETE'])
def delete_investor(id):
    connection = connect
    cursor = connection.cursor()
    cursor.execute("DELETE FROM investor WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Investor deleted successfully!'}), 200


@app.route('/api/additems', methods=['POST'])
def add_items():
    data = request.get_json()  
    
    connection = connect
    cursor = connection.cursor()


    for item in data['items']:
        name = item['name']
        quantity = item['quantity']
        price = item['price']
        

        cursor.execute("SELECT * FROM inventory WHERE name = %s", (name,))
        existing_item = cursor.fetchone()
        
        if existing_item:
            cursor.execute("UPDATE inventory SET quantity = quantity + %s WHERE name = %s", (quantity, name))
        else:
            cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    
    connection.commit()  
    cursor.close()
    
    return jsonify({'message': 'Items added successfully!'}), 201


@app.route('/api/currentinventory', methods=['GET'])
def get_current_inventory():
    connection = connect
    cursor = connection.cursor(dictionary=True)
    

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    

    total_value = sum(item['quantity'] * item['price'] for item in items)
    
    cursor.close()
    
    return jsonify({
        'inventory': items,
        'total': total_value
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
