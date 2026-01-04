package com.jasser.instabot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
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
        webView = findViewById(R.id.webViewID); // سنضيفه في الـ layout

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setUserAgentString("Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                if (url.contains("emailsignup")) {
                    autoFillRegistration();
                }
            }
        });

        findViewById(R.id.btnCreate).setOnClickListener(v -> startCreationProcess());
    }

    private void startCreationProcess() {
        emailUser = "jasser" + new Random().nextInt(99999);
        emailDomain = "1secmail.com";
        statusText.setText("Target Email: " + emailUser + "@" + emailDomain);
        webView.loadUrl("https://www.instagram.com/accounts/emailsignup/");
    }

    private void autoFillRegistration() {
        String pass = "JasserBot@" + new Random().nextInt(999);
        String fullName = "Jasser AI Bot";
        String username = emailUser + "js";

        // كود جافا سكريبت محسن للبحث عن الحقول وملئها
        String js = "javascript:(function() {" +
                "var fill = function() {" +
                "  var inputs = document.querySelectorAll('input');" +
                "  if(inputs.length >= 4) {" +
                "    inputs[0].value = '" + emailUser + "@" + emailDomain + "';" +
                "    inputs[1].value = '" + fullName + "';" +
                "    inputs[2].value = '" + username + "';" +
                "    inputs[3].value = '" + pass + "';" +
                "    console.log('Fields filled!');" +
                "    var btn = document.querySelector('button[type=\"submit\"]');" +
                "    if(btn) btn.click();" +
                "  } else { setTimeout(fill, 2000); }" + // إعادة المحاولة كل ثانيتين
                "}; fill();" +
                "})()";
        
        new Handler(Looper.getMainLooper()).postDelayed(() -> 
            webView.evaluateJavascript(js, null), 3000); // انتظر 3 ثواني للتحميل
    }
}
