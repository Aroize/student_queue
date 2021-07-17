package ru.aroize.queue.presentation.fragment

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import com.google.android.material.progressindicator.CircularProgressIndicator
import com.google.android.material.textfield.TextInputLayout
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import ru.aroize.network.cmd.auth.RegistrationCmd
import ru.aroize.queue.App
import ru.aroize.queue.MainActivity
import ru.aroize.queue.R
import ru.aroize.queue.domain.auth.RegisterViewModel
import ru.aroize.queue.utils.TextFieldTrafficLight
import ru.aroize.queue.utils.toSingle
import javax.inject.Inject

class RegisterFragment : Fragment() {

    @Inject lateinit var model: RegisterViewModel

    private val trafficLight = TextFieldTrafficLight(
        6, { signUpBtn.isEnabled = false }, { signUpBtn.isEnabled = true }
    )

    private lateinit var loginInput: TextInputLayout
    private lateinit var emailInput: TextInputLayout
    private lateinit var passwordInput: TextInputLayout
    private lateinit var repeatPasswordInput: TextInputLayout
    private lateinit var nameInput: TextInputLayout
    private lateinit var surnameInput: TextInputLayout

    private lateinit var signUpBtn: Button
    private lateinit var signInBtn: Button
    private lateinit var loadingIndicator: CircularProgressIndicator

    override fun onAttach(context: Context) {
        super.onAttach(context)
        App.appComponent.inject(this)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(R.layout.register_layout, container, false)

        loginInput = root.findViewById(R.id.login_input_field)
        val loginWatcher = TextFieldTrafficLight.TextFieldWatcher(0, trafficLight) {
            val isNotBlank = it.isNotBlank()
            if (isNotBlank) {
                loginInput.error = null
                loginInput.isErrorEnabled = false
            } else {
                loginInput.isErrorEnabled = true
                loginInput.error = getString(R.string.login_is_blank)
            }
            isNotBlank
        }
        loginInput.editText?.addTextChangedListener(loginWatcher)

        emailInput = root.findViewById(R.id.email_input_field)
        val emailWatcher = TextFieldTrafficLight.TextFieldWatcher(1, trafficLight) {
            val isNotBlank = it.isNotBlank()
            if (isNotBlank) {
                emailInput.error = null
                emailInput.isErrorEnabled = false
            } else {
                emailInput.isErrorEnabled = true
                emailInput.error = getString(R.string.empty_email)
            }
            isNotBlank
        }
        emailInput.editText?.addTextChangedListener(emailWatcher)

        passwordInput = root.findViewById(R.id.password_input_field)
        val passwordWatcher = TextFieldTrafficLight.TextFieldWatcher(2, trafficLight) {
            val isNotBlank = it.isNotBlank()
            if (isNotBlank) {
                passwordInput.error = null
                passwordInput.isErrorEnabled = false
            } else {
                passwordInput.isErrorEnabled = true
                passwordInput.error = getString(R.string.empty_password)
            }
            isNotBlank
        }
        passwordInput.editText?.addTextChangedListener(passwordWatcher)

        repeatPasswordInput = root.findViewById(R.id.password_repeat_field)
        val passwordRepeatWatcher = TextFieldTrafficLight.TextFieldWatcher(3, trafficLight) {
            val match = repeatPasswordInput.editText?.text.toString() == passwordInput.editText?.text.toString()
            if (match) {
                repeatPasswordInput.error = null
                repeatPasswordInput.isErrorEnabled = false
            } else {
                repeatPasswordInput.isErrorEnabled = true
                repeatPasswordInput.error = getString(R.string.password_match)
            }
            match
        }
        repeatPasswordInput.editText?.addTextChangedListener(passwordRepeatWatcher)
        passwordInput.editText?.addTextChangedListener(passwordRepeatWatcher)

        nameInput = root.findViewById(R.id.name_input_field)
        val nameWatcher = TextFieldTrafficLight.TextFieldWatcher(4, trafficLight) {
            val isNotBlank = it.isNotBlank()
            if (isNotBlank) {
                nameInput.error = null
                nameInput.isErrorEnabled = false
            } else {
                nameInput.isErrorEnabled = true
                nameInput.error = getString(R.string.empty_name)
            }
            isNotBlank
        }
        nameInput.editText?.addTextChangedListener(nameWatcher)

        surnameInput = root.findViewById(R.id.surname_input_field)
        val surnameWatcher = TextFieldTrafficLight.TextFieldWatcher(5, trafficLight) {
            val isNotBlank = it.isNotBlank()
            if (isNotBlank) {
                surnameInput.error = null
                surnameInput.isErrorEnabled = false
            } else {
                surnameInput.isErrorEnabled = true
                surnameInput.error = getString(R.string.empty_surname)
            }
            isNotBlank
        }
        surnameInput.editText?.addTextChangedListener(surnameWatcher)

        signUpBtn = root.findViewById(R.id.register_btn)
        signUpBtn.isEnabled = false
        signUpBtn.setOnClickListener {
            val login = loginInput.editText!!.text.toString()
            val email = emailInput.editText!!.text.toString()
            val password = passwordInput.editText!!.text.toString()
            val name = nameInput.editText!!.text.toString()
            val surname = surnameInput.editText!!.text.toString()

            model.register(login, email, password, name, surname)
        }

        signInBtn = root.findViewById(R.id.auth_btn)
        signInBtn.setOnClickListener {
            (activity as MainActivity).openAuthPage()
        }

        loadingIndicator = root.findViewById(R.id.loading_indicator)

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val registered = Observer<Boolean> {
            signInBtn.callOnClick()
        }
        val loading = Observer<Boolean> { load ->
            if (load) {
                signInBtn.visibility = View.GONE
                signUpBtn.visibility = View.INVISIBLE
                loadingIndicator.visibility = View.VISIBLE
            } else {
                signInBtn.visibility = View.VISIBLE
                signUpBtn.visibility = View.VISIBLE
                loadingIndicator.visibility = View.GONE
            }
        }
        val error = Observer<String> {
            Toast.makeText(requireContext(), it, Toast.LENGTH_SHORT).show()
        }

        model.success.observe(viewLifecycleOwner, registered)
        model.loading.observe(viewLifecycleOwner, loading)
        model.error.observe(viewLifecycleOwner, error)
    }
}