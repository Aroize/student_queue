package ru.aroize.queue.domain.auth

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import ru.aroize.network.cmd.auth.AuthCmd
import ru.aroize.network.core.ApiManager
import ru.aroize.network.dto.User
import ru.aroize.queue.core.UserRepository
import ru.aroize.queue.utils.toSingle
import javax.inject.Inject

class AuthViewModel @Inject constructor(private val userRepository: UserRepository): ViewModel() {

    val errors: MutableLiveData<String> by lazy { MutableLiveData() }
    val auth: MutableLiveData<User> by lazy { MutableLiveData() }
    val loading: MutableLiveData<Boolean> by lazy { MutableLiveData() }

    fun auth(email: String, password: String) {
        val cmd = AuthCmd(email, password)
        loading.value = true
        cmd.toSingle()
            .observeOn(AndroidSchedulers.mainThread())
            .doOnEvent { _, _ -> loading.value = false }
            .subscribe({
                val (creds, user) = it
                ApiManager.default().updateCredentials(creds)
                userRepository.save(user)
                auth.value = user
            }, {
                errors.value = it.message
            })
    }
}