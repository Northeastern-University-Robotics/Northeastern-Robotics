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

public class TestActivity extends AppCompatActivity {
    private TextView mTextViewResult;
    private TextView mTextViewLeft;
    private TextView mTextViewRight;
    private TextView mTextViewPosition;

    int n; //for the user inputted number
    EditText oddEvenInput; //for the user input before converted to integer
    Button submitButton; //button object ... same name as xml file
    private Button jsonButton;
    private Button newScreenButton;

    // joystick attributes
    private int leftAngle;
    private int leftStrength;
    private int rightAngle;
    private int rightStrength;
    private int xCoordinate;
    private int yCoordinate;
    private int testCount;

    private boolean requestFailed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        OkHttpClient client = new OkHttpClient();
    }
    
}
