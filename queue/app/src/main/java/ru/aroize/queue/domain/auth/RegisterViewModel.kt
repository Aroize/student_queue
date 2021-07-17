package ru.aroize.queue.domain.auth

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import ru.aroize.network.cmd.auth.RegistrationCmd
import ru.aroize.queue.utils.toSingle
import javax.inject.Inject

class RegisterViewModel @Inject constructor() : ViewModel() {

    val error: MutableLiveData<String> by lazy { MutableLiveData() }
    val loading: MutableLiveData<Boolean> by lazy { MutableLiveData() }
    val success: MutableLiveData<Boolean> by lazy { MutableLiveData() }

    fun register(
        login: String,
        email: String,
        password: String,
        name: String,
        surname: String
    ) {

        loading.value = true

        RegistrationCmd(login, password, email, name, surname)
            .toSingle()
            .observeOn(AndroidSchedulers.mainThread())
            .doOnEvent { _, _ -> loading.value = false }
            .subscribe({ success.value = true }, { error.value = it.message })
    }
}