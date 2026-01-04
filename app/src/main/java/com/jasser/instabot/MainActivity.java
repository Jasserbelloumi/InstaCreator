package com.jasser.instabot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import java.util.Random;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private TextView statusText;
    private String currentEmail, currentPass, currentUser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        webView = findViewById(R.id.webViewID);
        
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setUserAgentString("Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                // تشغيل المحرك التلقائي بمجرد تحميل أي صفحة
                startFullAutomation();
            }
        });

        findViewById(R.id.btnCreate).setOnClickListener(v -> {
            generateNewIdentity();
            webView.loadUrl("https://www.instagram.com/accounts/emailsignup/");
        });
    }

    private void generateNewIdentity() {
        int rand = new Random().nextInt(9999);
        currentEmail = "jasser" + rand + "@1secmail.com";
        currentPass = "Jasser@" + rand + "!";
        currentUser = "jasser_bot_" + rand;
        statusText.setText("الإيميل الحالي: " + currentEmail);
    }

    private void startFullAutomation() {
        // سكربت جافا سكريبت شامل للتعامل مع كل الحقول
        String js = "javascript:(function() {" +
            "  function clickNext() {" +
            "    var btns = document.querySelectorAll('button');" +
            "    for(var i=0; i<btns.size; i++) {" +
            "      if(btns[i].innerText.includes('التالي') || btns[i].type == 'submit') btns[i].click();" +
            "    }" +
            "  }" +
            "  /* 1. ملء البريد */" +
            "  var email = document.querySelector('input[name=\"emailOrPhone\"]');" +
            "  if(email) { email.value = '" + currentEmail + "'; clickNext(); }" +
            "  /* 2. ملء الاسم والباسورد */" +
            "  var full = document.querySelector('input[name=\"fullName\"]');" +
            "  var pass = document.querySelector('input[name=\"password\"]');" +
            "  var user = document.querySelector('input[name=\"username\"]');" +
            "  if(full) full.value = 'Jasser Bot';" +
            "  if(user) user.value = '" + currentUser + "';" +
            "  if(pass) { pass.value = '" + currentPass + "'; clickNext(); }" +
            "  /* 3. تخطي تاريخ الميلاد (اختيار عشوائي) */" +
            "  var selectors = document.querySelectorAll('select');" +
            "  if(selectors.length >= 3) {" +
            "    selectors[0].value = '1'; selectors[1].value = '1'; selectors[2].value = '1995';" +
            "    clickNext();" +
            "  }" +
            "})()";
        
        new Handler(Looper.getMainLooper()).postDelayed(() -> 
            webView.evaluateJavascript(js, null), 4000);
    }
}
