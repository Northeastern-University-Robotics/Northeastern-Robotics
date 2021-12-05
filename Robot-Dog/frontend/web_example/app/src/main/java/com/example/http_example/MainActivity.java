package com.example.http_example;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

import io.github.controlwear.virtual.joystick.android.JoystickView;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import android.widget.MediaController;
import android.widget.VideoView;
import android.net.Uri;

public class MainActivity extends AppCompatActivity {
    private TextView mTextViewResult;
    private TextView mTextViewLeft;
    private TextView mTextViewRight;
    private TextView mTextViewPosition;

    int n; //for the user inputted number
    EditText oddEvenInput; //for the user input before converted to integer
    Button submitButton; //button object ... same name as xml file
    private Button jsonButton;
    com.google.android.material.slider.Slider slider;
    int s;

    VideoView videoView;//video viewer

    private int leftAngle;
    private int leftStrength;
    private int rightAngle;
    private int rightStrength;
    private int xCoordinate;
    private int yCoordinate;

    private boolean requestFailed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        this.leftAngle = this.leftStrength = this.rightAngle = this.rightStrength = this.xCoordinate = this.yCoordinate = 0;
        this.requestFailed = false;

        setContentView(R.layout.activity_main);

        mTextViewResult = findViewById(R.id.text_view_result);
        OkHttpClient client = new OkHttpClient();


        oddEvenInput=(EditText)findViewById(R.id.oddEvenInput); //connect to text input in xml file
        submitButton= (Button) findViewById(R.id.submitButton);//connect to button in xml file
        slider=(com.google.android.material.slider.Slider)findViewById(R.id.slider);

        videoView = (VideoView) this.findViewById(R.id.videoView); //connect to video viewer in xml file

        String  videoRtspUrl= "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov";
        videoView.setVideoPath(videoRtspUrl);
        videoView.requestFocus();
        videoView.start();

        submitButton.setOnClickListener(new View.OnClickListener() { //onclick listener for submit button
            @Override
            public void onClick(View view) {
                try {
                    n = Integer.valueOf(oddEvenInput.getText().toString()); //convert the input to an integer
                    String url = "http://69.164.212.94:1500/isEven?n=" + n;
                    makeRequest(url, client);
                } catch (NumberFormatException e) {
                    System.out.println("Submitted string is empty");
                    System.out.println(e.toString());
                }
            }
        });

        mTextViewLeft = findViewById(R.id.textView_left);
        mTextViewRight = findViewById(R.id.textView_right);

        JoystickView joystick_left = findViewById(R.id.joystick_left);
        joystick_left.setOnMoveListener((int angle, int strength) -> {
            if (angle != 0 && strength != 0) {
                this.leftAngle = angle;
                this.leftStrength = strength;
                mTextViewLeft.setText(String.format("%d : %d", angle, strength));
            }
        });

        JoystickView joystick_right = findViewById(R.id.joystick_right);
        joystick_right.setOnMoveListener((int angle, int strength) -> {
            if (angle != 0 && strength != 0) {
                this.rightAngle = angle;
                this.rightStrength = strength;
                mTextViewRight.setText(String.format("%d : %d", angle, strength));
            }
        });

        slider.addOnChangeListener(new com.google.android.material.slider.Slider.OnChangeListener() {
            @Override
            public void onValueChange(@NonNull com.google.android.material.slider.Slider slider, float value, boolean fromUser) {
                s= (int)value;
                String url = "http://69.164.212.94:1500/isEven?n="+s;
                makeRequest(url, client);
            }
        });

        jsonButton = (Button) findViewById(R.id.jsonButton);
        // Make JSON request to server
        jsonButton.setOnClickListener(new View.OnClickListener() { //onclick listener for submit button
            @Override
            public void onClick(View view) {
                String url = "http://69.164.212.94:1500/joystick?leftAngle=" + leftAngle +
                        "&leftStrength=" + leftStrength + "&rightAngle=" + rightAngle +
                        "&rightStrength=" + rightStrength + "&xCoord=" + xCoordinate +
                        "&yCoord=" + yCoordinate;
                makeRequest(url, client);
            }
        });

        Timer t = new Timer();
        t.schedule(new TimerTask() {
            @Override
            public void run() {
                if (!requestFailed) {
                    System.out.println("Hello World");
                    String url = "http://69.164.212.94:1500/joystick?leftAngle=" + leftAngle +
                            "&leftStrength=" + leftStrength + "&rightAngle=" + rightAngle +
                            "&rightStrength=" + rightStrength + "&xCoord=" + xCoordinate +
                            "&yCoord=" + yCoordinate;
                    makeRequest(url, client);
                }
            }
        }, 0, 1000);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        this.xCoordinate = (int) event.getX();
        this.yCoordinate = (int) event.getY();

        mTextViewPosition = findViewById(R.id.textView_position);
        mTextViewPosition.setText("x: " + this.xCoordinate + ", y: " + this.yCoordinate);

        return false;
    }

    private void makeRequest(String url, OkHttpClient client) {
        System.out.println("Beginning request");
        Request request = new Request.Builder()
                .url(url)
                .build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                System.out.println("On failure" + e.toString());
                requestFailed = true;
                MainActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        mTextViewResult.setText(e.toString());
                    }
                });
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                System.out.println("On Response" + response.isSuccessful());
                if (response.isSuccessful()) {
                    String myResponse = response.body().string();

                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mTextViewResult.setText(myResponse);
                        }
                    });
                } else {
                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mTextViewResult.setText("else");
                        }
                    });
                }
            }
        });
    }

    private void makeJSONRequest(String url, OkHttpClient client) {
        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                MainActivity.this.runOnUiThread(() -> mTextViewResult.setText(e.toString()));
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response res) throws IOException {
                if (res.isSuccessful()) {
                    String response = res.body().string();
                    MainActivity.this.runOnUiThread(() -> mTextViewResult.setText(response));
                }
                res.body().close();
            }
        });
    }
}
