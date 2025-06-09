class WS{
    constructor(WS) {
      this._Initialize();
    }
    _Initialize() {
  
            // Создаем новый экземпляр WebSocket
        this._websocket = new WebSocket('ws://localhost:8765');
  
        // Обработчик события открытия соединения
        this._websocket.onopen = function(event) {
            console.log("WebSocket соединение открыто");
        };
  
        // Обработчик сообщений
        this._websocket.onmessage = function(event) {
            console.log("Получено сообщение: " + event.data);
        };
  
        // Обработчик ошибок
        this._websocket.onerror = function(event) {
            console.log("Ошибка WebSocket: " + event.data);
        };
  
    }
  
    _sendMessage(message) {
        // Отправка сообщения на сервер
        if (this._websocket.readyState === WebSocket.OPEN) {
          this._websocket.send(message);
        } else {
            console.log("WebSocket не открыт");
        }
    }
  };

  export { WS };