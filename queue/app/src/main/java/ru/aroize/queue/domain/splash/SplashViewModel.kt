package ru.aroize.queue.domain.splash

import android.util.Log
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import ru.aroize.network.cmd.auth.RefreshCredentialsCmd
import ru.aroize.network.core.ApiManager
import ru.aroize.network.utils.Credentials
import ru.aroize.prefs.PreferenceManager
import ru.aroize.queue.utils.UiThreadUtils
import ru.aroize.queue.utils.toSingle

class SplashViewModel : ViewModel() {

    val user: MutableLiveData<Int> by lazy {
        MutableLiveData()
    }

    fun attach() {
        val id = PreferenceManager.int("USER_ID")
        val access = PreferenceManager.string("ACCESS_TOKEN")
        val refresh = PreferenceManager.string("REFRESH_TOKEN")

        if (id == 0 || access.isNullOrBlank() || refresh.isNullOrBlank()) {
            user.value = -1
        } else {
            val credentials = Credentials(id, access, refresh)
            ApiManager.default().updateCredentials(credentials)

            RefreshCredentialsCmd()
                .toSingle()
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe({
                    ApiManager.default().updateCredentials(credentials)
                    user.value = credentials.id
                }, {
                    Log.e("Aroize", "Exception while refreshing at splash", it)
                    user.value = -1
                })
        }
    }
}