class WS{
    constructor(WS) {
        this._Initialize();
        this._
      }
    _Initialize() {

            // Создаем новый экземпляр WebSocket
        var websocket = new WebSocket('ws://localhost:8765');

        // Обработчик события открытия соединения
        websocket.onopen = function(event) {
            console.log("WebSocket соединение открыто");
        };

        // Обработчик сообщений
        websocket.onmessage = function(event) {
            console.log("Получено сообщение: " + event.data);
        };

        // Обработчик ошибок
        websocket.onerror = function(event) {
            console.log("Ошибка WebSocket: " + event.data);
        };

    return this.websocket
    }

    _sendMessage(message) {
        // Отправка сообщения на сервер
        if (this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(message);
        } else {
            console.log("WebSocket не открыт");
        }
    }
};



