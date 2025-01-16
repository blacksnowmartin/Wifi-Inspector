
// script.js
document.getElementById("scanButton").addEventListener("click", () => {
    const wifiList = document.getElementById("wifiList");
    wifiList.innerHTML = "<p>Scanning...</p>";

    // Mock data since real WiFi scanning requires native APIs
    setTimeout(() => {
        const mockNetworks = [
            { name: "HomeWiFi", signal: "-45 dBm", security: "WPA2" },
            { name: "CoffeeShopWiFi", signal: "-60 dBm", security: "WPA3" },
            { name: "LibraryWiFi", signal: "-75 dBm", security: "WEP" },
            { name: "FreePublicWiFi", signal: "-85 dBm", security: "Open" }
        ];

        wifiList.innerHTML = ""; // Clear loading text

        if (mockNetworks.length > 0) {
            mockNetworks.forEach(network => {
                const networkDiv = document.createElement("div");
                networkDiv.className = "network";
                networkDiv.innerHTML = `
                    <strong>${network.name}</strong>
                    <span>Signal Strength: ${network.signal}</span><br>
                    <span>Security: ${network.security}</span>
                `;
                wifiList.appendChild(networkDiv);
            });
        } else {
            wifiList.innerHTML = "<p>No networks found.</p>";
        }
    }, 2000); // Simulate delay
});