import android.content.Context
import android.net.wifi.WifiManager
import android.net.wifi.WifiConfiguration
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var wifiManager: WifiManager
    private lateinit var ssidTextView: TextView
    private lateinit var bssidTextView: TextView
    private lateinit var securityStatusTextView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        ssidTextView = findViewById(R.id.ssidTextView)
        bssidTextView = findViewById(R.id.bssidTextView)
        securityStatusTextView = findViewById(R.id.securityStatusTextView)

        wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        displayWifiInfo()
    }

    private fun displayWifiInfo() {
        val wifiInfo = wifiManager.connectionInfo
        val ssid = wifiInfo.ssid
        val bssid = wifiInfo.bssid
        val securityStatus = checkSecurityStatus(ssid)

        ssidTextView.text = "SSID: $ssid"
        bssidTextView.text = "BSSID: $bssid"
        securityStatusTextView.text = "Security Status: $securityStatus"
    }

    private fun checkSecurityStatus(ssid: String): String {
        // Simplified security check
        return if (ssid.contains("secure")) {
            "Secure"
        } else {
            "Not Secure"
        }
    }
}
