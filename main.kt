#bsmartin
import android.content.Context
import android.net.wifi.WifiManager
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

        initializeViews()
        wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        displayWifiInfo()
    }

    private fun initializeViews() {
        ssidTextView = findViewById(R.id.ssidTextView)
        bssidTextView = findViewById(R.id.bssidTextView)
        securityStatusTextView = findViewById(R.id.securityStatusTextView)
    }

    private fun displayWifiInfo() {
        val wifiInfo = wifiManager.connectionInfo
        ssidTextView.text = "SSID: ${wifiInfo.ssid}"
        bssidTextView.text = "BSSID: ${wifiInfo.bssid}"
        securityStatusTextView.text = "Security Status: ${checkSecurityStatus(wifiInfo.ssid)}"
    }

    private fun checkSecurityStatus(ssid: String): String {
        return if (ssid.contains("secure", ignoreCase = true)) {
            "Secure"
        } else {
            "Not Secure"
        }
    }
}
