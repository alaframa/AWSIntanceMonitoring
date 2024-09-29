from flask import render_template, jsonify
from function.aws import getAwsData, startAWS,stopAWS

def init_routes(app):
    @app.route('/')
    def index():
        # Call a function from funct1.py
        result = ""

        print  (result)
        return render_template('index.html', result=result)

    @app.route("/data")
    def dataAWS():
        data = getAwsData()
        
        return jsonify(data)
    
    @app.route('/action/<action>/<instanceId>')
    def action(action, instanceId):
        if action not in ['start', 'stop']:
            return jsonify({'msg': 'invalid request'}), 400  # Return 400 Bad Request

        # Get AWS data
        data = getAwsData()

        # Validate if the instanceId is in the AWS data
        instance = next((item for item in data if item['Instance ID'] == instanceId), None)

        if instance:
            if action == 'start':
                startAWS(instanceId)
            elif action == 'stop':
                stopAWS(instanceId)
            return jsonify({'msg': 'valid'}), 200  # Return 200 OK
        else:
            return jsonify({'msg': 'invalid instance ID'}), 400  # Return 400 Bad Request





