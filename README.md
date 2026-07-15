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

## Add the Repository t* Home Assistant

1. Open **Home As*istant**.
2. Navigate to:

   **Settings** → **Add-ons** → **Add-on Store**

3. Click the three*dot menu in the top-right corner.
*. Select **Repositories**.
5. Add *he repository URL:

```text
https://github.com/centron-sg1/HAEC2Control
```

6. Click **Add**.

---

## Install the Add-on

1. Locate **AWS*EC2 Control** in the Add-on Store.*2. Click **Install**.
3. Wait for *he Docker image to build.

---

##*Configure the Add-on

Open the add*on configuration tab and enter:

`*`yaml
aws_access_key_id: YOUR_ACCE*S_KEY_ID
aws_secret_access_key: YO*R_SECRET_ACCESS_KEY
```

Example:
*```yaml
aws_access_key_id: AKIAxxx*xxxxxxxxxxxx
aws_secret_access_key* abcdefghijklmnopqrstuvwxyz1234567*9
```

Click **Save**.

---

## St*rt the Add-on

1. Click **Start**.*2. Open the***Logs** tab*

You should see something similar*to:

```text
* Running on all addr*sses (0.0.0.0)
* Running on http://0.0.0.0:5000
```

---

## Verify I*stallation

Open a browser and nav*gate to:

```text
http*//HOME_ASSISTANT_IP:5000/
```

Exa*ple:

```text
http://192.168.2.4:5000/
```

Expected response:

```te*t
AWS EC2 Control API (boto3) runn*ng
```

---

## Test AWS Connectiv*ty

List all EC2 instances in a re*ion:

```text
http://HOME_ASSISTAN*_IP:5000/instances/ap-southeast-2
*``

Example response:

```json
{
 *"count": 1,
  "instances": [
    {
      "id": "i-03e74250d9e20285e",
      "name": "Sydney Server",
      "state": "running"
    }
  ]
}
`*`

---

## Create a Home Assistant*Sensor

Add the following to your *onfiguration:

```yaml
sensor:
  -*platform: rest
    name: EC2 Sydne* State
    unique_id: ec2_sydney_s*ate
    resource: http://localhost:5000/status/ap-southeast-2/i-03e74250d9e20285e
    method: GET
    va*ue_template: >
      {% set s = va*ue_json.state %}
      {% if s == *running' %} Running ✅
      {% eli* s == 'pending' %} Starting ⏳
    * {% elif s == 'stopping' %} Stoppi*g ⏳
      {% elif s == 'stopped' %* Stopped ⛔
      {% else %} {{ s }*
      {% endif %}
    scan_interv*l: 30
```

Restart Home Assistant.*
---

## Create a Control Switch

*dd the following to your configura*ion:

```yaml
switch:
  - platform* rest
    name: EC2_Switch_Sydney
*   resource: http://localhost:5000/control
    method: POST

    body*on: >
      {"action":"start","reg*on":"ap-southeast-2","instance_id"*"i-03e74250d9e20285e"}

    body_o*f: >
      {"action":"stop","regio*":"ap-southeast-2","instance_id":"*-03e74250d9e20285e"}

    headers:*      Content-Type: application/js*n

    state_resource: http://localhost:5000/status/ap-southeast-2/i-03e74250d9e20285e

    is_on_templa*e: "{{ value_json.state == 'runnin*' }}"

    scan_interval: 30
```

*estart Home Assistant.

A switch w*ll now appear on your dashboard al*owing you to start and stop your E*2 instance.

---

## Troubleshooti*g

### Unable to locate credential*

Verify:

```yaml
aws_access_key_*d:
aws_secret_access_key:
```

hav* been configured correctly.

### A*cessDenied

Ensure your IAM user h*s:

- ec2:DescribeInstances
- ec2:*tartInstances
- ec2:StopInstances
* ec2:RebootInstances

### Add-on s*arts but API is unreachable

Check*the add-on logs and verify port 50*0 is listening:

```bash
curl http*//localhost:5000/
```

Expected re*ponse:

```text
AWS EC2 Control AP* (boto3) running
```

### No insta*ces returned

Verify:
- The region*is correct.
- The IAM user has*EC2 permissions.
- The instance*exists*in the selected region.
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

## Example Home Assistant Sensor

The following REST sensor displays the current state of an EC2 instance in a user-friendly format, Add to your configuration.yaml.

```yaml
sensor:
  - platform: rest
    name: EC2 Sydney State
    unique_id: ec2_sydney_state
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
    name: EC2_Switch_Sydney
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

## License

GPL-3
