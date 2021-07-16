package ru.aroize.queue

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.bottomnavigation.BottomNavigationView
import ru.aroize.queue.presentation.fragment.AuthFragment
import ru.aroize.queue.presentation.fragment.ProfileFragment
import ru.aroize.queue.presentation.fragment.RegisterFragment
import ru.aroize.queue.presentation.fragment.SplashFragment

class MainActivity : AppCompatActivity() {

    private lateinit var bottomNavigation: BottomNavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_layout)
        supportActionBar?.hide()
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, SplashFragment())
            .commit()

        bottomNavigation = findViewById(R.id.bottom_navigation)
        bottomNavigation.setOnItemSelectedListener {
            when (it.itemId) {
                R.id.schedule -> { true }
                R.id.groups -> { true }
                R.id.profile -> {
                    true
                }
                else -> false
            }
        }
    }

    fun openAuthPage() {
        bottomNavigation.visibility = View.GONE
        supportFragmentManager.beginTransaction()
            .setCustomAnimations(android.R.anim.fade_in, android.R.anim.fade_out)
            .replace(R.id.fragment_container, AuthFragment())
            .commit()
    }

    fun openRegisterPage() {
        bottomNavigation.visibility = View.GONE
        supportFragmentManager.beginTransaction()
            .setCustomAnimations(android.R.anim.fade_in, android.R.anim.fade_out)
            .replace(R.id.fragment_container, RegisterFragment())
            .commit()
    }

    fun openProfilePage(id: Int) {
        bottomNavigation.visibility = View.VISIBLE
        supportFragmentManager.beginTransaction()
            .setCustomAnimations(android.R.anim.fade_in, android.R.anim.fade_out)
            .replace(R.id.fragment_container, ProfileFragment().apply {
                arguments = Bundle().apply { putInt("UID", id) }
            })
            .commit()
    }
}