package com.jasser.instabot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import okhttp3.*;
import org.json.*;
import java.io.IOException;
import java.util.Random;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private TextView statusText;
    private String currentEmail, currentPass, currentUser;
    private final OkHttpClient client = new OkHttpClient();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        statusText = findViewById(R.id.statusText);
        webView = findViewById(R.id.webViewID);
        
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                startFullAutomation();
                if(url.contains("confirm")) { startOtpCheck(); }
            }
        });

        findViewById(R.id.btnCreate).setOnClickListener(v -> {
            generateNewIdentity();
            webView.loadUrl("https://www.instagram.com/accounts/emailsignup/");
        });
    }

    private void generateNewIdentity() {
        int rand = new Random().nextInt(99999);
        currentEmail = "jasser" + rand + "@1secmail.com";
        currentPass = "Jasser@" + rand + "!";
        currentUser = "jasser_bot_" + rand;
        statusText.setText("جاري العمل على: " + currentEmail);
    }

    private void startOtpCheck() {
        String user = currentEmail.split("@")[0];
        String domain = "1secmail.com";
        String url = "https://www.1secmail.com/api/v1/?action=getMessages&login=" + user + "&domain=" + domain;

        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                try {
                    JSONArray json = new JSONArray(response.body().string());
                    if (json.length() > 0) {
                        String msgId = json.getJSONObject(0).getString("id");
                        fetchOtpCode(user, domain, msgId);
                    } else {
                        new Handler(Looper.getMainLooper()).postDelayed(() -> startOtpCheck(), 5000);
                    }
                } catch (Exception e) { e.printStackTrace(); }
            }
            @Override
            public void onFailure(Call call, IOException e) {}
        });
    }

    private void fetchOtpCode(String user, String domain, String id) {
        String url = "https://www.1secmail.com/api/v1/?action=readMessage&login=" + user + "&domain=" + domain + "&id=" + id;
        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                try {
                    JSONObject json = new JSONObject(response.body().string());
                    String body = json.getString("body");
                    String otp = body.replaceAll("[^0-9]", "").substring(0, 6); // استخراج 6 أرقام
                    new Handler(Looper.getMainLooper()).post(() -> {
                        webView.evaluateJavascript("document.querySelector('input[name=\"email_confirmation_code\"]').value='" + otp + "';", null);
                        webView.evaluateJavascript("document.querySelector('button[type=\"submit\"]').click();", null);
                        statusText.setText("تم التأكيد بنجاح! الحساب: " + currentUser);
                    });
                } catch (Exception e) { e.printStackTrace(); }
            }
            @Override
            public void onFailure(Call call, IOException e) {}
        });
    }

    private void startFullAutomation() {
        String js = "javascript:(function() {" +
            "  var email = document.querySelector('input[name=\"emailOrPhone\"]');" +
            "  if(email) { email.value = '" + currentEmail + "'; document.querySelector('button[type=\"submit\"]').click(); }" +
            "  var full = document.querySelector('input[name=\"fullName\"]');" +
            "  if(full) { " +
            "    full.value = 'Jasser Account';" +
            "    document.querySelector('input[name=\"password\"]').value = '" + currentPass + "';" +
            "    document.querySelector('button[type=\"submit\"]').click(); " +
            "  }" +
            "  var selectors = document.querySelectorAll('select');" +
            "  if(selectors.length >= 3) {" +
            "    selectors[0].value = '5'; selectors[1].value = '5'; selectors[2].value = '1990';" +
            "    document.querySelectorAll('button')[1].click();" +
            "  }" +
            "})()";
        webView.evaluateJavascript(js, null);
    }
}
