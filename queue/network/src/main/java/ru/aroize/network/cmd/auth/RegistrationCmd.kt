package ru.aroize.network.cmd.auth

import org.json.JSONObject
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.dto.User

class RegistrationCmd(
    login: String,
    password: String,
    email: String,
    name: String,
    surname: String
) : BaseCommand<User>("auth.register") {

    init {
        addParam("login", login)
        addParam("password", password)
        addParam("email", email)
        addParam("name", name)
        addParam("surname", surname)
    }

    override fun parse(json: JSONObject): User {
        return User.parse(json)
    }
}