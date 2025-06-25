class WS {
    constructor() {
        this._Initialize();
        this.receivedData = null;  // Property to store received data
    }

    _Initialize() {
        // Create a new WebSocket instance
        this._websocket = new WebSocket('wss://qure.space/ws');
        //this._websocket = new WebSocket('ws://127.0.0.1:8765');

        // Connection opened
        this._websocket.onopen = (event) => {
            console.log("WebSocket connection opened");
        };

        // Message received
        this._websocket.onmessage = (event) => {
            // console.log("Received message from server: " + event.data);
            this.receivedData = event.data;  // Store the received data
            this._processData(event.data);   // Call another method with the data
            // this.receivedData = null;
        };

        // Connection error
        this._websocket.onerror = (event) => {
            console.log("WebSocket error: " + event.data);
        };

    }

    _sendMessage(message) {
        // Send a message to the server
        if (this._websocket.readyState === WebSocket.OPEN) {
            this._websocket.send(message);
        } else {
            console.log("WebSocket is not open");
        }
    }

    // Method to process the received data
    _processData(data) {
        // console.log("Processing received data:", data);
        // You can add your logic here to handle the data
    }

    // Method to access the received data
    getReceivedData() {
        console.log(this.receivedData);
        return this.receivedData;
    }

    // WS status
    getState() {
        return this._websocket.readyState;
    }
}

export { WS };
