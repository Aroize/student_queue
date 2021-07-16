package ru.aroize.queue

import android.app.Application
import ru.aroize.network.core.ApiConfig
import ru.aroize.network.core.ApiManager
import ru.aroize.prefs.PreferenceManager
import ru.aroize.queue.dagger.ApplicationComponent
import ru.aroize.queue.dagger.DaggerApplicationComponent

class App : Application() {
    override fun onCreate() {
        super.onCreate()

        PreferenceManager.init(this)

        initDagger()
        initNetwork()
    }

    private fun initDagger() {
        appComponent = DaggerApplicationComponent.create()
    }

    private fun initNetwork() {
        val config = ApiConfig(
            "http",
            "192.168.0.14",
            5022,
            "v0.1"
        )
        val manager = ApiManager.default()
        manager.init(config)
    }

    companion object {
        lateinit var appComponent: ApplicationComponent
    }
}