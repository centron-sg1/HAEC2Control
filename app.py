from flask import Flask, jsonify, request
import boto3
from datetime import datetime

app = Flask(__name__)


# ✅ Create EC2 client
def get_ec2(region):
    return boto3.client("ec2", region_name=region)


# ✅ Helper: format EC2 instance data
def format_instances(reservations):
    instances = []

    for r in reservations:
        for i in r["Instances"]:
            name = None

            # Get Name tag if exists
            if "Tags" in i:
                for t in i["Tags"]:
                    if t["Key"] == "Name":
                        name = t["Value"]

            instances.append({
                "id": i["InstanceId"],
                "name": name,
                "state": i["State"]["Name"]
            })

    return instances


# ✅ Root test endpoint
@app.route("/")
def home():
    return "AWS EC2 Control API (boto3) running"


# ✅ CONTROL endpoint (for Home Assistant REST switch)
@app.route("/control", methods=["POST"])
def control():
    try:
        data = request.json

        region = data.get("region")
        instance_id = data.get("instance_id")
        action = data.get("action")

        if not all([region, instance_id, action]):
            return jsonify({"error": "Missing required fields"}), 400

        ec2 = get_ec2(region)

        if action == "start":
            ec2.start_instances(InstanceIds=[instance_id])
        elif action == "stop":
            ec2.stop_instances(InstanceIds=[instance_id])
        elif action == "reboot":
            ec2.reboot_instances(InstanceIds=[instance_id])
        else:
            return jsonify({"error": "Invalid action"}), 400

        return jsonify({
            "result": action,
            "instance_id": instance_id,
            "region": region,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ STATUS endpoint (used by HA switch state + sensors)
@app.route("/status/<region>/<instance_id>")
def status(region, instance_id):
    try:
        ec2 = get_ec2(region)

        response = ec2.describe_instances(InstanceIds=[instance_id])
        instances = format_instances(response["Reservations"])

        if not instances:
            return jsonify({"error": "Instance not found"}), 404

        instance = instances[0]

        return jsonify({
            "id": instance["id"],
            "name": instance["name"],
            "state": instance["state"],
            "last_updated": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ LIST ALL INSTANCES (optional but useful)
@app.route("/instances/<region>")
def list_instances(region):
    try:
        ec2 = get_ec2(region)

        response = ec2.describe_instances()
        instances = format_instances(response["Reservations"])

        return jsonify({
            "count": len(instances),
            "instances": instances
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Run Flask app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
