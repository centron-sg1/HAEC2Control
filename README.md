# AWS EC2 Control for Home Assistant

Control and monitor AWS EC2 instances directly from Home Assistant using a lightweight REST API powered by Flask and Boto3.

## Features

- Start EC2 instances
- Stop EC2 instances
- Reboot EC2 instances
- Monitor instance status
- List all EC2 instances in a region
- Supports multiple AWS regions
- Designed for Home Assistant Add-on deployment

## API Endpoints

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

### Get Instance Status

```http
GET /status/<region>/<instance_id>
```

Example:

```http
GET /status/ap-southeast-2/i-0123456789abcdef0
```

Response:

```json
{
  "id": "i-0123456789abcdef0",
  "name": "HomeAssistant-Server",
  "state": "running",
  "last_updated": "2026-07-15T10:00:00"
}
```

---

### Control an Instance

```http
POST /control
```

Request Body:

```json
{
  "region": "ap-southeast-2",
  "instance_id": "i-xxxxxxxxxx",
  "action": "start"
}
```

Supported actions:

- start
- stop
- reboot

Response:

```json
{
  "result": "start",
  "instance_id": "i-0123456789abcdef0",
  "region": "ap-southeast-2",
  "timestamp": "2026-07-15T10:00:00"
}
```

## Home Assistant Add-on Configuration

Add your AWS credentials in the add-on configuration:

```yaml
aws_access_key_id: YOUR_ACCESS_KEY
aws_secret_access_key: YOUR_SECRET_KEY
```

### Required AWS Permissions

The IAM user or role used by this add-on requires permissions similar to:

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

## Installation

### Add Custom Repository

In Home Assistant:

1. Navigate to **Settings** → **Add-ons**
2. Click **Repositories**
3. Add this repository URL
4. Install **AWS EC2 Control**
5. Configure AWS credentials
6. Start the add-on

## Example Home Assistant REST Sensor

```yaml
sensor:
  - platform: rest
    resource: http://homeassistant.local:5000/status/ap-southeast-2/i-0123456789abcdef0
    name: AWS Instance Status
    value_template: "{{ value_json.state }}"
```

## Example REST Command

```yaml
rest_command:
  start_aws_instance:
    url: "http://homeassistant.local:5000/control"
    method: POST
    content_type: "application/json"
    payload: >
      {
        "region":"ap-southeast-2",
        "instance_id":"i-0123456789abcdef0",
        "action":"start"
      }
```

## Security Notes

- Store AWS credentials securely.
- Use a dedicated IAM user with minimum required permiss*ons.
- Do not expose the*API directly to the internet.
- Re*trict network access to trusted sy*tems.

## Troubleshooting

### Unable to locate credentials

Verify t*e add-on configuration contains va*id:

```yaml
aws_access_key_id:
aw*_secret_access_key:
```

### AccessDenied

Ensure the IAM user has:

* ec2:DescribeInstances
- ec2:Start*nstances
- ec2:StopInstances
- ec2*RebootInstances

### API Not Reach*ble

Verify the add-on is running *nd listening on port 5000.

Test:
*```bash
curl http://HOME_ASSISTANT_IP:5000/
```

Expected response:

*``text
AWS EC2 Control API (boto3)*running
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
      {"action":"start","region":"ap-southeast-2","instance_id":"ii-0123456789abcdef0"}

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
