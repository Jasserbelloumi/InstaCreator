package com.jasser.instabot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.Random;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private TextView statusText;
    private String currentEmail, currentPass, currentUser;
    private ArrayList<String> savedAccounts = new ArrayList<>();
    private Handler handler = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        webView = findViewById(R.id.webViewID);
        Button btnShow = findViewById(R.id.btnShowAccounts);

        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                runAutomator();
            }
        });

        findViewById(R.id.btnCreate).setOnClickListener(v -> startAutomation());
        btnShow.setOnClickListener(v -> Toast.makeText(this, savedAccounts.toString(), Toast.LENGTH_LONG).show());
    }

    private void startAutomation() {
        currentEmail = "jasser" + new Random().nextInt(99999) + "@1secmail.com";
        currentPass = "PassJasser@" + new Random().nextInt(999);
        currentUser = "jasser_bot_" + new Random().nextInt(9999);
        statusText.setText("بدء إنشاء الحساب: " + currentEmail);
        webView.loadUrl("https://www.instagram.com/accounts/emailsignup/");
    }

    private void runAutomator() {
        // سكربت حقن ذكي للتعامل مع الواجهات المختلفة (مثل التي في الصور)
        String js = "javascript:(function() {" +
                "  var input = document.querySelector('input[name=\"emailOrPhone\"]') || document.querySelector('input[type=\"text\"]');" +
                "  if(input && !input.value) {" +
                "    input.value = '" + currentEmail + "';" +
                "    var nextBtn = document.querySelector('button[type=\"submit\"]') || document.querySelectorAll('button')[0];" +
                "    setTimeout(function() { nextBtn.click(); }, 1000);" +
                "  }" +
                "  var codeInput = document.querySelector('input[name=\"email_confirmation_code\"]');" +
                "  if(codeInput) { /* هنا ننتظر الرمز من الخارج */ }" +
                "})()";
        webView.evaluateJavascript(js, null);
    }
}
