package ru.aroize.queue.presentation.fragment

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import com.google.android.material.textfield.TextInputLayout
import ru.aroize.network.dto.User
import ru.aroize.queue.App
import ru.aroize.queue.MainActivity
import ru.aroize.queue.R
import ru.aroize.queue.domain.auth.AuthViewModel
import ru.aroize.queue.utils.TextFieldTrafficLight
import javax.inject.Inject

class AuthFragment : Fragment() {


    @Inject lateinit var model: AuthViewModel

    private val trafficLight = TextFieldTrafficLight(
        2, { signInBtn.isEnabled = false }, { signInBtn.isEnabled = true }
    )

    private lateinit var emailInput: TextInputLayout
    private lateinit var passwordInput: TextInputLayout

    private lateinit var signInBtn: Button

    override fun onAttach(context: Context) {
        super.onAttach(context)
        App.appComponent.inject(this)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(R.layout.auth_layout, container, false)

        signInBtn = root.findViewById(R.id.auth_btn)
        signInBtn.isEnabled = false
        signInBtn.setOnClickListener {
            val email = emailInput.editText?.text.toString()
            val password = passwordInput.editText?.text.toString()
            model.auth(email, password)
        }

        val signUpBtn = root.findViewById<Button>(R.id.register_btn)
        signUpBtn.setOnClickListener {
            (activity as MainActivity).openRegisterPage()
        }

        emailInput = root.findViewById(R.id.email_input_field)
        val emailWatcher = TextFieldTrafficLight.TextFieldWatcher(0, trafficLight) {
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
        val passwordWatcher = TextFieldTrafficLight.TextFieldWatcher(1, trafficLight) {
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

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val loading = Observer<Boolean> {

        }

        val auth = Observer<User> {
            (activity as MainActivity).openProfilePage(it.id)
        }

        val error = Observer<String> { msg ->
            Toast.makeText(requireContext(), msg, Toast.LENGTH_SHORT).show()
        }

        model.loading.observe(viewLifecycleOwner, loading)
        model.auth.observe(viewLifecycleOwner, auth)
        model.errors.observe(viewLifecycleOwner, error)
    }
}