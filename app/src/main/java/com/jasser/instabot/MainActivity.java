package com.jasser.instabot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Random;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private String emailUser, emailDomain;
    private TextView statusText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        webView = new WebView(this);
        configureWebView();

        findViewById(R.id.btnCreate).setOnClickListener(v -> startCreationProcess());
        findViewById(R.id.btnGetCode).setOnClickListener(v -> checkEmails());
    }

    private void configureWebView() {
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setUserAgentString("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                injectData();
            }
        });
    }

    private void startCreationProcess() {
        // توليد بريد وهمي عشوائي
        String[] domains = {"1secmail.com", "1secmail.org", "1secmail.net"};
        emailUser = "user_" + new Random().nextInt(99999);
        emailDomain = domains[new Random().nextInt(domains.length)];
        
        statusText.setText("Email: " + emailUser + "@" + emailDomain);
        setContentView(webView);
        webView.loadUrl("https://www.instagram.com/accounts/emailsignup/");
    }

    private void injectData() {
        String pass = "PassBot@" + new Random().nextInt(999);
        String js = "javascript:(function() {" +
                "var inputs = document.getElementsByTagName('input');" +
                "if(inputs.length > 0) {" +
                "inputs[0].value = '" + emailUser + "@" + emailDomain + "';" +
                "inputs[1].value = 'Jasser Bot';" +
                "inputs[2].value = '" + emailUser + "_inst';" +
                "inputs[3].value = '" + pass + "';" +
                "}" +
                "})()";
        webView.evaluateJavascript(js, null);
    }

    private void checkEmails() {
        new Thread(() -> {
            try {
                URL url = new URL("https://www.1secmail.com/api/v1/?action=getMessages&login=" + emailUser + "&domain=" + emailDomain);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                JSONArray json = new JSONArray(rd.readLine());
                
                if (json.length() > 0) {
                    String msgId = json.getJSONObject(0).getString("id");
                    fetchEmailBody(msgId);
                } else {
                    showToast("No code yet, wait 5 seconds...");
                }
            } catch (Exception e) { e.printStackTrace(); }
        }).start();
    }

    private void fetchEmailBody(String id) {
        try {
            URL url = new URL("https://www.1secmail.com/api/v1/?action=readMessage&login=" + emailUser + "&domain=" + emailDomain + "&id=" + id);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            JSONObject msg = new JSONObject(rd.readLine());
            String body = msg.getString("body");
            // استخراج 6 أرقام (رمز إنستا)
            final String code = body.replaceAll("[^0-9]", "").substring(0, 6);
            
            new Handler(Looper.getMainLooper()).post(() -> {
                statusText.setText("INSTA CODE: " + code);
                Toast.makeText(this, "Code Found: " + code, Toast.LENGTH_LONG).show();
            });
        } catch (Exception e) { e.printStackTrace(); }
    }

    private void showToast(String msg) {
        new Handler(Looper.getMainLooper()).post(() -> Toast.makeText(this, msg, Toast.LENGTH_SHORT).show());
    }
}
