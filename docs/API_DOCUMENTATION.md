## **Overview**  
This API provides endpoints to manage Telegram bot interactions, including webhook setup, message handling, and connection status checks. Built with **Flask**, it supports seamless integration with Telegram's Bot API.  

---

## **Base URL**  
`https://example.com`  

---

## **Authentication**  
- All endpoints (except `/webhook/<token>`) require **user authentication** (implementation depends on your setup).  
- The `/webhook/<token>` endpoint uses the **bot token** for verification.  

---

## **API Endpoints**  

### **1. Telegram Webhook Handler**  
**Endpoint:** `POST /webhook/<token>`  
**Description:**  
Handles incoming Telegram bot updates (messages, commands).  

#### **Request:**  
| Parameter | Type   | Required | Description          |  
|-----------|--------|----------|----------------------|  
| `token`   | string | ✅       | Bot token for auth   |  

**Request Body (Telegram Update Object):**  
```json
{
  "update_id": 123,
  "message": {
    "message_id": 456,
    "text": "/start",
    "chat": { "id": 789 }
  }
}
```

#### **Responses:**  
| Status Code | Response Body         | Description                     |  
|-------------|-----------------------|---------------------------------|  
| `200`       | `{"status": "ok"}`    | Update processed successfully   |  
| `400`       | `{"status": "error"}` | Invalid request format          |  
| `500`       | `{"status": "error"}` | Internal server error           |  

---

### **2. Set Telegram Webhook**  
**Endpoint:** `POST /api/telegram/set_webhook`  
**Description:**  
Configures a Telegram bot webhook and tests the connection.  

#### **Request Body (JSON):**  
| Field        | Type   | Required | Description               |  
|--------------|--------|----------|---------------------------|  
| `user_id`    | string | ✅       | Unique user identifier    |  
| `bot_token`  | string | ✅       | Telegram bot token        |  
| `chat_id`    | string | ✅       | Target chat ID            |  

**Example:**  
```json
{
  "user_id": "user123",
  "bot_token": "123:ABC-DEF",
  "chat_id": "-100123456"
}
```

#### **Responses:**  
| Status Code | Response Body                                   | Description                     |  
|-------------|-------------------------------------------------|---------------------------------|  
| `200`       | `{"success": true, "message": "Webhook set"}`   | Webhook configured successfully |  
| `400`       | `{"success": false, "error": "Invalid data"}`   | Missing/invalid parameters      |  
| `500`       | `{"success": false, "error": "Failed to set"}`  | Telegram API error              |  

---

### **3. Send Telegram Message**  
**Endpoint:** `POST /api/telegram/send_message`  
**Description:**  
Sends a message via the connected Telegram bot.  

#### **Request Body (JSON):**  
| Field          | Type   | Required | Description               |  
|----------------|--------|----------|---------------------------|  
| `user_id`      | string | ✅       | User who owns the bot      |  
| `message_text` | string | ✅       | Text to send              |  

**Example:**  
```json
{
  "user_id": "user123",
  "message_text": "Hello, world!"
}
```

#### **Responses:**  
| Status Code | Response Body                                   | Description                     |  
|-------------|-------------------------------------------------|---------------------------------|  
| `200`       | `{"success": true, "message": "Message sent"}`  | Message delivered               |  
| `400`       | `{"success": false, "error": "Invalid data"}`   | Missing `user_id` or `message`  |  
| `500`       | `{"success": false, "error": "Failed to send"}` | Telegram API error              |  

---

### **4. Disconnect Telegram Bot**  
**Endpoint:** `POST /api/telegram/disconnect`  
**Description:**  
Removes the bot configuration for a user.  

#### **Request Body (JSON):**  
| Field      | Type   | Required | Description               |  
|------------|--------|----------|---------------------------|  
| `user_id`  | string | ✅       | User to disconnect        |  

**Example:**  
```json
{
  "user_id": "user123"
}
```

#### **Responses:**  
| Status Code | Response Body                                      | Description                     |  
|-------------|----------------------------------------------------|---------------------------------|  
| `200`       | `{"success": true, "message": "Disconnected"}`     | Bot disconnected successfully   |  
| `404`       | `{"success": false, "error": "No config found"}`   | User has no active bot          |  

---

### **5. Check Bot Connection Status**  
**Endpoint:** `GET /api/telegram/status`  
**Description:**  
Checks if a user has an active Telegram bot connection.  

#### **Query Parameters:**  
| Parameter | Type   | Required | Description               |  
|-----------|--------|----------|---------------------------|  
| `user_id` | string | ✅       | User to check             |  

**Example Request:**  
```
GET /api/telegram/status?user_id=user123
```

#### **Responses:**  
| Status Code | Response Body                                      | Description                     |  
|-------------|----------------------------------------------------|---------------------------------|  
| `200`       | `{"success": true, "status": "connected"}`         | Bot is connected               |  
| `200`       | `{"success": true, "status": "disconnected"}`      | No active bot for user          |  

---

## **Error Handling**  
| Status Code | Error Type               | Resolution Steps                     |  
|-------------|--------------------------|--------------------------------------|  
| `400`       | Invalid/Missing Data     | Verify request body/query params     |  
| `404`       | User Not Found           | Check `user_id`                      |  
| `500`       | Telegram API Failure     | Retry or check bot token validity    |  

---

## **Example Workflow**  
1. **Set Webhook** → `POST /api/telegram/set_webhook`  
2. **Send Message** → `POST /api/telegram/send_message`  
3. **Check Status** → `GET /api/telegram/status?user_id=user123`  
4. **Disconnect** → `POST /api/telegram/disconnect`  

---

## **Interactive Documentation**  
For real-time testing, use:  
- **Postman Collection** (import via OpenAPI/Swagger)  
- **FastAPI Auto-Docs** (if integrated) at `/docs`  

---