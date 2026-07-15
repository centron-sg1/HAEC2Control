# AWS EC2 Control for Home Assistant

Control and monitor AWS EC2 instances directly from Home Assistant using a lightweight REST API powered by Flask and Boto3.
Creates a container in Home Assistant, running a rest api that is accessable from Home assistant using "rest" commands

## Features

- Start EC2 instances
- Stop EC2 instances
- Reboot EC2 instances
- Monitor instance status
- List all EC2 instances in a region
- Supports multiple AWS regions
- Designed for Home Assistant Add-on deployment

## API Endpoints
# Installation

## Prerequisites

Before installing this add-on, ensure you have:

- Home Assistant OS or Home Assistant Supervised
- An AWS account
- At least one EC2 instance
- An AWS IAM user with programmatic access
- AWS Access Key ID and Secret Access Key

## Create an AWS IAM User

1. Log in to the AWS Console.
2. Navigate to **IAM** → **Users**.
3. Create a new user.
4. Enable **Programmatic Access**.
5. Assign the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:RebootInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

6. Save the generated:
 * - Access Key ID
   - Secret Acces* Key

---

## Add the Repository to Home Assistant

1. Open **Home Assistant**.
2. Navigate to:

   **Settings** → **Add-ons** → **Add-on Store**

3. Click the three*dot menu in the top-right corner.
4. Select **Repositories**.
5. Add the repository URL:

```text
https://github.com/centron-sg1/HAEC2Control
```

6. Click **Add**.

---

## Install the Add-on

1. Locate "AWS EC2 Control" in the Add-on Store.
2. <img alt="image" src="https://github.com/user-attachments/assets/7576934e-e3c8-4e37-a5fb-bc8bf4481ea3" />
3. Click "Install".
4. Wait for the Docker image to build.

---
<img width="1162" height="599" alt="image" src="https://github.com/user-attachments/assets/27355732-0f66-4966-a323-8a675e508afa" />

## Configure the Add-on
<img alt="image" src="https://github.com/user-attachments/assets/b3ff7c00-3f15-4a15-a842-b8ea3d685482" />
Open the add-on configuration tab and enter:


aws_access_key_id: YOUR_ACCESS_KEY_ID
aws_secret_access_key: YOUR_SECRET_ACCESS_KEY


Example:
aws_access_key_id: AKIAxxx*xxxxxxxxxxxx
aws_secret_access_key* abcdefghijklmnopqrstuvwxyz123456789

Click "Save".

---

## Start the Add-on

1. Click "Start".
2. Open the "Logs" tab

You should see something similar to:


* Running on all addresses (0.0.0.0)
* Running on http://HOME_ASSISTANT_IP:5000


---

## Verify Installation

Open a browser and navigate to:

```text
http://HOME_ASSISTANT_IP:5000/
```

Expected response:

```text
AWS EC2 Control API (boto3) runnnng
```

---

## Test AWS Connectivity

List all EC2 instances in a region:

```text
http://HOME_ASSISTANT_IP:5000/instances/ap-southeast-2
*``

Example response:

```json
{
 *"count": 1,
  "instances": [
    {
      "id": "i-0123456789abcdef0",
      "name": "Your Server",
      "state": "running"
    }
  ]
}
`*`

---

## Example Home Assistant Sensor

The following REST sensor displays the current state of an EC2 instance in a user-friendly format, Add to your configuration.yaml.

```yaml
sensor:
  - platform: rest
    name: EC2 Sydney State
    unique_id: ec2_yourserver_state
    resource: http://localhost:5000/status/ap-southeast-2/i-0123456789abcdef0
    method: GET
    value_template: >
      {% set s = value_json.state %}
      {% if s == 'running' %} Running ✅
      {% elif s == 'pending' %} Starting ⏳
      {% elif s == 'stopping' %} Stopping ⏳
      {% elif s == 'stopped' %} Stopped ⛔
      {% else %} {{ s }}
      {% endif %}
    scan_interval: 30
```

### Example States

| AWS State | Home Assistant Display |
|------------|------------------------|
| running | Running ✅ |
| pending | Starting ⏳ |
| stopping | Stopping ⏳ |
| stopped | Stopped ⛔ |

This sensor polls the API every 30 seconds and converts the raw AWS EC2 state into a more readable status for dashboards, automations, and notifications.

## Example Home Assistant Switch

The following REST switch allows Home Assistant to start and stop an AWS EC2 instance directly from the dashboard, Add to your configuration.yaml..

```yaml
switch:
  - platform: rest
    name: EC2_Switch_YourServer
    resource: http://localhost:5000/control
    method: POST

    body_on: >
      {"action":"start","region":"ap-southeast-2","instance_id":"i-0123456789abcdef0"}

    body_off: >
      {"action":"stop","region":"ap-southeast-2","instance_id":"i-0123456789abcdef0"}

    headers:
      Content-Type: application/json

    state_resource: http://localhost:5000/status/ap-southeast-2/i-0123456789abcdef0

    is_on_template: "{{ value_json.state == 'running' }}"

    scan_interval: 30
```

### How It Works

When the switch is turned **On**, Home Assistant sends:

```json
{
  "action": "start",
  "region": "ap-southeast-2",
  "instance_id": "i-0123456789abcdef0"
}
```

When the switch is turned **Off**, Home Assistant sends:

```json
{
  "action": "stop",
  "region": "ap-southeast-2",
  "instance_id": "i-0123456789abcdef0"
}
```

The switch state is automatically updated every 30 seconds using:

```http
GET /status/ap-southeast-2/i-0123456789abcdef0
```

### Dashboard Result

The switch will:

- ✅ Turn ON when the EC2 instance is running
- ⏳ Show updating while the instance is starting
- ⏳ Show updating while the instance is stopping
- ⛔ Turn OFF when the EC2 instance is stopped

This provides a simple and native Home Assistant switch for controlling EC2 instances without requiring custom integrations.

## Troubleshooting

### Unable to locate credential

Verify:

```yaml
aws_access_key_id:
aws_secret_access_key:
```

have been configured correctly.

### AccessDenied

Ensure your IAM user h*s:

- ec2:DescribeInstances
- ec2:StartInstances
- ec2:StopInstances
- ec2:RebootInstances

### Add-on starts but API is unreachable

Check the add-on logs and verify port 5000 is listening:

```bash
curl http://localhost:5000/
```

Expected response:

```text
AWS EC2 Control API (boto3) running
```

### No instances returned

Verify:
- The region is correct.
- The IAM user has EC2 permissions.
- The instance exists in the selected region.
### Health Check

```http
GET /
```

Response:

```text
AWS EC2 Control API (boto3) running
```

---

### List Instances

```http
GET /instances/<region>
```

Example:

```http
GET /instances/ap-southeast-2
```

Response:

```json
{
  "count": 2,
  "instances": [
    {
      "id": "i-0123456789abcdef0",
      "name": "HomeAssistant-Server",
      "state": "running"
    }
  ]
}
```

---

```


## License

GPL-3
