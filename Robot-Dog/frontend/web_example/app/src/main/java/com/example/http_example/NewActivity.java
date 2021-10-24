package com.example.http_example;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.android.material.bottomnavigation.BottomNavigationItemView;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.example.http_example.databinding.ActivityNewBinding;

public class NewActivity extends AppCompatActivity {

    private ActivityNewBinding binding;

    private Button prevScreenButton;
    private BottomNavigationItemView homeButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityNewBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_activity_new);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(binding.navView, navController);

        this.prevScreenButton = findViewById(R.id.previous_button);

        this.prevScreenButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v)
            {
                // Create intent to start MainActivity from NewActivity
                Intent intent = new Intent(NewActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });

        this.homeButton = (BottomNavigationItemView)findViewById(R.id.navigation_home);

        this.homeButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v)
            {
                // Create intent to start MainActivity from NewActivity
                Intent intent = new Intent(NewActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });
    }

}